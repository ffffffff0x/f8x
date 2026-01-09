<h1 align="center">
  <br>
  <img src="./assets/img/banner2.png" width="300px" alt="f8x">
</h1>

<h4 align="center">一款红/蓝队环境自动化部署工具,支持多种场景,渗透,开发,代理环境,服务可选项等.</h4>

<p align="center">
  <a href="#开始">开始</a> •
  <a href="#支持选项">支持选项</a> •
  <a href="#实际效果">实际效果</a> •
  <a href="#faq">FAQ</a> •
  <a href="#license">License</a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/platform-linux-important?color=%23942000">
    <img src="https://img.shields.io/badge/Category-automation-yellow.svg">
    <img src="https://img.shields.io/github/release/ffffffff0x/f8x"></a>
    <img src="https://github.com/ffffffff0x/f8x/workflows/dev/badge.svg">
</p>

[English](README.md) | 简体中文

---

大多数场景下，在不同的云购买一些 vps 服务器用于部署红 / 蓝队设施，不能做到开箱即用，使用 f8x 可以快速部署所需要的各类服务。同时兼顾到本地 VM 虚拟机的需求，可以选择走 socket 代理进行安装部署，Proxychains-ng 也会自动安装，只需做好 Proxychains-ng 配置即可。

## 开始

**下载**
- Pages 加速
  - wget : `wget -O f8x https://f8x.wgpsec.org/f8x`
  - curl : `curl -o f8x https://f8x.wgpsec.org/f8x`

- github 直链
  - wget : `wget -O f8x https://raw.githubusercontent.com/ffffffff0x/f8x/main/f8x`
  - curl : `curl -o f8x https://raw.githubusercontent.com/ffffffff0x/f8x/main/f8x`

**使用**
```bash
bash f8x -h
```

如果你希望方便点使用可以直接加到环境变量中
- wget : `wget -O f8x https://f8x.wgpsec.org/f8x && mv --force f8x /usr/local/bin/f8x && chmod +x /usr/local/bin/f8x`
  - `f8x -h`
- curl : `curl -o f8x https://f8x.wgpsec.org/f8x && mv --force f8x /usr/local/bin/f8x && chmod +x /usr/local/bin/f8x`
  - `f8x -h`

**系统依赖**

f8x 基本上不需要任何依赖,或者说它就是为了帮助你安装各种依赖而生的😁

**f8x-ctf**

该脚本用于部署 CTF 环境,支持 (Web、Misc、Crypto、Pwn、Iot) 分类

- wget : `wget -O f8x-ctf https://f8x.wgpsec.org/f8x-ctf`
  - `bash f8x-ctf -help`
- curl : `curl -o f8x-ctf https://f8x.wgpsec.org/f8x-ctf`
  - `bash f8x-ctf -help`

**f8x-dev**

该脚本用于部署中间件和数据库环境,支持 (apache、nginx、tomcat、Database、php) 分类

- wget : `wget -O f8x-dev https://f8x.wgpsec.org/f8x-dev`
  - `bash f8x-dev -help`
- curl : `curl -o f8x-dev https://f8x.wgpsec.org/f8x-dev`
  - `bash f8x-dev -help`

---

## 支持选项

目前 f8x 支持以下部署选项 (Linux arm64 下大部分都支持)

**1. 批量化安装**
- 使用 -b 选项安装基本环境 (gcc、make、git、vim、telnet、jq、unzip 等基本工具)
- 使用 -p 选项安装代理环境 (警告:国外云服务器上不要用,会降速)
- 使用 -d 选项安装开发环境 (python3、pip3、Go、Docker、Docker-Compose、SDKMAN)
- 使用 -k 选项安装渗透环境 (hashcat、ffuf、OneForAll、ksubdomain、impacket 等渗透工具)
  - -ka 信息收集、扫描、爆破、抓取
  - -kb 漏洞利用
  - -kc 后渗透、C2
  - -kd 其他
  - -ke 功能重叠或长期不维护
- 使用 -s 选项安装蓝队环境 (Fail2Ban、chkrootkit、rkhunter、河马webshell查杀工具)
- 使用 -f 选项安装其他工具 (Bash_Insulter、vlmcsd、AdguardTeam、trash-cli 等辅助工具)
- 使用 -cloud 选项安装云应用 (Terraform、Serverless Framework、wrangler)
- 使用 -all 选项全自动化部署 (默认不走代理,兼容 CentOS7/8,Debain10/9,Ubuntu20/18,Fedora33)

