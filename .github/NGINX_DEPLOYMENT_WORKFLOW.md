# Nginx 配置自动部署工作流

## 📋 概述

本工作流会自动检测 Nginx 配置文件的变化，并在推送到 main/master 分支时自动部署到服务器。

---

## 🚀 触发条件

### 自动触发

当以下文件发生变化并推送到 `main` 或 `master` 分支时：

```yaml
paths:
  - '.github/nginx.conf'           # Nginx 主配置文件
  - '.github/workflows/deploy-nginx.yml'  # 工作流本身
```

### 手动触发

也可以在 GitHub Actions 页面手动触发：

1. 进入 **Actions** 标签
2. 选择 **Deploy Nginx Configuration**
3. 点击 **Run workflow**
4. （可选）填写部署原因
5. 点击 **Run workflow**

---

## 🔄 工作流程

### 1. 本地验证（Local Validation）

```bash
# 在 GitHub Actions runner 上验证配置语法
sudo nginx -t
```

✅ **目的**：确保配置语法正确，避免部署错误配置

### 2. 备份当前配置（Backup）

```bash
# 在服务器上创建备份
BACKUP_FILE="/etc/nginx/backups/nginx.conf.backup.YYYYMMDD_HHMMSS"
sudo cp /etc/nginx/nginx.conf $BACKUP_FILE

# 保留最近 10 个备份
ls -t /etc/nginx/backups/nginx.conf.backup.* | tail -n +11 | xargs -r rm -f
```

✅ **目的**：如果新配置有问题，可以快速恢复

### 3. 部署新配置（Deploy）

```bash
# 上传新配置到临时位置
scp .github/nginx.conf user@server:/tmp/nginx.conf.new

# 移动到正确位置
sudo mv /tmp/nginx.conf.new /etc/nginx/nginx.conf
sudo chmod 644 /etc/nginx/nginx.conf
sudo chown root:root /etc/nginx/nginx.conf
```

✅ **目的**：安全地替换配置文件

### 4. 测试并重载（Test & Reload）

```bash
# 测试配置语法
sudo nginx -t

# 如果测试失败，自动恢复备份
if [ test_failed ]; then
  sudo cp $LATEST_BACKUP /etc/nginx/nginx.conf
  sudo nginx -t
fi

# 平滑重载（不中断服务）
sudo systemctl reload nginx
```

✅ **目的**：
- 确保配置有效
- 失败时自动回滚
- 平滑重启，零停机时间

### 5. 健康检查（Health Check）

```bash
# 检查 Nginx 状态
systemctl is-active --quiet nginx

# 验证关键配置
grep -q "media_internal" /etc/nginx/nginx.conf
grep -q "sendfile on" /etc/nginx/nginx.conf

# 测试 HTTP 响应
curl -s -o /dev/null -w "%{http_code}" http://server/
```

✅ **目的**：确认服务正常运行

---

## 🛡️ 安全特性

### 1. 自动备份

- ✅ 每次部署前自动备份
- ✅ 保留最近 10 个备份
- ✅ 备份路径：`/etc/nginx/backups/`

### 2. 配置验证

- ✅ 部署前在本地验证语法
- ✅ 部署后在服务器验证语法
- ✅ 失败时自动回滚到备份

### 3. 平滑重载

- ✅ 使用 `systemctl reload` 而非 `restart`
- ✅ 不会中断现有连接
- ✅ 零停机时间

### 4. 权限控制

- ✅ 配置文件权限：`644`（root:root）
- ✅ 只有 root 可以修改
- ✅ SSH 私钥通过 GitHub Secrets 管理

---

## 📊 部署结果

### 成功示例

```
## ✅ Nginx Configuration Deployment Successful

- **Server**: 8.148.251.135
- **Config Path**: /etc/nginx/nginx.conf
- **Backup Dir**: /etc/nginx/backups
- **Trigger**: push

### Changes
+ location /media_internal/ {
+     internal;
+     alias /home/DRF_VUE/drf_vue/backend/media/;
+     ...
+ }
```

### 失败示例

```
## ❌ Nginx Configuration Deployment Failed

**Server**: 8.148.251.135
**Error**: Check the logs above for details

### Recovery Steps
1. SSH to server: `ssh -p 22 user@8.148.251.135`
2. Check latest backup: `ls -lt /etc/nginx/backups/`
3. Restore backup: `sudo cp <backup_file> /etc/nginx/nginx.conf`
4. Test config: `sudo nginx -t`
5. Reload Nginx: `sudo systemctl reload nginx`
```

---

## 🔧 配置要求

### GitHub Secrets

