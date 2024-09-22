import os
import re
import sys
import json
import subprocess
from config import *
from PIL import Image, ImageTk
from ttkbootstrap import Style, tk
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, simpledialog, ttk, StringVar, font,Text

def center_window(window, width, font):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

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

def load_config(config_path):
    if not os.path.exists(config_path):
        return {"信息收集": {}, "渗透测试": {}, "漏洞利用": {}, "内网安全": {}, "管理工具": {}}
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误：{e}")
        return None

def run_command(command, root):
    try:
        if command.lower().startswith('java'):
            # 直接执行Java命令，不打开新的命令行窗口
            subprocess.Popen(command, shell=True)
        else:
            # 使用start命令在新的命令行窗口中运行其他命令
            subprocess.Popen(f'start cmd /k {command} && echo {command}', shell=True)
        # 关闭 GUI 窗口
        root.destroy()
    except Exception as e:
        print(f"Error executing command: {e}")
        messagebox.showerror("错误", f"命令执行失败：{e}")

class ToolSelectionDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("选择工具")
        self.iconname("tool selection")
        tk.Label(master, text="请输入工具编号：").grid(row=0)
        self.tool_id_entry = tk.Entry(master)
        self.tool_id_entry.grid(row=0, column=1)
        self.tool_id_entry.bind('<Return>', self.apply)  # 绑定回车键
        return self.tool_id_entry  # initial focus

    def apply(self):
        tool_id = self.tool_id_entry.get()
        if tool_id:  # 检查输入是否为空
            self.result = tool_id  # 设置结果，这样 self.top.result() 能够返回工具编号
            self.ok()  # 关闭对话框并确认输入
        else:
            messagebox.showerror("错误", "工具编号不能为空")

    def command_selection(self, tool_id):
        tool_info = config['tools'][tool_id]
        command_dialog = CommandSelectionDialog(tool_info, self.top)
        command_dialog.mainloop()
        if command_dialog.command_id:
            command_to_run = tool_info['commands'].get(command_dialog.command_id)
            if command_to_run:
                run_command(command_to_run, self.top)
            else:
                messagebox.showerror("错误", "输入的命令编号无效")

class CommandSelectionDialog(simpledialog.Dialog):
    def __init__(self, tool_info, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tool_info = tool_info
        self.command_id = None

    def body(self, master):
        self.title("选择命令")
        self.iconname("command selection")
        tk.Label(master, text="请选择命令编号：").grid(row=0)
        self.command_id_entry = tk.Entry(master)
        self.command_id_entry.grid(row=0, column=1)
        self.command_id_entry.bind('<Return>', self.apply)  # 绑定回车键
        for i, cmd in enumerate(self.tool_info['commands']):
            tk.Radiobutton(master, text=f"{i}. {cmd}", variable=self.command_id_entry, value=str(i)).grid(row=i+1, column=0, sticky=tk.W)
        return self.command_id_entry  # initial focus

    def apply(self):
        self.command_id = self.command_id_entry.get()
        if self.command_id:  # 检查输入是否为空
            self.result = self.command_id  # 设置结果
            self.ok()  # 关闭对话框并确认输入
        else:
            messagebox.showerror("错误", "命令编号不能为空")


def show_command_dialog(tool_info, root, custom_font, callback):
    dialog = Toplevel(root)
    dialog.grab_set()
    center_window(dialog, dialog_width, dialog_height)
    
    Label(dialog, text=f"{tool_info['name']} 支持以下命令：", font=custom_font).pack(pady=5)
    
    command_labels = [f"{i}. {cmd}" for i, cmd in tool_info['commands'].items()]
    command_var = StringVar(dialog)
    command_var.set(command_labels[0])
    ttk.Label(dialog, text="选择命令：", font=custom_font).pack(pady=5)
    command_entry = ttk.Combobox(dialog, textvariable=command_var, values=command_labels, font=custom_font)
    command_entry.pack(pady=pady)
    
    # 定义param_combobox和param_text
    Label(dialog, text="选择参数进行修改：", font=custom_font).pack(pady=pady)
    param_var = StringVar(dialog)
    param_combobox = ttk.Combobox(dialog, textvariable=param_var, font=custom_font)
    param_combobox.pack(pady=5)
    
    Label(dialog, text="修改参数值：", font=custom_font).pack(pady=10)
    param_text = Text(dialog, height=10, width=100, font=custom_font)
    param_text.pack(pady=5)
    
    # 绑定事件
    command_entry.bind('<<ComboboxSelected>>', lambda event, tool_info=tool_info, dialog=dialog, custom_font=custom_font, param_combobox=param_combobox, param_text=param_text: update_parameters(event, tool_info, dialog, custom_font, param_combobox, param_text))
    
    Button(dialog, text="执行命令", command=lambda: execute_command(tool_info, command_var, param_var, param_text, param_combobox, callback), font=custom_font).pack(pady=10)
    
    dialog.protocol("WM_DELETE_WINDOW", lambda: (dialog.destroy(), root.quit()))

def update_parameters(event, tool_info, dialog, custom_font, param_combobox, param_text):
    selected_command = event.widget.get()
    match = re.match(r"(\d+)\.\s*(.*)", selected_command)
    if match:
        command_number = match.group(1)
        command_to_run = tool_info['commands'][command_number]
        params = command_to_run.split() if ' ' in command_to_run else [command_to_run]
        param_combobox['values'] = params
        param_combobox.current(0)
        param_text.delete("1.0", "end")
        if params:
            param_text.insert("1.0", params[0])
        
def execute_command(tool_info, command_var, param_var, param_text, param_combobox, callback):
    selected_command = command_var.get()
    match = re.match(r"(\d+)\.\s*(.*)", selected_command)
    if match:
        command_number = match.group(1)
        original_command = tool_info['commands'][command_number]
        command_parts = original_command.split() if ' ' in original_command else [original_command]
        selected_param_index = param_combobox.current()
        modified_param = param_text.get("1.0", "end").strip()
        command_parts[selected_param_index] = modified_param
        modified_command = ' '.join(command_parts)
        callback(modified_command)
    else:
        messagebox.showerror("错误", "无法解析命令编号")
        
def main():
    global root, custom_font
    config = load_config('config.json')
    
    if not config:
        messagebox.showerror("错误", "无法加载配置文件，程序退出。")
        sys.exit(1)
    
    root = tk.Tk()
    style = Style(theme=themes)  # 设置主题
    root.withdraw()  # 隐藏主窗口
    icon_image = load_icon(icon_path)
    if icon_image:
        root.iconphoto(True, icon_image)
    
    custom_font = font.Font(family=font_family, size=font_size, weight=font_weight)
    
    if len(sys.argv) < 2:
        messagebox.showerror("错误", "请通过命令行参数输入工具编号。")
        sys.exit(1)
    
    tool_id = sys.argv[1]
    tool_info = None
    for category_key, tools in config.items():
        if str(tool_id) in tools:
            tool_info = tools[str(tool_id)]
            os.chdir(tool_info['path'])
            break
    
    if tool_info:
        show_command_dialog(tool_info, root, custom_font, lambda cmd: run_command(cmd, root))
    else:
        messagebox.showerror("错误", "输入的工具编号无效，程序退出。")
        sys.exit(1)

    root.mainloop()

if __name__ == "__main__":
    main()
