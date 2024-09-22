import os
import json
import subprocess
from config import *
from datetime import datetime
from PIL import Image, ImageTk
from ttkbootstrap import Style,tk
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, simpledialog,ttk,StringVar,ttk, messagebox, simpledialog,font


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

def save_config(config_path, config):
    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置文件时出错：{e}")

def load_config(config_path):
    if not os.path.exists(config_path):
        return {"信息收集": {}, "渗透测试": {}, "漏洞利用": {}, "内网安全": {}, "管理工具": {}}
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误：{e}")
        return None


def show_tools(config, dialog, category):
    global combobox_tool
    global selected_tool  # 声明 selected_tool 为全局变量
    tools = config.get(category, {})
    tool_names = [(f"{tool_id} - {tool_info.get('name', '未知工具')}", tool_id) for tool_id, tool_info in tools.items()]
    combobox_tool['values'] = [name for name, _ in tool_names]  # 只显示名称
    if tool_names:
        selected_tool.set(tool_names[0][1])  # 设置默认显示的ID
    combobox_tool.current(0)  # 确保下拉框显示默认值
    combobox_tool.bind('<<ComboboxSelected>>', lambda event: update_selected_tool(config, category, combobox_tool.get()))


def remove_tool(config, config_path, root):
    global combobox_tool
    global selected_tool
    center_window(root, dialog_width, dialog_height)  # 确保主窗口居中

    # 创建一个对话框并居中显示
    dialog = Toplevel(root)
    center_window(dialog, dialog_width, dialog_height)

    # 显示类别选择下拉框
    Label(dialog, text="请选择类别：", font=custom_font).pack(pady=pady)
    categories = list(config.keys())
    selected_category = StringVar(dialog)
    selected_category.set(categories[0])  # 默认选择第一个类别
    combobox_category = ttk.Combobox(dialog, textvariable=selected_category, values=categories, state="readonly", width=dialog_width)
    combobox_category.pack(pady=pady)
    combobox_category.bind('<<ComboboxSelected>>', lambda event: show_tools(config, dialog, selected_category.get()))
    combobox_category.bind('<Return>', lambda event: on_confirm(config, config_path, root, dialog, selected_category.get(), combobox_tool.get()))
    
    # 显示工具列表
    Label(dialog, text="请选择要删除的工具：", font=custom_font).pack(pady=pady)
    selected_tool = StringVar(dialog)  # 定义 selected_tool 变量
    combobox_tool = ttk.Combobox(dialog, textvariable=selected_tool, state="readonly", width=dialog_width)
    combobox_tool.pack(pady=pady)
    combobox_tool.bind('<<ComboboxSelected>>', lambda event: update_selected_tool(config, selected_category.get(), combobox_tool.get()))
    combobox_tool.bind('<Return>', lambda event: on_confirm(config, config_path, root, dialog, selected_category.get(), combobox_tool.get()))
    
    Button(dialog, text="确定", command=lambda: on_confirm(config, config_path, root, dialog, selected_category.get(), combobox_tool.get()), font=custom_font).pack(pady=pady)

    dialog.protocol("WM_DELETE_WINDOW", lambda: on_cancel(dialog))

    # 立即显示默认类别的工具列表
    show_tools(config, dialog, categories[0])    

def update_selected_tool(config, category, tool_name):
    global selected_tool
    tools = config.get(category, {})
    for name, tool_id in [(f"{tool_id} - {tool_info.get('name', '未知工具')}", tool_id) for tool_id, tool_info in tools.items()]:
        if name == tool_name:
            selected_tool.set(tool_id)
            break
         
