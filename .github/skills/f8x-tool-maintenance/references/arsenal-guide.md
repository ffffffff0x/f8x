# Arsenal 投递物配置指南

Arsenal 是 f8x 的多平台二进制投递物构建功能，用于预下载渗透工具的跨平台二进制，便于投递到目标机执行。

## 位置

`Arsenal_Build()` 函数在 f8x 脚本约行 11359，通过 `./f8x -arsenal` 触发。

## 目录结构

```
/pentest/arsenal/
├── fscan/
│   ├── fscan_linux_amd64
│   ├── fscan_linux_arm64
│   └── fscan_windows_amd64.exe
├── chisel/
│   ├── chisel_linux_amd64
│   ├── chisel_linux_arm64
│   └── chisel_windows_amd64.exe
└── ...
```

## ARSENAL_TOOLS 列表

在 `Arsenal_Build()` 函数中的 `ARSENAL_TOOLS` 变量里添加一行：

```
工具名|github_repo|版本变量|文件名模式
```

### 平台占位符

文件名模式中使用占位符，在下载时被自动替换：

| 占位符 | 含义 | 映射规则 |
|--------|------|----------|
| `{PLATFORM}` | 标准平台名 | `linux_amd64` / `linux_arm64` / `windows_amd64` |
| `{K8S_PLATFORM}` | k8spider 专用 | `linux-amd64` / `linux-arm64`（用连字符） |
| `{FRP_PLATFORM}` | frp 专用 | 版本号嵌入目录名的格式 |
| `{CHISEL_PLATFORM}` | chisel 专用 | 大小写和格式特殊映射 |

Windows 文件会自动添加 `.exe` 后缀（如果没有的话）。

标准格式示例（使用 `{PLATFORM}`）：
```
gogo|chainreactors/gogo|${gogo_Ver}|gogo_{PLATFORM}
zombie|chainreactors/zombie|${zombie_Ver}|zombie_{PLATFORM}
cdk|cdk-team/CDK|${cdk_Ver}|cdk_{PLATFORM}
```

## 标准格式 vs 自定义 Case

### 标准格式（默认 `*)` 分支处理）

如果工具的 release 文件名格式就是 `工具名_平台`（如 `gogo_linux_amd64`），只需在 ARSENAL_TOOLS 添加一行，走默认下载逻辑。

### 自定义 Case 块

如果 release 文件名格式非标准，需要在 `case "${tool_name}" in` 中添加分支：

```bash
xxx)
    case "$platform" in
        linux_amd64)   local archive="xxx_${ver}_linux_amd64.tar.gz" ;;
        linux_arm64)   local archive="xxx_${ver}_linux_arm64.tar.gz" ;;
        windows_amd64) local archive="xxx_${ver}_windows_amd64.zip" ;;
    esac
    dl_url="https://github.com/${repo}/releases/download/${ver}/${archive}"
    out_file="xxx_${platform}"
    local tmp_dir="/tmp/arsenal_xxx_${platform}"
    mkdir -p "$tmp_dir"
    $Proxy_OK wget "$dl_url" -O "$tmp_dir/archive" ${wget_option} 2>/dev/null
    cd "$tmp_dir" && tar -xzf archive
    mv "$tmp_dir/xxx" "${tool_dir}/${out_file}"
    chmod +x "${tool_dir}/${out_file}"
    rm -rf "$tmp_dir"
    ;;
```

常见的需要自定义 case 的情况：
- tar.gz/zip 压缩包（frp, chisel, ligolo-ng, peirates, etcdctl, k8spider）
- 非标准文件名（fscan: amd64 版叫 `fscan` 而非 `fscan_linux_amd64`）
- 特殊平台映射（k8spider 使用 `{K8S_PLATFORM}` 连字符格式）
- Windows-only 工具（GodPotato, mimikatz, SharpHound 等）

当前已有自定义 case 的工具：fscan, frpc, chisel, k8spider, ingressnightmare, peirates, etcdctl, iox, ligolo-agent。

## 平台约定

默认下载 3 个平台：`linux_amd64 linux_arm64 windows_amd64`

特殊情况处理：
- **Windows-only 工具**（GodPotato, mimikatz, SharpHound, winPEAS, PrintSpoofer, SharpWMI, SharPersist, StandIn）：非 windows 平台输出 `⏭️ (windows only)`
- **Linux-only 工具**（peirates, cdk）：windows 平台输出 `⏭️ (no windows build)`

## 新增 Arsenal 工具 Checklist

1. [ ] 确认工具有 GitHub Releases 页面且提供预编译二进制
2. [ ] 确认版本变量已在 f8x 顶部定义（`xxx_Ver="v1.0"`）
3. [ ] 在 `ARSENAL_TOOLS` 中添加一行
4. [ ] 检查 release 文件名格式：标准 → 用 `{PLATFORM}`，非标准 → 添加自定义 case 块
5. [ ] 如需特殊平台占位符，确认映射逻辑正确
6. [ ] 运行 `./f8x -arsenal` 测试下载
7. [ ] 确认 3 个平台的二进制都成功下载到 `/pentest/arsenal/xxx/`
