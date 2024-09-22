import threading
import subprocess
from config import *
from concurrent.futures import ThreadPoolExecutor

class beyond:
    executor = ThreadPoolExecutor(max_workers=max_workers)

    @staticmethod
    def execute_command(command):
        try:
            print(f"尝试执行命令：{command}")
            subprocess.run(command, shell=True, check=True)
            print(f"命令执行成功：{command}")
        except subprocess.CalledProcessError as e:
            print(f"执行命令时出错：{e}")
        except Exception as e:
            print(f"执行命令时发生异常：{e}")


    @staticmethod
    def command_1():
        beyond.executor.submit(beyond.execute_command, 'start E:\\tools\\private_tools')

    @staticmethod
    def command_2():
        beyond.executor.submit(beyond.execute_command, 'python3 tools.py 2')

    @staticmethod
    def command_3():
        beyond.executor.submit(beyond.execute_command, 'python3 tools.py 3')

    @staticmethod
    def command_4():
        beyond.executor.submit(beyond.execute_command, 'python3 tools.py 4')

    @staticmethod
    def command_5():
        beyond.executor.submit(beyond.execute_command, 'python3 tools.py 5')

    @staticmethod
    def command_6():
        beyond.executor.submit(beyond.execute_command, 'python3 tools.py 6')

    @staticmethod
    def shutdown():
        print("正在关闭线程池...")
        beyond.executor.shutdown(wait=False)  # 不等待正在执行的任务完成
