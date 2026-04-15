---
name: f8x-tool-maintenance
description: 维护 f8x 渗透工具安装器：新增工具安装函数、更新版本号、管理 F8X_TOOL_LIST 注册、构建 Arsenal 多平台投递物。当修改 f8x 脚本、添加新渗透工具、更新工具版本、检查工具覆盖、或构建 arsenal 二进制时，务必使用此 skill。即使用户只是提到 "装个 xxx 工具"、"f8x 里加一下"、"更新一下版本" 也应触发。
---

# f8x 工具维护

f8x (`/Users/f0x/pte-project/infra-plat/f8x/f8x`) 是一个 12800+ 行的 Bash 脚本，包含 161 个安装函数，自动化安装渗透测试工具。

## 架构概览

新增或修改一个工具涉及**最多 5 个位置**：

```
① 版本变量 (行 93-435 区域)
② 安装函数 (行 3305-6990 区域)
③ 安装组调用 (行 10502-10950 区域)
④ F8X_TOOL_LIST 注册 (行 10957+)
⑤ Arsenal 投递物 [可选] (行 11359+)
```

其中 ①②④ 是必须的，③ 看工具分类决定，⑤ 仅适用于需要投递到目标机执行的工具。

## 新增工具流程

### Step 1: 添加版本变量（行 93-435 区域）

f8x 的版本变量分两个区域：
- **渗透工具** (行 93-370)：`Software version variable setting (pentest)`
- **其他工具** (行 373-435)：`Software version variable setting (other)`

最简单情况只需一个变量：
```bash
# https://github.com/作者/工具/releases
xxx_Ver="v1.0.0"
```

但很多工具还需要定义**关联的文件名变量**，因为 release 文件名中嵌入了版本号：
```bash
# https://github.com/作者/工具/releases
xxx_Ver="v1.0.0"
xxx_bin_amd64="xxx_1.0.0_linux_amd64.tar.gz"
xxx_bin_arm64="xxx_1.0.0_linux_arm64.tar.gz"
```

更新版本时，这些 `_bin_*`、`_File_*`、`_Dir_*` 变量中的版本号也必须同步修改，这是最容易出错的地方。

位置约定：云安全工具放在 `k8spider_Ver` 附近，AD 工具放在 `ligolo_ng_Ver` 附近。

**版本覆盖机制**：f8x 在行 460 会 `source ./f8x_version.sh`（如果存在），可以在不修改主脚本的情况下覆盖版本号，适合测试和自定义部署。

### Step 2: 编写安装函数（行 3305-6990 区域）

**函数命名**：渗透工具推荐 `Pentest_xxx_Install()`，但不是强制的。F8X_TOOL_LIST 中实际存在多种命名风格：
- `Pentest_xxx_Install()` — 大多数渗透工具
- `xxx_Install()` — 基础设施工具（`frp_Install`, `nps_Install`, `RedGuard_Install`, `Docker_Install` 等）

函数名只要和 F8X_TOOL_LIST 注册时一致即可。

根据工具类型选择模板 → 详见 `references/install-templates.md`

四种常见模板：
- **模板 A**：GitHub Release 下载裸二进制（Go/Rust 静态编译工具）
- **模板 A2**：GitHub Release 下载压缩包（tar.gz/zip，用预定义的 `_bin_*` 变量）
- **模板 B**：Git Clone + pip install（Python PoC/工具）
- **模板 C**：pip install（PyPI 包）

**内置 helper 函数**（直接在安装函数中调用，无需自己实现）：
- `Install_Switch7 "requirements.txt"` — 自动用 pip3/pip 安装 requirements.txt
- `Install_Switch8 "包名"` — pip install 指定包（带 `--break-system-packages` 兼容新版 pip）
- `Install_Switch "apt包名"` — apt install

### Step 3: 注册到安装组（行 10502-10950 区域）

根据工具类别在对应函数中添加调用。调用链：`-ka` → `kali_Tools("a")` → `kali_Tools_TypeA()`

