# GitHub Actions 自动化部署配置指南

## 📋 目录结构

```
.github/
├── workflows/
│   ├── ci-cd.yml              # 完整的 CI/CD 流水线
│   ├── deploy-backend.yml     # 后端部署工作流
│   └── deploy-frontend.yml    # 前端部署工作流
├── gunicorn.service           # Gunicorn systemd 服务配置
└── DEPLOYMENT_GUIDE.md        # 本文件
```

## 🔧 服务器准备工作

### 1. 创建必要的目录结构

在服务器上执行以下命令：

```bash
# 创建项目目录
sudo mkdir -p /home/DRF_VUE/drf_vue/backend
sudo mkdir -p /home/front

# 设置权限
sudo chown -R $USER:$USER /home/DRF_VUE
sudo chown -R $USER:$USER /home/front

# 创建日志目录
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
```

### 2. 安装必要的软件

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和依赖
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo apt install -y nginx git rsync

# 安装 Node.js (如果需要服务器端构建)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 3. 配置 SSH 密钥认证

#### 方法一：使用 SSH 密钥（推荐）

1. **在本地生成 SSH 密钥对**（如果还没有）：
```bash
ssh-keygen -t ed25519 -C "github-actions@drf-vue" -f ~/.ssh/github_actions_deploy
```

2. **将公钥添加到服务器**：
```bash
ssh-copy-id -i ~/.ssh/github_actions_deploy.pub -p YOUR_SERVER_PORT user@YOUR_SERVER_IP
```

3. **测试连接**：
```bash
ssh -i ~/.ssh/github_actions_deploy -p YOUR_SERVER_PORT user@YOUR_SERVER_IP
```

4. **将私钥添加到 GitHub Secrets**：
```bash
cat ~/.ssh/github_actions_deploy
```
复制输出内容，保存到 GitHub Secrets 中的 `SSH_PRIVATE_KEY`

#### 方法二：使用 GitHub Deploy Keys

1. 在服务器上生成密钥对
2. 将公钥添加到 GitHub 仓库的 Deploy Keys
3. 将私钥保存到 GitHub Secrets

### 4. 配置 Gunicorn 服务

```bash
# 复制服务文件到服务器
sudo cp .github/gunicorn.service /etc/systemd/system/drf_vue_backend.service

# 重新加载 systemd
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable drf_vue_backend

# 启动服务
sudo systemctl start drf_vue_backend

# 检查状态
sudo systemctl status drf_vue_backend
```

### 5. 配置 Nginx

你的项目根目录已经有 `nginx.conf` 文件，需要：

```bash
# 备份现有配置
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak

# 复制新的配置
sudo cp nginx.conf /etc/nginx/nginx.conf

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

### 6. 配置环境变量

在服务器上创建后端环境变量文件：

```bash
# 在服务器上创建 .env 文件
nano /home/DRF_VUE/drf_vue/backend/.env
```

添加以下内容（根据实际情况修改）：

```env
# Django 配置
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-server-ip

# 数据库配置
DATABASE_URL=postgres://db_user:db_password@localhost:5432/db_name

# JWT 配置
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=minutes=60
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=days=7

# CORS 配置
CORS_ALLOWED_ORIGINS=https://your-domain.com

# 媒体文件配置
MEDIA_ROOT=/home/DRF_VUE/drf_vue/backend/media
STATIC_ROOT=/home/DRF_VUE/drf_vue/backend/staticfiles
```

## 🔐 配置 GitHub Secrets

在 GitHub 仓库中，进入 **Settings → Secrets and variables → Actions**，添加以下 secrets：

### 必需的 Secrets

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `SERVER_HOST` | 服务器 IP 地址或域名 | `8.148.251.135` 或 `example.com` |
| `SERVER_USER` | SSH 登录用户名 | `root` 或 `ubuntu` |
| `SERVER_PORT` | SSH 端口号 | `22` |
| `SSH_PRIVATE_KEY` | SSH 私钥内容 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `VITE_API_BASE_URL` | 前端 API 基础 URL | `https://your-domain.com/api/` |

### 可选的 Secrets

| Secret 名称 | 说明 |
|------------|------|
| `CODECOV_TOKEN` | Codecov 代码覆盖率令牌 |

**添加步骤：**
1. 点击 "New repository secret"
2. 输入名称和值
3. 点击 "Add secret"

## 🚀 使用方法

### 自动触发部署

工作流会在以下情况自动触发：

1. **推送代码到 main/master 分支**：
   - 修改 `backend/**` 目录 → 触发后端部署
   - 修改 `frontend/**` 目录 → 触发前端部署
   - 其他修改 → 触发完整 CI/CD 流程

2. **手动触发**：
   - 进入 GitHub Actions 页面
   - 选择对应的工作流
   - 点击 "Run workflow"

### 工作流程说明

