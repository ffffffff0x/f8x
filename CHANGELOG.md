# Changelog

## Details

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
