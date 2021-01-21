# f8x

一款红队环境自动化部署工具,支持多种场景,渗透,开发,代理环境,服务可选项等


# 开始

**安装**

下载 f8x 文件
```
wget https://github.com/ffffffff0x/f8x/blob/main/f8x
```

**使用**
```
bash f8x -h
```

**系统依赖**

f8x基本上不需要任何依赖,或者说它就是为了帮助你安装各种依赖而生的😁

---

# 支持选项

目前 f8x 支持以下部署选项

**批量化安装**
- 使用 -b 选项安装基本环境        (gcc、make、git、vim、telnet、jq、unzip 等基本工具)
- 使用 -p 选项安装代理环境        (警告:国外云服务器上不要用,会降速)
- 使用 -d 选项安装开发环境        (python3,pip3,Go,Docker,Docker-Compose)
- 使用 -k 选项安装渗透环境        (hashcat、ffuf、OneForAll、ksubdomain、impacket 等渗透工具)
- 使用 -s 选项加固 linux 服务器   (Fail2Ban)
- 使用 -f 选项安装其他工具        (Bash_Insulter、vlmcsd、AdguardTeam、trash-cli)
- 使用 -h 选项查看帮助文档

**开发可选项**
- 使用 -ssh 选项配置 SSH 环境     (RedHat 系默认可用,无需重复安装)
- 使用 -python2 选项安装 python2 环境
- 使用 -pip2-force 选项强制安装 pip2 环境   (建议在 -python2 选项失败的情况下运行)
- 使用 -ruby 选项安装 ruby 环境
- 使用 -rust 选项安装 rust 环境
- 使用 -oraclejdk 选项安装 oraclejdk 环境
- 使用 -openjdk 选项安装 openjdk 环境
- 使用 -perl 选项安装 perl 环境
- 使用 -nn 选项安装 npm & NodeJs 环境

**安全可选项**
- 使用 -volatility 选项安装 volatility 工具
- 使用 -binwalk 选项安装 binwalk 环境
- 使用 -binwalk-force 选项强制安装 binwalk 环境    (建议在 -binwalk 选项失败的情况下运行)
- 使用 -vulhub 选项安装 vulhub 环境
- 使用 -cs 选项部署 CobaltStrike 环境
- 使用 -frp 选项部署 frp 环境
- 使用 -nps 选项部署 nps 环境
- 使用 -suricata 选项部署 Suricata 环境

**服务可选项**
- 使用 -sharry 选项部署 sharry 文件服务
- 使用 -bt 选项部署宝塔服务

**其他可选项**
- 使用 -ssr 选项部署 ssr 工具
- 使用 -music 选项部署 UnblockNeteaseMusic 服务
- 使用 -optimize 选项改善设备选项,优化性能
- 使用 -info 选项查看系统各项信息
- 使用 -clear 选项清理系统使用痕迹

**一把梭,就是干**
- 使用 -all 选项全自动化部署(仅兼容国外vps服务器,仅兼容CentOS7/8,Debain10/9,Ubuntu20,Fedora33,只能运行一次,做好心理准备)

---

# 实际效果




---

# TODO

- [ ] 将 xray 社区版集成到 -k 选项中
- [ ] 将 masscan 集成到 -k 选项中
- [ ] 生成错误日志
- [ ] 安装包和遗留文件的清理

---

# License

[Apache License 2.0](https://github.com/ffffffff0x/f8x/blob/main/LICENSE)
