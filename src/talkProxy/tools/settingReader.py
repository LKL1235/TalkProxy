import logging
import yaml
from typing import Optional


class SettingReader:
    __config = None

    @staticmethod
    def InitConfig(configPath: str) -> bool:
        try:
            with open(configPath, encoding="utf-8") as f:
                SettingReader.__config = yaml.safe_load(f)
        except Exception as e:
            logging.error(f"配置文件读取失败:{e}")
            return False
        return True

    def __getConfig(route: str, value_type: type) -> str:
        data = SettingReader.__config
        keys = route.split(".")
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None

        if not isinstance(data, value_type):
            logging.error("读取配置类型错误")
            return None
        return data

    @staticmethod
    def getStr(route: str, default: Optional[str] = None) -> str | None:
        data = SettingReader.__getConfig(route, str)
        return default if data is None else data

    @staticmethod
    def getInt(route: str, default: int = 0) -> int | None:
        data = SettingReader.__getConfig(route, int)
        return default if data is None else data

    @staticmethod
    def getList(route: str, default: Optional[list] = None) -> list | None:
        data = SettingReader.__getConfig(route, list)
        return default if data is None else data

    @staticmethod
    def getDict(route: str, default: Optional[dict] = None) -> dict | None:
        data = SettingReader.__getConfig(route, dict)
        return default if data is None else data

    @staticmethod
    def getBool(route: str, default: Optional[bool] = None) -> bool | None:
        data = SettingReader.__getConfig(route, bool)
        return default if data is None else data