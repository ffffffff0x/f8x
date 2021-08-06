# Changelog

## Details

### [1.5.5] - 2021-8-6

**功能添加**

* -k 支持部分软件安装
  * -k -a 信息收集、扫描、爆破、抓取
  * -k -b 漏洞利用
  * -k -c 后渗透、C2
  * -k -d 其他
  * -k -e 功能重叠或长期不维护
* -k 选项添加 Amass、gobuster、dirsearch、Gopherus、gron、unfurl、qsreplace、Interlace、SecLists、jaeles、subjs、assetfinder、hakrawler [#8](https://github.com/ffffffff0x/f8x/issues/8)
* 添加 -lua 选项
* 添加 -mock 选项

**功能修改**

* 修复 nuclei 的安装问题
* 修复 remote-method-guesser 的安装问题

本次添加内容较多,若存在问题,欢迎在 issue 反馈

### [1.5.4] - 2021-07-12

**功能添加**

* -k 选项添加 JNDI-Injection-Exploit、Platypus、Neo-reGeorg、AppInfoScanner

**功能修改**

* 修复 naabu 的安装问题
* 优化 -info 的信息输出

### [1.5.3] - 2021-06-02

**功能添加**

* -k 选项添加 ZoomEye-python、nali、dalfox
* -f 选项添加 anew

**功能修改**

* CobaltStrike4.1 更换至 CobaltStrike4.3
* 修复小 bug
* 更新大部分软件的版本

### [1.5.2] - 2021-04-21

**功能添加**
* -k 选项添加 shiro_rce_tool
* debian 系安装 nginx 时添加 zlib1g 和 zlib1g.dev [#6](https://github.com/ffffffff0x/f8x/issues/6)
* debian 系安装 Python3 时添加 python3-distutils

**功能修改**
* 安装 xray 至 /usr/local/bin/
* 下载 xray poc 至 /pentest/xray
* 暂时注释 RustScan、WAFW00F、MassBleed、exploitdb 的安装

### [1.5.1] - 2021-04-15

* -k 选项添加 swagger-hack、shiro-exploit、ysoserial、remote-method-guesser、SSRFmap、See-SURF、testssl.sh、MassBleed

### [1.5.0] - 2021-04-12

* -k 选项添加 jadx、Diggy、CORScanner、swagger-exp
* 修复安装 bettercap 时的一个错误
* 修复安装 ApkAnalyser 时的一个错误
* 添加2个变量,为后续走web代理做准备,并且可以忽略一些banner信息
* -goby 选项添加服务端启动命令
* 继续优化使用体验,添加对开发环境依赖、渗透杂项工具、pip 模块的重复安装检测

### [1.4.9] - 2021-04-06

* 添加 -clash 选项
* 添加 -nginx 选项
* 更新 -info 选项
* 添加对 Ubuntu15.04、Ubuntu14.04、Ubuntu12.04 系统的支持
* -k 选项添加 httpx、subfinder、mapcidr、apktool、OpenRedireX、gau、apkleaks
* -f 选项添加 fzf、annie、you-get、ffmpeg、aria2、filebrowser、starship
* -sharry 选项移至 -f
* 优化使用体验,已安装过的不会重复安装

### [1.4.8] - 2021-03-28

* 添加 -aircrack 选项
* 添加 -zsh 选项
* -k 选项添加 commix、exploitdb、tplmap、routersploit、bettercap、mitmproxy、naabu、proxify、pypykatz、CrackMapExec
* -s 选项添加 BruteShark
* 更新所有软件安装的版本
* 体积缩减 50%

### [1.4.7] - 2021-03-21
* -s 选项添加 anti-portscan
* -k 选项添加 Responder、Girsh、ApkAnalyser
* -f 选项添加 thefuck
* 修改检查是否已安装状态的方法
* 完善 -info 的输出
* 调整默认的安装逻辑，在检测到前置软件为安装时会自动安装

### [1.4.6] - 2021-03-10
* 添加 -clamav 选项
* 添加 -update 选项
* -d 选项添加 SDKMAN
* -rmlock 选项添加一条命令 `dpkg --configure -a > /dev/null 2>&1`
* 修复 -pip2-force 选项的文件链接问题
* 将 -ssr 选项的安装包移至 github,走 jsdelivr cdn 下载

### [1.4.5] - 2021-02-28

* 添加 -swap 选项,用于添加 swap 分区
* 添加 -cloud 选项,用于安装 Terraform、Serverless Framework、wrangler
* 添加 -bypass 选项,用于安装一些代码混淆的模块
* 添加对 kali2021、Ubuntu 21.01、Ubuntu 19.10、Debian 11 系统的支持
* 添加对 docker 环境下的判断
* 添加 nn_Check、Rust_Check 用于检查依赖
* Debian 系 Docker 安装完毕后会自动删除 /etc/apt/sources.list.d/docker.list
* 修复 -rust 选项不会走代理的错误
* 重构 -nn 选项的安装方式

### [1.4.4] - 2021-02-24

* 修复 -viper 选项的路径问题 [#2](https://github.com/ffffffff0x/f8x/issues/2)
* 在安装渗透杂项工具时,删除 redis 的安装

### [1.4.3] - 2021-02-21

* 安装 volatility3 时添加下载 Symbol Tables
* 部署 CobaltStrike 时添加 genCrossC2
* 安装 Docker 时添加安装 lazydocker
* 添加对不支持的平台的判断
* -d 选项添加 Terraform
* -b 选项安装基础工具中部分工具移动到 -d 选项
* 参考 sast 工具优化一些问题

### [1.4.2] - 2021-02-16

* 现在默认4个系统已经完全兼容,无报错
* 默认检查是否存在 /tmp 目录
* 删除 /pentest 确认选项
* 删除 wget 默认的输出报错
* 默认 Python2_Install 模块中的 pip2 安装失败后,自动调用 pip2_Install

### [1.4.1] - 2021-02-13
* 添加 -hfish 选项
* 添加 -lt 选项
* 添加 -chromium 选项
* -k 选项添加 rad
* -k 选项添加 crawlergo
* -k 选项添加 w13scan
* -s 选项添加 chkrootkit
* -s 选项添加 rkhunter
* -s 选项添加 shellpub
* -volatility 选项简化为 -vol
* -volatility3 选项简化为 -vol3
* -cs 选项的命令生成添加持久性支持
* 修改 -h 显示效果
* 修改默认下不走代理
* 增强判断 Debian 系版本的兼容性
* 修改 Proxychains-ng 的代理下载走 cdn.ffffffff0x.com
* Python3_Install 函数新增安装 virtualenv

### [1.4.0] - 2021-02-09
* 添加 -mobsf 安装选项
* 添加 -nodejsscan 安装选项
* -k 选项添加 Nuclei 工具
* 修改部署 CobaltStrike 环境的提示信息
* 优化 -h 的排列效果

### [1.3.9] - 2021-02-02
* 提高 -pip2-force 选项的兼容性

### [1.3.8] - 2021-02-02
* 添加 -volatility3 安装选项
* 添加一个 pip2_Check 函数单独判断 pip2 命令是否存在,不存在自动调用 Python2_Install 函数进行安装
* 安装pip 渗透模块时添加 pefile

### [1.3.7] - 2021-02-01
* 添加 -viper 安装选项
* -k 选项添加 pocsuite3 工具
* 添加一个 pip3_Check 函数单独判断 pip3 命令是否存在,不存在自动调用 Python3_Install 函数进行安装
* 安装开发环境依赖时,debian 系安装 libcurl4-openssl-dev
* 修复安装 Impacket 时的一个错误

### [1.3.6] - 2021-01-26
* 修几个小 bug

### [1.3.5] - 2021-01-26
* 添加 -goby 安装选项
* 添加 -awvs13 安装选项
* 添加 -arl 安装选项
* 将 fscan 集成到 -k 选项中

### [1.3.4] - 2021-01-26
* 参考 oneforall 丰富输出信息

### [1.3.3] - 2021-01-26
* 修复 python2 pip 的升级问题
* 优化 -d 的逻辑

### [1.3.2] - 2021-01-24
* 删除 - b 中的一个重复安装
* 修复代理开关中的逻辑错误
* 添加 setuptools 模块的安装
* python2 默认继承到 -d 选项中
* -asciinema 选项添加判断, 用于通过 CI 检测

### [1.3.1] - 2021-01-24
* 添加 -rmlock 选项运行除锁模块
* 给错误日志加上时间
* 代理开关添加一个 IS_CI 变量的判断,便于CI运行
* 添加 EPEL 源的判断
* -b 选项中添加 aptitude 的安装
* 修复 -nn 的小 bug
* 修复 -asciinema 的小 bug

### [1.3.0] - 2021-01-23
* 添加 -remove 卸载国内vps云监控
* 添加 -asciinema 安装 asciinema 截图工具
* 所有报错默认生成错误日志
* 在部署 CobaltStrike 环境时加入 jdk 环境检测
* 安装 vlmcsd 环境前会检测已有环境
* 安装 Bash_Insulter 环境前会检测已有环境

### [1.2.0] - 2021-01-23
* 添加 -vulfocus 安装选项
* 略微修改报错信息

### [1.1.0] - 2021-01-23
* 将 xray 社区版集成到 -k 选项中
* 将 masscan 集成到 -k 选项中
* 将 Yum_Rm_Lock 与 Rm_Lock 合并
