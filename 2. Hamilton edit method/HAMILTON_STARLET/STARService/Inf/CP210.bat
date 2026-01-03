@echo Off
%~d0
CD "%~p0"
IF %PROCESSOR_ARCHITECTURE% == x86 (
 C:\Windows\Sysnative\pnputil.exe /add-driver CP210x_W10\*.inf
) ELSE (
  C:\Windows\System32\pnputil.exe /add-driver CP210x_W10\*.inf
)


