#!/bin/bash

###############################################################################
# DRF Vue 项目服务器快速配置脚本
# 用途：在 Ubuntu/Debian 服务器上快速配置部署环境
# 使用方法：sudo bash setup_server.sh
###############################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    log_error "请使用 sudo 运行此脚本"
    exit 1
fi

log_info "开始配置 DRF Vue 项目服务器..."

###############################################################################
# 1. 系统更新和基础软件安装
###############################################################################
log_info "步骤 1/8: 更新系统和安装基础软件..."

apt update && apt upgrade -y
apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    nginx \
    git \
    rsync \
    curl \
    wget \
    build-essential \
    libpq-dev \
    postgresql \
    postgresql-contrib

log_info "基础软件安装完成"

###############################################################################
# 2. 创建目录结构
###############################################################################
log_info "步骤 2/8: 创建项目目录结构..."

mkdir -p /home/DRF_VUE/drf_vue/backend
mkdir -p /home/front
mkdir -p /var/log/gunicorn

# 设置权限
chown -R www-data:www-data /var/log/gunicorn
chmod -R 755 /var/log/gunicorn

log_info "目录结构创建完成"

###############################################################################
# 3. 配置 PostgreSQL 数据库（可选）
###############################################################################
log_info "步骤 3/8: 配置 PostgreSQL 数据库..."

read -p "是否需要配置 PostgreSQL 数据库？(y/n): " setup_db

if [ "$setup_db" = "y" ] || [ "$setup_db" = "Y" ]; then
    # 启动 PostgreSQL
    systemctl enable postgresql
    systemctl start postgresql
    
    # 创建数据库和用户
    read -p "请输入数据库名称 (默认: drf_vue_db): " db_name
    db_name=${db_name:-drf_vue_db}
    
    read -p "请输入数据库用户名 (默认: drf_vue_user): " db_user
    db_user=${db_user:-drf_vue_user}
    
    read -s -p "请输入数据库密码: " db_password
    echo
    
    # 创建用户和数据库
    su - postgres -c "psql -c \"CREATE USER ${db_user} WITH PASSWORD '${db_password}';\""
    su - postgres -c "psql -c \"CREATE DATABASE ${db_name} OWNER ${db_user};\""
    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${db_name} TO ${db_user};\""
    
    log_info "PostgreSQL 配置完成"
    log_info "数据库: ${db_name}"
    log_info "用户: ${db_user}"
else
    log_warn "跳过 PostgreSQL 配置"
fi

###############################################################################
# 4. 配置 Gunicorn systemd 服务
###############################################################################
log_info "步骤 4/8: 配置 Gunicorn 服务..."

cat > /etc/systemd/system/drf_vue_backend.service << 'EOF'
[Unit]
Description=DRF Vue Backend Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/DRF_VUE/drf_vue/backend
Environment="PATH=/home/DRF_VUE/drf_vue/backend/venv/bin"
ExecStart=/home/DRF_VUE/drf_vue/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8001 \
    --timeout 300 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    config.wsgi:application

Restart=on-failure
RestartSec=5s
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd
systemctl daemon-reload
systemctl enable drf_vue_backend

log_info "Gunicorn 服务配置完成"

###############################################################################
# 5. 配置 Nginx
###############################################################################
log_info "步骤 5/8: 配置 Nginx..."

# 备份现有配置
if [ -f /etc/nginx/nginx.conf ]; then
    cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d%H%M%S)
    log_info "已备份原有 Nginx 配置"
fi

read -p "是否有自定义的 nginx.conf 文件路径？(直接回车跳过，使用默认配置): " nginx_conf_path

if [ -n "$nginx_conf_path" ] && [ -f "$nginx_conf_path" ]; then
    cp "$nginx_conf_path" /etc/nginx/nginx.conf
    log_info "已应用自定义 Nginx 配置"
else
    log_warn "使用默认 Nginx 配置，请手动上传项目的 nginx.conf 文件"
fi

# 测试 Nginx 配置
nginx -t && log_info "Nginx 配置测试通过" || log_error "Nginx 配置测试失败"

