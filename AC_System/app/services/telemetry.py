import psutil
import time

# Inicjalizacja zmiennych stanu dla pomiaru sieci
_last_net_io = psutil.net_io_counters()
_last_net_time = time.time()

def get_cpu_temp() -> float:
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read().strip()) / 1000.0
    except FileNotFoundError:
        return 0.0

def get_system_metrics() -> dict:
    global _last_net_io, _last_net_time
    
    # Pobieranie aktualnego stanu sieci i czasu
    current_net_io = psutil.net_io_counters()
    current_net_time = time.time()
    
    # Obliczanie różnicy czasu (w sekundach) od ostatniego wywołania
    time_delta = current_net_time - _last_net_time
    
    if time_delta > 0:
        # Obliczanie prędkości (bajty na sekundę) -> konwersja na Megabajty (MB/s)
        # Aby użyć Megabitów (Mbps), pomnóż bajty przez 8 przed podzieleniem przez 1024**2
        download_speed_mbs = (current_net_io.bytes_recv - _last_net_io.bytes_recv) / time_delta / (1024 * 1024)
        upload_speed_mbs = (current_net_io.bytes_sent - _last_net_io.bytes_sent) / time_delta / (1024 * 1024)
    else:
        download_speed_mbs = 0.0
        upload_speed_mbs = 0.0
        
    # Aktualizacja stanu dla następnego wywołania funkcji
    _last_net_io = current_net_io
    _last_net_time = current_net_time

    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=None),
        "ram_usage_percent": psutil.virtual_memory().percent,
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "temperature_c": get_cpu_temp(),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "network_download_mbs": round(download_speed_mbs, 2),  # MB/s
        "network_upload_mbs": round(upload_speed_mbs, 2)       # MB/s
    }