# 🚀 快速开始 - 缓存清理

## 问题场景

当你遇到以下情况时，需要清理缓存：

1. ✅ **修改了分页配置**（如从 PageNumberPagination 改为 LimitOffsetPagination）
2. ✅ **更新了 Serializer 字段**
3. ✅ **修改了 ViewSet 逻辑**
4. ✅ **前端数据显示异常**（可能是旧缓存导致）
5. ✅ **部署新版本后**

## 快速解决

### Windows 用户

双击运行：
```
backend\clear_cache.bat
```

选择选项 `1` 清空所有缓存。

### Linux/Mac 用户

```bash
cd backend
chmod +x clear_cache.sh
./clear_cache.sh
```

选择选项 `1` 清空所有缓存。

### 命令行方式

```bash
cd backend
python manage.py clear_cache
```

输入 `yes` 确认执行。

## 选择性清理

如果只想清理特定模块的缓存：

```bash
# 只清理内容缓存
python manage.py clear_cache --pattern "contents:*"

# 只清理分类缓存
python manage.py clear_cache --pattern "categories:*"

# 只清理标签缓存
python manage.py clear_cache --pattern "tags:*"

# 只清理角色权限缓存
python manage.py clear_cache --pattern "roles:*"
python manage.py clear_cache --pattern "permissions:*"
```

## 验证效果

清理后刷新浏览器页面（Ctrl+F5 强制刷新），应该能看到最新的数据。

## 更多信息

详细文档：[docs/cache_cleanup_guide.md](./docs/cache_cleanup_guide.md)
