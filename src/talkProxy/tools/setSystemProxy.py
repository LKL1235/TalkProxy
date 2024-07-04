import winreg
import logging

# TODO:是否需要重写 ProxyOverride 的值?
# localhost;127.*;192.168.*;10.*;172.16.*

reg_key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'

def open_reg_key() -> winreg.HKEYType | None:
    """打开注册表项"""
    try:
        return winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_WRITE)
    except OSError as e:
        logging.error(f'打开注册表项失败: {e}')
        return None

def set_proxy(proxy_address:str = '127.0.0.1', proxy_port:str = '7899'):
    """设置 Windows 全局系统代理"""
    try:
        # 打开注册表项
        key = open_reg_key()
        if key is None:
            logging.error('打开注册表项失败')
            return False
        # 设置代理服务器地址
        winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, f'{proxy_address}:{proxy_port}')
        # 启用代理
        winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
        # 关闭注册表项
        winreg.CloseKey(key)
        logging.info(f'代理设置成功, proxy_addr:{proxy_server}, proxy_enable:{proxy_enable}')
        return True
    except OSError as e:
        logging.error(f'设置代理失败: {e}')
        return False

def unset_proxy():
    """取消 Windows 全局系统代理"""
    try:
        # 打开注册表项
        key = open_reg_key()
        if key is None:
            logging.error('打开注册表项失败')
            return False
        # 删除代理服务器地址
        # winreg.DeleteValue(key, 'ProxyServer')
        # 禁用代理
        winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
        # 关闭注册表项
        winreg.CloseKey(key)
        logging.info('代理设置已取消')
        return True
    except OSError as e:
        logging.error(f'取消代理失败: {e}')
        return False
    
def get_proxy():
    """获取 Windows 全局系统代理"""
    try:
        # 打开注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_READ)
        # 获取代理服务器地址
        proxy_server, _ = winreg.QueryValueEx(key, 'ProxyServer')
        # 获取代理状态
        proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
        # 关闭注册表项
        winreg.CloseKey(key)
        logging.info(f'获取代理成功, proxy_addr:{proxy_server}, proxy_enable:{proxy_enable}')
        return proxy_server, proxy_enable
    except OSError as e:
        logging.error(f'获取代理失败: {e}')
        return None, None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d")
    set_proxy('127.0.0.1', '7899')
    proxy_server,proxy_enable =get_proxy()
    print(proxy_server,proxy_enable)