**2. 开发环境**
- 使用 -docker 选项安装 docker 环境
- 使用 -lua 选项安装 lua 环境
- 使用 -nn 选项安装 npm & NodeJs 环境
- 使用 -go 选项安装 go 环境
- 使用 -oraclejdk(8/11) 选项安装 oraclejdk 环境
- 使用 -openjdk 选项安装 openjdk 环境
- 使用 -py3(7/8/9/10) 选项安装 python3 环境
- 使用 -py2 选项安装 python2 环境
- 使用 -pip2-f 选项强制安装 pip2 环境 (建议在 -python2 选项失败的情况下运行)
- 使用 -perl 选项安装 perl 环境
- 使用 -ruby 选项安装 ruby 环境
- 使用 -rust 选项安装 rust 环境
- 使用 -code 选项安装 code-server 环境
- 使用 -chromium 选项安装 Chromium 环境 (用于配合 -k 选项中的 rad、crawlergo)
- 使用 -phantomjs 选项安装 PhantomJS

**3. 蓝队工具**
- 使用 -binwalk 选项安装 binwalk 环境
- 使用 -binwalk-f 选项强制安装 binwalk 环境 (建议在 -binwalk 选项失败的情况下运行)
- 使用 -clamav 选项安装 ClamAV 工具
- 使用 -lt 选项部署 LogonTracer 环境 (非超高配置机器不要部署,这个应用太吃配置了)
- 使用 -suricata 选项部署 Suricata 环境
- 使用 -vol 选项安装 volatility 取证工具
- 使用 -vol3 选项安装 volatility3 取证工具

**4. 红队工具**
- 使用 -aircrack 选项部署 aircrack-ng 环境
- 使用 -bypass 选项部署 Bypass 环境
- 使用 -goby 选项部署 Goby 环境 (需要图形化环境)
- 使用 -wpscan 选项安装 wpscan 工具
- 使用 -yakit 选项部署 yakit 环境

