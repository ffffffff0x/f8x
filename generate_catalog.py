#!/usr/bin/env python3
"""
generate_catalog.py — 从 f8x 脚本自动提取工具目录，生成 index.json
供 redc 软件商店在线加载

用法: python3 generate_catalog.py [f8x_script_path] [output_path]
默认: python3 generate_catalog.py ./f8x ./index.json
"""

import re
import json
import sys
import os
from datetime import datetime, timezone

# ── 分类映射表 ──
# 根据 f8x Help() 中的分组和 Main case 语句中的 flag 分配分类
CATEGORY_MAP = {
    # Batch installation
    "-b":     {"category": "basic",          "name": "Basic Tools",         "nameZh": "基础工具集",      "desc": "gcc, make, git, vim, curl, wget, jq, unzip ...", "descZh": "基础编译和常用工具集合", "tags": ["batch"]},
    "-p":     {"category": "basic",          "name": "Proxy Environment",   "nameZh": "代理环境",        "desc": "Install proxy environment (proxychains)", "descZh": "安装代理环境", "tags": ["proxy"]},
    "-d":     {"category": "development",    "name": "Dev Environment",     "nameZh": "开发环境全套",    "desc": "Python3, pip3, Go, Docker, Docker-Compose, SDKMAN", "descZh": "一键安装开发环境", "tags": ["batch"]},
    "-k":     {"category": "pentest-recon",  "name": "Pentest Suite",       "nameZh": "渗透工具全套",    "desc": "All pentest tools (recon + exploit + post)", "descZh": "全部渗透工具套件", "tags": ["batch"]},
    "-ka":    {"category": "pentest-recon",  "name": "Recon Suite",         "nameZh": "侦查工具全套",    "desc": "nmap, masscan, ffuf, httpx, subfinder ...", "descZh": "一键安装侦查工具", "tags": ["batch"]},
    "-kb":    {"category": "pentest-exploit","name": "Exploit Suite",       "nameZh": "利用工具全套",    "desc": "Metasploit, Nuclei, xray, Sqlmap ...", "descZh": "一键安装利用工具", "tags": ["batch"]},
    "-kc":    {"category": "pentest-post",   "name": "Post Suite C",        "nameZh": "后渗透工具 C",    "desc": "impacket, hashcat, Responder ...", "descZh": "后渗透/AD 攻击工具集", "tags": ["batch"]},
    "-kd":    {"category": "pentest-post",   "name": "Post Suite D",        "nameZh": "后渗透工具 D",    "desc": "Advanced post-exploitation tools", "descZh": "高级后渗透工具集", "tags": ["batch"]},
    "-ke":    {"category": "pentest-post",   "name": "Post Suite E",        "nameZh": "后渗透工具 E",    "desc": "Pentest tools suite E", "descZh": "渗透工具集 E", "tags": ["batch"]},
    "-s":     {"category": "blue-team",      "name": "Blue Team Suite",     "nameZh": "蓝队工具全套",    "desc": "Fail2Ban, rkhunter, anti-portscan, shellpub", "descZh": "一键安装蓝队防御工具", "tags": ["batch"]},
    "-f":     {"category": "misc",           "name": "Fun Tools Suite",     "nameZh": "实用工具全套",    "desc": "AdGuard, fzf, lux, ttyd, duf, yq ...", "descZh": "一键安装实用工具集", "tags": ["batch"]},
    "-cloud": {"category": "misc",           "name": "Cloud Tools",         "nameZh": "云工具套件",      "desc": "Terraform, redc, Serverless Framework", "descZh": "云相关工具集", "tags": ["batch", "cloud"]},
    "-all":   {"category": "basic",          "name": "Full Install",        "nameZh": "全量安装",        "desc": "Fully automated deployment of all tools", "descZh": "全自动部署所有工具", "tags": ["batch"]},

    # Development Environment
    "-docker":      {"category": "development",    "name": "Docker",              "nameZh": "Docker",              "desc": "Install Docker engine", "descZh": "安装 Docker 引擎", "tags": ["container"]},
    "-docker-cn":   {"category": "development",    "name": "Docker (China)",      "nameZh": "Docker (阿里云源)",   "desc": "Install Docker with Aliyun mirror", "descZh": "使用阿里云源安装 Docker", "tags": ["container"]},
    "-lua":         {"category": "development",    "name": "Lua",                 "nameZh": "Lua",                 "desc": "Install Lua", "descZh": "安装 Lua", "tags": ["language"]},
    "-nn":          {"category": "development",    "name": "Node.js + npm",       "nameZh": "Node.js",             "desc": "Install Node.js and npm", "descZh": "安装 Node.js 和 npm", "tags": ["language"]},
    "-go":          {"category": "development",    "name": "Go",                  "nameZh": "Go 语言",             "desc": "Install Go", "descZh": "安装 Go 语言环境", "tags": ["language"]},
    "-openjdk":     {"category": "development",    "name": "OpenJDK",             "nameZh": "OpenJDK",             "desc": "Install OpenJDK", "descZh": "安装 OpenJDK", "tags": ["language"]},
    "-oraclejdk":   {"category": "development",    "name": "Oracle JDK",          "nameZh": "Oracle JDK",          "desc": "Install Oracle JDK", "descZh": "安装 Oracle JDK", "tags": ["language"]},
    "-oraclejdk8":  {"category": "development",    "name": "Oracle JDK 8",        "nameZh": "Oracle JDK 8",        "desc": "Install Oracle JDK 8", "descZh": "安装 Oracle JDK 8", "tags": ["language"]},
    "-oraclejdk11": {"category": "development",    "name": "Oracle JDK 11",       "nameZh": "Oracle JDK 11",       "desc": "Install Oracle JDK 11", "descZh": "安装 Oracle JDK 11", "tags": ["language"]},
    "-oraclejdk17": {"category": "development",    "name": "Oracle JDK 17",       "nameZh": "Oracle JDK 17",       "desc": "Install Oracle JDK 17", "descZh": "安装 Oracle JDK 17", "tags": ["language"]},
    "-py3":         {"category": "development",    "name": "Python 3",            "nameZh": "Python 3",            "desc": "Install Python 3", "descZh": "安装 Python 3", "tags": ["language"]},
    "-py37":        {"category": "development",    "name": "Python 3.7",          "nameZh": "Python 3.7",          "desc": "Install Python 3.7", "descZh": "安装 Python 3.7", "tags": ["language"]},
    "-py38":        {"category": "development",    "name": "Python 3.8",          "nameZh": "Python 3.8",          "desc": "Install Python 3.8", "descZh": "安装 Python 3.8", "tags": ["language"]},
    "-py39":        {"category": "development",    "name": "Python 3.9",          "nameZh": "Python 3.9",          "desc": "Install Python 3.9", "descZh": "安装 Python 3.9", "tags": ["language"]},
    "-py310":       {"category": "development",    "name": "Python 3.10",         "nameZh": "Python 3.10",         "desc": "Install Python 3.10", "descZh": "安装 Python 3.10", "tags": ["language"]},
    "-py2":         {"category": "development",    "name": "Python 2",            "nameZh": "Python 2",            "desc": "Install Python 2", "descZh": "安装 Python 2", "tags": ["language"]},
    "-pyenv":       {"category": "development",    "name": "pyenv",               "nameZh": "pyenv 版本管理",      "desc": "Install pyenv", "descZh": "安装 pyenv Python 版本管理器", "tags": ["language"]},
    "-perl":        {"category": "development",    "name": "Perl",                "nameZh": "Perl",                "desc": "Install Perl", "descZh": "安装 Perl", "tags": ["language"]},
    "-ruby":        {"category": "development",    "name": "Ruby",                "nameZh": "Ruby",                "desc": "Install Ruby", "descZh": "安装 Ruby", "tags": ["language"]},
    "-rust":        {"category": "development",    "name": "Rust",                "nameZh": "Rust",                "desc": "Install Rust", "descZh": "安装 Rust", "tags": ["language"]},
    "-code":        {"category": "development",    "name": "code-server",         "nameZh": "code-server",         "desc": "Install VS Code in browser", "descZh": "安装浏览器版 VS Code", "tags": ["ide"]},
    "-chromium":    {"category": "development",    "name": "Chromium",            "nameZh": "Chromium 浏览器",     "desc": "Install Chromium headless", "descZh": "安装 Chromium 无头浏览器", "tags": ["browser"]},
    "-crawl":       {"category": "development",    "name": "Crawl Tools",         "nameZh": "爬虫工具集",          "desc": "Install crawl tools", "descZh": "安装爬虫工具集", "tags": ["crawler"]},
    "-phantomjs":   {"category": "development",    "name": "PhantomJS",           "nameZh": "PhantomJS",           "desc": "Install PhantomJS", "descZh": "安装 PhantomJS", "tags": ["browser"]},
    "-jenv":        {"category": "development",    "name": "jenv",                "nameZh": "jenv Java 版本管理",  "desc": "Install jenv for Java version management", "descZh": "安装 jenv Java 版本管理器", "tags": ["language"]},


    # Blue Team
    "-binwalk":     {"category": "blue-team",      "name": "Binwalk",             "nameZh": "Binwalk 固件分析",    "desc": "Firmware analysis tool", "descZh": "固件分析工具", "tags": ["forensics"]},
    "-binwalk-f":   {"category": "blue-team",      "name": "Binwalk (force)",     "nameZh": "Binwalk 强制安装",    "desc": "Force install binwalk", "descZh": "强制安装 Binwalk", "tags": ["forensics"]},
    "-clamav":      {"category": "blue-team",      "name": "ClamAV",              "nameZh": "ClamAV 杀毒",        "desc": "Open source antivirus", "descZh": "开源杀毒引擎", "tags": ["antivirus"]},
    "-vol":         {"category": "blue-team",      "name": "Volatility",          "nameZh": "Volatility 内存取证", "desc": "Memory forensics framework", "descZh": "内存取证框架", "tags": ["forensics"]},
    "-vol3":        {"category": "blue-team",      "name": "Volatility 3",        "nameZh": "Volatility 3",       "desc": "Volatility 3 memory forensics", "descZh": "Volatility 3 内存取证", "tags": ["forensics"]},
    "-lt":          {"category": "blue-team",      "name": "LogonTracer",         "nameZh": "LogonTracer 日志",    "desc": "Windows logon event analysis", "descZh": "Windows 登录事件分析", "tags": ["forensics"]},
    "-suricata":    {"category": "blue-team",      "name": "Suricata",            "nameZh": "Suricata IDS",       "desc": "Network IDS/IPS", "descZh": "网络入侵检测/防御系统", "tags": ["ids"]},

    # Red Team Tools
    "-aircrack":    {"category": "red-infra",      "name": "aircrack-ng",         "nameZh": "aircrack-ng WiFi",   "desc": "WiFi security auditing", "descZh": "WiFi 安全审计工具", "tags": ["wifi"]},
    "-bypass":      {"category": "red-infra",      "name": "Bypass",              "nameZh": "Bypass 绕过",        "desc": "AV/EDR bypass tools", "descZh": "杀软/EDR 绕过工具", "tags": ["evasion"]},
    "-cs":          {"category": "red-infra",      "name": "CobaltStrike",        "nameZh": "CobaltStrike C2",    "desc": "CobaltStrike C2 framework", "descZh": "CobaltStrike C2 框架", "tags": ["c2"]},
    "-cs45":        {"category": "red-infra",      "name": "CobaltStrike 4.5",    "nameZh": "CobaltStrike 4.5",   "desc": "CobaltStrike 4.5 C2", "descZh": "CobaltStrike 4.5 C2 框架", "tags": ["c2"]},
    "-wpscan":      {"category": "pentest-exploit","name": "WPScan",              "nameZh": "WPScan WordPress",   "desc": "WordPress scanner", "descZh": "WordPress 漏洞扫描器", "tags": ["web"]},
    "-wx":          {"category": "pentest-exploit","name": "wxappUnpacker",       "nameZh": "wxappUnpacker 小程序","desc": "WeChat mini-program unpacker", "descZh": "微信小程序解包工具", "tags": ["mobile"]},
    "-yakit":       {"category": "red-infra",      "name": "Yakit",               "nameZh": "Yakit 安全平台",     "desc": "Yakit security platform", "descZh": "Yakit 安全测试平台", "tags": ["platform"]},
    "-msf":         {"category": "pentest-exploit","name": "Metasploit",          "nameZh": "Metasploit 框架",    "desc": "Penetration testing framework", "descZh": "渗透测试框架", "tags": ["framework"]},

    # Red Team Infrastructure
    "-frp":         {"category": "red-infra",      "name": "frp",                 "nameZh": "frp 内网穿透",       "desc": "Fast reverse proxy", "descZh": "快速反向代理/内网穿透", "tags": ["proxy", "tunnel"]},
    "-nps":         {"category": "red-infra",      "name": "nps",                 "nameZh": "nps 内网穿透",       "desc": "Intranet proxy server", "descZh": "轻量级内网穿透代理", "tags": ["proxy", "tunnel"]},
    "-rg":          {"category": "red-infra",      "name": "RedGuard",            "nameZh": "RedGuard 流量伪装",  "desc": "C2 front flow control", "descZh": "C2 前置流量控制工具", "tags": ["proxy", "evasion"]},
    "-interactsh":  {"category": "red-infra",      "name": "Interactsh",          "nameZh": "Interactsh OOB",    "desc": "OOB interaction server", "descZh": "带外交互收集服务器", "tags": ["oob"]},
    "-merlin":      {"category": "red-infra",      "name": "Merlin",              "nameZh": "Merlin C2",          "desc": "Merlin C2 (HTTP/2)", "descZh": "Merlin C2 框架", "tags": ["c2"]},
    "-sliver":      {"category": "red-infra",      "name": "Sliver",              "nameZh": "Sliver C2",          "desc": "Sliver C2 framework", "descZh": "Sliver C2 框架", "tags": ["c2"]},
    "-sliver-client":{"category": "red-infra",     "name": "Sliver Client",       "nameZh": "Sliver 客户端",      "desc": "Sliver C2 client only", "descZh": "Sliver C2 仅客户端", "tags": ["c2"]},
    "-sps":         {"category": "red-infra",      "name": "SharPyShell",         "nameZh": "SharPyShell",        "desc": "SharPyShell webshell", "descZh": "SharPyShell Webshell 框架", "tags": ["webshell"]},
    "-http":        {"category": "red-infra",      "name": "SimpleHTTPServer",    "nameZh": "SimpleHTTPServer",   "desc": "Simple HTTP file server", "descZh": "简易 HTTP 文件服务", "tags": ["http"]},
    "-arl":         {"category": "red-infra",      "name": "ARL",                 "nameZh": "ARL 资产侦察",       "desc": "Asset Reconnaissance Lighthouse", "descZh": "灯塔资产侦察系统", "tags": ["asset"]},
    "-pupy":        {"category": "red-infra",      "name": "Pupy",                "nameZh": "Pupy RAT",           "desc": "Cross-platform RAT", "descZh": "跨平台远控工具", "tags": ["c2", "rat"]},
    "-viper":       {"category": "red-infra",      "name": "Viper",               "nameZh": "Viper 图形化 C2",    "desc": "Graphical C2 platform", "descZh": "图形化 C2 平台", "tags": ["c2"]},
    "-mythic":      {"category": "red-infra",      "name": "Mythic",              "nameZh": "Mythic C2",          "desc": "Mythic C2 framework", "descZh": "Mythic C2 框架", "tags": ["c2"]},

    # Docker-based / Vuln Environments
    "-awvs":        {"category": "red-infra",      "name": "AWVS",                "nameZh": "AWVS 漏扫",          "desc": "Acunetix web vulnerability scanner", "descZh": "Acunetix Web 漏洞扫描器", "tags": ["vuln-scanner"]},

    "-mobsf":       {"category": "red-infra",      "name": "MobSF",               "nameZh": "MobSF 移动安全",     "desc": "Mobile security framework", "descZh": "移动安全测试框架", "tags": ["mobile"]},
    "-nodejsscan":  {"category": "red-infra",      "name": "nodejsscan",          "nameZh": "nodejsscan",         "desc": "Node.js security scanner", "descZh": "Node.js 安全扫描器", "tags": ["scanner"]},
    "-vulhub":      {"category": "vuln-env",       "name": "VulHub",              "nameZh": "VulHub 漏洞环境",    "desc": "Docker vulnerable environments", "descZh": "Docker 漏洞环境集", "tags": ["docker", "vuln"]},
    "-vulfocus":    {"category": "vuln-env",       "name": "VulFocus",            "nameZh": "VulFocus 靶场",      "desc": "Vulnerability target platform", "descZh": "漏洞靶场平台", "tags": ["docker", "vuln"]},
    "-metarget":    {"category": "vuln-env",       "name": "Metarget",            "nameZh": "Metarget 靶机",      "desc": "Cloud-native target construction", "descZh": "自动化云原生靶机构建", "tags": ["cloud", "vuln"]},
    "-TerraformGoat":{"category": "vuln-env",      "name": "TerraformGoat",       "nameZh": "TerraformGoat 云靶场","desc": "Terraform vulnerable cloud env", "descZh": "基于 Terraform 的云漏洞靶场", "tags": ["cloud", "terraform"]},

    # Misc Services
    "-asciinema":   {"category": "misc",           "name": "asciinema",           "nameZh": "asciinema 终端录制",  "desc": "Terminal session recorder", "descZh": "终端会话录制工具", "tags": ["terminal"]},
    "-bt":          {"category": "misc",           "name": "宝塔面板",            "nameZh": "宝塔面板",            "desc": "BT Panel", "descZh": "宝塔服务器管理面板", "tags": ["panel"]},
    "-aa":          {"category": "misc",           "name": "aaPanel",             "nameZh": "aaPanel 面板",        "desc": "aaPanel server management", "descZh": "aaPanel 服务器管理面板", "tags": ["panel"]},
    "-1panel":      {"category": "misc",           "name": "1Panel",              "nameZh": "1Panel 面板",         "desc": "1Panel server management", "descZh": "1Panel 服务器管理面板", "tags": ["panel"]},
    "-music":       {"category": "misc",           "name": "UnblockNeteaseMusic", "nameZh": "网易云解锁",          "desc": "Unblock Netease Music", "descZh": "网易云音乐解锁", "tags": ["music"]},
    "-nginx":       {"category": "misc",           "name": "Nginx",               "nameZh": "Nginx Web 服务器",   "desc": "Nginx from source", "descZh": "从源码编译安装 Nginx", "tags": ["web", "server"]},
    "-ssh":         {"category": "basic",          "name": "SSH Server",          "nameZh": "SSH 服务",            "desc": "Install SSH server", "descZh": "安装并配置 SSH 服务", "tags": ["service"]},
    "-ssr":         {"category": "misc",           "name": "SSR",                 "nameZh": "SSR 代理",            "desc": "Install SSR", "descZh": "安装 SSR", "tags": ["proxy"]},
    "-zsh":         {"category": "misc",           "name": "Zsh + Oh-My-Zsh",     "nameZh": "Zsh 终端",            "desc": "Install zsh with Oh-My-Zsh", "descZh": "安装 Zsh 及 Oh-My-Zsh", "tags": ["shell"]},
    "-jq":          {"category": "misc",           "name": "jq",                  "nameZh": "jq JSON 处理",        "desc": "Command-line JSON processor", "descZh": "命令行 JSON 处理器", "tags": ["cli"]},


    # Supplementary
    "-ad":          {"category": "pentest-recon",  "name": "Attack & Detect",     "nameZh": "攻防检测工具",        "desc": "Attack & Detection tools", "descZh": "攻防检测工具集", "tags": ["batch"]},
    "-k8s":         {"category": "development",    "name": "Kubernetes",          "nameZh": "Kubernetes",          "desc": "Install Kubernetes", "descZh": "安装 Kubernetes", "tags": ["container", "k8s"]},
    "-proxy":       {"category": "basic",          "name": "Proxychains",         "nameZh": "Proxychains 代理链",  "desc": "Install Proxychains-ng", "descZh": "安装 Proxychains-ng 代理链", "tags": ["proxy"]},
    "-debug":       {"category": "development",    "name": "Debug Tools",         "nameZh": "调试工具",            "desc": "Install debugging tools", "descZh": "安装调试工具", "tags": ["debug"]},
    "-py2-f":       {"category": "development",    "name": "Python 2 (force)",    "nameZh": "Python 2 (强制)",     "desc": "Force install Python 2", "descZh": "强制安装 Python 2", "tags": ["language"]},
    "-pip2-f":      {"category": "development",    "name": "pip2 (force)",        "nameZh": "pip2 (强制)",         "desc": "Force install pip2", "descZh": "强制安装 pip2", "tags": ["language"]},
    "-ruby-f":      {"category": "development",    "name": "Ruby (force)",        "nameZh": "Ruby (强制安装)",     "desc": "Force install Ruby", "descZh": "强制安装 Ruby", "tags": ["language"]},
    "-update":      {"category": "system",         "name": "Update f8x",          "nameZh": "更新 f8x",            "desc": "Update f8x to latest version", "descZh": "更新 f8x 到最新版本", "tags": ["system"]},
    "-upgrade":     {"category": "system",         "name": "Upgrade Tools",       "nameZh": "升级渗透工具",        "desc": "Upgrade installed pentest tools", "descZh": "升级已安装的渗透工具", "tags": ["system"]},

    # Other (system tools, not installable software — included for completeness)
    "-clear":       {"category": "system",         "name": "Clear Logs",          "nameZh": "清理痕迹",            "desc": "Clean up system usage traces", "descZh": "清理系统使用痕迹", "tags": ["system"]},
    "-info":        {"category": "system",         "name": "System Info",         "nameZh": "系统信息",            "desc": "View system information", "descZh": "查看系统信息", "tags": ["system"]},
    "-optimize":    {"category": "system",         "name": "Optimize",            "nameZh": "系统优化",            "desc": "Optimize system performance", "descZh": "优化系统性能参数", "tags": ["system"]},
    "-remove":      {"category": "system",         "name": "Remove Watchers",     "nameZh": "卸载监控",            "desc": "Remove VPS cloud monitoring", "descZh": "卸载 VPS 云监控", "tags": ["system"]},
    "-swap":        {"category": "system",         "name": "Swap Partition",      "nameZh": "Swap 分区",           "desc": "Configure swap partition", "descZh": "配置 swap 交换分区", "tags": ["system"]},
    "-rmlock":      {"category": "system",         "name": "Remove Lock",         "nameZh": "解锁包管理器",        "desc": "Run the unlock module", "descZh": "解除包管理器锁", "tags": ["system"]},
}

