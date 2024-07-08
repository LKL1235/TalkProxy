import logging
import requests
import yaml

def get_remote_config(url:str)-> dict| None:
    remote_config = requests.get(url, timeout=10)
    if remote_config.status_code != 200:
        return None
    try:
        remote_config_dict = yaml.safe_load(remote_config.text)
    except Exception as e:
        logging.error(f"解析远程配置文件失败:{e}")
        return None
    return remote_config_dict