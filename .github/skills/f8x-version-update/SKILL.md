---
name: f8x-version-update
description: 批量检查和更新 f8x 中工具的版本号。当需要检查哪些工具有新版本、更新某个工具的版本、或批量更新版本时使用。即使用户只是说 "检查一下版本"、"xxx 更新了没"、"升级一下工具" 也应触发。
---

# f8x 版本更新

f8x 中所有工具版本都硬编码在脚本顶部（行 93-435），每次上游发布新版本都需要手动更新。这个 skill 指导如何安全地完成版本更新。

## 检查流程

### Step 1: 运行 check_releases.py

```bash
cd /Users/f0x/pte-project/infra-plat/f8x
python3 check_releases.py --file f8x --output diff.txt
```

脚本会扫描 f8x 中所有 `# https://github.com/owner/repo` 注释后面的 `_Ver`/`_Version` 变量，与 GitHub Releases API 对比，输出需要更新的工具列表。

输出格式：
```
owner/repo: v1.0.0 -> v2.0.0 (xxx_Ver) https://github.com/owner/repo/releases/tag/v2.0.0
```

环境变量：
- `GITHUB_TOKEN` — 提高 API 速率限制（建议设置，否则 60 次/小时会很快用完）
- `HTTP_PROXY` / `HTTPS_PROXY` — 代理（脚本默认使用 `--proxy http://127.0.0.1:7890`，可用 `--proxy ""` 禁用）

### Step 2: 人工筛选

**不要盲目更新所有有新版本的工具。** 逐个检查 diff.txt 中的工具，确认：

1. **新 release 是否包含预编译二进制？** 有些项目发布 release 但只打了 tag 没有 assets，或者只有源码包。如果没有二进制，跳过
2. **文件名格式是否变了？** 对比新旧 release 的 asset 文件名，如果命名规则变了（比如 `_amd64` → `-amd64`），安装函数也要同步改
3. **是否有 breaking changes？** 看 release notes，如果 CLI 用法变了可能需要调整安装函数

用 GitHub API 快速拿到 release assets 列表（比打开网页更快更准）：
```bash
curl -s https://api.github.com/repos/OWNER/REPO/releases/latest | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'Tag: {d[\"tag_name\"]}')
for a in d.get('assets',[]): print(f'  {a[\"name\"]}')"
```

如果 diff.txt 里有大量工具需要更新，逐个处理——每个工具走完 Step 2→3→4 的完整循环再开始下一个，不要一口气改完所有再验证，否则出错时很难定位是哪个工具改坏的。

### Step 3: 逐个更新版本变量

确认要更新后，修改 f8x 脚本（行 93-435 区域）。

**首先**，用变量前缀搜索找出该工具的所有关联变量，确认要改几个：
```bash
grep "^httpx_" f8x       # 找出 httpx 的所有版本相关变量
grep "^frp_" f8x         # 找出 frp 的所有版本相关变量
```
这一步能避免"只改了 `_Ver` 忘了改 `_bin_*`"的常见错误。

#### 简单情况：只有 `_Ver`

```bash
# 改前
xxx_Ver="v1.0.0"
# 改后
xxx_Ver="v2.0.0"
```

#### 常见情况：`_Ver` + 关联文件名变量

这是最容易出错的地方。文件名变量里嵌入了版本号，必须全部同步修改：

```bash
# 改前
httpx_Ver="v1.8.1"
httpx_bin_amd64="httpx_1.8.1_linux_amd64.zip"
httpx_bin_arm64="httpx_1.8.1_linux_arm64.zip"

# 改后（注意 _Ver 带 v 前缀，文件名里不带 v）
httpx_Ver="v1.9.0"
httpx_bin_amd64="httpx_1.9.0_linux_amd64.zip"
httpx_bin_arm64="httpx_1.9.0_linux_arm64.zip"
```

#### 复杂情况：`_Ver` + `_File_*` + `_Dir_*`

某些工具（如 frp）解压后目录名也包含版本号：

```bash
# 改前
frp_Ver="v0.67.0"
frp_File_amd64="frp_0.67.0_linux_amd64.tar.gz"
frp_File_arm64="frp_0.67.0_linux_arm64.tar.gz"
frp_Dir_amd64="frp_0.67.0_linux_amd64"
frp_Dir_arm64="frp_0.67.0_linux_arm64"

# 改后 — 4 个变量都要改
frp_Ver="v0.68.0"
frp_File_amd64="frp_0.68.0_linux_amd64.tar.gz"
frp_File_arm64="frp_0.68.0_linux_arm64.tar.gz"
frp_Dir_amd64="frp_0.68.0_linux_amd64"
frp_Dir_arm64="frp_0.68.0_linux_arm64"
```

### Step 4: 验证

更新后做两件事：

1. **语法检查**：`bash -n f8x`
2. **搜索残留旧版本号**：用旧版本号 grep 一下，确认没有遗漏
   ```bash
   grep "1.8.1" f8x  # 用旧版本号搜索，应该没有匹配
   ```

## 关联文件名变量的命名模式

f8x 中关联变量的后缀没有统一标准，以下是实际存在的几种：

| 后缀模式 | 示例 | 含义 |
|----------|------|------|
| `_bin_amd64` / `_bin_arm64` | `httpx_bin_amd64` | 完整文件名（最常见） |
| `_File_amd64` / `_File_arm64` | `frp_File_amd64`, `chisel_File_amd64` | 同上，另一种命名 |
| `_Install_amd64` | `Nuclei_Install_amd64` | 同上，早期命名 |
| `_Dir_amd64` / `_Dir_arm64` | `frp_Dir_amd64` | 解压后的目录名 |

更新某个工具时，先搜索该工具的变量前缀找出所有关联变量：
```bash
grep "^httpx_" f8x       # 找出 httpx 的所有版本相关变量
grep "^frp_" f8x         # 找出 frp 的所有版本相关变量
```

## 版本号格式注意事项

- `_Ver` 变量通常带 `v` 前缀（`v1.0.0`），但文件名中一般不带（`httpx_1.0.0_linux_amd64.zip`）
- 少数工具的 `_Ver` 不带 `v`（如 `Adinfo_Ver="v0.3"` 但 release tag 是 `v0.3`）
- 通过 GitHub Releases 页面的 asset 文件名来确认准确格式，不要猜

## 常见陷阱

- **只改了 `_Ver` 忘了改 `_bin_*`**：下载时 404，因为文件名里还是旧版本号
- **release 没有预编译文件**：有些项目只打 tag 不发布 assets，或只有源码 tarball
- **pre-release 版本**：`check_releases.py` 用的是 `releases/latest` API，不会返回 pre-release，但如果 fallback 到 `tags` 就可能拿到非稳定版
- **文件名格式变更**：上游改了命名规则但没改功能，需要同步修改安装函数中的解压/移动逻辑
- **Arsenal 也用了版本变量**：如果工具在 Arsenal 里有 case 块，检查是否也需要更新

## 关键文件

| 文件 | 作用 |
|------|------|
| `/Users/f0x/pte-project/infra-plat/f8x/f8x` | 主脚本，版本变量在行 93-435 |
| `/Users/f0x/pte-project/infra-plat/f8x/check_releases.py` | 版本检查脚本 |
| `/Users/f0x/pte-project/infra-plat/f8x/f8x_version.sh` | 版本覆盖（可选，用于测试） |