# ── 预设组合 ──
PRESETS = [
    {"id": "pentest-full",  "name": "Full Pentest",  "nameZh": "渗透全套",  "description": "Install all recon + exploit tools", "flags": ["-ka", "-kb"]},
    {"id": "dev-env",       "name": "Dev Environment","nameZh": "开发环境",  "description": "Python3, Go, Docker, Node.js, SDKMAN", "flags": ["-d"]},
    {"id": "blue-team",     "name": "Blue Team",     "nameZh": "蓝队防御",  "description": "Fail2Ban, rkhunter, anti-portscan", "flags": ["-s"]},
    {"id": "c2-setup",      "name": "C2 Setup",      "nameZh": "C2 快速部署","description": "CobaltStrike + frp + RedGuard", "flags": ["-cs45", "-frp", "-rg"]},
    {"id": "basic-all",     "name": "Basic Setup",   "nameZh": "基础环境",  "description": "Base tools + SSH + Zsh", "flags": ["-b", "-ssh", "-zsh"]},
    {"id": "recon-light",   "name": "Recon Light",   "nameZh": "轻量侦查",  "description": "Recon tools suite (nmap, httpx, subfinder, ffuf ...)", "flags": ["-ka"]},
]

# ── 分类元数据 ──
CATEGORIES = [
    {"id": "basic",          "name": "Basic Environment",  "nameZh": "基础环境"},
    {"id": "development",    "name": "Development",         "nameZh": "开发环境"},
    {"id": "pentest-recon",  "name": "Pentest - Recon",     "nameZh": "渗透 - 侦查"},
    {"id": "pentest-exploit","name": "Pentest - Exploit",   "nameZh": "渗透 - 利用"},
    {"id": "pentest-post",   "name": "Pentest - Post",      "nameZh": "渗透 - 后渗透"},
    {"id": "blue-team",      "name": "Blue Team",           "nameZh": "蓝队防御"},
    {"id": "red-infra",      "name": "Red Team Infra",      "nameZh": "红队基础设施"},
    {"id": "vuln-env",       "name": "Vulnerable Envs",     "nameZh": "靶场环境"},
    {"id": "misc",           "name": "Miscellaneous",       "nameZh": "杂项工具"},
    {"id": "system",         "name": "System Tools",        "nameZh": "系统工具"},
]


