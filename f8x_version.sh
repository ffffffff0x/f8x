#!/usr/bin/env bash
#set -x

# ===================== Basic variable settings =====================
P_Dir=/pentest
T_Dir=/ffffffff0x
Default_DNS=223.5.5.5
Proxy_URL="https://cdn.ffffffff0x.com/?durl=https://codeload.github.com/rofl0r/proxychains-ng/zip/master"

# ===================== Software version variable setting (dev) =====================
# https://www.ruby-lang.org/en/downloads/
Ruby_Ver="3.0"
Ruby_Dir="ruby-3.0.0"
Ruby_bin="ruby-3.0.0.tar.gz"
# https://go.dev/dl/
Go_Version="go1.18.6"
Go_Bin_amd64="go1.18.6.linux-amd64.tar.gz"
Go_Bin_arm64="go1.18.6.linux-arm64.tar.gz"
# https://nodejs.org/dist/
node_Ver="v17.4.0"
node_bin_amd64="node-v17.4.0-linux-x64.tar.xz"
node_bin_arm64="node-v17.4.0-linux-arm64.tar.xz"
node_Dir_amd64="node-v17.4.0-linux-x64"
node_Dir_arm64="node-v17.4.0-linux-arm64"
# http://nginx.org/en/download.html
nginx_Ver="1.18.0"
nginx_bin="nginx-1.18.0.tar.gz"
# https://www.lua.org/download.html
lua_bin="lua-5.4.3.tar.gz"
lua_dir="lua-5.4.3"
# https://github.com/stedolan/jq/releases
jq_bin="jq-1.6.zip"
jq_dir="jq-1.6"
jq_ver="jq-1.6"
# https://github.com/tsl0922/ttyd/releases
ttyd_Ver="1.7.1"
ttyd_bin_amd64="ttyd.x86_64"
ttyd_bin_arm64="ttyd.arm"
# https://github.com/coder/code-server
code_server_Ver="v4.7.0"
code_server_bin1_amd64="code-server-4.7.1-amd64.rpm"
code_server_bin2_amd64="code-server_4.7.1_amd64.deb"
code_server_bin1_arm64="code-server-4.7.1-arm64.rpm"
code_server_bin2_arm64="code-server_4.7.1_arm64.deb"
# https://www.python.org/downloads/
py37_ver="3.7.12"
py37_bin="Python-3.7.12.tar.xz"
py37_dir="Python-3.7.12"
py38_ver="3.8.12"
py38_bin="Python-3.8.12.tar.xz"
py38_dir="Python-3.8.12"
py39_ver="3.9.8"
py39_bin="Python-3.9.8.tar.xz"
py39_dir="Python-3.9.8"
py310_ver="3.10.4"
py310_bin="Python-3.10.4.tar.xz"
py310_dir="Python-3.10.4"
# https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2FLAST_CHANGE?alt=media
# https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/958422/
chromium_Ver="958422"
# https://phantomjs.org/download.html
phantomjs_bin="phantomjs-2.1.1-linux-x86_64.tar.bz2"
phantomjs_dir="phantomjs-2.1.1-linux-x86_64"

