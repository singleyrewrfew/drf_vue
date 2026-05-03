#!/bin/bash
# ========================================
# 清空 Redis 缓存脚本
# 
# 用途：清除所有或指定模式的 Redis 缓存
# 使用场景：代码更新后清除旧缓存，避免数据不一致
# ========================================

cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  Redis 缓存清理工具"
echo "========================================"
echo ""

clear_cache() {
    local pattern=$1
    python manage.py clear_cache --pattern "$pattern"
}

echo "请选择操作："
echo ""
echo "1. 清空所有缓存（谨慎使用）"
echo "2. 清空内容相关缓存（contents:*）"
echo "3. 清空分类相关缓存（categories:*）"
echo "4. 清空标签相关缓存（tags:*）"
echo "5. 清空角色权限缓存（roles:* permissions:*）"
echo "6. 自定义模式"
echo "0. 退出"
echo ""

read -p "请输入选项 (0-6): " choice

case $choice in
    1)
        clear_cache "*"
        ;;
    2)
        clear_cache "contents:*"
        ;;
    3)
        clear_cache "categories:*"
        ;;
    4)
        clear_cache "tags:*"
        ;;
    5)
        clear_cache "roles:*"
        clear_cache "permissions:*"
        ;;
    6)
        echo ""
        read -p "请输入缓存模式（如 contents:*）: " pattern
        clear_cache "$pattern"
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项，请重新运行脚本"
        exit 1
        ;;
esac

echo ""
echo "操作完成！"