def extract_flags_from_script(script_path):
    """从 f8x 脚本的 Main case 语句中提取所有可用 flag"""
    with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 提取 case 语句中的 flag
    # 匹配模式: -flag | flag) 或 -flag)
    flags = set()
    for match in re.finditer(r'^\s+(-[\w-]+)\s*(?:\||\))', content, re.MULTILINE):
        flag = match.group(1)
        if flag not in ('-h',):  # 排除帮助
            flags.add(flag)

    return sorted(flags)


def extract_version(script_path):
    """提取 f8x 版本号"""
    with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = re.match(r'^F8x_Version="(.+)"', line)
            if m:
                return m.group(1)
    return "unknown"


# ── Batch flag → entry function mapping ──
# Maps batch flags to their top-level function names in the f8x script
BATCH_ENTRY_FUNCTIONS = {
    "-k":     ["kali_Tools"],
    "-ka":    ["kali_Tools_TypeA"],
    "-kb":    ["kali_Tools_TypeB"],
    "-kc":    ["kali_Tools_TypeC"],
    "-kd":    ["kali_Tools_TypeD"],
    "-ke":    ["kali_Tools_TypeE"],
    "-b":     ["Base_Install"],
    "-d":     ["Dev_Tools"],
    "-s":     ["Secure"],
    "-f":     ["Fun_Tools"],
    "-cloud": ["cloud"],
    "-ad":    ["Ad_Tools"],
    "-all":   ["all_Install"],
}


