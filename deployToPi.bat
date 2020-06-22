@ECHO off
set ip=raspberrypi
set user=pi
set projectPath=home/%user%/Robot/
echo Deploying files to %projectPath% in user %user% at %ip%
scp -r .\*.py Robots Hardware CameraServer Autonomy %user%@%ip%:/%projectPath%



