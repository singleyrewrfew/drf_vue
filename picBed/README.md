# PicBed - 图床服务系统

一个功能完善的图床后端服务系统,支持图片上传、存储、处理和管理。

## 功能特性

### 核心功能
- ✅ 图片上传与验证(支持JPG、PNG、GIF、WebP等格式)
- ✅ 断点续传与分块上传
- ✅ 多种存储策略(本地存储、AWS S3、阿里云OSS)
- ✅ RESTful API接口
- ✅ JWT用户认证
- ✅ 细粒度权限控制
- ✅ 图片处理(压缩、格式转换、水印、尺寸调整)
- ✅ Redis缓存支持
- ✅ 异步任务处理(Celery)
- ✅ Docker容器化部署

### 技术栈
- **框架**: Django 4.2.7 + Django REST Framework 3.14.0
- **认证**: JWT (djangorestframework-simplejwt)
- **图片处理**: Pillow
- **任务队列**: Celery + Redis
- **缓存**: Django Redis
- **API文档**: drf-yasg (Swagger/ReDoc)
- **容器化**: Docker + Docker Compose

## 快速开始

### 环境要求
- Python 3.11+
- Redis 6.0+
- PostgreSQL 15+ (生产环境)
- Docker & Docker Compose (推荐)

### 本地开发环境

1. **克隆项目**
```bash
cd c:\Users\ZQY\Desktop\drf_vue\picBed
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件,配置必要的参数
```

5. **数据库迁移**
```bash
python manage.py migrate
```

6. **创建超级用户**
```bash
python manage.py createsuperuser
```

7. **启动开发服务器**
```bash
python manage.py runserver
```

8. **启动Celery Worker** (新终端)
```bash
celery -A picBed worker -l INFO
```

### Docker部署

1. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件
```

2. **启动服务**
```bash
docker-compose up -d
```

3. **查看服务状态**
```bash
docker-compose ps
```

4. **运行数据库迁移**
```bash
docker-compose exec web python manage.py migrate
```

5. **创建超级用户**
```bash
docker-compose exec web python manage.py createsuperuser
```

## API文档

启动服务后,访问以下地址查看API文档:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## API端点

### 认证相关
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/refresh/` - 刷新Token

### 用户管理
- `GET /api/auth/users/` - 获取用户信息
- `GET /api/auth/users/profile/` - 获取用户详情
- `POST /api/auth/users/change_password/` - 修改密码

### 图片管理
- `POST /api/images/upload/` - 上传图片
- `POST /api/images/upload_init/` - 初始化分块上传
- `POST /api/images/upload_chunk/` - 上传分块
- `POST /api/images/upload_complete/` - 完成分块上传
- `GET /api/images/` - 获取图片列表
- `GET /api/images/{id}/` - 获取图片详情
- `DELETE /api/images/{id}/` - 删除图片
- `GET /api/images/{id}/preview/` - 图片预览

### 相册管理
- `GET /api/images/albums/` - 获取相册列表
- `POST /api/images/albums/` - 创建相册
- `GET /api/images/albums/{id}/` - 获取相册详情
- `PUT /api/images/albums/{id}/` - 更新相册
- `DELETE /api/images/albums/{id}/` - 删除相册

### 图片处理
- `POST /api/process/process/{id}/process/` - 处理图片
- `POST /api/process/process/batch_process/` - 批量处理
- `POST /api/process/process/{id}/compress/` - 压缩图片
- `POST /api/process/process/{id}/convert/` - 格式转换
- `POST /api/process/process/{id}/resize/` - 调整尺寸
- `POST /api/process/process/{id}/watermark/` - 添加水印

### 健康检查
- `GET /health/` - 健康检查
- `GET /health/ready/` - 就绪检查
- `GET /health/live/` - 存活检查

## 使用示例

### 1. 用户注册
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### 2. 用户登录
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 上传图片
```bash
curl -X POST http://localhost:8000/api/images/upload/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "title=My Image" \
  -F "is_public=false"
```

### 4. 获取图片列表
```bash
curl -X GET http://localhost:8000/api/images/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. 图片处理
```bash
curl -X POST http://localhost:8000/api/process/process/1/compress/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quality": 85
  }'
```

## 存储策略配置

### 本地存储
```env
STORAGE_BACKEND=local
MEDIA_ROOT=media
```

### AWS S3
```env
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket
AWS_S3_REGION_NAME=us-east-1
```

### 阿里云OSS
```env
STORAGE_BACKEND=oss
ALIYUN_ACCESS_KEY_ID=your_access_key
ALIYUN_ACCESS_KEY_SECRET=your_secret_key
ALIYUN_OSS_BUCKET_NAME=your_bucket
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
```

## 存储管理

### 查看存储统计
```bash
python manage.py cleanup_storage --stats
```

### 清理孤立文件
```bash
python manage.py cleanup_storage --orphaned
```

### 清理旧图片
```bash
python manage.py cleanup_storage --old 365
```

### 更新用户存储使用量
```bash
python manage.py cleanup_storage --update-usage
```

## 性能优化

### Redis缓存
系统使用Redis缓存热门图片数据,提升访问速度。

### 异步处理
图片处理任务通过Celery异步执行,避免阻塞主线程。

### 静态文件
使用Whitenoise提供静态文件服务,支持缓存和压缩。

## 监控与日志

### 日志文件
- `logs/app.log` - 应用日志
- `logs/app.json` - JSON格式日志

### 日志级别
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- DEBUG: 调试信息

### 健康检查
访问 `/health/` 端点检查服务健康状态。

## 安全特性

- JWT认证机制
- 密码加密存储
- API访问速率限制
- 文件类型验证
- 文件大小限制
- CORS跨域配置

## 项目结构

```
picBed/
├── picBed/              # 项目配置
│   ├── settings.py      # 配置文件
│   ├── urls.py          # 主路由
│   └── celery.py        # Celery配置
├── core/                # 核心模块
│   ├── exceptions.py    # 异常处理
│   ├── middleware.py    # 中间件
│   └── responses.py     # 响应格式
├── users/               # 用户管理
│   ├── models.py        # 用户模型
│   ├── views.py         # 用户视图
│   └── serializers.py   # 序列化器
├── images/              # 图片管理
│   ├── models.py        # 图片模型
│   ├── views.py         # 图片视图
│   └── serializers.py   # 序列化器
├── storage/             # 存储管理
│   ├── backends.py      # 存储后端
│   └── monitor.py       # 存储监控
├── processing/          # 图片处理
│   ├── processor.py     # 处理器
│   └── tasks.py         # 异步任务
├── media/               # 媒体文件
├── logs/                # 日志文件
├── Dockerfile           # Docker配置
├── docker-compose.yml   # Docker Compose配置
├── requirements.txt     # 依赖列表
└── manage.py            # Django管理脚本
```

## 开发指南

### 运行测试
```bash
python manage.py test
```

### 代码风格检查
```bash
flake8 .
```

### 创建迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

## 故障排查

### 常见问题

1. **Redis连接失败**
   - 检查Redis服务是否启动
   - 确认REDIS_URL配置正确

2. **图片上传失败**
   - 检查文件大小是否超过限制
   - 确认文件格式是否支持
   - 检查存储路径权限

3. **Celery任务不执行**
   - 确认Celery Worker是否启动
   - 检查Redis连接状态
   - 查看Celery日志

## 许可证

MIT License

## 联系方式

如有问题或建议,请提交Issue或Pull Request。
