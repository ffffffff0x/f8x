# 安装函数模板

## 模板 A：GitHub Release 裸二进制下载

适用于：Go/Rust 静态编译工具，release 直接提供裸二进制文件（不是压缩包）。

```bash
Pentest_xxx_Install(){
    name="xxx"
    which xxx > /dev/null 2>&1
    if [ $? == 0 ]; then
        Echo_ALERT "$name installed"
    else
        case $Linux_architecture_Name in
            *"linux-x86_64"*)  xxx_arch="linux_amd64" ;;
            *"linux-arm64"*)   xxx_arch="linux_arm64" ;;
            *)                 xxx_arch="linux_amd64" ;;
        esac
        $Proxy_OK wget ${GitProxy}https://github.com/AUTHOR/REPO/releases/download/${xxx_Ver}/xxx_${xxx_arch} \
            -O /usr/local/bin/xxx ${wget_option} 2>/dev/null || Echo_ERROR2
        chmod +x /usr/local/bin/xxx
        which xxx > /dev/null 2>&1 && Echo_INFOR "Successfully installed $name $xxx_Ver" || Echo_ERROR3
    fi
}
```

## 模板 A2：GitHub Release 压缩包下载（用预定义 bin 变量）

适用于：release 是 tar.gz/zip 压缩包的工具。这是 f8x 中更常见的模式——在顶部预定义文件名变量，安装函数中直接引用。

**顶部版本变量**（行 93-435）：
```bash
# https://github.com/AUTHOR/REPO/releases
xxx_Ver="v1.0.0"
xxx_bin_amd64="xxx_1.0.0_linux_amd64.tar.gz"
xxx_bin_arm64="xxx_1.0.0_linux_arm64.tar.gz"
```

**安装函数**：
```bash
Pentest_xxx_Install(){
    name="xxx"
    which xxx > /dev/null 2>&1
    if [ $? == 0 ]; then
        Echo_ALERT "$name installed"
    else
        case $Linux_architecture_Name in
            *"linux-x86_64"*)  xxx_bin="${xxx_bin_amd64}" ;;
            *"linux-arm64"*)   xxx_bin="${xxx_bin_arm64}" ;;
            *)                 xxx_bin="${xxx_bin_amd64}" ;;
        esac
        local tmp_dir="/tmp/xxx_install"
        mkdir -p "$tmp_dir"
        $Proxy_OK wget ${GitProxy}https://github.com/AUTHOR/REPO/releases/download/${xxx_Ver}/${xxx_bin} \
            -O "$tmp_dir/${xxx_bin}" ${wget_option} 2>/dev/null || Echo_ERROR2
        cd "$tmp_dir" && tar -xzf "${xxx_bin}"  # 或 unzip
        mv "$tmp_dir/xxx" /usr/local/bin/xxx
        chmod +x /usr/local/bin/xxx
        rm -rf "$tmp_dir"
        which xxx > /dev/null 2>&1 && Echo_INFOR "Successfully installed $name $xxx_Ver" || Echo_ERROR3
    fi
}
```

更新版本时，`xxx_Ver` 和 `xxx_bin_amd64`/`xxx_bin_arm64` 中的版本号都要同步改。

## 模板 B：Git Clone + Pip（Python PoC/工具集）

适用于：GitHub 上的 Python 工具，需要 clone 整个仓库并安装依赖。

```bash
Pentest_xxx_Install(){
    name="xxx"
    dir="$P_Dir/xxx"    # 默认 /pentest/xxx
    if test -d $dir; then
        Echo_ALERT "$name is already installed in $dir"
    else
        $Proxy_OK git clone --depth 1 ${GitProxy}https://github.com/AUTHOR/REPO.git $dir \
            > /dev/null 2>&1 && Echo_INFOR "Downloaded $name in the $dir" || Echo_ERROR "Failed"
        cd $dir && Install_Switch7 "requirements.txt" 2>/dev/null
        chmod +x $dir/xxx.py 2>/dev/null
        ln -sf $dir/xxx.py /usr/local/bin/xxx 2>/dev/null
    fi
}
```

## 模板 C：Pip Install（PyPI 包）

适用于：已发布到 PyPI 的 Python 包。

```bash
Pentest_xxx_Install(){
    name="xxx"
    which xxx > /dev/null 2>&1
    if [ $? == 0 ]; then
        Echo_ALERT "$name installed"
    else
        Install_Switch8 "xxx"
        which xxx > /dev/null 2>&1 && Echo_INFOR "Successfully installed $name via pip" || Echo_ERROR3
    fi
}
```

也可以用更直接的写法：
```bash
pip3 install xxx 2>/dev/null || pip install xxx 2>/dev/null || Echo_ERROR2
```

## 内置 Helper 函数速查

这些函数由 f8x 自身提供，安装函数中直接调用即可：

| Helper | 作用 | 示例 |
|--------|------|------|
| `Install_Switch7 "文件名"` | 用 pip3/pip 安装 requirements.txt | `Install_Switch7 "requirements.txt"` |
| `Install_Switch8 "包名"` | pip install 单个包（兼容新版 pip 的 `--break-system-packages`） | `Install_Switch8 "certipy-ad"` |
| `Install_Switch "apt包名"` | apt install | `Install_Switch "tcpdump"` |
| `Echo_ALERT "msg"` | 黄色提示（工具已安装等） | |
| `Echo_INFOR "msg"` | 绿色成功信息 | |
| `Echo_ERROR "msg"` | 红色自定义错误 | |
| `Echo_ERROR2` | 红色下载失败 | |
| `Echo_ERROR3` | 红色安装后 which 检查失败 | |

## 全局变量速查

| 变量 | 含义 | 默认值 |
|------|------|--------|
| `$P_Dir` | 渗透工具安装根目录 | `/pentest` |
| `$T_Dir` | f8x 自身数据目录 | `/ffffffff0x` |
| `$Proxy_OK` | 代理前缀（`proxychains4` 或空） | 空 |
| `${GitProxy}` | GitHub 镜像加速前缀 | 空 |
| `$Linux_architecture_Name` | 系统架构标识 | `linux-x86_64` 或 `linux-arm64` |
| `${wget_option}` | wget 静默选项 | `-q --show-progress` |
