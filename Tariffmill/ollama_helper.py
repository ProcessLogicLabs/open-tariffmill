"""
Ollama integration utilities for TariffMill.

Provides helper functions for connecting to a local Ollama server,
fetching available models, testing connectivity, and checking system
capability for running local LLM models.
"""

import json
import sys
import urllib.request
import urllib.error

DEFAULT_BASE_URL = "http://localhost:11434"


def test_ollama_connection(base_url=DEFAULT_BASE_URL):
    """
    Test connection to the Ollama server.

    Args:
        base_url: Ollama server URL (default: http://localhost:11434)

    Returns:
        Tuple of (is_available: bool, status_message: str)
    """
    try:
        url = f"{base_url.rstrip('/')}/api/tags"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            model_count = len(data.get('models', []))
            return True, f"Connected - {model_count} model(s) available"
    except urllib.error.URLError as e:
        return False, f"Cannot connect to Ollama at {base_url}: {e.reason}"
    except Exception as e:
        return False, f"Connection error: {e}"


def fetch_ollama_models(base_url=DEFAULT_BASE_URL):
    """
    Fetch list of installed model names from Ollama server.

    Args:
        base_url: Ollama server URL (default: http://localhost:11434)

    Returns:
        List of model name strings (e.g. ['llama3.1:8b', 'codellama:13b'])
    """
    try:
        url = f"{base_url.rstrip('/')}/api/tags"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            models = data.get('models', [])
            return [m['name'] for m in models if 'name' in m]
    except Exception:
        return []


def get_system_memory():
    """
    Get total and available physical memory in bytes.

    Returns:
        Tuple of (total_bytes, available_bytes). Returns (0, 0) on failure.
    """
    if sys.platform == 'win32':
        try:
            import ctypes
            import ctypes.wintypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.wintypes.DWORD),
                    ("dwMemoryLoad", ctypes.wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_uint64),
                    ("ullAvailPhys", ctypes.c_uint64),
                    ("ullTotalPageFile", ctypes.c_uint64),
                    ("ullAvailPageFile", ctypes.c_uint64),
                    ("ullTotalVirtual", ctypes.c_uint64),
                    ("ullAvailVirtual", ctypes.c_uint64),
                    ("ullAvailExtendedVirtual", ctypes.c_uint64),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return stat.ullTotalPhys, stat.ullAvailPhys
        except Exception:
            pass
    else:
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            mem = {}
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(':')] = int(parts[1]) * 1024  # kB to bytes
            total = mem.get('MemTotal', 0)
            avail = mem.get('MemAvailable', mem.get('MemFree', 0))
            return total, avail
        except Exception:
            pass
    return 0, 0


def get_model_info(model_name, base_url=DEFAULT_BASE_URL):
    """
    Get detailed info about an Ollama model.

    Args:
        model_name: Name of the model (e.g. 'qwen2.5:7b')
        base_url: Ollama server URL

    Returns:
        Dict with model details, or None on failure.
    """
    try:
        # Get model details from /api/show
        url = f"{base_url.rstrip('/')}/api/show"
        payload = json.dumps({"model": model_name}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))

        details = data.get('details', {})
        model_info_data = data.get('model_info', {})

        # Find context length from model_info keys (varies by architecture)
        context_length = 0
        for key, val in model_info_data.items():
            if key.endswith('.context_length') and isinstance(val, int):
                context_length = val
                break

        # Get model file size from /api/tags
        model_size_bytes = 0
        try:
            tags_url = f"{base_url.rstrip('/')}/api/tags"
            tags_req = urllib.request.Request(tags_url, method='GET')
            with urllib.request.urlopen(tags_req, timeout=5) as tags_resp:
                tags_data = json.loads(tags_resp.read().decode('utf-8'))
                for m in tags_data.get('models', []):
                    if m.get('name') == model_name:
                        model_size_bytes = m.get('size', 0)
                        break
        except Exception:
            pass

        return {
            'parameter_size': details.get('parameter_size', 'unknown'),
            'quantization': details.get('quantization_level', 'unknown'),
            'family': details.get('family', 'unknown'),
            'context_length': context_length,
            'model_size_bytes': model_size_bytes,
        }
    except Exception:
        return None


