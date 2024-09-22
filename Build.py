import json
import os
from tkinter import ttk
from config import line_count,python3_path,java_path

def read_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def gen_click(config):
    no = 1
    with open('beyond.py', 'w', encoding='utf-8') as f:
        f.write("""import threading
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

""")
        for category, tools in config.items():
            for tool_id, tool in tools.items():
                cmd = list(tool['commands'].values())[0].replace("\\", "\\\\")
                if "start" in cmd or "add_tools.py" in cmd or "remove_tools.py" in cmd:
                    f.write(f"""
    @staticmethod
    def command_{tool_id}():
        beyond.executor.submit(beyond.execute_command, '{cmd}')
""")
                else:
                    f.write(f"""
    @staticmethod
    def command_{tool_id}():
        beyond.executor.submit(beyond.execute_command, '{python3_path} tools.py {tool_id}')
""")
        f.write("""
    @staticmethod
    def shutdown():
        print("正在关闭线程池...")
        beyond.executor.shutdown(wait=False)  # 不等待正在执行的任务完成
""")
                

def gen_body(config):
    with open('gui.py', 'w', encoding='utf-8') as f:
        f.write("""import os,json
import subprocess
from config import *
import tkinter as tk
from tkinter import ttk
from beyond import beyond
import ttkbootstrap as ttk
from PIL import Image, ImageTk

def load_icon(path):
    if os.path.exists(path):
        try:
            image = Image.open(path)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"加载图像时发生错误: {e}")
            return None
    else:
        print(f"文件不存在: {path}")
        return None

def open_tool_directory(event, button_id):
    print(f"尝试打开工具目录：{button_id}")
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    for category, buttons in config.items():
        for button, details in buttons.items():
            if button == button_id:
                tool_path = details['path']
                if os.path.exists(tool_path):
                    try:
                        os.startfile(tool_path)
                    except Exception as e:
                        print(f"打开目录时发生错误: {e}")
                        return
                else:
                    print(f"文件不存在: {tool_path}")
                    return
                    
def bind_button_right_click(button, button_id):
    button.bind("<Button-3>", lambda event, button_id=button_id: open_tool_directory(event, button_id))

try:
    root = ttk.Window(themename=themes)
    root.title("渗透工具箱")
    root.geometry(f"{width}x{height}+{(root.winfo_screenwidth()-width)//2}+{(root.winfo_screenheight()-height)//2}")

    style = ttk.Style()
    style.configure("Custom.TButton", font=(font_family_GUI, font_size_GUI, font_weight_GUI), padding=padding, width=button_width, background=background, foreground=foreground, relief=relief)

    f = ttk.Frame(root)
    f.pack(pady=5, fill='x', side='top')
    pk = ttk.Notebook(root)
    pk.pack(side='left', padx=(10, 0), expand='yes', fill='both')
""")
        no = 1
        for category, tools in config.items():
            f.write(f"""
    f_{no} = ttk.Frame(pk)
""")
            col = 0
            row = 1
            for tool_id, tool_info in tools.items():
                col += 1
                if col % line_count == 0:
                    col = 1
                    row += 1
                    f.write(f"""
    f_{no+1} = ttk.Frame(pk)
""")
                cmd = list(tool_info['commands'].values())[0]
                tool_path = tool_info.get('directory', '')  # 获取工具的目录路径
                f.write(f"""
    btn_{tool_id} = ttk.Button(f_{no}, text="{tool_info['name']}", command=beyond.command_{tool_id}, style="Custom.TButton")
    btn_{tool_id}.grid(row={row}, column={col}, padx=padx, pady=pady)
    bind_button_right_click(btn_{tool_id}, '{tool_id}')
""")
            no += 1
            f.write(f"""
    pk.add(f_{no-1}, text='{category}')
""")
        f.write("""
    root.update_idletasks()
    icon_image = load_icon(icon_path)
    if icon_image:
        root.iconphoto(True, icon_image)
    else:
        print("无法加载图标，可能是因为文件不存在或路径错误。")

    root.mainloop()
except Exception as e:
    print(f"发生错误: {e}")
""")

if __name__ == "__main__":
    config_path = 'config.json'
    config = read_config(config_path)
    if config:
        gen_click(config)
        gen_body(config)
    else:
        print("无法加载配置文件，GUI 未更新。")