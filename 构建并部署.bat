@echo off
chcp 65001 >nul
cd /d "%~dp0STS2 Momoi"

tasklist /FI "IMAGENAME eq SlayTheSpire2.exe" 2>nul | find /I "SlayTheSpire2.exe" >nul
if not errorlevel 1 (
    echo.
    echo [错误] 游戏还在运行。请先完全关闭 Slay the Spire 2，再运行本脚本。
    echo.
    pause
    exit /b 1
)

echo 正在构建并部署 STS2_Momoi ...
echo.
dotnet build "STS2 Momoi.csproj"
if errorlevel 1 (
    echo.
    echo [失败] 构建没有通过，请把上面的错误发给我。
    pause
    exit /b 1
)

echo.
echo [完成] 已部署：
dir "D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.dll"
dir "D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.pck"
echo.
echo 现在可以重新启动游戏，进战斗测试。
pause
