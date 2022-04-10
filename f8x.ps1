# ======================== !! NOTE !! ========================
#  ________ ________ ________ ________ ________ ________ ________ ________ ________     ___    ___
# |\  _____\\  _____\\  _____\\  _____\\  _____\\  _____\\  _____\\  _____\\   __  \   |\  \  /  /|
# \ \  \__/\ \  \__/\ \  \__/\ \  \__/\ \  \__/\ \  \__/\ \  \__/\ \  \__/\ \  \|\  \  \ \  \/  / /
#  \ \   __\\ \   __\\ \   __\\ \   __\\ \   __\\ \   __\\ \   __\\ \   __\\ \  \\\  \  \ \    / /
#   \ \  \_| \ \  \_| \ \  \_| \ \  \_| \ \  \_| \ \  \_| \ \  \_| \ \  \_| \ \  \\\  \  /     \/
#    \ \__\   \ \__\   \ \__\   \ \__\   \ \__\   \ \__\   \ \__\   \ \__\   \ \_______\/  /\   \
#     \|__|    \|__|    \|__|    \|__|    \|__|    \|__|    \|__|    \|__|    \|_______/__/ /\ __\
#                                                                                      |__|/ \|__|
# 注: 该脚本仅用于安装基础软件
# Note: This script is only used to install the base software
# To execute this script:
# 1) Open powershell window as administrator
# 2) Allow script execution by running command "set-ExecutionPolicy Unrestricted"
# 3) running "curl -o f8x.ps1 https://f8x.io/ps1"
# 4) Unblock the install script by running "Unblock-File .\f8x.ps1"
# 5) Execute the script by running ".\f8x.ps1"

param (
  [string]$chrome_link = "http://dl.google.com/chrome/install/375.126/chrome_installer.exe"
)

function Banner {

Write-Host "  _______   ___   ___   ___ "
Write-Host " |   ____| / _ \  \  \ /  / "
Write-Host " |  |__   | (_) |  \  V  / "
Write-Host " |   __|   > _ <    >   < "
Write-Host " |  |     | (_) |  /  .  \ "
Write-Host " |__|      \___/  /__/ \__\ "

}

function chocolatey-install {

  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

}

function chrome-install {
    Write-Host "Installing chrome"
    $Path = $env:TEMP; $Installer = "chrome_installer.exe";
    Invoke-WebRequest $chrome_link -OutFile $Path\$Installer;
    Start-Process -FilePath $Path\$Installer -Args "/silent /install" -Verb RunAs -Wait;
    Remove-Item $Path\$Installer
    Write-Host "Successfully installed chrome"
}

Banner
chrome-install
chocolatey-install

# proxy
# choco config set proxy <locationandport>

# update
choco outdated

# base_install
# https://community.chocolatey.org/packages
choco install -y notepadplusplus.install
choco install -y 7zip.install
choco install -y jdk8
choco install -y python3
choco install -y git
choco install -y 010editor.install
choco install -y everything
