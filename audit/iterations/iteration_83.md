# QA attempt 83: FAIL

command failed (1): powershell -NoProfile -ExecutionPolicy Bypass -File build.ps1 -Python C:\Users\Julia\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
STDOUT:

STDERR:
Traceback (most recent call last):
  File "C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\scripts\build_figures.py", line 10, in <module>
    import matplotlib
ModuleNotFoundError: No module named 'matplotlib'
C:\Users\Julia\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe failed with exit code 1
At C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\build.ps1:9 char:9
+         throw "$Program failed with exit code $LASTEXITCODE"
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : OperationStopped: (C:\Users\Julia\...ith exit code 1:String) [], RuntimeException
    + FullyQualifiedErrorId : C:\Users\Julia\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.ex 
   e failed with exit code 1
 

