import os,json
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
    root.title("渗透工具箱 v0.2")
    root.geometry(f"{width}x{height}+{(root.winfo_screenwidth()-width)//2}+{(root.winfo_screenheight()-height)//2}")

    style = ttk.Style()
    style.configure("Custom.TButton", font=(font_family_GUI, font_size_GUI, font_weight_GUI), padding=padding, width=button_width, background=background, foreground=foreground, relief=relief)

    f = ttk.Frame(root)
    f.pack(pady=5, fill='x', side='top')
    pk = ttk.Notebook(root)
    pk.pack(side='left', padx=(10, 0), expand='yes', fill='both')

    f_1 = ttk.Frame(pk)

    btn_1 = ttk.Button(f_1, text="打开渗透测试目录", command=beyond.command_1, style="Custom.TButton")
    btn_1.grid(row=1, column=1, padx=padx, pady=pady)
    bind_button_right_click(btn_1, '1')

    pk.add(f_1, text='渗透测试')

    f_2 = ttk.Frame(pk)

    btn_2 = ttk.Button(f_2, text="打开信息收集目录", command=beyond.command_2, style="Custom.TButton")
    btn_2.grid(row=1, column=1, padx=padx, pady=pady)
    bind_button_right_click(btn_2, '2')

    pk.add(f_2, text='信息收集')

    f_3 = ttk.Frame(pk)

    btn_3 = ttk.Button(f_3, text="打开漏洞利用目录", command=beyond.command_3, style="Custom.TButton")
    btn_3.grid(row=1, column=1, padx=padx, pady=pady)
    bind_button_right_click(btn_3, '3')

    pk.add(f_3, text='漏洞利用')

    f_4 = ttk.Frame(pk)

    btn_4 = ttk.Button(f_4, text="打开内网安全目录", command=beyond.command_4, style="Custom.TButton")
    btn_4.grid(row=1, column=1, padx=padx, pady=pady)
    bind_button_right_click(btn_4, '4')

    pk.add(f_4, text='内网安全')

    f_5 = ttk.Frame(pk)

    btn_5 = ttk.Button(f_5, text="添加工具", command=beyond.command_5, style="Custom.TButton")
    btn_5.grid(row=1, column=1, padx=padx, pady=pady)
    bind_button_right_click(btn_5, '5')

    btn_6 = ttk.Button(f_5, text="删除工具", command=beyond.command_6, style="Custom.TButton")
    btn_6.grid(row=1, column=2, padx=padx, pady=pady)
    bind_button_right_click(btn_6, '6')

    pk.add(f_5, text='管理工具')

    root.update_idletasks()
    icon_image = load_icon(icon_path)
    if icon_image:
        root.iconphoto(True, icon_image)
    else:
        print("无法加载图标，可能是因为文件不存在或路径错误。")

    root.mainloop()
except Exception as e:
    print(f"发生错误: {e}")
