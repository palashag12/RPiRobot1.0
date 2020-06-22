@ECHO off
set /p ip=Enter Pi IP:
set user=pi
set projectPath=home/%user%/Robot/
echo Deploying files to %projectPath% in user %user% at %ip%
scp -r .\*.py Robots Hardware CameraServer Autonomy %user%@%ip%:/%projectPath%


