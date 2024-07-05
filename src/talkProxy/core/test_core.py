import unittest
import logging
class Test(unittest.TestCase):
    
    def test_hysteria(self):
        from talkProxy.tools.settingReader import SettingReader
        from talkProxy.tools.config import GlobalConfig
        import os
        config_dir_name = 'config'
        config_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_dir_name)
        config_file_name = 'config.yaml'
        file_list_name = 'file_list.yaml'
        config_file_path = os.path.join(config_dir_path, config_file_name)
        file_list_path = os.path.join(config_dir_path, file_list_name)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s', datefmt='%H:%M:%S')
        SettingReader.InitConfig(os.path.join(config_dir_path,'setting.yaml'))
        a = GlobalConfig()
        res = a.InitConfig()
        if res is False:
            logging.error('初始化配置失败')
        logging.debug(res)
        logging.debug(a.get_proxy_config_list())


        import time
        bin_path = os.path.join(os.path.dirname(__file__),'hysteria-windows-amd64-avx.exe')

        from talkProxy.core.hysteria import Hysteria
        from talkProxy.log.Logger import subProcessLogHandler
        # 示例命令
        def config1():
            proxy = a.get_proxy_config('Hongkong-100M')
            config_path = proxy.file_path
            cmd = [bin_path, "-c", config_path]
            hysteria = Hysteria(cmd=cmd)
            hysteria.start()
            print(id(hysteria))
            start_time = time.time()
            while True:
                try:
                    log_message = next(hysteria.get_logs())
                    logging.info(f"Received log: {log_message}")
                except StopIteration:
                    pass

                # 检查是否需要停止
                if (time.time() - start_time > 10):
                    # hysteria.stop()
                    break

                time.sleep(1)
        config1()