def on_confirm(config, config_path, root, dialog, category, tool_name):
    global selected_tool
    tool_id = selected_tool.get()
    if tool_id:
        if tool_id in config[category]:
            tool_info = config[category][tool_id]
            tool_name = tool_info.get("name", "未知工具")
            confirm_dialog = Toplevel(root)
            center_window(confirm_dialog, dialog_width, dialog_height)

            Label(confirm_dialog, text=f"您确定要删除工具 {tool_name} 吗？", font=custom_font).pack(pady=pady)
            yes_button = Button(confirm_dialog, text="是", command=lambda: on_confirm_yes(config, category, tool_id, config_path, confirm_dialog, root), font=custom_font)
            yes_button.pack(side="left", padx=padx, pady=pady)
            no_button = Button(confirm_dialog, text="否", command=lambda: on_confirm_no(confirm_dialog, root), font=custom_font)
            no_button.pack(side="right", padx=padx, pady=pady)

            # 绑定回车键到 yes_button
            confirm_dialog.bind('<Return>', lambda event: on_confirm_yes(config, category, tool_id, config_path, confirm_dialog, root))
            confirm_dialog.protocol("WM_DELETE_WINDOW", lambda: on_confirm_no(confirm_dialog, root))
            confirm_dialog.focus_force()
            confirm_dialog.update_idletasks()
            confirm_dialog.update()
        else:
            messagebox.showinfo("提示", "编号不存在，请重新输入")
            dialog.destroy()
    else:
        messagebox.showerror("错误", "请选择一个工具")

def on_cancel(dialog):
    dialog.destroy()
    root.destroy()  # 销毁主窗口

def on_confirm_yes(config, category, tool_id, config_path, confirm_dialog, root):
    try:
        tool_name = config[category][tool_id].get("name", "未知工具")
        with open("delete_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {tool_name} 被删除\n")
        del config[category][tool_id]
        save_config(config_path, config)
        messagebox.showinfo("成功", "工具已删除")
        bat_path = r"E:\tools\private_tools\beyond_GUI\重建脚本.bat"
        subprocess.Popen(bat_path, shell=True)
    except Exception as e:
        print(f"执行重建脚本时出错：{e}")
    finally:
        confirm_dialog.destroy()
        if ask_continue(root):
            remove_tool(config, config_path, root)
        else:
            root.destroy()

def on_confirm_no(confirm_dialog, root):
    confirm_dialog.destroy()
    root.destroy()  # 销毁主窗口

def on_ok(entry, dialog):
    if entry.winfo_exists():  # 检查 entry 组件是否存在
        response = entry.get().lower() == 'y'
        entry.destroy()
        dialog.destroy()
        return response
    else:
        dialog.destroy()
        return False  # 或者根据你的需求返回其他值

def ask_continue(root):
    dialog = Toplevel(root)
    dialog.grab_set()  # 设置模态对话框，阻止其他窗口获取焦点
    center_window(dialog, dialog_width, dialog_height)  # 设置你想要的宽度和高度
    Label(dialog, text="是否继续删除工具？(y/n):", font=custom_font).pack(pady=pady)
    entry = Entry(dialog, font=custom_font)
    entry.pack(pady=pady)
    entry.focus_set()  # 将焦点设置到输入框

    ok_button = Button(dialog, text="确定", command=lambda: on_ok(entry, dialog), font=custom_font)
    ok_button.pack(pady=pady)

    # 绑定回车键到 ok_button 的命令
    entry.bind('<Return>', lambda event: ok_button.invoke())

    dialog.protocol("WM_DELETE_WINDOW", lambda: on_ok(entry, dialog))  # 处理关闭按钮事件
    dialog.focus_force()
    dialog.wait_window()  # 等待对话框关闭
    return on_ok(entry, dialog)  # 这里应该返回 on_ok 函数的返回值

def main():
    base_path = 'E:\\tools\\private_tools'
    config_path = 'config.json'
    config = load_config(config_path)

    if config is None:
        print("无法加载配置文件，程序退出。")
        return

    global root, custom_font, selected_tool
    root = Tk()
    style = Style(theme=themes)  # 假设 themes 是从 config 模块读取的主题名称
    selected_tool = StringVar()  # 初始化 selected_tool 变量
    center_window(root, dialog_width, dialog_height)  # 窗口居中
    icon_image = load_icon(icon_path)  # 使用单独导入的 icon_path 变量
    if icon_image:
        root.iconphoto(True, icon_image)  # 设置窗口图标
    root.withdraw()
    # 定义自定义字体
    custom_font = font.Font(family=font_family, size=font_size, weight=font_weight)

    remove_tool(config, config_path, root)
    root.mainloop()

if __name__ == "__main__":
    main()