需要在 GitHub 仓库设置中添加以下 Secrets：

| Secret | 说明 | 示例 |
|--------|------|------|
| `SERVER_HOST` | 服务器 IP 或域名 | `8.148.251.135` |
| `SERVER_USER` | SSH 用户名 | `root` 或 `ubuntu` |
| `SERVER_PORT` | SSH 端口 | `22` |
| `SSH_PRIVATE_KEY` | SSH 私钥 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |

### 添加步骤

1. 进入 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加上述 Secrets

---

## 🧪 测试方法

### 1. 本地测试配置语法

```bash
# 安装 Nginx（如果未安装）
sudo apt-get install nginx

# 测试配置
sudo nginx -t -c .github/nginx.conf
```

### 2. 手动触发工作流

```bash
# 推送一个小的修改
echo "# Test deployment" >> .github/nginx.conf
git add .github/nginx.conf
git commit -m "test: trigger nginx deployment"
git push origin main
```

### 3. 查看工作流日志

1. 进入 **Actions** 标签
2. 选择最新的 **Deploy Nginx Configuration** 运行
3. 查看详细日志

---

## 🐛 故障排查

### 问题1：SSH 连接失败

**症状**：
```
ssh: connect to host 8.148.251.135 port 22: Connection timed out
```

**解决**：
1. 检查 `SERVER_HOST` 和 `SERVER_PORT` 是否正确
2. 确保服务器防火墙允许 SSH 连接
3. 验证 SSH 私钥是否正确

### 问题2：Nginx 配置语法错误

**症状**：
```
nginx: [emerg] unknown directive "xxx" in /etc/nginx/nginx.conf:123
```

**解决**：
1. 工作流会自动恢复到备份
2. 检查本地配置语法：`sudo nginx -t`
3. 修复错误后重新推送

### 问题3：权限不足

**症状**：
```
Permission denied (publickey).
```

**解决**：
1. 确保 SSH 私钥有正确的权限
2. 确保公钥已添加到服务器的 `~/.ssh/authorized_keys`
3. 检查 `SERVER_USER` 是否有 sudo 权限

### 问题4：Nginx 重载失败

**症状**：
```
Job failed: Nginx failed to start!
```

**解决**：
1. SSH 到服务器
2. 查看日志：`sudo journalctl -u nginx --no-pager -n 50`
3. 恢复备份：`sudo cp /etc/nginx/backups/nginx.conf.backup.LATEST /etc/nginx/nginx.conf`
4. 重新加载：`sudo systemctl reload nginx`

---

## 📝 最佳实践

### 1. 提交前本地测试

```bash
# 在本地验证配置
sudo nginx -t -c .github/nginx.conf

# 确保没有语法错误后再推送
git add .github/nginx.conf
git commit -m "feat: update nginx configuration"
git push
```

### 2. 使用有意义的提交信息

```bash
# ✅ 好的提交信息
git commit -m "feat: add X-Accel-Redirect support for media files"

# ❌ 不好的提交信息
git commit -m "update nginx"
```

### 3. 监控部署结果

- ✅ 检查 GitHub Actions 日志
- ✅ 验证网站是否正常访问
- ✅ 检查 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`

### 4. 定期清理备份

工作流会自动保留最近 10 个备份，但也可以手动清理：

```bash
# 查看所有备份
ls -lt /etc/nginx/backups/

# 删除旧备份（保留最近 5 个）
cd /etc/nginx/backups/
ls -t nginx.conf.backup.* | tail -n +6 | xargs -r rm -f
```

---

## 🎯 与其他工作流的关系

### 工作流对比

| 工作流 | 触发条件 | 部署内容 | 频率 |
|--------|---------|---------|------|
| `deploy-backend.yml` | `backend/**` 变化 | Django 后端代码 | 低频 |
| `deploy-frontend.yml` | `front/**` 或 `frontend/**` 变化 | 前端静态文件 | 中频 |
| `deploy-nginx.yml` | `.github/nginx.conf` 变化 | Nginx 配置 | 低频 |

### 独立性

- ✅ 三个工作流完全独立
- ✅ 可以并行运行
- ✅ 互不影响

---

## 📚 相关文档

- [Nginx X-Accel-Redirect 配置说明](./NGINX_X_ACCEL_REDIRECT_SETUP.md)
- [后端部署工作流](./workflows/deploy-backend.yml)
- [前端部署工作流](./workflows/deploy-frontend.yml)

---

## 🔄 更新历史

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-05-03 | 1.0.0 | 初始版本，支持自动部署和回滚 |

---

**最后更新**: 2026-05-03  
**维护者**: Development Team
