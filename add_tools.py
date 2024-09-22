import os
import json
import threading
import subprocess
from config import *
from PIL import Image, ImageTk
from ttkbootstrap import Style, tk
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, simpledialog, ttk, font

def center_window(window, width, height):
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

def get_total_tool_count(config):
    total_count = 0
    for category in config.values():
        total_count += len(category)  # 累加每个类别中的工具数量，包括重复的ID
    return total_count

def add_command_dialog(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, index=0, answers=None):
    if index == command_count:
        update_gui_callback(config, base_path, config_path, root, category, next_id, commands, answers)
        return

    dialog = Toplevel(root)
    dialog.grab_set()  # 设置模态对话框，阻止其他窗口获取焦点
    center_window(dialog, dialog_width, dialog_height)
    Label(dialog, text=f"请输入命令 {index + 1}：", font=custom_font).pack(pady=pady)
    entry = Entry(dialog, width=width, font=custom_font)
    entry.pack(pady=pady)
    entry.focus_set()  # 将焦点设置到输入框
    entry.bind('<Return>', lambda event: on_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, index, entry.get(), dialog, answers))
    Button(dialog, text="确定", command=lambda: on_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, index, entry.get(), dialog, answers), font=custom_font).pack(pady=pady)

    # 确保新窗口在最前面
    dialog.lift()
    dialog.focus_force()

    dialog.protocol("WM_DELETE_WINDOW", lambda: on_close(index, dialog, commands))
    dialog.grab_release()  # 释放模态对话框

def on_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, index, value, dialog, answers):
    # 获取选择的环境
    environment = answers[4]
    if environment == "Python3":
        command_prefix = python3_path
    elif environment == "Java":
        command_prefix = java_path+' -jar'
    else:
        command_prefix = ""

    # 拼接命令
    full_command = f"{command_prefix} {value}" if command_prefix else value
    commands[index] = full_command  # 存储拼接后的命令

    dialog.destroy()  # 销毁当前对话框
    save_config(config_path, config)  # 保存配置

    if index + 1 < command_count:
        # 还有更多的命令需要输入
        add_command_dialog(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, index + 1, answers)
    else:
        # 所有命令都已输入，调用回调函数来更新 GUI 和保存配置
        update_gui_callback(config, base_path, config_path, root, category, next_id, commands, answers)
def on_close(index, dialog, commands):
    # 显示警告对话框
    response = messagebox.showwarning("警告", "未完成操作，所有窗口将被关闭！")
    
    # 销毁当前对话框和所有Toplevel对话框，无论警告对话框的结果如何
    dialog.destroy()
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    
    # 退出主循环
    root.quit()

