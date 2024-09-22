Set WshShell = CreateObject("WScript.Shell")

' 获取当前VBScript文件的完整路径
scriptPath = WScript.ScriptFullName

' 获取当前VBScript文件所在的目录
folderPath = Left(scriptPath, InStrRev(scriptPath, "\"))

' 设置当前目录为VBScript文件所在的目录
WshShell.CurrentDirectory = folderPath

' 构建Python脚本的完整路径
pythonScriptPath = folderPath & "\gui.py"

' 运行Python脚本
WshShell.Run "python3 " & pythonScriptPath, 0, True

Set WshShell = Nothing