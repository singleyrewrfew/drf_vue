# PicBed API 文档

## 概述

本文档描述了 PicBed 图床系统的所有 REST API 接口。所有接口都需要认证（特别标注的除外），使用 JWT Token 进行身份验证。

**基础 URL:** `http://localhost:8000/api`

**认证方式:** 在请求头中携带 JWT Token
```
Authorization: Bearer <your_access_token>
```

---

## 目录

1. [认证接口](#1-认证接口)
2. [用户接口](#2-用户接口)
3. [图片上传接口](#3-图片上传接口)
4. [图片管理接口](#4-图片管理接口)
5. [相册管理接口](#5-相册管理接口)
6. [图片处理接口](#6-图片处理接口)
7. [健康检查接口](#7-健康检查接口)

---

## 1. 认证接口

### 1.1 用户注册

**接口:** `POST /api/auth/register/`

**权限:** 无需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码（至少 8 位） |
| password_confirm | string | 是 | 确认密码 |

**请求示例:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "password_confirm": "password123"
}
```

**响应示例:**
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null,
      "bio": "",
      "storage_quota": 1073741824,
      "storage_used": 0,
      "storage_available": 1073741824,
      "storage_usage_percentage": 0,
      "created_at": "2026-03-31T16:00:00Z",
      "updated_at": "2026-03-31T16:00:00Z"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
    }
  }
}
```

---

### 1.2 用户登录

**接口:** `POST /api/auth/login/`

**权限:** 无需认证

**限流:** 5 次/分钟/IP

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**请求示例:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null,
      "bio": ""
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
    }
  }
}
```

---

### 1.3 刷新 Token

**接口:** `POST /api/auth/refresh/`

**权限:** 无需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| refresh | string | 是 | Refresh Token |

**请求示例:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

**响应示例:**
```json
{
  "code": 200,
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
  }
}
```

---

## 2. 用户接口

### 2.1 获取当前用户信息

**接口:** `GET /api/users/profile/`

**权限:** 需认证

**响应示例:**
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "avatar": "http://localhost:8000/media/avatars/avatar.jpg",
    "bio": "个人简介",
    "storage_quota": 1073741824,
    "storage_used": 1024000,
    "storage_available": 1072717824,
    "storage_usage_percentage": 0.095,
    "created_at": "2026-03-31T16:00:00Z",
    "updated_at": "2026-03-31T16:00:00Z"
  }
}
```

---

### 2.2 更新用户信息

**接口:** `PUT /api/users/` 或 `PATCH /api/users/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | 否 | 新邮箱 |
| avatar | file | 否 | 新头像文件 |
| bio | string | 否 | 个人简介 |

**请求示例 (multipart/form-data):**
```
email: newemail@example.com
bio: 新的个人简介
avatar: [file]
```

**响应示例:**
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "newemail@example.com",
    "avatar": "http://localhost:8000/media/avatars/new_avatar.jpg",
    "bio": "新的个人简介",
    ...
  }
}
```

---

### 2.3 修改密码

**接口:** `POST /api/users/change_password/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| old_password | string | 是 | 旧密码 |
| new_password | string | 是 | 新密码（至少 8 位） |

**请求示例:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "密码修改成功"
}
```

---

## 3. 图片上传接口

### 3.1 简单上传（推荐小文件）

**接口:** `POST /api/images/upload/`

**权限:** 需认证

**请求格式:** `multipart/form-data`

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 图片文件 |
| album | integer | 否 | 相册 ID |
| title | string | 否 | 图片标题（最大 200 字符） |
| description | string | 否 | 图片描述 |
| tags | array | 否 | 标签数组，如 `["标签 1", "标签 2"]` |
| is_public | boolean | 否 | 是否公开，默认 false |

**请求示例 (cURL):**
```bash
curl -X POST http://localhost:8000/api/images/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "title=测试图片" \
  -F "description=这是一张测试图片" \
  -F "tags=[\"测试\", \"示例\"]" \
  -F "is_public=true"
```

**Python 示例:**
```python
import requests

headers = {'Authorization': f'Bearer {token}'}
files = {'file': open('image.jpg', 'rb')}
data = {
    'title': '测试图片',
    'description': '这是一张测试图片',
    'tags': ['测试', '示例'],
    'is_public': True
}

response = requests.post(
    'http://localhost:8000/api/images/upload/',
    headers=headers,
    files=files,
    data=data
)
```

**响应示例:**
```json
{
  "code": 201,
  "message": "图片上传成功",
  "data": {
    "id": 1,
    "album": null,
    "filename": "image.jpg",
    "file_size": 1024000,
    "file_hash": "d41d8cd98f00b204e9800998ecf8427e",
    "width": 1920,
    "height": 1080,
    "format": "JPEG",
    "title": "测试图片",
    "description": "这是一张测试图片",
    "tags": ["测试", "示例"],
    "is_public": true,
    "access_count": 0,
    "storage_backend": "local",
    "url": "http://localhost:8000/media/images/image.jpg",
    "user_username": "testuser",
    "album_name": null,
    "created_at": "2026-03-31T16:00:00Z",
    "updated_at": "2026-03-31T16:00:00Z"
  }
}
```

---

### 3.2 分块上传（推荐大文件）

#### 3.2.1 初始化上传

**接口:** `POST /api/images/upload_init/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filename | string | 是 | 文件名 |
| file_size | integer | 是 | 文件总大小（字节） |
| file_hash | string | 是 | 文件 MD5 哈希值 |
| chunk_size | integer | 是 | 分块大小（字节），最大 10MB |

**请求示例:**
```json
{
  "filename": "large_image.jpg",
  "file_size": 52428800,
  "file_hash": "d41d8cd98f00b204e9800998ecf8427e",
  "chunk_size": 1048576
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "分块上传初始化成功",
  "data": {
    "upload_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_chunks": 50,
    "chunk_size": 1048576
  }
}
```

---

#### 3.2.2 上传分块

**接口:** `POST /api/images/upload_chunk/`

**权限:** 需认证

**请求格式:** `multipart/form-data`

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| upload_id | string | 是 | 初始化返回的 upload_id |
| chunk_number | integer | 是 | 分块编号（从 1 开始） |
| chunk | file | 是 | 分块文件 |

**请求示例:**
```bash
curl -X POST http://localhost:8000/api/images/upload_chunk/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "upload_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "chunk_number=1" \
  -F "chunk=@chunk_1.dat"
```

**响应示例:**
```json
{
  "code": 200,
  "message": "分块 1 上传成功",
  "data": {
    "chunk_number": 1,
    "uploaded_chunks": 1,
    "total_chunks": 50
  }
}
```

---

#### 3.2.3 完成上传

**接口:** `POST /api/images/upload_complete/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| upload_id | string | 是 | 初始化返回的 upload_id |
| album | integer | 否 | 相册 ID |
| title | string | 否 | 图片标题 |
| description | string | 否 | 图片描述 |
| tags | array | 否 | 标签数组 |
| is_public | boolean | 否 | 是否公开 |

**请求示例:**
```json
{
  "upload_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "大图片",
  "description": "通过分块上传的图片",
  "tags": ["测试"],
  "is_public": false
}
```

**响应示例:**
```json
{
  "code": 201,
  "message": "图片上传成功",
  "data": {
    "id": 2,
    "album": null,
    "filename": "large_image.jpg",
    "file_size": 52428800,
    "file_hash": "d41d8cd98f00b204e9800998ecf8427e",
    "width": 4096,
    "height": 2160,
    "format": "JPEG",
    "title": "大图片",
    "description": "通过分块上传的图片",
    "tags": ["测试"],
    "is_public": false,
    "access_count": 0,
    "storage_backend": "local",
    "url": "http://localhost:8000/media/images/large_image.jpg",
    "user_username": "testuser",
    "album_name": null,
    "created_at": "2026-03-31T16:00:00Z",
    "updated_at": "2026-03-31T16:00:00Z"
  }
}
```

---

## 4. 图片管理接口

### 4.1 获取图片列表

**接口:** `GET /api/images/`

**权限:** 需认证

**查询参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| album | integer | 否 | 按相册 ID 筛选 |
| is_public | boolean | 否 | 按是否公开筛选 |
| format | string | 否 | 按图片格式筛选（JPEG, PNG 等） |
| search | string | 否 | 搜索标题、描述、文件名 |
| ordering | string | 否 | 排序字段，如 `-created_at`, `file_size` |
| page | integer | 否 | 页码 |

**请求示例:**
```
GET /api/images/?album=1&is_public=true&ordering=-created_at&page=1
```

**响应示例:**
```json
{
  "code": 200,
  "count": 100,
  "next": "http://localhost:8000/api/images/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "album": null,
      "filename": "image.jpg",
      "file_size": 1024000,
      "file_hash": "d41d8cd98f00b204e9800998ecf8427e",
      "width": 1920,
      "height": 1080,
      "format": "JPEG",
      "title": "测试图片",
      "description": "",
      "tags": [],
      "is_public": true,
      "access_count": 10,
      "storage_backend": "local",
      "url": "http://localhost:8000/media/images/image.jpg",
      "user_username": "testuser",
      "album_name": null,
      "created_at": "2026-03-31T16:00:00Z",
      "updated_at": "2026-03-31T16:00:00Z"
    }
  ]
}
```

---

### 4.2 获取单张图片详情

**接口:** `GET /api/images/{id}/`

**权限:** 需认证

**响应示例:** 同图片列表中的单个对象

---

### 4.3 删除图片

**接口:** `DELETE /api/images/{id}/`

**权限:** 需认证

**响应示例:**
```json
{
  "code": 200,
  "message": "图片删除成功"
}
```

---

### 4.4 预览图片

**接口:** `GET /api/images/{id}/preview/`

**权限:** 需认证（私有图片仅所有者可访问）

**响应示例:**
```json
{
  "code": 200,
  "data": {
    "url": "http://localhost:8000/media/images/image.jpg",
    "width": 1920,
    "height": 1080,
    "format": "JPEG"
  }
}
```

---

### 4.5 获取公开图片列表

**接口:** `GET /api/images/public/`

**权限:** 无需认证

**响应示例:** 同图片列表

---

## 5. 相册管理接口

### 5.1 创建相册

**接口:** `POST /api/images/albums/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 相册名称 |
| description | string | 否 | 相册描述 |
| is_public | boolean | 否 | 是否公开，默认 false |

**请求示例:**
```json
{
  "name": "旅行照片",
  "description": "2026 年旅行照片集",
  "is_public": true
}
```

**响应示例:**
```json
{
  "code": 201,
  "data": {
    "id": 1,
    "name": "旅行照片",
    "description": "2026 年旅行照片集",
    "cover": null,
    "is_public": true,
    "image_count": 0,
    "user_username": "testuser",
    "created_at": "2026-03-31T16:00:00Z",
    "updated_at": "2026-03-31T16:00:00Z"
  }
}
```

---

### 5.2 获取相册列表

**接口:** `GET /api/images/albums/`

**权限:** 需认证

**查询参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| is_public | boolean | 否 | 按是否公开筛选 |

**响应示例:**
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "旅行照片",
      "description": "2026 年旅行照片集",
      "cover": "http://localhost:8000/media/images/cover.jpg",
      "is_public": true,
      "image_count": 25,
      "user_username": "testuser",
      "created_at": "2026-03-31T16:00:00Z",
      "updated_at": "2026-03-31T16:00:00Z"
    }
  ]
}
```

---

### 5.3 获取相册详情

**接口:** `GET /api/images/albums/{id}/`

**权限:** 需认证

**响应示例:** 同相册列表中的单个对象

---

### 5.4 更新相册

**接口:** `PUT /api/images/albums/{id}/` 或 `PATCH /api/images/albums/{id}/`

**权限:** 需认证（仅相册所有者）

**请求参数:** 同创建相册

---

### 5.5 删除相册

**接口:** `DELETE /api/images/albums/{id}/`

**权限:** 需认证（仅相册所有者）

**响应示例:**
```json
{
  "code": 200,
  "message": "相册删除成功"
}
```

---

## 6. 图片处理接口

所有图片处理接口都是异步的，会立即返回任务 ID，后台使用 Celery 处理。

### 6.1 处理图片（通用）

**接口:** `POST /api/process/process/{image_id}/`

**权限:** 需认证（仅图片所有者）

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| operations | array | 是 | 操作数组，每个操作包含 type 和 params |

**支持的操作类型:**

1. **resize** - 调整尺寸
   ```json
   {
     "type": "resize",
     "params": {
       "width": 800,
       "height": 600,
       "maintain_aspect": true
     }
   }
   ```

2. **compress** - 压缩
   ```json
   {
     "type": "compress",
     "params": {
       "quality": 85,
       "format": "JPEG"
     }
   }
   ```

3. **convert** - 格式转换
   ```json
   {
     "type": "convert",
     "params": {
       "target_format": "PNG"
     }
   }
   ```

4. **watermark** - 添加水印
   ```json
   {
     "type": "watermark",
     "params": {
       "watermark_text": "© My Website",
       "position": "bottom-right",
       "opacity": 128
     }
   }
   ```

**完整请求示例:**
```json
{
  "operations": [
    {
      "type": "resize",
      "params": {
        "width": 800,
        "height": 600,
        "maintain_aspect": true
      }
    },
    {
      "type": "compress",
      "params": {
        "quality": 85,
        "format": "JPEG"
      }
    }
  ]
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "图片处理任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_id": 1,
    "status": "processing"
  }
}
```

---

### 6.2 批量处理图片

**接口:** `POST /api/process/batch_process/`

**权限:** 需认证

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_ids | array | 是 | 图片 ID 数组 |
| operations | array | 是 | 操作数组 |

**请求示例:**
```json
{
  "image_ids": [1, 2, 3],
  "operations": [
    {
      "type": "compress",
      "params": {
        "quality": 85,
        "format": "JPEG"
      }
    }
  ]
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "批量处理任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_count": 3,
    "status": "processing"
  }
}
```

---

### 6.3 压缩图片

**接口:** `POST /api/process/compress/{image_id}/`

**权限:** 需认证（仅图片所有者）

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quality | integer | 否 | 质量 1-100，默认 85 |
| format | string | 否 | 目标格式 |

**请求示例:**
```json
{
  "quality": 75,
  "format": "WEBP"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "压缩任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_id": 1
  }
}
```

---

### 6.4 转换图片格式

**接口:** `POST /api/process/convert/{image_id}/`

**权限:** 需认证（仅图片所有者）

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| target_format | string | 是 | 目标格式（JPEG, PNG, WEBP 等） |

**请求示例:**
```json
{
  "target_format": "PNG"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "格式转换任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_id": 1
  }
}
```

---

### 6.5 调整图片尺寸

**接口:** `POST /api/process/resize/{image_id}/`

**权限:** 需认证（仅图片所有者）

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| width | integer | 否 | 目标宽度 |
| height | integer | 否 | 目标高度 |
| maintain_aspect | boolean | 否 | 保持宽高比，默认 true |

**注意:** width 和 height 至少提供一个

**请求示例:**
```json
{
  "width": 800,
  "height": 600,
  "maintain_aspect": true
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "尺寸调整任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_id": 1
  }
}
```

---

### 6.6 添加水印

**接口:** `POST /api/process/watermark/{image_id}/`

**权限:** 需认证（仅图片所有者）

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| watermark_text | string | 是 | 水印文本 |
| position | string | 否 | 位置，默认 bottom-right |
| opacity | integer | 否 | 透明度 0-255，默认 128 |

**position 可选值:** top-left, top-right, bottom-left, bottom-right, center

**请求示例:**
```json
{
  "watermark_text": "© My Website",
  "position": "bottom-right",
  "opacity": 128
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "水印添加任务已提交",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "image_id": 1
  }
}
```

---

## 7. 健康检查接口

### 7.1 健康检查

**接口:** `GET /health/`

**权限:** 无需认证

**响应示例:**
```json
{
  "status": "healthy",
  "timestamp": 1711900800,
  "services": {
    "database": "healthy",
    "redis": "healthy"
  },
  "response_time_ms": 5
}
```

---

### 7.2 就绪检查

**接口:** `GET /health/ready/`

**权限:** 无需认证

**响应示例:**
```json
{
  "status": "ready"
}
```

---

### 7.3 存活检查

**接口:** `GET /health/live/`

**权限:** 无需认证

**响应示例:**
```json
{
  "status": "alive"
}
```

---

## 附录：错误响应格式

所有错误响应遵循统一格式：

```json
{
  "code": 400,
  "message": "错误描述",
  "details": {
    "field_name": ["具体错误信息"]
  },
  "status_code": 400
}
```

### 常见错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或 token 无效 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 快速开始示例

### Python 完整示例

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# 1. 注册
register_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'password123',
    'password_confirm': 'password123'
}
response = requests.post(f'{BASE_URL}/auth/register/', json=register_data)
tokens = response.json()['data']['tokens']
access_token = tokens['access']

# 2. 上传图片
headers = {'Authorization': f'Bearer {access_token}'}
files = {'file': open('test.jpg', 'rb')}
data = {
    'title': '测试图片',
    'is_public': True
}
response = requests.post(
    f'{BASE_URL}/images/upload/',
    headers=headers,
    files=files,
    data=data
)
image_id = response.json()['data']['id']

# 3. 压缩图片
process_data = {
    'quality': 85,
    'format': 'WEBP'
}
response = requests.post(
    f'{BASE_URL}/process/compress/{image_id}/',
    headers=headers,
    json=process_data
)
task_id = response.json()['data']['task_id']

print(f'处理任务 ID: {task_id}')
```

---

## API 文档在线查看

启动服务后，可以访问以下地址查看交互式 API 文档：

- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`
