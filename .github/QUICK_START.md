# GitHub Actions 自动化部署 - 快速开始

## 🚀 5 分钟快速配置

### 第一步：准备服务器（在服务器上执行）

```bash
# 1. 下载并运行自动配置脚本
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/.github/setup_server.sh
chmod +x setup_server.sh
sudo bash setup_server.sh

# 2. 按照提示完成配置
# - 配置数据库（可选）
# - 生成 SSH 密钥
# - 创建部署用户
```

### 第二步：配置 GitHub Secrets（在 GitHub 网页上操作）

进入你的仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 5 个必需的 secrets：

| Secret 名称 | 值示例 | 说明 |
|------------|--------|------|
| `SERVER_HOST` | `8.148.251.135` | 服务器 IP 或域名 |
| `SERVER_USER` | `root` 或 `deployer` | SSH 登录用户 |
| `SERVER_PORT` | `22` | SSH 端口 |
| `SSH_PRIVATE_KEY` | `-----BEGIN...` | SSH 私钥内容 |
| `VITE_API_BASE_URL` | `https://your-domain.com/api/` | API 地址 |

**获取 SSH 私钥的方法：**
```bash
# 在服务器上查看私钥
cat /root/.ssh/github_actions/deploy_key

# 复制全部内容（包括 BEGIN 和 END 行），粘贴到 GitHub Secrets
```

### 第三步：配置后端环境变量（在服务器上执行）

```bash
# 1. 创建 .env 文件
nano /home/DRF_VUE/drf_vue/backend/.env

# 2. 参考 .github/.env.production.example 填写配置
# 至少需要设置：
# - DJANGO_SECRET_KEY
# - DB_* (数据库配置)
# - DJANGO_ALLOWED_HOSTS
# - CORS_ALLOWED_ORIGINS

# 3. 保存退出（Ctrl+X, Y, Enter）
```

### 第四步：初始化部署（首次部署）

#### 方法 A：使用 GitHub Actions 自动部署（推荐）

```bash
# 1. 提交代码到 main/master 分支
git add .
git commit -m "feat: initial deployment"
git push origin main

# 2. 在 GitHub 查看 Actions 执行状态
# https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

#### 方法 B：手动首次部署

```bash
# 在服务器上执行
cd /home/DRF_VUE/drf_vue/backend

# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 3. 执行数据库迁移
python manage.py migrate

# 4. 创建超级用户
python manage.py createsuperuser

# 5. 收集静态文件
python manage.py collectstatic --noinput

# 6. 启动 Gunicorn
sudo systemctl start drf_vue_backend
sudo systemctl enable drf_vue_backend

# 7. 检查状态
sudo systemctl status drf_vue_backend
```

### 第五步：验证部署

```bash
# 1. 测试后端 API
curl http://localhost:8001/api/health

# 2. 测试 Nginx
curl http://localhost:80

# 3. 从外部访问
# 浏览器打开: http://YOUR_SERVER_IP

# 4. 查看日志
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/error.log
```

## ✅ 检查清单

- [ ] 服务器已安装 Python、Nginx、PostgreSQL
- [ ] SSH 密钥已生成并配置到 GitHub Secrets
- [ ] 后端 .env 文件已配置
- [ ] 数据库已创建并配置
- [ ] Gunicorn 服务正在运行
- [ ] Nginx 配置正确并正在运行
- [ ] GitHub Actions 工作流已成功执行
- [ ] 可以从外部访问网站

## 🔧 常用命令速查

### 服务管理

```bash
# 后端服务
sudo systemctl start drf_vue_backend
sudo systemctl stop drf_vue_backend
sudo systemctl restart drf_vue_backend
sudo systemctl status drf_vue_backend

# Nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo nginx -t  # 测试配置

# 查看进程
ps aux | grep gunicorn
ps aux | grep nginx
```

### 日志查看

```bash
# 实时查看日志
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# 查看最近 100 行
sudo tail -n 100 /var/log/gunicorn/error.log
```

### 数据库操作

```bash
# 连接到 PostgreSQL
sudo -u postgres psql

# 查看数据库
\l

# 切换到数据库
\c drf_vue_db