def add_tool(config, base_path, config_path, root, update_gui_callback, next_id):
    # 获取所有类别及其编号
    global current_index
    categories = {i+1: category for i, category in enumerate(config.keys())}
    questions = [
        "请选择添加工具添加到的类别（输入数字）：",
        "请输入要添加工具的名称：",
        "请输入相对于基础路径的工具子路径：",
        "请选择工具环境（Python3 或 Java）："
    ]
    answers = [""] * len(questions)
    current_index = 0
    
    def ask_integer(parent, prompt, title="输入", minvalue=1):
        dialog = Toplevel(parent)
        dialog.title(title)
        center_window(dialog, dialog_width, dialog_height)  # 自定义宽度和高度
        Label(dialog, text=prompt, font=custom_font).pack(pady=pady)
        entry = Entry(dialog, font=custom_font)
        entry.pack(pady=pady)
        entry.focus_set()

        def on_ok():
            try:
                value = int(entry.get())
                if value < minvalue:
                    raise ValueError(f"值必须大于等于 {minvalue}")
                dialog.result = value  # 设置结果，以便在对话框关闭后可以访问
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的整数")

        Button(dialog, text="确定", command=on_ok, font=custom_font).pack(pady=pady)
        dialog.bind('<Return>', on_ok)
        dialog.grab_set()  # 模态对话框
        dialog.wait_window()  # 等待对话框关闭
        return dialog.result if hasattr(dialog, 'result') else None

    def on_tool_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, answers, index, value, dialog):
        global current_index  # 声明 current_index 为全局变量
        if index >= len(answers):
            answers.extend([None] * (index + 1 - len(answers)))
        answers[index] = value
        current_index += 1
        dialog.destroy()  # 销毁当前对话框

        if current_index < len(questions):
            create_dialog(current_index, category, next_id, config, root, update_gui_callback)
        else:
            # 工具信息输入完成，询问命令数量
            command_count_dialog = Toplevel(root)
            center_window(command_count_dialog, dialog_width, dialog_height)

            # 确保新窗口在最前面
            command_count_dialog.lift()
            command_count_dialog.focus_force()

            Label(command_count_dialog, text="请输入命令数量：", font=custom_font).pack(pady=pady)
            entry = Entry(command_count_dialog, font=custom_font)
            entry.pack(pady=pady)
            entry.focus_set()

            def on_command_count_ok(event=None):
                try:
                    command_count = int(entry.get())
                    commands = [""] * command_count
                    add_command_dialog(config, base_path, config_path, root, update_gui_callback, category, next_id, command_count, commands, 0, answers)
                    command_count_dialog.destroy()
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的整数")

            Button(command_count_dialog, text="确定", command=on_command_count_ok, font=custom_font).pack(pady=pady)
            entry.bind('<Return>', on_command_count_ok)
            command_count_dialog.protocol("WM_DELETE_WINDOW", lambda: on_command_count_cancel(command_count_dialog))
    def on_command_count_cancel(dialog):
        dialog.destroy()
        root.quit()
        
    def on_tool_close(index, dialog, answers):
        dialog.destroy()
        root.quit()  # 退出主循环，关闭所有窗口

    def create_dialog(index, category, next_id, config, root, update_gui_callback):
        dialog = Toplevel(root)
        center_window(dialog, dialog_width, dialog_height)

        # 确保新窗口在最前面
        dialog.lift()
        dialog.focus_force()

        icon_image = load_icon(icon_path)
        if icon_image:
            dialog.iconphoto(True, icon_image)

        if index == 0:  # 如果是第一个问题，让用户选择类别
            Label(dialog, text=questions[index], font=custom_font).pack(pady=pady)
            categories = {i+1: category for i, category in enumerate(config.keys())}
            categories_list = [f"{key}. {value}" for key, value in categories.items()]
            combobox = ttk.Combobox(dialog, values=categories_list, state="readonly", width=width, font=custom_font)
            combobox.pack(pady=pady)
            combobox.bind('<<ComboboxSelected>>', lambda event: on_tool_ok(config, base_path, config_path, root, update_gui_callback, categories[int(event.widget.get().split('.')[0])], next_id, answers, index+1, "", dialog))
            Button(dialog, text="确定", command=lambda: on_tool_ok(config, base_path, config_path, root, update_gui_callback, categories[int(combobox.get().split('.')[0])], next_id, answers, index+1, "", dialog), font=custom_font).pack(pady=pady)
        elif index == 3:  # 环境选择
            Label(dialog, text=questions[index], font=custom_font).pack(pady=pady)
            environments = ["Python3", "Java"]
            combobox = ttk.Combobox(dialog, values=environments, state="readonly", width=width, font=custom_font)
            combobox.pack(pady=pady)
            combobox.bind('<<ComboboxSelected>>', lambda event: on_tool_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, answers, index+1, combobox.get(), dialog))
            Button(dialog, text="确定", command=lambda: on_tool_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, answers, index+1, combobox.get(), dialog), font=custom_font).pack(pady=pady)
        else:
            Label(dialog, text=questions[index], font=custom_font).pack(pady=pady)
            entry = Entry(dialog, width=width, font=custom_font)
            entry.pack(pady=pady)
            entry.focus_set()  # 将焦点设置到输入框
            entry.bind('<Return>', lambda event: on_tool_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, answers, index, entry.get(), dialog))
            Button(dialog, text="确定", command=lambda: on_tool_ok(config, base_path, config_path, root, update_gui_callback, category, next_id, answers, index, entry.get(), dialog), font=custom_font).pack(pady=pady)

        dialog.protocol("WM_DELETE_WINDOW", lambda: on_tool_close(index, dialog, answers))

    create_dialog(current_index, "", 0, config, root, update_gui_callback)

