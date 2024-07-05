import queue
import subprocess
import threading
from typing import IO
import logging
from talkProxy.log.Logger import subProcessLogHandler

class Hysteria(threading.Thread):
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self, cmd:list[str]) -> None:
        super().__init__()
        self.sub_process = None
        self.stdout = None
        self.stderr = None
        self.stdout_thread = None
        self.stderr_thread = None
        self.cmd = cmd
        self.setup_logger()
        self._stop_event = threading.Event()
        
    def setup_logger(self):
        self.log_queue = queue.Queue()

        
    def run(self):
        self.run_external_program(self.cmd)
        
    def stop(self):
        self._stop_event.set()
        if self.sub_process:
            self.sub_process.terminate()
            self.sub_process.wait()
        if self.stdout_thread:
            self.stdout_thread.join()
        if self.stderr_thread:
            self.stderr_thread.join()
        

    def run_external_program(self, cmd:list[str]):
        # 使用subprocess.Popen运行命令,并将stdout和stderr重定向到管道
        self.sub_process = subprocess.Popen(args = [*cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 创建并启动一个线程来读取输出
        self.stdout_thread = threading.Thread(target=self.read_output, args=(self.sub_process.stdout,))
        self.stderr_thread = threading.Thread(target=self.read_output, args=(self.sub_process.stderr,))
        # 启动两个线程
        self.stdout_thread.start()
        self.stderr_thread.start()
        # 等待外部程序完成
        self.sub_process.wait()
        logging.error('外部程序已退出')

    def read_output(self, stream:IO[str]):
        while not self._stop_event.is_set():
            output = stream.readline()
            if output == '':
                break
            self.log_queue.put(output.strip())
                
    def get_logs(self):
        """获取日志消息"""
        while True:
            try:
                yield self.log_queue.get_nowait()
            except queue.Empty:
                return


        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s')

    