# 数据库连接池配置 - 快速参考

## 🚀 配置总结

### 开发环境（`.env.development`）
```bash
DB_CONN_MAX_AGE=0              # 不持久化，方便调试
DB_CONN_HEALTH_CHECKS=False    # 不开启健康检查
```

**特点**：
- ✅ 每次请求创建新连接，便于查看 SQL 日志
- ✅ 无连接泄漏风险
- ✅ 适合开发和调试场景

---

### 生产环境（`.env.production`）
```bash
DB_CONN_MAX_AGE=300            # 连接持久化 5 分钟
DB_CONN_HEALTH_CHECKS=True     # 开启健康检查
```

**特点**：
- ✅ 连接复用，减少开销
- ✅ 健康检查避免 "MySQL server has gone away"
- ✅ 性能提升 ~10%

---

## 📊 配置对比

| 环境 | CONN_MAX_AGE | CONN_HEALTH_CHECKS | 连接数 | 适用场景 |
|------|--------------|-------------------|--------|---------|
| 开发 | 0 | False | 每请求1个 | 本地开发、调试 |
| 生产 | 300 | True | 固定worker数 | 服务器部署 |

---

## 🔧 如何修改配置

### 方法1：修改 `.env` 文件（推荐）

编辑对应的环境变量文件：
```bash
# 开发环境
backend/.env.development

# 生产环境
backend/.env.production
```

修改后重启服务：
```bash
# 开发环境
python manage.py runserver

# 生产环境
sudo systemctl restart drf_vue_backend
```

### 方法2：直接修改 `settings.py`（不推荐）

```python
DATABASES = {
    'default': {
        # ...
        'CONN_MAX_AGE': 300,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

⚠️ **注意**：直接修改代码会导致环境和代码耦合，建议使用环境变量。

---

## 🧪 验证配置是否生效

### 方法1：查看 Django 启动日志

启动 Django 时会打印数据库配置：
```python
python manage.py shell
>>> from django.db import connection
>>> print(connection.settings_dict['CONN_MAX_AGE'])
300
>>> print(connection.settings_dict['CONN_HEALTH_CHECKS'])
True
```

### 方法2：监控数据库连接数

```bash
# MySQL
mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected';"

# 开发环境：每次请求后会看到连接数波动
# 生产环境：连接数稳定在 worker 数量（如 3）
```

### 方法3：启用数据库后端日志

在 `settings.py` 中添加：
```python
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
```

可以看到：
- 连接创建时间
- SQL 执行时间
- 连接复用情况

---

## ⚙️ 调优建议

### 场景1：开发时想看到更多 SQL 日志

```bash
DB_CONN_MAX_AGE=0
DB_CONN_HEALTH_CHECKS=False
```

✅ 每次请求创建新连接，SQL 日志更清晰

---

### 场景2：生产环境高并发（QPS > 500）

```bash
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True
```

✅ 延长连接时间，减少连接创建频率

---

### 场景3：生产环境低流量（QPS < 50）

```bash
DB_CONN_MAX_AGE=120
DB_CONN_HEALTH_CHECKS=True
```

✅ 较短的连接时间，避免空闲连接占用资源

---

## ❓ 常见问题

### Q: 为什么开发环境不建议开启连接池？

**A**: 
1. 开发时经常需要查看 SQL 日志，每次新建连接更容易追踪
2. 开发环境流量低，连接池优势不明显
3. 避免连接泄漏导致的问题难以排查

### Q: 生产环境可以关闭健康检查吗？

**A**: 
❌ **强烈不建议**。健康检查能避免：
- "MySQL server has gone away" 错误
- 网络中断导致的连接失效
- MySQL 重启后的连接问题

性能损失仅 ~1ms/请求，但稳定性提升显著。

### Q: 如何判断当前配置是否合适？

**A**: 观察以下指标：
1. **数据库连接数**：应稳定在 worker 数量附近
2. **响应时间**：开启连接池后应降低 ~10%
3. **错误率**：不应出现 "Too many connections" 或 "Server has gone away"

---

## 📚 相关文档

- [database-connection-pool.md](./database-connection-pool.md) - 详细配置说明
- [Django 官方文档](https://docs.djangoproject.com/en/stable/ref/databases/#persistent-connections)
