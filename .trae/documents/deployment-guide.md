# Django + Vue CMS 项目部署教程

## 目录

1. [服务器准备](#1-服务器准备)
2. [环境配置](#2-环境配置)
3. [后端部署](#3-后端部署)
4. [前端部署](#4-前端部署)
5. [Nginx 配置](#5-nginx-配置)
6. [进程管理](#6-进程管理)
7. [HTTPS 配置](#7-https-配置可选)
8. [常见问题](#8-常见问题)

---

## 1. 服务器准备

### 1.1 推荐配置

| 配置项 | 最低配置 | 推荐配置 |
|--------|----------|----------|
| CPU | 1核 | 2核+ |
| 内存 | 1GB | 2GB+ |
| 硬盘 | 20GB | 50GB+ |
| 系统 | Ubuntu 20.04/22.04 | Ubuntu 22.04 |

### 1.2 更新系统

```bash
# 更新软件包列表
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git vim ufw
```

### 1.3 配置防火墙

```bash
# 开放必要端口
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw allow 8001    # Django（可选，仅调试用）

# 启用防火墙
sudo ufw enable
```

---

## 2. 环境配置

### 2.1 安装 Python 3

```bash
# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 2.2 安装 Node.js

```bash
# 使用 NodeSource 安装 Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version
npm --version

# 安装 pnpm（可选，推荐）
npm install -g pnpm
```

### 2.3 安装 Nginx

```bash
# 安装 Nginx
sudo apt install -y nginx

# 启动并设置开机自启
sudo systemctl start nginx
sudo systemctl enable nginx

# 验证安装
nginx -v
```

### 2.4 安装 MySQL（可选，推荐生产环境使用）

```bash
# 安装 MySQL
sudo apt install -y mysql-server mysql-client

# 启动并设置开机自启
sudo systemctl start mysql
sudo systemctl enable mysql

# 安全配置
sudo mysql_secure_installation

# 创建数据库和用户
sudo mysql -u root -p
```

```sql
-- 在 MySQL 命令行中执行
CREATE DATABASE cms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cms_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON cms_db.* TO 'cms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2.5 安装 Redis（可选，用于缓存）

```bash
# 安装 Redis
sudo apt install -y redis-server

# 启动并设置开机自启
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

---

## 3. 后端部署

### 3.1 创建项目目录

```bash
# 创建项目目录
sudo mkdir -p /var/www/cms
sudo chown -R $USER:$USER /var/www/cms

# 进入项目目录
cd /var/www/cms
```

### 3.2 上传代码

**方式一：使用 Git（推荐）**

```bash
# 克隆代码
git clone https://github.com/your-username/your-repo.git .

# 或者从私有仓库克隆
git clone https://username:token@github.com/your-username/your-repo.git .
```

**方式二：使用 SCP 上传**

```bash
# 在本地机器上执行
scp -r /path/to/drf_vue/* user@your-server-ip:/var/www/cms/
```

### 3.3 创建虚拟环境

```bash
# 进入后端目录
cd /var/www/cms/backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Gunicorn
pip install gunicorn
```

### 3.4 配置环境变量

```bash
# 创建 .env 文件
vim .env
```

```env
# Django 配置
DJANGO_SECRET_KEY=your-super-secret-key-change-this-in-production
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# 数据库配置（如果使用 MySQL）
DB_ENGINE=django.db.backends.mysql
DB_NAME=cms_db
DB_USER=cms_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=3306

# JWT 配置
JWT_ACCESS_TOKEN_LIFETIME_HOURS=2
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# CORS 允许的域名
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 3.5 配置 MySQL（如果使用 MySQL）

修改 `backend/config/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'cms_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

安装 MySQL 客户端库：

```bash
pip install mysqlclient
```

### 3.6 初始化数据库

```bash
# 确保在虚拟环境中
cd /var/www/cms/backend
source venv/bin/activate

# 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

### 3.7 创建初始化脚本

```bash
# 创建初始化脚本
vim /var/www/cms/backend/init_data.py
```

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.roles.models import Permission, Role
from apps.users.models import User

def create_permissions():
    permissions_data = [
        {'name': '查看内容', 'code': 'content.view'},
        {'name': '创建内容', 'code': 'content.create'},
        {'name': '编辑内容', 'code': 'content.edit'},
        {'name': '删除内容', 'code': 'content.delete'},
        {'name': '发布内容', 'code': 'content.publish'},
        {'name': '查看用户', 'code': 'user.view'},
        {'name': '创建用户', 'code': 'user.create'},
        {'name': '编辑用户', 'code': 'user.edit'},
        {'name': '删除用户', 'code': 'user.delete'},
        {'name': '管理角色', 'code': 'role.manage'},
        {'name': '管理权限', 'code': 'permission.manage'},
        {'name': '管理分类', 'code': 'category.manage'},
        {'name': '管理标签', 'code': 'tag.manage'},
        {'name': '管理媒体', 'code': 'media.manage'},
        {'name': '管理评论', 'code': 'comment.manage'},
    ]
    
    for perm_data in permissions_data:
        Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults={'name': perm_data['name']}
        )
    print('权限创建完成')

def create_roles():
    admin_role, _ = Role.objects.get_or_create(
        code='admin',
        defaults={'name': '管理员', 'description': '系统管理员，拥有所有权限'}
    )
    
    editor_role, _ = Role.objects.get_or_create(
        code='editor',
        defaults={'name': '编辑', 'description': '内容编辑，可以管理内容'}
    )
    
    user_role, _ = Role.objects.get_or_create(
        code='user',
        defaults={'name': '普通用户', 'description': '普通用户，基本权限'}
    )
    
    # 给管理员角色分配所有权限
    admin_role.permissions.set(Permission.objects.all())
    
    # 给编辑角色分配内容相关权限
    editor_perms = Permission.objects.filter(code__startswith='content')
    editor_role.permissions.set(editor_perms)
    
    print('角色创建完成')

if __name__ == '__main__':
    create_permissions()
    create_roles()
```

```bash
# 运行初始化脚本
python init_data.py
```

---

## 4. 前端部署

### 4.1 配置环境变量

```bash
# 创建前端环境变量文件
vim /var/www/cms/frontend/.env.production
```

```env
VITE_API_BASE_URL=https://your-domain.com/api
```

### 4.2 安装依赖并构建

```bash
# 进入前端目录
cd /var/www/cms/frontend

# 安装依赖
npm install
# 或使用 pnpm
# pnpm install

# 构建生产版本
npm run build
```

### 4.3 预览构建结果

```bash
# 构建完成后，静态文件在 dist 目录
ls -la dist/

# 可以使用 serve 预览（可选）
npm install -g serve
serve -s dist -p 3000
```

---

## 5. Nginx 配置

### 5.1 创建 Nginx 配置文件

```bash
# 创建配置文件
sudo vim /etc/nginx/sites-available/cms
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com your-server-ip;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml;
    gzip_comp_level 6;

    # 前端静态文件
    location / {
        root /var/www/cms/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # 静态资源缓存
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Django 静态文件
    location /static/ {
        alias /var/www/cms/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # 媒体文件
    location /media/ {
        alias /var/www/cms/backend/media/;
        expires 30d;
        add_header Cache-Control "public";
        
        # 限制上传文件大小
        client_max_body_size 50M;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API 文档（可选，生产环境建议关闭）
    location /api/docs/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### 5.2 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled/

# 删除默认配置（可选）
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

---

## 6. 进程管理

### 6.1 使用 Systemd 管理 Gunicorn

```bash
# 创建 systemd 服务文件
sudo vim /etc/systemd/system/cms-backend.service
```

```ini
[Unit]
Description=CMS Backend (Gunicorn)
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/cms/backend
Environment="PATH=/var/www/cms/backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=config.settings"
ExecStart=/var/www/cms/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8001 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile /var/log/cms/access.log \
    --error-logfile /var/log/cms/error.log \
    --log-level info \
    config.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 6.2 创建日志目录

```bash
# 创建日志目录
sudo mkdir -p /var/log/cms
sudo chown -R www-data:www-data /var/log/cms

# 设置项目目录权限
sudo chown -R www-data:www-data /var/www/cms
```

### 6.3 启动服务

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start cms-backend

# 设置开机自启
sudo systemctl enable cms-backend

# 查看服务状态
sudo systemctl status cms-backend

# 查看日志
sudo journalctl -u cms-backend -f
```

### 6.4 管理命令

```bash
# 重启服务
sudo systemctl restart cms-backend

# 停止服务
sudo systemctl stop cms-backend

# 查看日志
tail -f /var/log/cms/error.log
tail -f /var/log/cms/access.log
```

---

## 7. HTTPS 配置（可选）

### 7.1 安装 Certbot

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx
```

### 7.2 获取 SSL 证书

```bash
# 获取证书（自动配置 Nginx）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 或者仅获取证书
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

### 7.3 自动续期

```bash
# 测试续期
sudo certbot renew --dry-run

# Certbot 会自动添加定时任务，无需手动配置
```

### 7.4 更新 Nginx 配置（如果手动配置）

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    # ... 其他配置同上 ...
}
```

---

## 8. 常见问题

### 8.1 权限问题

```bash
# 修复项目目录权限
sudo chown -R www-data:www-data /var/www/cms
sudo chmod -R 755 /var/www/cms

# 修复媒体目录权限
sudo chmod -R 775 /var/www/cms/backend/media
```

### 8.2 数据库连接失败

```bash
# 检查 MySQL 服务
sudo systemctl status mysql

# 测试数据库连接
mysql -u cms_user -p cms_db

# 检查防火墙
sudo ufw status
```

### 8.3 静态文件 404

```bash
# 重新收集静态文件
cd /var/www/cms/backend
source venv/bin/activate
python manage.py collectstatic --noinput

# 检查 Nginx 配置
sudo nginx -t
```

### 8.4 API 请求 502

```bash
# 检查 Gunicorn 服务
sudo systemctl status cms-backend

# 检查端口占用
sudo netstat -tlnp | grep 8001

# 查看 Gunicorn 日志
tail -f /var/log/cms/error.log
```

### 8.5 更新部署

```bash
# 拉取最新代码
cd /var/www/cms
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart cms-backend

# 更新前端
cd ../frontend
npm install
npm run build
```

---

## 9. 部署检查清单

- [ ] 服务器已更新并安装必要软件
- [ ] 防火墙已配置
- [ ] 数据库已创建并配置
- [ ] 后端代码已上传
- [ ] 虚拟环境已创建并安装依赖
- [ ] 环境变量已配置
- [ ] 数据库迁移已完成
- [ ] 超级管理员已创建
- [ ] 静态文件已收集
- [ ] 前端已构建
- [ ] Nginx 已配置并启动
- [ ] Gunicorn 服务已启动
- [ ] HTTPS 已配置（可选）
- [ ] 所有功能已测试

---

## 10. 快速部署脚本

创建一键部署脚本：

```bash
vim /var/www/cms/deploy.sh
```

```bash
#!/bin/bash
set -e

echo "=== 开始部署 CMS 项目 ==="

# 进入项目目录
cd /var/www/cms

# 拉取最新代码
echo ">>> 拉取最新代码..."
git pull

# 更新后端
echo ">>> 更新后端..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
deactivate

# 更新前端
echo ">>> 更新前端..."
cd ../frontend
npm install
npm run build

# 重启服务
echo ">>> 重启服务..."
sudo systemctl restart cms-backend
sudo systemctl reload nginx

echo "=== 部署完成 ==="
```

```bash
# 添加执行权限
chmod +x /var/www/cms/deploy.sh

# 执行部署
./deploy.sh
```
