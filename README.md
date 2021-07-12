<h1 align="center">
  <br>
  <img src="./assets/img/banner.png" width="300px" alt="f8x">
</h1>

<h4 align="center">一款红/蓝队环境自动化部署工具,支持多种场景,渗透,开发,代理环境,服务可选项等.</h4>

<p align="center">
  <a href="#开始">开始</a> •
  <a href="#支持选项">支持选项</a> •
  <a href="#faq">FAQ</a> •
  <a href="#实际效果">实际效果</a> •
  <a href="#todo">TODO</a> •
  <a href="#license">License</a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Category-automation-red.svg">
    <img src="https://img.shields.io/github/release/ffffffff0x/f8x"></a>
    <img src="https://github.com/ffffffff0x/f8x/workflows/dev/badge.svg">
</p>

---

大多数场景下，在不同的云购买一些 vps 服务器用于部署红 / 蓝队设施，不能做到开箱即用，使用此工具可以快速部署所需要的各类服务。同时兼顾到本地 VM 虚拟机的需求，可以选择走 socket 代理进行安装部署，Proxychains-ng 也会自动安装，只需做好 Proxychains-ng 配置即可。

## 开始

**下载**

- 访问 [releases](https://github.com/ffffffff0x/f8x/releases) 下载

- 在网络不佳的情况下通过 CF Workers 加速下载
  - wget : `wget -O f8x https://f8x.io/`
  - curl : `curl -o f8x https://f8x.io/`

**使用**
```bash
bash f8x -h
```

如果你希望方便点使用可以直接加到环境变量中
- wget : `wget -O f8x https://f8x.io/ && mv --force f8x /usr/local/bin/f8x && chmod +x /usr/local/bin/f8x`
- curl : `curl -o f8x https://f8x.io/ && mv --force f8x /usr/local/bin/f8x && chmod +x /usr/local/bin/f8x`

**系统依赖**

f8x 基本上不需要任何依赖,或者说它就是为了帮助你安装各种依赖而生的😁

**f8x-dev**

部分开发环境安装独立到该脚本
- wget : `wget -O f8x-dev https://f8x.io/dev`
- curl : `curl -o f8x-dev https://f8x.io/dev`

---

## 支持选项

目前 f8x 支持以下部署选项

**1. 批量化安装**
- 使用 -b 选项安装基本环境        (gcc、make、git、vim、telnet、jq、unzip 等基本工具)
- 使用 -p 选项安装代理环境        (警告:国外云服务器上不要用,会降速)
- 使用 -d 选项安装开发环境        (python3、pip3、Go、Docker、Docker-Compose、SDKMAN)
- 使用 -k 选项安装渗透环境        (hashcat、ffuf、OneForAll、ksubdomain、impacket 等渗透工具)
- 使用 -s 选项安装蓝队环境        (Fail2Ban、chkrootkit、rkhunter、河马webshell查杀工具)
- 使用 -f 选项安装其他工具        (Bash_Insulter、vlmcsd、AdguardTeam、trash-cli 等辅助工具)
- 使用 -cloud 选项安装云应用      (Terraform、Serverless Framework、wrangler)
- 使用 -all 选项全自动化部署      (默认不走代理,兼容 CentOS7/8,Debain10/9,Ubuntu20/18,Fedora33)

**2. 开发环境**
- 使用 -nn 选项安装 npm & NodeJs 环境
- 使用 -oraclejdk 选项安装 oraclejdk 环境
- 使用 -openjdk 选项安装 openjdk 环境
- 使用 -python3 选项安装 python3 环境
- 使用 -python2 选项安装 python2 环境
- 使用 -pip2-f 选项强制安装 pip2 环境          (建议在 -python2 选项失败的情况下运行)
- 使用 -perl 选项安装 perl 环境
- 使用 -ruby 选项安装 ruby 环境
- 使用 -rust 选项安装 rust 环境
- 使用 -chromium 选项安装 Chromium 环境        (用于配合 -k 选项中的 rad、crawlergo)

**3. 蓝队服务**
- 使用 -binwalk 选项安装 binwalk 环境
- 使用 -binwalk-f 选项强制安装 binwalk 环境    (建议在 -binwalk 选项失败的情况下运行)
- 使用 -clamav 选项安装 ClamAV 工具
- 使用 -hfish 选项安装 HFish 蜜罐
- 使用 -lt 选项部署 LogonTracer 环境           (非超高配置机器不要部署,这个应用太吃配置了)
- 使用 -suricata 选项部署 Suricata 环境
- 使用 -vol 选项安装 volatility 取证工具
- 使用 -vol3 选项安装 volatility3 取证工具

**4. 红队服务**
- 使用 -aircrack 选项部署 aircrack-ng 环境
- 使用 -bypass 选项部署 Bypass 环境
- 使用 -cs 选项部署 CobaltStrike 环境
- 使用 -frp 选项部署 frp 环境
- 使用 -goby 选项部署 Goby 环境                (需要图形化环境)
- 使用 -nps 选项部署 nps 环境

**5. 基于 Docker 的环境部署**
- 使用 -arl 选项部署 ARL 环境(872 MB)
- 使用 -awvs14 选项部署 AWVS13 环境(1.04 GB)
- 使用 -mobsf 选项部署 MobSF 环境(1.54 GB)
- 使用 -nodejsscan 选项部署 nodejsscan 环境(873 MB)
- 使用 -viper 选项部署 Viper 环境(2.1 GB)
- 使用 -vulhub 选项部署 vulhub 环境(210 MB)
- 使用 -vulfocus 选项部署 vulfocus 环境(1.04 GB)

**6. 杂项服务**
- 使用 -asciinema 选项安装 asciinema 截图工具
- 使用 -bt 选项部署宝塔服务
- 使用 -clash 选项安装 clash 工具
- 使用 -music 选项部署 UnblockNeteaseMusic 服务
- 使用 -nginx 选项配置 nginx 服务
- 使用 -ssh 选项配置 ssh 环境                  (RedHat 系默认可用,无需重复安装)
- 使用 -ssr 选项部署 ssr 工具
- 使用 -zsh 选项部署 zsh 工具

**7. 其他**
- 使用 -clear 选项清理系统使用痕迹
- 使用 -info 选项查看系统各项信息
- 使用 -optimize 选项改善设备选项,优化性能
- 使用 -remove 选项卸载国内 vps 云监控
- 使用 -rmlock 选项运行除锁模块
- 使用 -swap 选项配置 swap 分区
- 使用 -update 选项更新 f8x 工具

---

## FAQ

**-p 选项会执行什么**

1. 替换你的 DNS(默认为 223.5.5.5), 如果判断是 debian 系还会帮你安装 resolvconf, 长期修改 DNS
2. 检查基础的编译环境是否安装, 并通过默认的包管理器安装 gcc,make,unzip 这些基本软件
3. 可选的从 https://github.com/rofl0r/proxychains-ng 或 ffffffff0x.com 下载 Proxychains-ng 的源码, 编译安装
4. 要求你修改 /etc/proxychains.conf 文件
5. 修改 pip 代理为 https://mirrors.aliyun.com/pypi/simple/
6. 修改 docker 代理为 https://docker.mirrors.ustc.edu.cn , 并重启 docker 服务

---

## 实际效果

**-h 查看帮助**

<h3 align="center">
  <img src="./assets/img/1.png"></a>
</h3>

**-all 全自动化部署**

以 vultr vps 为例,$10/mo 的配置,结果分别如下

| <br><b><p align="center">CentOS 7(完全兼容)</p> | <br><b><p align="center">Debian 10(完全兼容)</p> |
| - | - |
| <p align="center"><a href="https://asciinema.org/a/405335"><img src="https://asciinema.org/a/405335.svg" /></p></a> | <p align="center"><a href="https://asciinema.org/a/405338"><img src="https://asciinema.org/a/405338.svg" /></p></a> |
| <br><b><p align="center">Fedora 33(完全兼容)</p> | <br><b><p align="center">Ubuntu 20.10(完全兼容)</p> |
| <p align="center"><a href="https://asciinema.org/a/405339"><img src="https://asciinema.org/a/405339.svg" /></p></a> | <p align="center"><a href="https://asciinema.org/a/405333"><img src="https://asciinema.org/a/405333.svg" /></p></a> |

---

## TODO

- [x] 将 xray 社区版集成到 -k 选项中
- [x] 将 masscan 集成到 -k 选项中
- [x] 生成错误日志
- [x] vulfocus 安装选项
- [x] 卸载国内vps云监控
- [x] 参考 oneforall 丰富输出信息
- [x] goby 安装选项
- [x] awvs
- [x] CS CrossC2 插件
- [x] 增加虚拟内存
- [x] tomcat 指定版本安装选项(使用 sdkman 进行安装)
- [x] 完善 -info 选项内容

> 完事了,摸鱼

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
