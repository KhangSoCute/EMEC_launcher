@echo Off
%~d0
CD "%~p0"
C:\Windows\Sysnative\pnputil.exe /add-driver CP210x_W7\*.inf
C:\Windows\Sysnative\pnputil.exe -a CP210x_W7\*.inf