**5. 红队基础设施**
- 使用 -awvs14 选项部署 AWVS13 环境(1.04 GB)
- 使用 -cs 选项部署 CobaltStrike4.3 环境
- 使用 -cs45 选项部署 CobaltStrike4.5 环境
- 使用 -frp 选项部署 frp 工具
- 使用 -interactsh 选项部署 interactsh 工具 (https://github.com/projectdiscovery/interactsh)
- 使用 -merlin 选项部署 merlin 环境 (https://github.com/Ne0nd0g/merlin)
- 使用 -msf 选项部署 Metasploit 环境
- 使用 -nps 选项部署 nps 工具
- 使用 -pupy 选项部署 pupy 环境 (https://github.com/n1nj4sec/pupy)
- 使用 -rg 选项部署 RedGuard 工具 (https://github.com/wikiZ/RedGuard)
- 使用 -sliver 选项部署 sliver 环境 (https://github.com/BishopFox/sliver)
- 使用 -sliver-client 选项安装 sliver-client 工具
- 使用 -sps 选项部署 SharPyShell 工具 (https://github.com/antonioCoco/SharPyShell)
- 使用 -viper 选项部署 Viper 环境(2.1 GB)

**6. 基于 Docker 的环境部署**
- 使用 -arl 选项部署 ARL 环境(872 MB)
- 使用 -mobsf 选项部署 MobSF 环境(1.54 GB)
- 使用 -nodejsscan 选项部署 nodejsscan 环境(873 MB)
- 使用 -vulhub 选项部署 vulhub 环境(210 MB)
- 使用 -vulfocus 选项部署 vulfocus 环境(1.04 GB)
- 使用 -TerraformGoat 选项部署 TerraformGoat 环境

**7. 杂项服务**
- 使用 -asciinema 选项安装 asciinema 截图工具
- 使用 -bt 选项部署宝塔服务
- 使用 -clash 选项安装 clash 工具 (https://github.com/juewuy/ShellClash)
- 使用 -nginx 选项配置 nginx 服务
- 使用 -ssh 选项配置 ssh 环境 (RedHat 系默认可用,无需重复安装)
- 使用 -ssr 选项部署 ssr 工具
- 使用 -zsh 选项部署 zsh 工具

**8. 其他**
- 使用 -clear 选项清理系统使用痕迹
- 使用 -info 选项查看系统各项信息
- 使用 -optimize 选项改善设备选项,优化性能
- 使用 -remove 选项卸载国内 vps 云监控
- 使用 -rmlock 选项运行除锁模块
- 使用 -swap 选项配置 swap 分区
- 使用 -update 选项更新 f8x 工具
- 使用 -upgrade 选项更新渗透工具

---

## 实际效果

**-h 查看帮助**

<h3 align="center">
  <img src="./assets/img/1.png"></a>
</h3>

**-all 全自动化部署**

以 vultr vps 为例,结果分别如下

| <br><b><p align="center">CentOS 7(完全兼容)</p> | <br><b><p align="center">Debian 10(完全兼容)</p> |
| - | - |
| <p align="center"><a href="https://asciinema.org/a/WTGNRBd9WYLHUOgZcce9sjkeY"><img src="https://asciinema.org/a/WTGNRBd9WYLHUOgZcce9sjkeY.svg" /></p></a> | <p align="center"><a href="https://asciinema.org/a/Mq0N07O9K2jWsDuUoukHTEVOt"><img src="https://asciinema.org/a/Mq0N07O9K2jWsDuUoukHTEVOt.svg" /></p></a> |
| <br><b><p align="center">Fedora 33</p> | <br><b><p align="center">Ubuntu 20.10</p> |
| <p align="center"><a href="https://asciinema.org/a/NccoFLvW5Xcl0PW0HnTu32vHf"><img src="https://asciinema.org/a/NccoFLvW5Xcl0PW0HnTu32vHf.svg" /></p></a> | <p align="center"><a href="https://asciinema.org/a/Us90ody5ffAOIrr9p93dmO8Ct"><img src="https://asciinema.org/a/Us90ody5ffAOIrr9p93dmO8Ct.svg" /></p></a> |

---

## FAQ

**-p 选项会执行什么**

1. 替换你的 DNS(默认为 223.5.5.5), 如果判断是 debian 系还会帮你安装 resolvconf, 长期修改 DNS
2. 检查基础的编译环境是否安装, 并通过默认的包管理器安装 gcc,make,unzip 这些基本软件
3. 可选的从 https://github.com/rofl0r/proxychains-ng 或 ffffffff0x.com 下载 Proxychains-ng 的源码, 编译安装
4. 要求你修改 /etc/proxychains.conf 文件
5. 修改 pip 代理为 https://mirrors.aliyun.com/pypi/simple/
6. 修改 docker 代理为 https://docker.mirrors.ustc.edu.cn , 并重启 docker 服务

**我想跑在 CI/CD 里,不想要交互行不行?**

当然没有问题, f8x 的 GitHub action 就是自动运行每个选项部署环境的。只需要在 /tmp 创建一个名为 IS_CI 的空文件即可
```bash
touch /tmp/IS_CI
wget -O f8x https://f8x.wgpsec.org/f8x && mv --force f8x /usr/local/bin/f8x && chmod +x /usr/local/bin/f8x
f8x -k
```

**如何自定义版本**

shell脚本在运行时，可以通过 `. ./test.sh` 这样同等进程运行修改当前shell环境变量，那么f8x对同目录下的 f8x_version.sh 文件做个判断，当有这个文件时，会加载这个文件中的内容，也就是覆盖f8x的变量值，这样只需要在当前目录下对 f8x_version.sh 文件做修改或定制，即可做到安装指定版本

---

## 开发日志

[f8x 开发记录](https://r0fus0d.blog.ffffffff0x.com/post/f8x_development_record/)

---

## License

[Apache License 2.0](https://github.com/ffffffff0x/f8x/blob/main/LICENSE)

---

# 404StarLink 2.0 - Galaxy

![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

f8x 是 404Team [星链计划2.0](https://github.com/knownsec/404StarLink2.0-Galaxy)中的一环，如果对 f8x 有任何疑问又或是想要找小伙伴交流，可以参考星链计划的加群方式。

- [https://github.com/knownsec/404StarLink2.0-Galaxy#community](https://github.com/knownsec/404StarLink2.0-Galaxy#community)

---

> create by ffffffff0x
