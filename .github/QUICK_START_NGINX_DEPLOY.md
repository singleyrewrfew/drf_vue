# Nginx 配置部署 - 快速开始

## 🚀 5分钟快速上手

### 前置条件

1. ✅ 已配置 GitHub Secrets（`SERVER_HOST`, `SERVER_USER`, `SERVER_PORT`, `SSH_PRIVATE_KEY`）
2. ✅ Nginx 已安装在服务器上
3. ✅ SSH 密钥已配置

---

## 📝 使用步骤

### 方法1：自动触发（推荐）

```bash
# 1. 修改 Nginx 配置
vim .github/nginx.conf

# 2. 提交更改
git add .github/nginx.conf
git commit -m "feat: update nginx configuration"

# 3. 推送到 main 分支
git push origin main

# 4. 等待工作流自动执行（约 2-3 分钟）
# 查看进度：GitHub → Actions → Deploy Nginx Configuration
```

### 方法2：手动触发

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Deploy Nginx Configuration**
4. 点击 **Run workflow**
5. （可选）填写部署原因
6. 点击 **Run workflow**

---

## ✅ 验证部署

### 1. 检查工作流状态

```
GitHub → Actions → Deploy Nginx Configuration
```

看到绿色 ✅ 表示成功，红色 ❌ 表示失败。

### 2. 测试网站访问

```bash
# 测试 HTTP 响应
curl -I http://8.148.251.135/

# 预期输出：
# HTTP/1.1 200 OK
# Server: nginx
```

### 3. 检查 Nginx 状态

```bash
# SSH 到服务器
ssh user@8.148.251.135

# 检查 Nginx 状态
sudo systemctl status nginx

# 查看最新日志
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 回滚操作

如果新配置有问题，可以快速回滚：

### 方法1：通过工作流自动回滚

工作流会在配置测试失败时**自动回滚**到最近的备份。

### 方法2：手动回滚

```bash
# 1. SSH 到服务器
ssh user@8.148.251.135

# 2. 查看可用备份
ls -lt /etc/nginx/backups/

# 3. 恢复最近的备份
sudo cp /etc/nginx/backups/nginx.conf.backup.LATEST /etc/nginx/nginx.conf

# 4. 测试配置
sudo nginx -t

# 5. 重载 Nginx
sudo systemctl reload nginx
```

---

## 📊 常见问题

### Q1: 工作流没有触发？

**检查**：
```bash
# 确保推送到正确的分支
git branch  # 应该在 main 或 master

# 确保修改了正确的文件
git diff HEAD~1 --name-only | grep nginx.conf
```

### Q2: 部署失败了怎么办？

**步骤**：
1. 查看工作流日志（GitHub Actions）
2. 找到错误信息
3. 修复配置
4. 重新推送

### Q3: 如何查看备份？

```bash
# SSH 到服务器
ssh user@8.148.251.135

# 列出所有备份
ls -lt /etc/nginx/backups/

# 查看某个备份的内容
sudo cat /etc/nginx/backups/nginx.conf.backup.20260503_120000
```

---

## 💡 提示

- ✅ 每次部署前会自动备份
- ✅ 保留最近 10 个备份
- ✅ 配置测试失败会自动回滚
- ✅ 平滑重载，零停机时间
- ✅ 详细的部署日志和报告

---

## 📚 更多信息

- [完整文档](./NGINX_DEPLOYMENT_WORKFLOW.md)
- [Nginx 配置说明](./NGINX_X_ACCEL_REDIRECT_SETUP.md)
- [工作流文件](./workflows/deploy-nginx.yml)
