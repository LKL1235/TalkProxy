import logging
import os
import yaml
from talkProxy.tools.common import randomStr
from talkProxy.tools.settingReader import SettingReader
from typing import Optional

config_dir_name = 'config'
config_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_dir_name)
config_file_name = 'config.yaml'
file_list_name = 'file_list.yaml'
config_file_path = os.path.join(config_dir_path, config_file_name)
file_list_path = os.path.join(config_dir_path, file_list_name)

def checkParam(kwDict:dict, key:str, param_type:type, default:Optional[any] = None):
    if key not in kwDict:
        return default
    if not isinstance(kwDict[key], param_type):
        logging.error(f'{key}参数类型错误')
        return None
    return kwDict[key]
    

class BaseConfig:
    def __init__(self, file_path:str) -> None:
        self.config:dict = None
        self.file_path:str = file_path
        self.load_config()
        
    def load_config(self): 
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w+') as f:
                f.write('')
        with open(self.file_path, 'r+') as f:
            self.config = yaml.safe_load(f)
            if self.config is None:
                self.config = {}
            logging.debug(self.config)
            
    def reload_config(self):
        self.load_config()
        
    def save_config(self):
        with open(self.file_path, 'w') as f:
            yaml.dump(self.config, f)
        self.reload_config()

class GlobalConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__(config_file_path)
        self.file_list_config = FileListConfig()
        
    def InitConfig(self):
        if self.config is None:
            logging.error('全局配置文件为空')
            return False
        for key in self.config:
            if 'server' not in self.config[key] or 'auth' not in self.config[key]:
                logging.error(f'配置文件中的 {key} 缺少server或auth字段')
                return False
            if key not in self.file_list_config.config:
                logging.debug(f'配置文件中的 {key} 在文件列表中不存在, 创建...')
                new_config = self.new_proxy_config(key, self.config[key]['type'], **self.config[key])
                if new_config is None:
                    return False
            else:
                self.sync_proxy_config(key, **self.config[key])
        default_proxy = SettingReader.getStr('default')
        if default_proxy is None or default_proxy == 'None':
            logging.debug(f'未找到默认代理配置, default:{default_proxy}')
            return None
        return self.get_proxy_config(default_proxy)
        
    def get_proxy_config_list(self) -> list[dict[str, str]]:
        return [{'name': key,'file': self.file_list_config.config[key]['file'], 'type': self.file_list_config.config[key]['type']} for key in self.file_list_config.config if 'file' in self.file_list_config.config[key] and 'type' in self.file_list_config.config[key]]
    
    def get_proxy_config(self, name:str) -> BaseConfig | None:
        config = self.file_list_config.config.get(name)
        if config is None:
            logging.error(f'未找到{name}的配置文件')
            return None
        if 'file' not in config or 'type' not in config:
            logging.error(f'{name}的配置文件缺少file或type字段')
            return None
        match self.file_list_config.config[name]['type']:
            case 'hysteria':
                return HysteriaConfig(config['file'])
            case _:
                logging.error(f'不支持的代理类型{self.file_list_config.config[name]["type"]}')
                return None
        
    def new_proxy_config(self, name:str, proxy_type:str, **kwargs:dict)-> BaseConfig | None:
        file_path = os.path.join(config_dir_path,f"{randomStr()}.yaml")
        config = None
        match proxy_type:
            case 'hysteria':
                server = checkParam(kwargs, 'server', str, None)
                auth = checkParam(kwargs, 'auth', str, None)
                if not all([server, auth]):
                    logging.error(f'创建{name}的hysteria配置文件失败, 缺少server或auth字段')
                    return None
                config = self.new_hysteria_config(file_path, **kwargs)
            case _:
                logging.error(f'不支持的代理类型{self.file_list_config.config[name]["type"]}')
                return None
        new_proxy_file_dict:dict = {'file':os.path.abspath(file_path), 'type':proxy_type}
        self.file_list_config.config[name] = new_proxy_file_dict
        self.file_list_config.save_config()
        return config
        
    def new_hysteria_config(self, file_path:str, server:str, auth:str, **kwargs:dict):
        hysteria = HysteriaConfig(file_path)
        if hysteria.config is None:
            logging.error('创建hysteria配置文件失败')
            return
        hysteria.config['server'] = server
        hysteria.config['auth'] = auth
        hysteria.config['http'] = checkParam(kwargs, 'http', dict, {'listen':f'http://127.0.0.1:{SettingReader.getInt("http_port")}'})
        hysteria.config['socks'] = checkParam(kwargs, 'socks', dict, {'listen':f'socks://127.0.0.1:{SettingReader.getInt("socks_port")}'})
        hysteria.config['tls'] = checkParam(kwargs, 'tls', dict, {'insecure':True})
        if 'bandwidth' in kwargs:
            hysteria.config['bandwidth'] = checkParam(kwargs, 'bandwidth', dict, {'up': '20 mbps', 'down': '100 mbps'})
        hysteria.save_config()
        
    def sync_proxy_config(self, name:str, **kwargs:dict):
        config = self.get_proxy_config(name)
        if config is None:
            return False
        logging.debug(config.config)
        for key in kwargs:
            config.config[key] = kwargs[key]
        config.save_config()
        return True
        
class FileListConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__(file_list_path)
        if self.config is None:
            self.config = {}
            self.save_config()
        
class HysteriaConfig(BaseConfig):
    def __init__(self, file_path:str) -> None:
        super().__init__(file_path)
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s', datefmt='%H:%M:%S')
    SettingReader.InitConfig(os.path.join(config_dir_path,'setting.yaml'))
    a = GlobalConfig()
    res = a.InitConfig()
    if res is False:
        logging.error('初始化配置失败')
    logging.debug(res)
    logging.debug(a.get_proxy_config_list())
    proxy = a.get_proxy_config('Hongkong-100M')
    config_path = proxy.file_path

    import time
    bin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'core','hysteria-windows-amd64-avx.exe')

    from talkProxy.core.hysteria import Hysteria
    from talkProxy.log.Logger import subProcessLogHandler
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
        if (time.time() - start_time > 10):
            hysteria.stop()
            break

        time.sleep(1)

