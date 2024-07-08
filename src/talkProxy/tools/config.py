import logging
import os
import threading
import yaml

from .remote_config import get_remote_config
from .common import randomStr, timestamp
from .settingReader import SettingReader
from typing import Any, Optional

config_dir_name = "config"
config_dir_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), config_dir_name
)
config_file_name = "config.yaml"
config_file_path = os.path.join(config_dir_path, config_file_name)
subscription_file_name = "subscription.yaml"
subscription_file_path = os.path.join(config_dir_path, subscription_file_name)


ProxyType: list[str] = ["hysteria2"]


class File:
    def __init__(self, name: str, type: str, path: str) -> None:  # noqa: A002
        self.name = name
        self.type = type
        self.path = path

    def __dict__(self) -> dict[str, str]:
        return {"name": self.name, "type": self.type, "path": self.path}

    def to_dict(self) -> dict[str, str]:
        return self.__dict__()


class Subscription:
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

    def __dict__(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "updateInterval": self.updateInterval,
            "lastUpdate": self.lastUpdate,
            "files": [file.to_dict() for file in self.files],
        }

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__()


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

    def load_config(self) -> bool:
        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, "w+") as f:
                    f.write("")
            with open(self.file_path, "r+") as f:
                self.config = yaml.safe_load(f)
                if self.config is None:
                    self.config = {}
                logging.debug(self.config)
            return True
        except Exception as e:
            logging.error(f"读取配置文件失败:{e}")
            return False

    def reload_config(self) -> bool:
        return self.load_config()

    def save_config(self) -> bool:
        try:
            with open(self.file_path, "w") as f:
                yaml.dump(self.config, f)
        except Exception as e:
            logging.error(f"保存配置文件失败:{e}")
            return False
        return self.reload_config()


class SubscriptionConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__(subscription_file_path)
        if "subscription" not in self.config:
            self.config["subscription"] = []
            if not self.save_config():
                logging.error("初始化配置文件失败")

    def add_subscription(self, subscription: Subscription) -> bool:
        for sub in self.config["subscription"]:
            if sub["name"] == subscription.name:
                logging.error(f"已存在{subscription.name}订阅")
                self.update_subscription(name=subscription.name, subscription=subscription)
                return True
        self.config["subscription"].append(subscription.to_dict())
        if not self.save_config():
            logging.error("初始化配置文件失败")
            return False
        return True

    def get_subscription(self, name: str) -> Subscription | None:
        for sub in self.config["subscription"]:
            if sub["name"] == name:
                return Subscription(**sub)
        return None

    def remove_subscription(self, name: str) -> bool:
        for sub in self.config["subscription"]:
            if sub["name"] == name:
                self.config["subscription"].remove(sub)
                if not self.save_config():
                    logging.error("初始化配置文件失败")
                    return False
        return True

    def update_subscription(self, name: str, subscription: Subscription) -> bool:
        for i, sub in enumerate(self.config["subscription"]):
            if sub["name"] == name:
                self.config["subscription"][i] = subscription.to_dict()
                if not self.save_config():
                    logging.error("初始化配置文件失败")
                    return False
        return True
    
    def is_subscription_exist(self, name: str) -> bool:
        return any(sub["name"] == name for sub in self.config["subscription"])

    def get_subscription_all(self) -> list[Subscription]:
        if not self.reload_config():
            logging.error("get_subscription_all reload_config 失败")
            return None
        subscription_list = []
        for subscription_str in self.config["subscription"]:
            subscription = Subscription(**subscription_str)
            subscription_list.append(subscription)
        return subscription_list
            