# ── Well-known tool URLs (for tools installed via package managers, not GitHub) ──
KNOWN_TOOL_URLS = {
    "nmap": "https://nmap.org",
    "masscan": "https://github.com/robertdavidgraham/masscan",
    "Metasploit": "https://github.com/rapid7/metasploit-framework",
    "Terraform": "https://www.terraform.io",
    "Docker and Docker-compose": "https://www.docker.com",
    "Go": "https://go.dev",
    "python3 and pip3": "https://www.python.org",
    "python2": "https://www.python.org",
    "Fail2Ban": "https://github.com/fail2ban/fail2ban",
    "rkhunter": "https://rkhunter.sourceforge.net",
    "mitmproxy": "https://mitmproxy.org",
    "ffmpeg": "https://ffmpeg.org",
    "htop": "https://github.com/htop-dev/htop",
    "exa": "https://github.com/ogham/exa",
    "ncdu": "https://dev.yorhel.nl/ncdu",
    "ncat": "https://nmap.org/ncat/",
    "john": "https://github.com/openwall/john",
    "starship": "https://github.com/starship/starship",
    "trash-cli": "https://github.com/andreafrancia/trash-cli",
    "kubectl": "https://kubernetes.io/docs/tasks/tools/",
    "Arjun": "https://github.com/s0md3v/Arjun",
    "apkleaks": "https://github.com/dwisiswant0/apkleaks",
    "ApkAnalyser": "https://github.com/aspect-labs/ApkAnalyser",
    "pypykatz": "https://github.com/skelsec/pypykatz",
    "Certipy": "https://github.com/ly4k/Certipy",
    "Coercer": "https://github.com/p0dalirius/Coercer",
    "DonPAPI": "https://github.com/login-securite/DonPAPI",
    "Exegol": "https://github.com/ThePorgs/Exegol",
    "evil-winrm": "https://github.com/Hackplayers/evil-winrm",
    "bloodhound-python": "https://github.com/fox-it/BloodHound.py",
    "bloodyAD": "https://github.com/CravateRouge/bloodyAD",
    "GitHacker": "https://github.com/WangYihang/GitHacker",
    "ZoomEye-python": "https://github.com/knownsec/ZoomEye-python",
    "SDKMAN!": "https://sdkman.io",
    "ldapsearch": "https://wiki.debian.org/LDAP/LDAPUtils",
    "ldeep": "https://github.com/franc-music/ldeep",
    "lsassy": "https://github.com/Hackndo/lsassy",
    "minikerberos": "https://github.com/skelsec/minikerberos",
    "mitm6": "https://github.com/dirkjanm/mitm6",
    "gpp-decrypt": "https://github.com/t0thkr1s/gpp-decrypt",
    "shellpub": "https://www.shellpub.com",
    "proxychains4": "https://github.com/rofl0r/proxychains-ng",
    "xfreerdp": "https://www.freerdp.com",
    "tccli": "https://github.com/TencentCloud/tencentcloud-cli",
    "nuclei-templates": "https://github.com/projectdiscovery/nuclei-templates",
    "nodejs && npm": "https://nodejs.org",
    "Oraclejdk": "https://www.oracle.com/java/",
}