# 查看表
\dt

# 退出
\q
```

### Git 操作

```bash
# 查看当前分支
git branch

# 拉取最新代码
git pull origin main

# 查看提交历史
git log --oneline -10
```

## 🐛 故障排查

### 问题 1：GitHub Actions 失败 - SSH 连接超时

**解决方案：**
```bash
# 1. 检查服务器防火墙
sudo ufw status
sudo ufw allow 22/tcp

# 2. 检查 SSH 服务
sudo systemctl status sshd

# 3. 测试 SSH 连接
ssh -v -p 22 user@server_ip

# 4. 确认 GitHub Secrets 中的 SSH_PRIVATE_KEY 正确
```

### 问题 2：Gunicorn 启动失败

**解决方案：**
```bash
# 1. 查看详细错误
sudo journalctl -u drf_vue_backend -n 50

# 2. 检查 Python 环境
cd /home/DRF_VUE/drf_vue/backend
source venv/bin/activate
python manage.py check

# 3. 检查 .env 文件
cat .env

# 4. 手动启动测试
gunicorn --bind 127.0.0.1:8001 config.wsgi:application
```

### 问题 3：Nginx 502 Bad Gateway

**解决方案：**
```bash
# 1. 检查后端是否运行
sudo systemctl status drf_vue_backend

# 2. 检查端口监听
sudo lsof -i :8001

# 3. 检查 Nginx 配置
sudo nginx -t
sudo cat /etc/nginx/nginx.conf

# 4. 重启服务
sudo systemctl restart drf_vue_backend
sudo systemctl restart nginx
```

### 问题 4：前端页面空白

**解决方案：**
```bash
# 1. 检查构建产物是否存在
ls -la /home/front/dist/
ls -la /home/front/dist_mobile/

# 2. 检查文件权限
sudo chown -R www-data:www-data /home/front/dist
sudo chmod -R 755 /home/front/dist

# 3. 检查 Nginx 配置中的 root 路径
grep -A 5 "location /" /etc/nginx/nginx.conf

# 4. 浏览器控制台查看错误
# F12 → Console 标签
```

### 问题 5：数据库连接失败

**解决方案：**
```bash
# 1. 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 2. 测试数据库连接
psql -U drf_vue_user -d drf_vue_db -h localhost

# 3. 检查 .env 中的数据库配置
grep DB_ .env

# 4. 查看 PostgreSQL 日志
sudo tail -f /var/log/postgresql/postgresql-*.log
```

## 📊 监控建议

### 设置简单的健康检查

```bash
# 创建健康检查脚本
cat > /usr/local/bin/health_check.sh << 'EOF'
#!/bin/bash

# 检查 Gunicorn
if ! systemctl is-active --quiet drf_vue_backend; then
    echo "❌ Gunicorn is down"
    systemctl restart drf_vue_backend
else
    echo "✅ Gunicorn is running"
fi

# 检查 Nginx
if ! systemctl is-active --quiet nginx; then
    echo "❌ Nginx is down"
    systemctl restart nginx
else
    echo "✅ Nginx is running"
fi

# 检查磁盘空间
df -h / | awk 'NR==2 {print "💾 Disk usage: " $5}'

# 检查内存
free -h | awk 'NR==2 {print "🧠 Memory usage: " $3 "/" $2}'
EOF

chmod +x /usr/local/bin/health_check.sh

# 添加到 crontab（每小时执行一次）
(crontab -l 2>/dev/null; echo "0 * * * * /usr/local/bin/health_check.sh >> /var/log/health_check.log 2>&1") | crontab -
```

## 🎯 下一步优化

1. **配置 HTTPS**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **设置备份策略**
   ```bash
   # 每天备份数据库
   0 2 * * * pg_dump drf_vue_db > /backup/db_$(date +\%Y\%m\%d).sql
   ```

3. **配置监控工具**
   - Prometheus + Grafana
   - Sentry（错误追踪）
   - LogRocket（前端监控）

4. **启用 CDN**
   - Cloudflare
   - 阿里云 CDN
   - 腾讯云 CDN

---

**需要帮助？** 查看完整文档：`.github/DEPLOYMENT_GUIDE.md`
