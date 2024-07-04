import datetime
import time
import psutil
from psutil._common import scpufreq

class CPU_info:
    def __init__(self: "CPU_info", cores_num: float, frequency: scpufreq, cpu_precent: float, cpu_avgload: tuple[float,float,float]) -> None:
        self.cores_num = cores_num
        self.frequency = frequency
        self.cpu_precent = cpu_precent
        self.cpu_avgload = cpu_avgload
        
    def __dict__(self: "CPU_info") -> dict[str, any]:
        return {
            "cores_num": self.cores_num,
            "frequency": self.frequency,
            "cpu_precent": self.cpu_precent,
            "cpu_avgload": self.cpu_avgload
        }
    
    def __str__(self: "CPU_info") -> str:
        return str(self.__dict__())
    
    def __repr__(self: "CPU_info") -> str:
        return f"CPU_info({self.cores_num}, {self.frequency}, {self.cpu_precent}, {self.cpu_avgload})"

class Net_info:
    def __init__(self: "Net_info", bytes_sent: int, bytes_recv: int) -> None:
        self.latest_bytes_sent = None
        self.latest_bytes_recv = None
        self.latest_timestamp = None
        self.bytes_sent = bytes_sent
        self.bytes_recv = bytes_recv
        self.timestamp = datetime.datetime.now().timestamp()
    
    def update(self: "Net_info"):
        self.latest_bytes_recv = self.bytes_recv
        self.latest_bytes_sent = self.bytes_sent
        self.latest_timestamp = self.timestamp
        record = psutil.net_io_counters(pernic=False)
        self.bytes_sent = record.bytes_sent
        self.bytes_recv = record.bytes_recv
        self.timestamp = datetime.datetime.now().timestamp()
        
    def avg_speed(self: "Net_info") -> tuple[float, float]:
        time_diff = self.timestamp - self.latest_timestamp
        speed_sent = (self.bytes_sent - self.latest_bytes_sent) / time_diff
        speed_recv = (self.bytes_recv - self.latest_bytes_recv) / time_diff
        def calculate_unit(value:float) -> str:
            match value:
                case value if value < 1024:
                    return f"{value}B/s"
                case value if value < 1024**2:
                    return f"{value/1024}KB/s"
                case value if value < 1024**3:
                    return f"{value/1024**2}MB/s"
                case value if value < 1024**4:
                    return f"{value/1024**3}GB/s"
                case _:
                    return f"{value/1024*4}GB/s"

        return {"sent":calculate_unit(speed_sent), "recv":calculate_unit(speed_recv)}
        
    def __dict__(self: "Net_info") -> dict[str, any]:
        return {
            "latest_bytes_sent": self.latest_bytes_sent,
            "latest_bytes_recv": self.latest_bytes_recv,
            "bytes_sent": self.bytes_sent,
            "bytes_recv": self.bytes_recv
        }
    
    def __str__(self: "Net_info") -> str:
        return str(self.__dict__())
    
    def __repr__(self: "Net_info") -> str:
        return f"Net_info({self.latest_bytes_sent}, {self.latest_bytes_recv}, {self.bytes_sent}, {self.bytes_recv})"

def get_cpu_info(averge:bool=False):
    cores_num = psutil.cpu_count(logical=False)
    frequency = psutil.cpu_freq()
    cpu_precent = psutil.cpu_percent(interval=1)
    cpu_avgload = None
    if averge:
        cpu_avgload = psutil.getloadavg()
    return CPU_info(cores_num, frequency, cpu_precent, cpu_avgload)

def get_cpu_precent() -> float:
    return psutil.cpu_percent(interval=1)

def get_memory_info():
    return psutil.virtual_memory()

def get_disk_info():
    return psutil.disk_usage('/')

def get_net_info():
    record = psutil.net_io_counters(pernic=False)
    bytes_sent = record.bytes_sent
    bytes_recv = record.bytes_recv
    return Net_info(bytes_sent, bytes_recv)

if __name__ == "__main__":
    print(get_cpu_info())
    print(get_memory_info())
    # print(psutil.disk_partitions()) # 查看所有硬盘及挂载
    print(get_disk_info())
    network = get_net_info()
    print(network)
    time.sleep(3)
    network.update()
    print(network.avg_speed())
    