# Functions that are infrastructure helpers, not actual installable tools
SKIP_FUNCTION_NAMES = {
    'Base_Install', 'Base_Tools', 'Base_Check', 'Dev_Base_Install',
    'Pentest_Base_Install', 'Pentest_pip_Install', 'Pentest_Misc_Install',
    'Rm_Lock', 'Proxy_Switch', 'Py_Check', 'pip2_Check', 'GO_Check',
    'Install_Switch', 'Install_Switch2', 'Install_Switch3', 'Install_Switch4', 'Install_Switch5',
}

# Tool names that are infrastructure, not user-facing tools
SKIP_TOOL_NAMES = {
    'pip module', 'python modules', 'basic tools', 'pip module record',
    'base', 'dev_base', 'misc',
}


def extract_functions(content):
    """Extract all bash function bodies as {name: body} dict."""
    functions = {}
    # Match function_name(){ or function_name ()  {
    func_pattern = re.compile(r'^(\w[\w-]*)\s*\(\)\s*\{', re.MULTILINE)
    positions = [(m.group(1), m.end()) for m in func_pattern.finditer(content)]

    for i, (name, start) in enumerate(positions):
        # Find matching closing brace by counting braces
        depth = 1
        pos = start
        while pos < len(content) and depth > 0:
            ch = content[pos]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            pos += 1
        functions[name] = content[start:pos-1]

    return functions