def get_running_models(base_url=DEFAULT_BASE_URL):
    """
    Get list of currently loaded/running models from Ollama.

    Returns:
        List of dicts with: name, size, size_vram, context_length
    """
    try:
        url = f"{base_url.rstrip('/')}/api/ps"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            for m in data.get('models', []):
                results.append({
                    'name': m.get('name', ''),
                    'size': m.get('size', 0),
                    'size_vram': m.get('size_vram', 0),
                    'context_length': m.get('context_length', 0),
                })
            return results
    except Exception:
        return []


def check_system_capability(model_name, base_url=DEFAULT_BASE_URL):
    """
    Check if the system can run the specified Ollama model.

    Performs connectivity, model availability, RAM, and GPU checks.

    Args:
        model_name: Name of the model to check
        base_url: Ollama server URL

    Returns:
        Dict with keys:
            can_run (bool): Whether the model can likely run
            warnings (list[str]): Warning messages
            info (dict): Detailed system/model info
    """
    warnings = []
    info = {
        'model': model_name,
        'server_connected': False,
        'model_available': False,
        'model_loaded': False,
        'gpu_accelerated': False,
        'parameter_size': '',
        'model_size_gb': 0.0,
        'free_ram_gb': 0.0,
        'total_ram_gb': 0.0,
    }
    can_run = True

    # 1. Check server connectivity
    connected, msg = test_ollama_connection(base_url)
    info['server_connected'] = connected
    if not connected:
        return {
            'can_run': False,
            'warnings': [f"Ollama server not reachable: {msg}"],
            'info': info,
        }

    # 2. Check model is installed
    models = fetch_ollama_models(base_url)
    info['model_available'] = model_name in models
    if not info['model_available']:
        return {
            'can_run': False,
            'warnings': [f"Model '{model_name}' not installed. Available: {', '.join(models) or 'none'}"],
            'info': info,
        }

    # 3. Get model info
    model_detail = get_model_info(model_name, base_url)
    if model_detail:
        info['parameter_size'] = model_detail['parameter_size']
        model_size_bytes = model_detail['model_size_bytes']
        info['model_size_gb'] = round(model_size_bytes / (1024 ** 3), 1) if model_size_bytes else 0.0

    # 4. Check system RAM
    total_ram, avail_ram = get_system_memory()
    if total_ram > 0:
        info['total_ram_gb'] = round(total_ram / (1024 ** 3), 1)
        info['free_ram_gb'] = round(avail_ram / (1024 ** 3), 1)

        if info['model_size_gb'] > 0:
            # Need model size + ~20% headroom for context/overhead
            required = info['model_size_gb'] * 1.2
            if info['free_ram_gb'] < required:
                can_run = False
                warnings.append(
                    f"Low memory: {info['free_ram_gb']:.1f} GB free, "
                    f"model needs ~{info['model_size_gb']:.1f} GB "
                    f"(+ overhead). Total RAM: {info['total_ram_gb']:.1f} GB"
                )

    # 5. Check running model status (GPU vs CPU)
    running = get_running_models(base_url)
    for rm in running:
        if rm['name'] == model_name:
            info['model_loaded'] = True
            if rm['size_vram'] > 0:
                info['gpu_accelerated'] = True
            else:
                info['gpu_accelerated'] = False
                warnings.append("Running on CPU only (no GPU acceleration) - inference will be slower")
            break

    if not info['model_loaded'] and not info.get('gpu_accelerated'):
        # Model not loaded yet — we can't check GPU until it loads
        # Just note it hasn't been loaded
        warnings.append("Model not currently loaded - first request may be slow")

    return {
        'can_run': can_run,
        'warnings': warnings,
        'info': info,
    }
