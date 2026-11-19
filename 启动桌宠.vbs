Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
scriptName = ChrW(&H684C) & ChrW(&H5BA0) & ".py"
CreateObject("WScript.Shell").Run "pythonw.exe -B """ & fso.BuildPath(folder, scriptName) & """", 0, False