def save_config(config_path, config):
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
def on_close(index, dialog, commands):
    dialog.destroy()
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
def load_config(config_path):
    if not os.path.exists(config_path):
        return {"信息收集": {}, "渗透测试": {}, "漏洞利用": {}, "内网安全": {}}

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误：{e}")
        return None

def update_gui(config, base_path, config_path, root, category, next_id, commands, answers):
    tool_name = answers[1]  # 获取工具名称
    tool_subpath = answers[2]  # 获取工具子路径
    first_tool_path = None
    if category in config and config[category]:
            first_tool = next(iter(config[category].values()))  # 获取第一个工具的信息
            first_tool_path = first_tool["path"]
    if not first_tool_path:
        first_tool_path = base_path
    full_path = os.path.join(first_tool_path, tool_subpath)  # 拼接完整路径
    next_id = get_total_tool_count(config) + 1
    config[category][next_id] = {
        "name": tool_name,
        "path": full_path,
        "commands": {str(i + 1): cmd for i, cmd in enumerate(commands)}
    }
    save_config(config_path, config)
    
    bat_path = r"E:\tools\private_tools\beyond_GUI\重建脚本.bat"
    try:
        subprocess.Popen(bat_path, shell=True)
    except Exception as e:
        print(f"执行重建脚本时出错：{e}")
    
    continue_dialog = ask_continue()  # 显示是否继续添加的对话框
    continue_dialog.wait_window()  # 等待对话框关闭
    response = continue_dialog.result if hasattr(continue_dialog, 'result') else 'n'

    if response == 'y':
        add_tool(config, base_path, config_path, root, update_gui, next_id)  # 继续添加工具
    else:
        # 关闭所有顶级窗口
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        # 退出主循环
        root.quit()

def ask_continue():
    dialog = Toplevel(root)
    dialog.grab_set()  # 设置模态对话框，阻止其他窗口获取焦点
    center_window(dialog, dialog_width, dialog_height)
    Label(dialog, text="是否继续添加工具？(y/n):", font=custom_font).pack(pady=pady)
    entry = Entry(dialog, width=width, font=custom_font)
    entry.pack(pady=pady)
    entry.focus_set()  # 将焦点设置到输入框
    entry.bind('<Return>', lambda event: on_continue_ok(entry.get(), dialog))
    Button(dialog, text="确定", command=lambda: on_continue_ok(entry.get(), dialog), font=custom_font).pack(pady=pady)

    # 确保新窗口在最前面
    dialog.lift()
    dialog.focus_force()

    dialog.protocol("WM_DELETE_WINDOW", lambda: on_close(dialog))

    return dialog  # 返回对话框对象

def on_continue_ok(value, dialog):
    if value.lower() == 'y' or value == '':
        dialog.result = 'y'
        dialog.destroy()
    else:
        dialog.result = 'n'
        dialog.destroy()
    
def main():
    base_path = 'E:\\tools\\private_tools'
    config_path = 'config.json'
    config = load_config(config_path)

    if config is None:
        print("无法加载配置文件，程序退出。")
        return

    global root, custom_font
    root = tk.Tk()
    style = Style(theme=themes)
    center_window(root, dialog_width, dialog_height)
    icon_image = load_icon(icon_path)
    if icon_image:
        root.iconphoto(True, icon_image)
    root.withdraw()
    custom_font = font.Font(family=font_family, size=font_size, weight=font_weight)

    # 获取所有工具的总数并自增，包括重复的ID
    next_id = get_total_tool_count(config) + 1
    add_tool(config, base_path, config_path, root, update_gui, next_id)

    root.mainloop()

if __name__ == "__main__":
    main()