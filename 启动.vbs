Set WshShell = CreateObject("WScript.Shell")

' ��ȡ��ǰVBScript�ļ�������·��
scriptPath = WScript.ScriptFullName

' ��ȡ��ǰVBScript�ļ����ڵ�Ŀ¼
folderPath = Left(scriptPath, InStrRev(scriptPath, "\"))

' ���õ�ǰĿ¼ΪVBScript�ļ����ڵ�Ŀ¼
WshShell.CurrentDirectory = folderPath

' ����Python�ű�������·��
pythonScriptPath = folderPath & "\gui.py"

' ����Python�ű�
WshShell.Run "python3 " & pythonScriptPath, 0, True

Set WshShell = Nothing