# 重启 Nginx
systemctl restart nginx
systemctl enable nginx

log_info "Nginx 配置完成"

###############################################################################
# 6. 配置防火墙
###############################################################################
log_info "步骤 6/8: 配置防火墙..."

if command -v ufw &> /dev/null; then
    ufw allow 22/tcp   # SSH
    ufw allow 80/tcp   # HTTP
    ufw allow 443/tcp  # HTTPS
    ufw --force enable
    log_info "防火墙配置完成"
else
    log_warn "UFW 未安装，跳过防火墙配置"
fi

###############################################################################
# 7. 创建部署用户（可选）
###############################################################################
log_info "步骤 7/8: 创建部署用户..."

read -p "是否创建专用的部署用户？(y/n): " create_deploy_user

if [ "$create_deploy_user" = "y" ] || [ "$create_deploy_user" = "Y" ]; then
    read -p "请输入部署用户名 (默认: deployer): " deploy_user
    deploy_user=${deploy_user:-deployer}
    
    if ! id "$deploy_user" &>/dev/null; then
        adduser --disabled-password --gecos "" "$deploy_user"
        usermod -aG sudo "$deploy_user"
        usermod -aG www-data "$deploy_user"
        
        # 设置目录权限
        chown -R "$deploy_user":"$deploy_user" /home/DRF_VUE
        chown -R "$deploy_user":"$deploy_user" /home/front
        
        log_info "部署用户 '${deploy_user}' 创建完成"
        log_info "请记得设置密码: sudo passwd $deploy_user"
    else
        log_warn "用户 '$deploy_user' 已存在"
    fi
else
    log_warn "跳过部署用户创建"
fi

###############################################################################
# 8. 生成 SSH 密钥对（用于 GitHub Actions）
###############################################################################
log_info "步骤 8/8: 生成 SSH 密钥对..."

read -p "是否为 GitHub Actions 生成 SSH 密钥对？(y/n): " generate_ssh

if [ "$generate_ssh" = "y" ] || [ "$generate_ssh" = "Y" ]; then
    SSH_KEY_DIR="/root/.ssh/github_actions"
    mkdir -p "$SSH_KEY_DIR"
    
    ssh-keygen -t ed25519 -C "github-actions@drf-vue" -f "$SSH_KEY_DIR/deploy_key" -N ""
    
    # 添加公钥到 authorized_keys
    cat "$SSH_KEY_DIR/deploy_key.pub" >> /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
    
    log_info "SSH 密钥对生成完成"
    log_info "私钥位置: $SSH_KEY_DIR/deploy_key"
    log_info "请将以下内容添加到 GitHub Secrets (SSH_PRIVATE_KEY):"
    echo "----------------------------------------"
    cat "$SSH_KEY_DIR/deploy_key"
    echo "----------------------------------------"
    log_warn "请妥善保管私钥，不要泄露！"
else
    log_warn "跳过 SSH 密钥生成"
fi

###############################################################################
# 完成
###############################################################################
echo
log_info "=========================================="
log_info "服务器配置完成！"
log_info "=========================================="
echo
log_info "后续步骤："
echo "1. 在 GitHub 仓库中配置 Secrets（参考 .github/DEPLOYMENT_GUIDE.md）"
echo "2. 上传项目代码到服务器或使用 GitHub Actions 自动部署"
echo "3. 配置后端环境变量文件: /home/DRF_VUE/drf_vue/backend/.env"
echo "4. 执行数据库迁移: cd /home/DRF_VUE/drf_vue/backend && python manage.py migrate"
echo "5. 收集静态文件: python manage.py collectstatic --noinput"
echo "6. 启动服务: systemctl start drf_vue_backend"
echo
log_info "常用命令："
echo "  查看后端状态: systemctl status drf_vue_backend"
echo "  查看 Nginx 状态: systemctl status nginx"
echo "  查看后端日志: tail -f /var/log/gunicorn/error.log"
echo "  查看 Nginx 日志: tail -f /var/log/nginx/error.log"
echo
log_info "祝部署顺利！🚀"
echo