def extract_github_urls(func_body):
    """Extract GitHub repo URLs from a function body."""
    urls = set()
    for m in re.finditer(r'github\.com/([\w._-]+/[\w._-]+?)(?:\.git|/releases|/archive|/raw|["\s/\)])', func_body):
        repo = m.group(1).rstrip('.')
        urls.add(f"https://github.com/{repo}")
    return urls


def extract_sub_tools(content, functions, entry_func_names):
    """
    Given entry function names for a batch flag, recursively extract all
    sub-tools (individual install functions) with name, description, and URL.
    """
    tools = []
    seen = set()

    def collect_install_calls(func_name, is_entry=False):
        """Recursively collect _Install function calls from a function."""
        if func_name in seen or func_name not in functions:
            return
        if func_name in SKIP_FUNCTION_NAMES and not is_entry:
            return
        seen.add(func_name)
        body = functions[func_name]

        # Find echo "Installing XXX" followed by function calls
        lines = body.split('\n')
        current_tool_name = None

        for line in lines:
            stripped = line.strip()

            # Skip commented-out lines
            if stripped.startswith('#'):
                continue

            # Extract tool name from echo "Installing XXX"
            echo_match = re.search(r'Installing\s+(.+?)\\n', stripped)
            if echo_match:
                current_tool_name = echo_match.group(1).strip()
                continue

            # Match function calls (XYZ_Install or XYZ_install)
            call_match = re.match(r'^([\w-]+_[Ii]nstall\w*)\b', stripped)
            if call_match:
                called_func = call_match.group(1)
                if called_func in SKIP_FUNCTION_NAMES:
                    current_tool_name = None
                    continue
                if called_func in functions:
                    func_body = functions[called_func]
                    # Extract GitHub URLs from the install function
                    urls = extract_github_urls(func_body)
                    # Extract tool name from name="xxx" in function body
                    name_match = re.search(r'name="([^"]+)"', func_body)
                    tool_name = current_tool_name or (name_match.group(1) if name_match else called_func.replace('_Install', '').replace('Pentest_', ''))

                    # Skip infrastructure/helper functions
                    if tool_name.lower() in SKIP_TOOL_NAMES:
                        current_tool_name = None
                        continue

                    # Deduplicate by function name
                    if called_func not in seen:
                        seen.add(called_func)
                        url = sorted(urls)[0] if urls else KNOWN_TOOL_URLS.get(tool_name, "")
                        tools.append({
                            "name": tool_name,
                            "url": url,
                        })
                current_tool_name = None
                continue

            # Match sub-function calls that are themselves aggregators (e.g., kali_Tools_TypeA)
            sub_call_match = re.match(r'^([\w-]+)\b', stripped)
            if sub_call_match:
                sub_func = sub_call_match.group(1)
                # Only recurse into known functions that aren't install functions
                if sub_func in functions and not sub_func.endswith('_Install') and sub_func not in ('echo', 'if', 'else', 'fi', 'case', 'esac', 'then', 'done', 'do', 'for', 'while', 'return', 'exit', 'cd', 'rm', 'mkdir', 'touch', 'chmod', 'mv', 'cp', 'cat', 'grep', 'sed', 'awk', 'which', 'test', 'local', 'export', 'source', 'eval', 'shift', 'break', 'continue', 'true', 'false', 'set', 'unset'):
                    collect_install_calls(sub_func)
                current_tool_name = None

    for func_name in entry_func_names:
        collect_install_calls(func_name, is_entry=True)

    return tools