| 触发选项 | 实际调用 | 分类 | 典型工具 |
|----------|----------|------|----------|
| `-ka` | `kali_Tools_TypeA()` (行 10539) | 信息收集/资产发现 | nmap, ffuf, subfinder, fscan, httpx 等 30+ |
| `-kb` | `kali_Tools_TypeB()` (行 10623) | 漏洞扫描/利用 | metasploit, sqlmap, nuclei, xray 等 |
| `-kc` | `kali_Tools_TypeC()` (行 10680) | 后渗透/内网 | impacket, responder, crackmapexec, mitmproxy 等 |
| `-kd` | `kali_Tools_TypeD()` (行 10715) | 密码/杂项 | hashcat, jadx, ncat, mapcidr, dnsx 等 |
| `-ke` | `kali_Tools_TypeE()` (行 10754) | 补充/大型字典 | SecLists, hakrawler, subjs, assetfinder |
| `-ad` | `Ad_Tools()` (行 10773) | AD 域渗透专用 | impacket, certipy, noPac, ligolo-ng 等 |
| `-cloud` | `cloud()` (行 10897) | 云安全 | k8spider, kubectl, kubeletctl, tccli 等 |

**分类决策**：不确定放哪个 Type 时，看工具在渗透流程中的位置——收集目标信息用 TypeA，发现和利用漏洞用 TypeB，拿到 shell 之后的操作用 TypeC，不好归类的放 TypeD。TypeE 留给辅助资源（字典、被动收集）。域渗透/云安全有专门的 `-ad` / `-cloud`。

格式：
```bash
echo -e "\033[1;33m\n>> Installing xxx\n\033[0m"
Pentest_xxx_Install
```

### Step 4: 注册到 F8X_TOOL_LIST（行 10957+）

让 `-install`、`--list-tools`、`--search` 能找到工具：

```
xxx|Pentest_xxx_Install|0
```

格式：`工具名(小写)|安装函数名|依赖级别`
- 0 = 无额外依赖（wget 下载二进制）
- 1 = 需要 Python（自动调用 `Py_Check`）
- 2 = 需要 Go（自动调用 `GO_Check`）
- 3 = 需要 Python + Go

注意：`--list-tools` 和 `--search` 不需要 root 权限（在 Main() 之前就被拦截处理）。

### Step 5: Arsenal 投递物 [可选]（行 11359+）

仅当工具需要投递到目标机上执行时才需要。

**适合 Arsenal 的工具**：
- Go/Rust 静态编译二进制，有 GitHub Releases 多平台预编译文件
- 需要在目标机上直接执行（fscan, chisel, frpc, cdk 等）
- agent 类工具（ligolo-agent）

**不适合 Arsenal 的**：
- Python 脚本（需要运行环境）
- 攻击机本地工具（nmap, responder）
- 系统工具（apt 包）

详见 `references/arsenal-guide.md`

## 更新工具版本

1. 在 GitHub Releases 页面确认最新版本
2. 修改版本变量 `xxx_Ver="vNEW"`
3. **关键**：同步修改所有关联的文件名变量（`_bin_amd64`、`_bin_arm64`、`_File_*`、`_Dir_*`），版本号嵌在文件名里！
   ```bash
   # 错误示例：只改了 Ver，忘了改 bin
   Nuclei_Ver="v3.8.0"
   Nuclei_Install_amd64="nuclei_3.7.0_linux_amd64.zip"  # ← 还是旧版本！
   ```
4. 如果 release 文件名格式变了，同步修改安装函数和 arsenal case 块
5. 批量检查用：`python3 check_releases.py`（根目录）
6. 也可以用 `f8x_version.sh` 临时覆盖版本号测试，不影响主脚本

## 常用命令

```bash
# 安装单个工具（需要 root）
./f8x -install nuclei

# 搜索工具（不需要 root）
./f8x --search nmap

# 列出所有工具（不需要 root）
./f8x --list-tools          # JSON 格式
./f8x --list-tools table    # 表格格式

# 构建 arsenal 投递物
./f8x -arsenal

# 安装工具套件
./f8x -ka    # 信息收集/资产发现 (TypeA, 30+ 工具)
./f8x -kb    # 漏洞扫描/利用 (TypeB)
./f8x -kc    # 后渗透/内网 (TypeC)
./f8x -kd    # 密码/杂项 (TypeD)
./f8x -ke    # 补充/大型字典 (TypeE)
./f8x -cloud # 云安全
./f8x -ad    # AD 域渗透
```

