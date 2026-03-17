# f8x AI 友好化工具安装改造设计文档

## 1. 问题背景

f8x 是一个 10,000+ 行的 bash 脚本，包含 119 个 `Pentest_*_Install` 安装函数，但只有约 20 个工具通过独立 CLI flag（如 `-nmap`、`-python3`）暴露给用户。

**核心问题**：nuclei、masscan、httpx、ffuf、sqlmap 等最常用渗透工具没有独立安装选项，只能通过套件批量安装（`-ka`/`-kb`/`-kc`/`-kd`），每个套件包含 14-38 个工具。

当 AI Agent（如 RedC、Kitsune 的自动部署助手）尝试安装单个工具时：
1. Agent 尝试 `./f8x -nuclei` → 失败（无此 flag）
2. Agent 不知道 nuclei 属于 `-kb` 套件
3. 即使知道，执行 `-kb` 也会安装 27 个不相关工具，浪费时间和带宽

## 2. 解决方案架构

### 2.1 工具映射表 `F8X_TOOL_LIST`

**位置**：f8x 脚本中，所有 Install 函数定义之后、Main() 函数之前

**格式**：管道分隔的字符串变量（不用 `declare -A` 关联数组，因为 macOS 默认 bash 3.2 不支持）

```bash
F8X_TOOL_LIST="
nuclei|Pentest_Nuclei_Install|0
nmap|Pentest_nmap_Install|0
masscan|Pentest_masscan_Install|0
httpx|Pentest_httpx_Install|0
sqlmap|Pentest_sqlmap_Install|1
..."
```

每行三个字段：
- **工具名**：小写，用于 `-install` 和 `--search` 匹配
- **安装函数名**：对应脚本中的 bash 函数
- **依赖等级**：0=基础（wget 下载二进制）、1=需 Python、2=需 Go、3=需 Python+Go

当前共 117 个工具条目。

### 2.2 三个新命令

#### `-install <工具名>` — 精确安装单个工具

```bash
F8x_Install_Tool(){
    local tool_name=$(echo "$1" | tr 'A-Z' 'a-z')
    local entry=$(echo "$F8X_TOOL_LIST" | grep "^${tool_name}|" | head -1)
    
    if [ -z "$entry" ]; then
        # 未找到精确匹配，自动执行模糊搜索给出建议
        F8x_Search_Tool "$1"
        return 1
    fi
    
    local func=$(echo "$entry" | cut -d'|' -f2)
    local dep_level=$(echo "$entry" | cut -d'|' -f3)
    
    # 根据依赖等级自动安装前置环境
    case $dep_level in
        1) Py_Check ;;
        2) GO_Check ;;
        3) Py_Check; GO_Check ;;
    esac
    
    # 调用对应的安装函数
    $func
}
```

**关键设计**：找不到精确匹配时自动触发模糊搜索，帮助 AI Agent 发现正确的工具名。

#### `--list-tools [json|table]` — 输出工具目录

- **JSON 模式**（默认）：输出 JSON 数组，供 AI Agent 程序化解析
- **table 模式**：输出人类可读的对齐表格

#### `--search <关键词>` — 模糊搜索

按工具名进行大小写不敏感的 grep 匹配，输出匹配结果和安装命令提示。

### 2.3 无 root 拦截

`--list-tools` 和 `--search` 是只读操作，不需要 root 权限。

在 `Main()` 函数调用之前（Main 包含 root 检查），扫描命令行参数，如果匹配到这两个命令则直接执行并 `exit 0`：

```bash
# Main() 函数定义结束后、调用前
for _arg in "$@"; do
    case $_arg in
        --list-tools) ... ; exit 0 ;;
        --search) ... ; exit 0 ;;
    esac
done

Main    # 这里才执行 root 检查
Banner
```

### 2.4 参数传递机制（重要）

f8x 的主循环是 `for cmd in $@`，**不支持 `shift`**。

解决方案：使用标志变量延迟消费下一个参数

```bash
_f8x_install_next=0
_f8x_search_next=0
_f8x_list_next=0

for cmd in $@
do
    # 在循环顶部检查标志
    if [ $_f8x_install_next -eq 1 ]; then
        _f8x_install_next=0
        F8x_Install_Tool "$cmd"
        continue
    fi
    # ... 类似处理 search 和 list
    
    case $cmd in
        -install)
            _f8x_install_next=1
            ;;
        # ... 其他 case
    esac
done

# 循环结束后处理未消费的尾部参数
if [ $_f8x_install_next -eq 1 ]; then
    echo "Error: -install requires a tool name"
fi
```

## 3. 文件变更清单

| 文件 | 变更说明 |
|------|----------|
| `f8x` | 新增 F8X_TOOL_LIST（~120行）、F8x_Install_Tool/F8x_List_Tools/F8x_Search_Tool 函数、早期拦截逻辑、for 循环 case 分支、尾部参数处理、帮助文本 |
| `README.md` | 新增 AI-Friendly Tool Management 章节 |
| `README.zh-cn.md` | 新增 AI 友好工具管理章节 |

## 4. 与 RedC/Kitsune 的集成

### RedC 侧变更

1. **`mod/ai/prompt.go` DeployAgentSystemPrompt**：Step 5.1 引导 Agent 使用 `./f8x --search` 和 `./f8x -install` 替代旧的套件安装
2. **`mod/ai/prompt.go` AgentSystemPrompt**：工作原则 7 更新为引导使用 `-install` 和 `--search`
3. **`templates/userdata-templates/f8x-bash/case.json`**：描述更新为 117 工具 + 新命令

### AI Agent 预期使用流程

```
用户: 帮我在 AWS 服务器上安装 nuclei
Agent:
  1. list_userdata_templates → 发现 f8x-bash 模板
  2. exec_userdata(template_name='f8x-bash') → 安装 f8x
  3. exec_command('./f8x --search nuclei') → 确认工具存在
  4. exec_command('./f8x -install nuclei') → 精确安装
  5. exec_command('nuclei -version') → 验证安装
```

## 5. 维护指南

### 添加新工具

1. 在 f8x 中编写 `Pentest_NewTool_Install()` 函数
2. 在 `F8X_TOOL_LIST` 变量中添加一行：`newtool|Pentest_NewTool_Install|<dep_level>`
3. 工具名用小写，与 `-install` 匹配时会自动转小写

### 依赖等级判断

- 如果安装函数里有 `pip install` / `python` 调用 → dep_level 含 1
- 如果安装函数里有 `go install` / `go build` 调用 → dep_level 含 2
- 如果两者都有 → dep_level = 3
- 否则 → dep_level = 0

### 测试验证

```bash
# 语法检查
bash -n f8x

# 功能测试（不需要 root）
bash f8x --list-tools | python3 -m json.tool > /dev/null  # JSON 有效性
bash f8x --list-tools | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"  # 工具计数
bash f8x --search nuclei  # 搜索测试
bash f8x --list-tools table | head  # 表格输出

# 安装测试（需要 root，Linux 环境）
sudo bash f8x -install nuclei
```

## 6. 已知限制

- f8x 实际只在 Linux 上运行（`Main()` 中有 `mac_Check` 退出），但 `--list-tools` 和 `--search` 在任何平台可用
- `-install` 仍需 root 权限（因为安装函数需要写入 `/usr/local/bin` 等系统目录）
- 工具映射表需要手动维护，添加新安装函数后需同步更新 `F8X_TOOL_LIST`
