#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Hermes 微信部署 — 一键安装脚本
# 5 分钟在微信部署你自己的 AI 助手
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════╗"
    echo "║   🤖 Hermes 微信 AI 助手 — 一键部署     ║"
    echo "║   5 分钟在微信拥有你的专属 AI 助手        ║"
    echo "╚══════════════════════════════════════════╝"
    echo -e "${NC}"
}

info()  { echo -e "${CYAN}[*]${NC} $*"; }
ok()    { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
err()   { echo -e "${RED}[✗]${NC} $*"; exit 1; }

PROFILE_NAME="${1:-hermes}"

banner

# ── Step 1: Prerequisites ──────────────────────────────────
echo ""
info "Step 1/6: 检查环境..."

# Python
if command -v python3 &>/dev/null; then
    PY=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
    if [ "$(echo "$PY >= 3.11" | bc 2>/dev/null || echo 0)" = "1" ] || \
       [ "$(printf '%s\n' "3.11" "$PY" | sort -V | head -1)" = "3.11" ]; then
        ok "Python $PY ✓"
    else
        err "需要 Python >= 3.11，当前: $PY"
    fi
else
    err "未找到 Python3，请先安装"
fi

# pip
python3 -m pip --version &>/dev/null || err "pip 未安装"

# OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    ok "系统: $NAME"
fi

# ── Step 2: Install Hermes Agent ───────────────────────────
echo ""
info "Step 2/6: 安装 Hermes Agent..."

# Check if hermes is already installed
if command -v hermes &>/dev/null; then
    ok "Hermes Agent 已安装: $(hermes --version 2>&1 | head -1)"
else
    info "正在安装 Hermes Agent（首次安装约 2-3 分钟）..."
    pip install hermes-agent 2>/dev/null || {
        warn "pip 安装失败，尝试从 GitHub 安装..."
        pip install git+https://github.com/NousResearch/hermes-agent.git || {
            err "安装失败。请手动安装: pip install hermes-agent"
        }
    }
    ok "Hermes Agent 安装完成"
fi

# ── Step 3: Configure API Key ──────────────────────────────
echo ""
info "Step 3/6: 配置 API Key..."

ENV_FILE="$HOME/.hermes/profiles/${PROFILE_NAME}/.env"

# Check if API key is already set
if [ -f "$ENV_FILE" ] && grep -q "DEEPSEEK_API_KEY" "$ENV_FILE" 2>/dev/null; then
    ok "API Key 已配置"
else
    echo ""
    echo -e "  ${YELLOW}需要 DeepSeek API Key${NC}"
    echo "  获取地址: https://platform.deepseek.com/api_keys"
    echo ""
    read -r -p "  请输入你的 DeepSeek API Key: " API_KEY

    if [ -z "$API_KEY" ]; then
        err "API Key 不能为空"
    fi

    mkdir -p "$(dirname "$ENV_FILE")"
    cat > "$ENV_FILE" <<EOF
# DeepSeek API Key
DEEPSEEK_API_KEY=${API_KEY}

# 微信配置（onboard.py 会自动填入以下内容）
WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
WEIXIN_DM_POLICY=open
WEIXIN_ALLOW_ALL_USERS=true
WEIXIN_HOME_CHANNEL=
WEIXIN_ACCOUNT_ID=
WEIXIN_TOKEN=
WEIXIN_BASE_URL=
EOF
    ok "API Key 已保存"
fi

# ── Step 4: Create Profile ─────────────────────────────────
echo ""
info "Step 4/6: 创建 Profile..."

if hermes profile list 2>/dev/null | grep -q "$PROFILE_NAME"; then
    ok "Profile '${PROFILE_NAME}' 已存在"
else
    hermes profile create "$PROFILE_NAME" 2>/dev/null || {
        # Fallback: manually create profile dirs
        PROFILE_DIR="$HOME/.hermes/profiles/${PROFILE_NAME}"
        mkdir -p "$PROFILE_DIR"/{home/.hermes/weixin/accounts,skills,cron,cache/images}
        ok "Profile '${PROFILE_NAME}' 已创建"
    }
fi

# ── Step 5: Copy Skills ────────────────────────────────────
echo ""
info "Step 5/6: 安装技能包..."

SKILLS_SRC="$(dirname "$0")/skills"
SKILLS_DST="$HOME/.hermes/profiles/${PROFILE_NAME}/skills"

if [ -d "$SKILLS_SRC" ]; then
    cp -r "$SKILLS_SRC"/* "$SKILLS_DST"/ 2>/dev/null || true
    ok "技能包已安装"
else
    warn "未找到技能包（skills/ 目录不存在），已跳过"
fi

# ── Step 6: WeChat Onboarding ──────────────────────────────
echo ""
info "Step 6/6: 微信扫码接入..."

ONBOARD_PY="$(dirname "$0")/onboard.py"

if [ ! -f "$ONBOARD_PY" ]; then
    warn "未找到 onboard.py，跳过微信接入"
    echo ""
    echo "  稍后运行: python3 onboard.py $PROFILE_NAME"
else
    echo ""
    echo -e "  ${YELLOW}即将生成微信二维码，请准备扫码${NC}"
    echo "  (二维码 35 秒过期，脚本会自动刷新)"
    echo ""
    read -r -p "  按 Enter 继续..."

    python3 -u "$ONBOARD_PY" "$PROFILE_NAME"
fi

# ── Done ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🎉 部署完成！                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo "  微信扫码后，发消息试试:"
echo "    你好"
echo "    帮我查天气"
echo "    P图：去掉这张照片的背景"
echo ""
echo "  管理命令:"
echo "    hermes profile list              查看 Profiles"
echo "    hermes gateway run --profile ${PROFILE_NAME} &  启动网关"
echo "    hermes cronjob list              查看定时任务"
echo ""