def generate_catalog(script_path):
    """生成完整目录"""
    with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    flags = extract_flags_from_script(script_path)
    version = extract_version(script_path)
    functions = extract_functions(content)
    modules = []

    for flag in flags:
        if flag in CATEGORY_MAP:
            info = CATEGORY_MAP[flag]
            mod_id = flag.lstrip('-').lower()
            mod = {
                "id": mod_id,
                "name": info["name"],
                "nameZh": info["nameZh"],
                "flag": flag,
                "category": info["category"],
                "description": info["desc"],
                "descriptionZh": info["descZh"],
                "tags": info["tags"],
            }
            # For batch flags, extract includes
            if "batch" in info["tags"] and flag in BATCH_ENTRY_FUNCTIONS:
                includes = extract_sub_tools(content, functions, BATCH_ENTRY_FUNCTIONS[flag])
                if includes:
                    mod["includes"] = includes
            modules.append(mod)
        else:
            # 未在映射表中的 flag，自动生成基本条目
            mod_id = flag.lstrip('-').lower()
            modules.append({
                "id": mod_id,
                "name": flag.lstrip('-'),
                "nameZh": flag.lstrip('-'),
                "flag": flag,
                "category": "misc",
                "description": f"Install {flag.lstrip('-')}",
                "descriptionZh": f"安装 {flag.lstrip('-')}",
                "tags": [],
            })

    # 计算每个分类的数量
    cat_counts = {}
    for m in modules:
        cat_counts[m["category"]] = cat_counts.get(m["category"], 0) + 1

    categories_with_count = []
    for cat in CATEGORIES:
        c = dict(cat)
        c["count"] = cat_counts.get(cat["id"], 0)
        categories_with_count.append(c)

    return {
        "version": version,
        "catalog_version": 3,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "modules": modules,
        "categories": categories_with_count,
        "presets": PRESETS,
    }


def main():
    script_path = sys.argv[1] if len(sys.argv) > 1 else "./f8x"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "./catalog.json"

    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found", file=sys.stderr)
        sys.exit(1)

    catalog = generate_catalog(script_path)

    # Warn about sub-tools with missing URLs
    missing_url = []
    for m in catalog['modules']:
        for t in m.get('includes', []):
            if not t.get('url'):
                missing_url.append((m['flag'], t['name']))
    if missing_url:
        print(f"⚠ {len(missing_url)} sub-tool(s) missing URL (add to KNOWN_TOOL_URLS):", file=sys.stderr)
        for flag, name in missing_url:
            print(f"  {flag}: {name}", file=sys.stderr)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"Generated {output_path}: {len(catalog['modules'])} modules, version {catalog['version']}")


if __name__ == "__main__":
    main()