#### 1. CI/CD Pipeline (`ci-cd.yml`)

这是完整的质量检查流程：
- ✅ 运行后端测试
- ✅ 构建前端项目
- ✅ 代码质量检查
- ⚠️ 不执行实际部署（仅作为 PR 检查）

#### 2. Backend Deployment (`deploy-backend.yml`)

后端专属部署流程：
- 🧪 运行测试套件
- 📦 上传代码到服务器
- 🔧 安装依赖
- 🗄️ 执行数据库迁移
- 🔄 重启 Gunicorn 服务

#### 3. Frontend Deployment (`deploy-frontend.yml`)

前端专属部署流程：
- 🏗️ 构建 PC 端、移动端、后台管理界面
- 📤 上传构建产物到服务器
- 🔐 设置文件权限
- 🔄 重启 Nginx

## 📊 监控和调试

### 查看 GitHub Actions 日志

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择对应的工作流运行
4. 查看详细日志

### 服务器端调试

```bash
# 查看 Gunicorn 日志
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# 检查服务状态
sudo systemctl status drf_vue_backend
sudo systemctl status nginx

# 查看进程
ps aux | grep gunicorn
ps aux | grep nginx
```

### 常见问题排查

#### 1. SSH 连接失败

```bash
# 测试 SSH 连接
ssh -v -p SERVER_PORT SERVER_USER@SERVER_HOST

# 检查 known_hosts
rm ~/.ssh/known_hosts
```

#### 2. 权限问题

```bash
# 修复文件权限
sudo chown -R www-data:www-data /home/DRF_VUE/drf_vue/backend
sudo chown -R www-data:www-data /home/front

# 修复静态文件权限
sudo chmod -R 755 /home/DRF_VUE/drf_vue/backend/staticfiles
```

#### 3. 端口被占用

```bash
# 检查端口占用
sudo lsof -i :8001  # Gunicorn
sudo lsof -i :80    # Nginx

# 杀死占用进程
sudo kill -9 PID
```

#### 4. 数据库迁移失败

```bash
# 手动执行迁移
cd /home/DRF_VUE/drf_vue/backend
source venv/bin/activate
python manage.py migrate

# 检查迁移状态
python manage.py showmigrations
```

## 🔒 安全建议

1. **使用非 root 用户部署**
   ```bash
   sudo adduser deployer
   sudo usermod -aG sudo deployer
   ```

2. **限制 SSH 访问**
   ```bash
   # 编辑 SSH 配置
   sudo nano /etc/ssh/sshd_config
   
   # 添加限制
   AllowUsers deployer
   PermitRootLogin no
   PasswordAuthentication no
   ```

3. **配置防火墙**
   ```bash
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw enable
   ```

4. **定期更新依赖**
   ```bash
   # 后端
   pip list --outdated
   pip install --upgrade package_name
   
   # 前端
   npm outdated
   npm update
   ```

5. **使用 HTTPS**
   ```bash
   # 安装 Certbot
   sudo apt install certbot python3-certbot-nginx
   
   # 获取证书
   sudo certbot --nginx -d your-domain.com
   
   # 自动续期
   sudo systemctl enable certbot.timer
   ```

## 📈 优化建议

### 1. 使用 Docker（可选）

如果需要更一致的部署环境，可以考虑 Docker 化：

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "config.wsgi:application"]
```

### 2. 添加健康检查

在 `.github/workflows/deploy-backend.yml` 中添加：

```yaml
- name: Health check
  run: |
    sleep 10
    curl -f http://localhost:8001/api/health || exit 1
```

### 3. 回滚策略

创建回滚脚本 `rollback.sh`：

```bash
#!/bin/bash
# 回滚到上一个版本
cd /home/DRF_VUE/drf_vue/backend
git checkout HEAD~1
systemctl restart drf_vue_backend
```

## 🎯 最佳实践

1. **分支策略**
   - `main/master`: 生产环境
   - `develop`: 开发环境
   - `feature/*`: 功能分支

2. **提交规范**
   ```
   feat: 新功能
   fix: 修复 bug
   docs: 文档更新
   style: 代码格式
   refactor: 重构
   test: 测试相关
   chore: 构建过程或辅助工具变动
   ```

3. **测试覆盖率目标**
   - 后端：≥ 80%
   - 关键业务逻辑：≥ 90%

4. **部署前检查清单**
   - [ ] 所有测试通过
   - [ ] 代码审查完成
   - [ ] 环境变量已配置
   - [ ] 数据库迁移脚本已准备
   - [ ] 备份当前版本

## 📞 支持

如果遇到问题：

1. 检查 GitHub Actions 日志
2. 查看服务器日志
3. 参考本文档的"常见问题排查"部分
4. 在项目中提 Issue

---

**最后更新**: 2026-04-28
**维护者**: Development Team