# ===================== Software version variable setting (pentest) =====================
# https://github.com/fatedier/frp/releases
frp_Ver="v0.44.0"
frp_File_amd64="frp_0.44.0_linux_amd64.tar.gz"
frp_File_arm64="frp_0.44.0_linux_arm64.tar.gz"
frp_Dir_amd64="frp_0.44.0_linux_amd64"
frp_Dir_arm64="frp_0.44.0_linux_arm64"
# https://github.com/ehang-io/nps/releases
nps_Ver="v0.26.10"
nps_File_amd64="linux_amd64_server.tar.gz"
nps_File_arm64="linux_arm64_server.tar.gz"
# https://github.com/wikiZ/RedGuard/releases
RedGuard_Ver="22.08.03"
RedGuard_File_amd64="RedGuard_64"
# https://github.com/RustScan/RustScan/releases
RustScan_Version="2.0.1"
RustScan_Install="rustscan_2.0.1_amd64.deb"
# https://github.com/boy-hack/ksubdomain/releases
ksubdomain_Ver="v1.9.5"
ksubdomain_Install="KSubdomain-v1.9.5-linux.tar"
# https://github.com/chaitin/xray/releases
xray_Ver="1.8.4"
xray_File_amd64="xray_linux_amd64.zip"
xray_bin_amd64="xray_linux_amd64"
xray_File_arm64="xray_linux_arm64.zip"
xray_bin_arm64="xray_linux_arm64"
# https://github.com/gobysec/Goby/releases
goby_Ver="Beta1.9.325"
goby_File="goby-linux-x64-1.9.325.zip"
# https://github.com/shadow1ng/fscan/releases
fscan_Ver="1.8.1"
fscan_Install_amd64="fscan_amd64"
fscan_Install_arm64="fscan_arm64"
# https://github.com/ffuf/ffuf/releases
ffuf_Ver="v1.5.0"
ffuf_Install_amd64="ffuf_1.5.0_linux_amd64.tar.gz"
ffuf_Install_arm64="ffuf_1.5.0_linux_arm64.tar.gz"
# https://github.com/projectdiscovery/nuclei/releases
Nuclei_Ver="v2.7.8"
Nuclei_Install_amd64="nuclei_2.7.8_linux_amd64.zip"
Nuclei_Install_arm64="nuclei_2.7.8_linux_arm64.zip"
# https://github.com/Ne0nd0g/merlin/releases
merlin_Ver="v1.5.0"
merlin_Install_amd64="merlinServer-Linux-x64.7z"
merlin_agent_windows="merlinAgent-Windows-x64.7z"
merlin_agent_linux="merlinAgent-Linux-x64.7z"
merlin_agent_darwin="merlinAgent-Darwin-x64.7z"
# https://github.com/chaitin/rad/releases
rad_Ver="0.4"
rad_File_amd64="rad_linux_amd64.zip"
rad_File_arm64="rad_linux_arm64.zip"
# https://github.com/Qianlitp/crawlergo/releases
crawlergo_Ver="v0.4.3"
crawlergo_File_amd64="crawlergo_linux_amd64"
crawlergo_File_arm64="crawlergo_linux_arm64"
# https://github.com/gloxec/CrossC2/releases
CrossC2_Ver="v3.1.0"
# https://github.com/nodauf/Girsh/releases
Girsh_Ver="v0.40"
Girsh_bin_amd64="Girsh_0.40_linux_amd64.tar.gz"
Girsh_bin_arm64="Girsh_0.40_linux_arm64.tar.gz"
# https://github.com/bettercap/bettercap/releases
bettercap_Ver="v2.31.1"
bettercap_bin_amd64="bettercap_linux_amd64_v2.31.1.zip"
bettercap_bin_arm64="bettercap_linux_aarch64_v2.31.1.zip"
# https://github.com/mitmproxy/mitmproxy/releases
mitmproxy_Ver="8.1.1"
mitmproxy_bin="mitmproxy-8.1.1-linux.tar.gz"
# https://github.com/projectdiscovery/naabu/releases
naabu_Ver="v2.1.0"
naabu_bin="naabu_2.1.0_linux_amd64.zip"
# https://github.com/projectdiscovery/proxify/releases
proxify_Ver="v0.0.6"
proxify_bin_amd64="proxify_0.0.6_linux_amd64.zip"
proxify_bin_arm64="proxify_0.0.6_linux_arm64.zip"
# https://github.com/hashcat/hashcat/releases
hashcat_Version="hashcat-6.2.6"
# https://github.com/projectdiscovery/subfinder/releases
subfinder_Ver="v2.5.3"
subfinder_bin_amd64="subfinder_2.5.3_linux_amd64.zip"
subfinder_bin_arm64="subfinder_2.5.3_linux_arm64.zip"
# https://github.com/projectdiscovery/httpx/releases
httpx_Ver="v1.2.4"
httpx_bin_amd64="httpx_1.2.4_linux_amd64.zip"
httpx_bin_arm64="httpx_1.2.4_linux_arm64.zip"
# https://github.com/projectdiscovery/mapcidr/releases
mapcidr_Ver="v1.0.3"
mapcidr_bin_amd64="mapcidr_1.0.3_linux_amd64.tar.gz"
mapcidr_bin_arm64="mapcidr_1.0.3_linux_arm64.tar.gz"
# https://github.com/ffffffff0x/iprange/releases
iprange_Ver="v1.0.1"
iprange_bin_amd64="iprange_1.0.1_linux_amd64.tar.gz"
iprange_bin_arm64="iprange_1.0.1_linux_arm64.tar.gz"
# https://github.com/projectdiscovery/dnsx/releases
dnsx_Ver="v1.1.1"
dnsx_bin_amd64="dnsx_1.1.1_linux_amd64.zip"
dnsx_bin_arm64="dnsx_1.1.1_linux_arm64.zip"
# https://github.com/iBotPeaches/Apktool/releases
apktool_Ver="v2.6.1"
apktool_bin="apktool_2.6.1.jar"
# https://github.com/lc/gau/releases
gau_Ver="v2.1.2"
gau_bin="gau_2.1.2_linux_amd64.tar.gz"
# https://github.com/skylot/jadx/releases
jadx_Ver="v1.4.4"
jadx_bin="jadx-1.4.4.zip"
# https://github.com/qtc-de/remote-method-guesser/releases
rmg_Ver="v4.3.1"
rmg_bin="rmg-4.3.1-jar-with-dependencies.jar"
# https://github.com/No-Github/anew/releases
anew_Ver="v1.0.3"
anew_bin_amd64="anew_1.0.3_linux_amd64.tar.gz"
anew_bin_arm64="anew_1.0.3_linux_arm64.tar.gz"
# https://github.com/zu1k/nali/releases
nali_Ver="v0.5.3"
nali_bin_amd64="nali-linux-amd64-v0.5.3.gz"
nali_bin_arm64="nali-linux-armv8-v0.5.3.gz"
# https://github.com/hahwul/dalfox/releases
dalfox_Ver="v2.8.2"
dalfox_bin_amd64="dalfox_2.8.2_linux_amd64.tar.gz"
dalfox_bin_arm64="dalfox_2.8.2_linux_arm64.tar.gz"
# https://github.com/ffffffff0x/DomainSplit/releases
DomainSplit_Ver="1.0"
# https://github.com/WangYihang/Platypus/releases
Platypus_Ver="v1.5.1"
Platypus_bin_amd64="Platypus_linux_amd64"
Platypus_bin_arm64="Platypus_linux_arm64"
# https://github.com/OWASP/Amass/releases
Amass_Ver="v3.20.0"
Amass_bin_amd64="amass_linux_amd64.zip"
Amass_bin_arm64="amass_linux_arm64.zip"
# https://github.com/OJ/gobuster/releases
gobuster_Ver="v3.2.0"
gobuster_bin_amd64="gobuster_3.2.0_Linux_x86_64.tar.gz"
gobuster_bin_arm64="gobuster_3.2.0_Linux_arm64.tar.gz"
# https://github.com/jaeles-project/gospider/releases
gospider_Ver="v1.1.6"
gospider_bin_amd64="gospider_v1.1.6_linux_x86_64.zip"
gospider_dir_amd64="gospider_v1.1.6_linux_x86_64"
gospider_bin_arm64="gospider_v1.1.6_linux_arm64.zip"
gospider_dir_arm64="gospider_v1.1.6_linux_arm64"
# https://github.com/tomnomnom/unfurl/releases
unfurl_Ver="v0.4.3"
unfurl_Bin="unfurl-linux-amd64-0.4.3.tgz"
# https://github.com/tomnomnom/qsreplace/releases
qsreplace_Ver="v0.0.3"
qsreplace_bin="qsreplace-linux-amd64-0.0.3.tgz"
# https://github.com/jaeles-project/jaeles/releases
jaeles_Ver="beta-v0.17"
jaeles_bin="jaeles-v0.17-linux.zip"
jaeles_sbin="jaeles-v0.17-linux"
# https://github.com/lc/subjs/releases
subjs_Ver="v1.0.1"
subjs_bin="subjs_1.0.1_linux_amd64.tar.gz"
# https://github.com/tomnomnom/assetfinder/releases
assetfinder_Ver="v0.1.1"
assetfinder_bin="assetfinder-linux-amd64-0.1.1.tgz"
# https://github.com/zhzyker/dismap/releases
dismap_Ver="v0.4"
dismap_bin_amd64="dismap-0.4-linux-amd64"
dismap_bin_arm64="dismap-0.4-linux-arm64"
# https://github.com/robhax/gojwtcrack/releases
gojwtcrack_Ver="0.1"
gojwtcrack_bin="gojwtcrack-linux-amd64.gz"
# https://github.com/fofapro/fapro/releases
fapro_Ver="v0.64"
fapro_bin_amd64="fapro_linux_x86_64.tar.gz"
fapro_bin_arm64="fapro_linux_arm64.tar.gz"
# https://github.com/wh1t3p1g/ysomap/releases
ysomap_Ver="v0.1.3"
ysomap_bin="ysomap.jar"
JNDIExploit_Ver="1.1"
JNDIExploit_bin="JNDIExploit.zip"
# https://github.com/shmilylty/netspy/releases
netspy_Ver="v0.0.5"
netspy_bin_amd64="netspy_linux_amd64.zip"
netspy_bin_arm64="netspy_linux_arm64.zip"
# https://github.com/cdk-team/CDK/releases
cdk_Ver="v1.5.0"
cdk_bin_amd64="cdk_linux_amd64"
cdk_bin_arm64="cdk_linux_arm64"
# https://github.com/projectdiscovery/interactsh/releases
interactsh_Ver="v1.0.7"
interactsh_client_bin_amd64="interactsh-client_1.0.7_Linux_x86_64.zip"
interactsh_server_bin_amd64="interactsh-server_1.0.7_Linux_x86_64.zip"
interactsh_client_bin_arm64="interactsh-client_1.0.7_Linux_arm.zip"
interactsh_server_bin_arm64="interactsh-server_1.0.7_Linux_arm.zip"
# https://github.com/BishopFox/sliver/releases
sliver_Ver="v1.5.29"
sliver_bin_Server="sliver-server_linux"
sliver_bin_Client="sliver-client_linux"
# https://github.com/mstxq17/MoreFind/releases
MoreFind_Ver="v1.2.6"
MoreFind_bin_amd64="MoreFind_1.2.6_Linux_x86_64.tar.gz"
MoreFind_bin_arm64="MoreFind_1.2.6_Linux_arm64.tar.gz"
# https://github.com/praetorian-inc/fingerprintx
fingerprintx_Ver="v1.0.1"
fingerprintx_Install_amd64="fingerprintx_1.0.1_linux_amd64.tar.gz"
fingerprintx_Install_arm64="fingerprintx_1.0.1_linux_arm64.tar.gz"
# https://github.com/teamssix/cf
cf_Ver="v0.4.2"
cf_Install_amd64="cf_v0.4.2_linux_amd64.tar.gz"
cf_Install_arm64="cf_v0.4.2_linux_arm64.tar.gz"

