# QA attempt 1: FAIL

command failed (1): powershell -NoProfile -ExecutionPolicy Bypass -File build.ps1 -Python C:\Python313\python.exe
STDOUT:

STDERR:
Traceback (most recent call last):
  File "C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\scripts\build_figures.py", line 386, in <module>
    main()
    ~~~~^^
  File "C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\scripts\build_figures.py", line 370, in main
    plot_architecture()
    ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\scripts\build_figures.py", line 139, in plot_architecture
    raise ValueError(f"Architecture label exceeds its box: {label_artist.get_text()}")
ValueError: Architecture label exceeds its box: $c$
energy + direction
C:\Python313\python.exe failed with exit code 1
At C:\Users\Julia\Desktop\coding\ASIoP\fast-mc-paper\build.ps1:9 char:9
+         throw "$Program failed with exit code $LASTEXITCODE"
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : OperationStopped: (C:\Python313\py...ith exit code 1:String) [], RuntimeException
    + FullyQualifiedErrorId : C:\Python313\python.exe failed with exit code 1
 

