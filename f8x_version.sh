#!/usr/bin/env bash
#set -x

# f8x 会自动 source 同目录下的 f8x_version.sh，用于覆盖默认版本号。
# 按需取消注释并修改，不想覆盖的保持注释即可。

### 运行说明
# 1) 直接放在 f8x 同目录即可被自动加载；或手动运行：
#    source ./f8x_version.sh
# 2) 仅声明需要改动的版本变量，其他保持默认。

### 开发环境示例
# Go_Version="go1.22.5"
# node_Ver="v22.11.0"
# code_server_Ver="v4.108.0"

### 渗透工具示例
# frp_Ver="v0.66.0"
# Nuclei_Ver="v3.6.2"
# subfinder_Ver="v2.12.0"
# httpx_Ver="v1.7.4"
# naabu_Ver="v2.3.7"
# xray_Ver="xpoc-0.1.0"
# nuclei 等 projectdiscovery 系列只改版本号，文件名保持 f8x 默认即可。

### 其他工具示例
# fzf_Ver="v0.65.2"
# AdGuardHome_Version="v0.107.66"

### 需要同时改文件名的示例
# jq_ver="jq-1.8.1"
# jq_bin="jq-1.8.1.zip"
# jq_dir="jq-1.8.1"

### 临时禁用某些工具安装（示例：置空版本）
# frp_Ver=""