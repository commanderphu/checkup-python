import psutil
import platform
from datetime import datetime
import GPUtil

def get_system_info():
    """Gathers basic system information."""
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }
    return info

def check_cpu():
    """Checks CPU usage and returns a score."""
    usage = psutil.cpu_percent(interval=1)
    score = max(1, 10 - int(usage // 10))
    return usage, score

def check_memory():
    """Checks memory usage and returns a score."""
    memory = psutil.virtual_memory()
    usage = memory.percent
    score = max(1, 10 - int(usage // 10))
    return usage, score

def check_disk():
    """Checks disk usage and returns a score."""
    disk = psutil.disk_usage('/')
    usage = disk.percent
    score = max(1, 10 - int(usage // 10))
    return usage, score

def check_network():
    """Checks network activity and returns a score."""
    net_io = psutil.net_io_counters()
    sent = net_io.bytes_sent
    recv = net_io.bytes_recv
    # Simplified scoring based on activity (lower activity = higher score)
    score = 10 if sent + recv < 1e6 else 5 if sent + recv < 1e7 else 1
    return sent, recv, score

def pc_checkup():
    """Performs a full PC checkup and prints results."""
    print("System Information:")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")
    print("\nCheckup Results:")
    
    cpu_usage, cpu_score = check_cpu()
    print(f"CPU Usage: {cpu_usage}% | Score: {cpu_score}/10")
    
    memory_usage, memory_score = check_memory()
    print(f"Memory Usage: {memory_usage}% | Score: {memory_score}/10")
    
    disk_usage, disk_score = check_disk()
    print(f"Disk Usage: {disk_usage}% | Score: {disk_score}/10")
    
    net_sent, net_recv, net_score = check_network()
    print(f"Network Sent: {net_sent} bytes, Received: {net_recv} bytes | Score: {net_score}/10")
    
    # Calculate overall score
    total_score = (cpu_score + memory_score + disk_score + net_score) / 4
    if total_score <= 4:
        status = "Rot"
    elif total_score <= 6:
        status = "Gelb"
    else:
        status = "Grün"
    
    print(f"\nGesamtbewertung: {total_score:.2f}/10 | Status: {status}")
    
    # Save results to a .txt file
    with open("checkup_results.txt", "w") as file:
        file.write("System Information:\n")
        for key, value in get_system_info().items():
            file.write(f"{key}: {value}\n")
        file.write("\nCheckup Results:\n")
        file.write(f"CPU Usage: {cpu_usage}% | Score: {cpu_score}/10\n")
        file.write(f"Memory Usage: {memory_usage}% | Score: {memory_score}/10\n")
        file.write(f"Disk Usage: {disk_usage}% | Score: {disk_score}/10\n")
        file.write(f"Network Sent: {net_sent} bytes, Received: {net_recv} bytes | Score: {net_score}/10\n")
        file.write(f"\nGesamtbewertung: {total_score:.2f}/10 | Status: {status}\n")

def get_hardware_info():
    """Gathers hardware information."""
    hardware_info = {
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical Processors": psutil.cpu_count(logical=True),
        "Total Memory (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Total Disk Space (GB)": round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    }
    
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_info = []
            for gpu in gpus:
                gpu_info.append(f"{gpu.name} (Memory: {gpu.memoryTotal}MB, Load: {gpu.load * 100:.1f}%)")
            hardware_info["GPU Info"] = "; ".join(gpu_info)
        else:
            hardware_info["GPU Info"] = "No GPU detected"
    except ImportError:
        hardware_info["GPU Info"] = "GPUtil not installed"
    return hardware_info

if __name__ == "__main__":
    pc_checkup()
    print("\nHardware Information:")
    for key, value in get_hardware_info().items():
        print(f"{key}: {value}")