## 关键文件路径

| 文件 | 作用 |
|------|------|
| `/Users/f0x/pte-project/infra-plat/f8x/f8x` | f8x 安装器主脚本（12800+ 行） |
| `/Users/f0x/pte-project/infra-plat/f8x/f8x_version.sh` | 版本覆盖配置（source 加载，可选） |
| `/Users/f0x/pte-project/infra-plat/f8x/check_releases.py` | 批量检查工具版本更新 |
| `/Users/f0x/pte-project/infra-plat/f8x/doc/ai-friendly-tool-install-design.md` | AI 友好化改造设计文档 |

## 端到端示例：添加 httpx

以 ProjectDiscovery 的 httpx 为例，走一遍完整的 5 步流程：

**Step 1** — 版本变量（行 93-370 区域，渗透工具段）：
```bash
# https://github.com/projectdiscovery/httpx/releases
httpx_Ver="v1.6.10"
httpx_bin_amd64="httpx_1.6.10_linux_amd64.zip"
httpx_bin_arm64="httpx_1.6.10_linux_arm64.zip"
```

**Step 2** — 安装函数（模板 A2，因为 release 是 zip 压缩包）：
```bash
Pentest_httpx_Install(){
    name="httpx"
    which httpx > /dev/null 2>&1
    if [ $? == 0 ]; then
        Echo_ALERT "$name installed"
    else
        case $Linux_architecture_Name in
            *"linux-x86_64"*)  httpx_bin="${httpx_bin_amd64}" ;;
            *"linux-arm64"*)   httpx_bin="${httpx_bin_arm64}" ;;
            *)                 httpx_bin="${httpx_bin_amd64}" ;;
        esac
        local tmp_dir="/tmp/httpx_install"
        mkdir -p "$tmp_dir"
        $Proxy_OK wget ${GitProxy}https://github.com/projectdiscovery/httpx/releases/download/${httpx_Ver}/${httpx_bin} \
            -O "$tmp_dir/${httpx_bin}" ${wget_option} 2>/dev/null || Echo_ERROR2
        cd "$tmp_dir" && unzip -o "${httpx_bin}" > /dev/null 2>&1
        mv "$tmp_dir/httpx" /usr/local/bin/httpx
        chmod +x /usr/local/bin/httpx
        rm -rf "$tmp_dir"
        which httpx > /dev/null 2>&1 && Echo_INFOR "Successfully installed $name $httpx_Ver" || Echo_ERROR3
    fi
}
```

**Step 3** — 注册到 `kali_Tools_TypeA()`（信息收集类工具）：
```bash
echo -e "\033[1;33m\n>> Installing httpx\n\033[0m"
Pentest_httpx_Install
```

**Step 4** — 注册到 F8X_TOOL_LIST：
```
httpx|Pentest_httpx_Install|0
```

**Step 5** — Arsenal（可选）：httpx 是静态二进制，但通常在攻击机本地使用做 HTTP 探测，不需要投递到目标机 → 跳过。

## 常见错误

- **版本号不同步**：改了 `xxx_Ver` 但忘了改 `xxx_bin_amd64` 里的版本号 → 下载 404。这是最高频的错误
- **写了函数但忘记注册**：安装函数写好了，但没有在 F8X_TOOL_LIST 里添加条目 → `-install xxx` 找不到工具
- **工具名大小写不匹配**：F8X_TOOL_LIST 里工具名是小写（`nuclei|...`），搜索时也用小写匹配，不要写成大写
- **Arsenal case 块缺 `;;`**：bash case 语法必须以 `;;` 结尾，漏了会导致穿透到下一个分支
- **release 文件名变了没跟进**：上游项目改了 release 命名格式（比如从 `_amd64` 变成 `-amd64`），但 f8x 变量还是旧格式

## 参考文件

- `references/install-templates.md` — 四种安装函数模板（含完整代码和内置 helper 说明）
- `references/arsenal-guide.md` — Arsenal 投递物配置指南（含 case 块模板和特殊平台占位符）
