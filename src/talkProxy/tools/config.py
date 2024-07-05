import logging
import os
import threading
import yaml
from .common import randomStr
from .settingReader import SettingReader
from typing import Optional

config_dir_name = "config"
config_dir_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), config_dir_name
)
config_file_name = "config.yaml"
config_file_path = os.path.join(config_dir_path, config_file_name)
subscription_file_name = "subscription.yaml"
subscription_file_path = os.path.join(config_dir_path, subscription_file_name)


def checkParam(kwDict: dict, key: str, param_type: type, default: Optional[any] = None):
    if key not in kwDict:
        return default
    if not isinstance(kwDict[key], param_type):
        logging.error(f"{key}参数类型错误")
        return None
    return kwDict[key]


class BaseConfig:
    def __init__(self, file_path: str) -> None:
        self.config: dict = None
        self.file_path: str = file_path
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w+") as f:
                f.write("")
        with open(self.file_path, "r+") as f:
            self.config = yaml.safe_load(f)
            if self.config is None:
                self.config = {}
            logging.debug(self.config)

    def reload_config(self):
        self.load_config()

    def save_config(self):
        with open(self.file_path, "w") as f:
            yaml.dump(self.config, f)
        self.reload_config()


class GlobalConfig(BaseConfig):
    __lock = threading.Lock()
    __instance = None

    def __init__(self) -> None:
        super().__init__(config_file_path)
        self.subScriptionConfig = SubScriptionConfig()
        if self.config == {}:
            self.config = {"http_port": 7899, "socks_port": 7900, "default": None}
            self.save_config()

    @classmethod
    def InitConfig(cls) -> "GlobalConfig":
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = GlobalConfig()
        return cls.__instance

    @classmethod
    def GetInstance(cls) -> None | "GlobalConfig":
        return cls.__instance

    def get_subscription_config(self):
        return self.subScriptionConfig

    def new_proxy_config(
        self, name: str, proxy_type: str, **kwargs: dict
    ) -> BaseConfig | None:
        file_path = os.path.join(config_dir_path, f"{randomStr()}.yaml")
        config = None
        match proxy_type:
            case "hysteria":
                server = checkParam(kwargs, "server", str, None)
                auth = checkParam(kwargs, "auth", str, None)
                if not all([server, auth]):
                    logging.error(
                        f"创建{name}的hysteria配置文件失败, 缺少server或auth字段"
                    )
                    return None
                config = self.new_hysteria_config(file_path, **kwargs)
            case _:
                logging.error(
                    f'不支持的代理类型{self.file_list_config.config[name]["type"]}'
                )
                return None
        new_proxy_file_dict: dict = {
            "file": os.path.abspath(file_path),
            "type": proxy_type,
        }
        self.file_list_config.config[name] = new_proxy_file_dict
        self.file_list_config.save_config()
        return config

    def new_hysteria_config(
        self, file_path: str, **kwargs: dict
    ):
        try:
            return HysteriaConfig(file_path, kwargs)
        except Exception as e:
            logging.error(f"创建hysteria配置文件失败:{e}")
            return None


    def sync_proxy_config(self, name: str, **kwargs: dict):
        config = self.get_proxy_config(name)
        if config is None:
            return False
        logging.debug(config.config)
        for key in kwargs:
            config.config[key] = kwargs[key]
        config.save_config()
        return True


class File:
    def __init__(self, name: str, type: str, path: str) -> None:
        self.name = name
        self.type = type
        self.path = path

    def __to_dict__(self) -> dict[str, str]:
        return {"name": self.name, "type": self.type, "path": self.path}


class SubScription:
    def __init__(
        self,
        name: str,
        url: str,
        updateInterval: str,
        lastUpdate: str,
        files: list[File],
    ) -> None:
        self.name = name
        self.url = url
        self.updateInterval = updateInterval
        self.lastUpdate = lastUpdate
        self.files = files

    def __to_dict__(self):
        return {
            "name": self.name,
            "url": self.url,
            "updateInterval": self.updateInterval,
            "lastUpdate": self.lastUpdate,
            "files": [file.__to_dict__() for file in self.files],
        }


class SubScriptionConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__(subscription_file_path)
        if "subscription" not in self.config:
            self.config["subscription"] = []
            self.save_config()
        self.subscription: list[SubScription] = self.config["subscription"]

    def add_subscription(self, subscription: SubScription):
        self.subscription.append(subscription.__to_dict__())
        self.save_config()
        
    def get_subscription(self, name: str) -> SubScription | None:
        for sub in self.subscription:
            if sub["name"] == name:
                return sub
        return None
    
    def get_subscription_all(self) -> list[SubScription]:
        return self.subscription


class HysteriaConfig(BaseConfig):
    def __init__(self, file_path: str, **kwargs) -> None:
        super().__init__(file_path)
        server = checkParam(kwargs, 'server', str, None)
        if server is None:
            logging.error("缺少server字段")
            raise ValueError("HysteriaConfig.__init__()缺少server字段")
        auth = checkParam(kwargs, 'auth', str, None)
        if auth is None:
            logging.error("缺少auth字段")
            raise ValueError("HysteriaConfig.__init__()缺少auth字段")
        http = checkParam(
            kwargs,
            "http",
            dict,
            {"listen": f'http://127.0.0.1:{SettingReader.getInt("http_port")}'},
        )
        socks = checkParam(
            kwargs,
            "socks",
            dict,
            {"listen": f'socks://127.0.0.1:{SettingReader.getInt("socks_port")}'},
        )
        tls = checkParam(kwargs, "tls", dict, {"insecure": True})
        params = {
            "server": server,
            "auth": auth,
            "http": http,
            "socks": socks,
            "tls": tls,
        }
        if "bandwidth" in kwargs:
            bandwidth = checkParam(
                kwargs, "bandwidth", dict, {"up": "20 mbps", "down": "100 mbps"}
            )
            params["bandwidth"] = bandwidth
        kwargs = kwargs.update(params)
        self.config = kwargs
        self.save_config()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s",
        datefmt="%H:%M:%S",
    )
    SettingReader.InitConfig(os.path.join(config_dir_path, "config.yaml"))
    a = GlobalConfig()
    res = a.InitConfig()
    if res is False:
        logging.error("初始化配置失败")
    logging.debug(res)
    logging.debug(a.get_proxy_config_list())
    proxy = a.get_proxy_config("Hongkong-100M")
    config_path = proxy.file_path

    import time

    bin_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "core",
        "hysteria-windows-amd64-avx.exe",
    )

    from talkProxy.core.hysteria import Hysteria

    # 示例命令
    cmd = [bin_path, "-c", config_path]
    hysteria = Hysteria(cmd=cmd)
    hysteria.start()
    start_time = time.time()
    while True:
        try:
            log_message = next(hysteria.get_logs())
            logging.info(f"Received log: {log_message}")
        except StopIteration:
            pass

        # 检查是否需要停止
        if time.time() - start_time > 10:
            hysteria.stop()
            break

        time.sleep(1)
