import threading


class ProxyManager():
    _lock = threading.Lock()
    _instance = None
    proxy = None
    
    
    def __init__(self) -> None:
        pass
    
    def __new__(cls) -> None:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def Init(cls:'ProxyManager') -> bool:
        pass
    
    @classmethod
    def Start(cls:'ProxyManager') -> bool:
        pass
    
    @classmethod
    def Stop(cls:'ProxyManager') -> bool:
        pass