class Hysteria2Config(BaseConfig):
    def __init__(self, file_path: str, **kwargs: dict[str, Any]) -> None:
        super().__init__(file_path)
        server = checkParam(kwargs, "server", str, None)
        if server is None:
            logging.error("缺少server字段")
            raise ValueError("Hysteria2Config.__init__()缺少server字段")
        auth = checkParam(kwargs, "auth", str, None)
        password = checkParam(kwargs, "password", str, None)
        if auth is None and password is None:
            logging.error("缺少auth字段")
            raise ValueError("Hysteria2Config.__init__()缺少auth(password)字段")
        auth = auth or password
        http = checkParam(
            kwargs,
            "http",
            dict,
            {"listen": f'127.0.0.1:{SettingReader.getInt("httpPort")}'},
        )
        socks = checkParam(
            kwargs,
            "socks",
            dict,
            {"listen": f'127.0.0.1:{SettingReader.getInt("socksPort")}'},
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
        new_params = kwargs
        new_params.update(params)
        self.config = new_params
        if not self.save_config():
            logging.error("初始化配置文件失败")
            raise ValueError("Hysteria2Config.__init__() save_config失败")


class GlobalConfig(BaseConfig):
    __lock = threading.Lock()
    __instance = None

    def __init__(self) -> None:
        super().__init__(config_file_path)
        self.subscriptionConfig = SubscriptionConfig()
        if self.config == {}:
            self.config = {"httpPort": 7899, "socksPort": 7900, "default": None}
            if not self.save_config():
                logging.error("初始化配置文件失败")

    @classmethod
    def InitConfig(cls: "GlobalConfig") -> "GlobalConfig":
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = GlobalConfig()
        return cls.__instance

    @classmethod
    def GetInstance(cls: "GlobalConfig") -> "GlobalConfig":
        return cls.__instance
    
    @classmethod
    def get_default_subscription(cls: "GlobalConfig") -> Optional[SubscriptionConfig]:
        globalConfig:GlobalConfig = cls.GetInstance()
        defaultSubscription = globalConfig.config.get("default", None)
        if not defaultSubscription:
            logging.error("未设置默认订阅")
            return None
        return globalConfig.subscriptionConfig.get_subscription(defaultSubscription)

    def get_subscription_config(self) -> "SubscriptionConfig":
        return self.subscriptionConfig

    def new_subscription(
        self, name: str, url: str, updateInterval: str
    ) -> Optional[Subscription]:
        res = self.subscriptionConfig.is_subscription_exist(name)
        if res:
            logging.error(f"已存在{name}订阅")
            return None
        remote_dict = get_remote_config(url)
        remote_proxies: list[dict] = remote_dict.get("proxies", None)
        if remote_proxies is None:
            logging.error(f"获取{name}:{url}订阅失败")
            return None
        lastUpdate = timestamp()
        new_config_file_list: list[File] = []
        for proxy in remote_proxies:
            proxy_name = proxy.get("name", None)
            proxy_type = proxy.get("type", None)
            if not all([proxy_name, proxy_type]):
                logging.error(f"获取{name}:{url}订阅失败, 代理信息不完整")
                continue
            if proxy_type not in ProxyType:
                logging.error(f"{name}:{url}中包含, 不支持的代理类型:{proxy_type}")
                continue
            new_config_file: File = self.new_proxy_config(**proxy)
            if not new_config_file:
                logging.error(f"创建{name}:{url}订阅中的{proxy_name}配置文件失败")
                continue
            new_config_file_list.append(new_config_file)
        return Subscription(name, url, updateInterval, lastUpdate, new_config_file_list)

    def new_proxy_config(self, **kwargs: dict) -> File | None:
        proxy_type = checkParam(kwargs, "type", str, None)
        if proxy_type is None:
            logging.error("缺少type字段")
            return None
        name = checkParam(kwargs, "name", str, None)
        if name is None:
            logging.error("缺少name字段")
            return None
        file_path = os.path.join(config_dir_path, f"{randomStr()}.yaml")
        config = None
        match proxy_type:
            case "hysteria2":
                config = self.new_hysteria2_config(file_path, **kwargs)
                if not config:
                    logging.error(f"创建{name}的hysteria2配置文件失败")
                    return None
            case _:
                logging.error(
                    f"不支持的代理类型, name: {name}, proxy_type: {proxy_type}, kwargs: {kwargs}"
                )
                return None
        if not config:
            logging.error(f"创建{name}的配置文件失败")
            return None
        new_proxy_file: File = File(
            name=name,
            type=proxy_type,
            path=os.path.abspath(file_path),
        )
        return new_proxy_file

    def new_hysteria2_config(
        self, file_path: str, **kwargs: dict
    ) -> Optional[Hysteria2Config]:
        try:
            return Hysteria2Config(file_path, **kwargs)
        except Exception as e:
            logging.error(f"创建hysteria2配置文件失败:{e}")
            return None

    def sync_proxy_config(self, name: str, url: str, updateInterval: int) -> bool:
        subscriptionConfig = self.subscriptionConfig.config["subscription"]
        index: list = [
            i
            for i, sub in enumerate(subscriptionConfig, start=0)
            if sub["name"] == name
        ]
        if not index:
            logging.error(f"未找到{name}订阅")
            return False
        index = index[-1]
        subscription: list = [sub for sub in subscriptionConfig if sub["name"] == name]
        if not subscription:
            logging.error(f"未找到{name}订阅")
            return False
        subscription: dict = subscription[-1]
        subscription: Subscription = Subscription(**subscription)
        old_file_list: list[str] = [file['path'] for file in subscription.files]
        old_file_list = [f for f in old_file_list if os.path.exists(f)]
        new_subscription = self.new_subscription(subscription.name, url, updateInterval)
        self.subscriptionConfig.update_subscription(name, new_subscription)
        [os.remove(file) for file in old_file_list]
        return True


def test():
    import logging
    import os
    from talkProxy.tools.settingReader import SettingReader
    from talkProxy.tools.config import GlobalConfig, config_dir_path
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
    # res = a.new_subscription("test","http://38.147.184.160:80/hood-list","10")
    # if not res:
        # logging.error("创建订阅失败")
        # return False
    # res = a.subScriptionConfig.add_subscription(res)
    # res = a.sync_proxy_config("test","http://38.147.184.160:80/hood-list","10")
    res = a.subscriptionConfig.get_subscription_all()
    if res is False:
        logging.error("添加订阅失败")
        return False
    name_list = [sub.name for sub in res]
    print(name_list)
    return True
        
def test_start():
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

    from talkProxy.core.hysteria2 import Hysteria2

    # 示例命令
    cmd = [bin_path, "-c", config_path]
    hysteria2 = Hysteria2(cmd=cmd)
    hysteria2.start()
    start_time = time.time()
    while True:
        try:
            log_message = next(hysteria2.get_logs())
            logging.info(f"Received log: {log_message}")
        except StopIteration:
            pass

        # 检查是否需要停止
        if time.time() - start_time > 10:
            hysteria2.stop()
            break

        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s",
        datefmt="%H:%M:%S",
    )
    test()