# ===================== Software version variable setting (other) =====================
# https://github.com/AdguardTeam/AdGuardHome/releases
AdGuardHome_Version="v0.107.16"
AdGuardHome_File_amd64="AdGuardHome_linux_amd64.tar.gz"
AdGuardHome_File_arm64="AdGuardHome_linux_arm64.tar.gz"
clash_Ver="v1.7.0"
clash_bin="clash-linux-amd64-v1.7.0.gz"
# https://github.com/junegunn/fzf/releases
fzf_Ver="0.34.0"
fzf_bin_amd64="fzf-0.34.0-linux_amd64.tar.gz"
fzf_bin_arm64="fzf-0.34.0-linux_arm64.tar.gz"
# https://github.com/iawia002/lux/releases
lux_Ver="v0.15.0"
lux_bin_amd64="lux_0.15.0_Linux_64-bit.tar.gz"
lux_bin_arm64="lux_0.15.0_Linux_ARM64.tar.gz"
# https://github.com/tomnomnom/gron/releases
gron_Ver="v0.7.1"
gron_bin_amd64="gron-linux-amd64-0.7.1.tgz"
gron_bin_arm64="gron-linux-arm64-0.7.1.tgz"
# https://github.com/abhimanyu003/sttr/releases
sttr_Ver="v0.2.13"
sttr_bin_amd64="sttr_0.2.13_linux_amd64.tar.gz"
sttr_bin_arm64="sttr_0.2.13_linux_arm64.tar.gz"
# https://github.com/sharkdp/bat/releases
bat_Ver="v0.22.1"
bat_bin_amd64="bat-musl_0.22.1_amd64.deb"
bat_bin_arm64="bat-musl_0.22.1_i686.deb"
# https://github.com/muesli/duf/releases
duf_Ver="v0.8.1"
duf_bin1_amd64="duf_0.8.1_linux_amd64.rpm"
duf_bin2_amd64="duf_0.8.1_linux_amd64.deb"
duf_bin1_arm64="duf_0.8.1_linux_arm64.rpm"
duf_bin2_arm64="duf_0.8.1_linux_arm64.deb"
# https://github.com/dalance/procs/releases
procs_Ver="v0.13.2"
procs_bin="procs-v0.13.2-x86_64-linux.zip"
# https://github.com/sharkdp/fd/releases
fd_Ver="v8.4.0"
fd_bin_amd64="fd_8.4.0_amd64.deb"
fd_bin_arm64="fd_8.4.0_arm64.deb"
# https://github.com/hashicorp/terraform/releases
Terraform_Ver="1.3.2"
Terraform_bin_amd64="terraform_1.3.2_linux_amd64.zip"
Terraform_bin_arm64="terraform_1.3.2_linux_arm64.zip"
# https://github.com/aliyun/aliyun-cli/releases
aliyun_cli_Ver="v3.0.128"
aliyun_cli_bin_amd64="aliyun-cli-linux-3.0.128-amd64.tgz"
aliyun_cli_bin_arm64="aliyun-cli-linux-3.0.128-arm64.tgz"
# https://github.com/bcicen/ctop/releases/
ctop_Ver="v0.7.7"
ctop_bin_amd64="ctop-0.7.7-linux-amd64"
ctop_bin_arm64="ctop-0.7.7-linux-arm64"
