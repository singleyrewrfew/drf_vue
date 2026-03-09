# 内容管理系统 (CMS) 开发计划

## 项目概述

### 技术栈
- **后端**: Django + Django REST Framework (DRF)
- **前端**: Vue 3 + Vite + Element Plus
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: JWT Token

### 功能模块
1. 用户管理（注册、登录、权限控制）
2. 内容管理（文章/页面的增删改查）
3. 分类与标签管理
4. 媒体文件管理
5. 评论系统
6. 搜索功能

---

## 一、项目结构规划

### 1.1 后端目录结构 (Django)
```
backend/
├── config/                 # 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # 应用模块
│   ├── users/             # 用户管理
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── permissions.py
│   ├── contents/          # 内容管理
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── categories/        # 分类管理
│   ├── tags/              # 标签管理
│   ├── media/             # 媒体管理
│   └── comments/          # 评论管理
├── utils/                  # 工具函数
│   ├── __init__.py
│   ├── pagination.py
│   └── response.py
├── manage.py
└── requirements.txt
```

### 1.2 前端目录结构 (Vue 3)
```
frontend/
├── public/
├── src/
│   ├── api/               # API 接口
│   │   ├── index.js
│   │   ├── user.js
│   │   ├── content.js
│   │   └── category.js
│   ├── assets/            # 静态资源
│   ├── components/        # 公共组件
│   │   ├── common/
│   │   └── layout/
│   ├── composables/       # 组合式函数
│   ├── directives/        # 自定义指令
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── stores/            # Pinia 状态管理
│   │   ├── index.js
│   │   ├── user.js
│   │   └── app.js
│   ├── styles/            # 样式文件
│   ├── utils/             # 工具函数
│   ├── views/             # 页面视图
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── content/
│   │   ├── category/
│   │   └── user/
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

---

## 二、数据库模型设计

### 2.1 用户模型 (User)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| password | VARCHAR(128) | 密码（加密） |
| avatar | ImageField | 头像 |
| role | VARCHAR(20) | 角色：admin/editor/user |
| is_active | Boolean | 是否激活 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 2.2 分类模型 (Category)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | VARCHAR(50) | 分类名称 |
| slug | VARCHAR(50) | URL 别名 |
| parent | ForeignKey | 父分类（支持多级） |
| description | TEXT | 描述 |
| sort_order | Integer | 排序 |
| created_at | DateTime | 创建时间 |

### 2.3 标签模型 (Tag)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | VARCHAR(30) | 标签名称 |
| slug | VARCHAR(30) | URL 别名 |
| created_at | DateTime | 创建时间 |

### 2.4 内容模型 (Content/Article)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| title | VARCHAR(200) | 标题 |
| slug | VARCHAR(200) | URL 别名 |
| summary | TEXT | 摘要 |
| content | LongTextField | 正文内容 |
| cover_image | ImageField | 封面图 |
| author | ForeignKey(User) | 作者 |
| category | ForeignKey(Category) | 分类 |
| tags | ManyToManyField(Tag) | 标签 |
| status | VARCHAR(20) | 状态：draft/published/archived |
| view_count | Integer | 浏览量 |
| is_top | Boolean | 是否置顶 |
| published_at | DateTime | 发布时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 2.5 媒体模型 (Media)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| file | FileField | 文件 |
| filename | VARCHAR(200) | 文件名 |
| file_type | VARCHAR(50) | 文件类型 |
| file_size | Integer | 文件大小 |
| uploader | ForeignKey(User) | 上传者 |
| created_at | DateTime | 上传时间 |

### 2.6 评论模型 (Comment)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| content | TextField | 评论内容 |
| article | ForeignKey(Content) | 关联文章 |
| user | ForeignKey(User) | 评论用户 |
| parent | ForeignKey('self') | 父评论（支持嵌套） |
| is_approved | Boolean | 是否审核通过 |
| created_at | DateTime | 创建时间 |

---

## 三、API 接口设计

### 3.1 用户认证 API
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register/ | 用户注册 |
| POST | /api/auth/login/ | 用户登录 |
| POST | /api/auth/logout/ | 用户登出 |
| POST | /api/auth/refresh/ | 刷新 Token |
| GET | /api/auth/profile/ | 获取当前用户信息 |
| PUT | /api/auth/profile/ | 更新用户信息 |
| PUT | /api/auth/password/ | 修改密码 |

### 3.2 内容管理 API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/contents/ | 获取内容列表（支持分页、筛选） |
| POST | /api/contents/ | 创建内容 |
| GET | /api/contents/{id}/ | 获取内容详情 |
| PUT | /api/contents/{id}/ | 更新内容 |
| DELETE | /api/contents/{id}/ | 删除内容 |
| POST | /api/contents/{id}/publish/ | 发布内容 |
| POST | /api/contents/{id}/archive/ | 归档内容 |

### 3.3 分类管理 API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/categories/ | 获取分类列表 |
| POST | /api/categories/ | 创建分类 |
| GET | /api/categories/{id}/ | 获取分类详情 |
| PUT | /api/categories/{id}/ | 更新分类 |
| DELETE | /api/categories/{id}/ | 删除分类 |

### 3.4 标签管理 API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/tags/ | 获取标签列表 |
| POST | /api/tags/ | 创建标签 |
| PUT | /api/tags/{id}/ | 更新标签 |
| DELETE | /api/tags/{id}/ | 删除标签 |

### 3.5 媒体管理 API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/media/ | 获取媒体列表 |
| POST | /api/media/upload/ | 上传文件 |
| DELETE | /api/media/{id}/ | 删除文件 |

### 3.6 评论管理 API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/comments/ | 获取评论列表 |
| POST | /api/comments/ | 发表评论 |
| PUT | /api/comments/{id}/ | 更新评论 |
| DELETE | /api/comments/{id}/ | 删除评论 |
| POST | /api/comments/{id}/approve/ | 审核通过 |

---

## 四、前端页面规划

### 4.1 公共页面
- 登录页面 `/login`
- 注册页面 `/register`
- 404 页面 `/404`

### 4.2 后台管理页面
- 仪表盘 `/dashboard`
- 内容管理
  - 内容列表 `/dashboard/contents`
  - 创建内容 `/dashboard/contents/create`
  - 编辑内容 `/dashboard/contents/:id/edit`
- 分类管理 `/dashboard/categories`
- 标签管理 `/dashboard/tags`
- 媒体管理 `/dashboard/media`
- 评论管理 `/dashboard/comments`
- 用户管理 `/dashboard/users` (管理员)
- 个人设置 `/dashboard/profile`

---

## 五、开发阶段划分

### 第一阶段：项目初始化（预计 1 天）
1. [ ] 创建 Django 项目结构
2. [ ] 配置 Django 设置（数据库、CORS、JWT 等）
3. [ ] 创建 Vue 项目结构
4. [ ] 配置 Vite、ESLint、Prettier
5. [ ] 安装必要依赖包

### 第二阶段：后端核心功能（预计 3 天）
1. [ ] 实现用户模型和认证系统
2. [ ] 实现分类、标签模型
3. [ ] 实现内容模型和 CRUD
4. [ ] 实现媒体上传功能
5. [ ] 实现评论系统
6. [ ] 编写 API 文档

### 第三阶段：前端核心功能（预计 4 天）
1. [ ] 搭建后台布局框架
2. [ ] 实现登录/注册页面
3. [ ] 实现内容管理页面
4. [ ] 实现分类、标签管理页面
5. [ ] 实现媒体管理页面
6. [ ] 实现评论管理页面
7. [ ] 实现用户管理页面

### 第四阶段：功能完善（预计 2 天）
1. [ ] 实现搜索功能
2. [ ] 实现富文本编辑器集成
3. [ ] 实现图片上传预览
4. [ ] 实现权限控制
5. [ ] 优化用户体验

### 第五阶段：测试与部署（预计 2 天）
1. [ ] 编写单元测试
2. [ ] 编写集成测试
3. [ ] 性能优化
4. [ ] 部署配置
5. [ ] 文档完善

---

## 六、技术要点

### 6.1 后端技术要点
- **认证**: djangorestframework-simplejwt
- **CORS**: django-cors-headers
- **图片处理**: Pillow
- **API 文档**: drf-spectator / drf-yasg
- **分页**: 自定义分页类
- **权限**: 自定义权限类

### 6.2 前端技术要点
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **UI 框架**: Element Plus
- **富文本编辑器**: TinyMCE / Quill
- **路由守卫**: 权限验证
- **请求拦截**: Token 自动刷新

---

## 七、开发规范

### 7.1 代码规范
- Python: PEP 8
- JavaScript: ESLint + Prettier
- Git 提交: Conventional Commits

### 7.2 分支管理
- `main`: 生产分支
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

---

## 八、依赖清单

### 8.1 后端依赖 (requirements.txt)
```
Django>=4.2
djangorestframework>=3.14
djangorestframework-simplejwt>=5.3
django-cors-headers>=4.3
Pillow>=10.0
drf-spectacular>=0.27
python-dotenv>=1.0
```

### 8.2 前端依赖 (package.json)
```json
{
  "dependencies": {
    "vue": "^3.4",
    "vue-router": "^4.2",
    "pinia": "^2.1",
    "axios": "^1.6",
    "element-plus": "^2.5"
  },
  "devDependencies": {
    "vite": "^5.0",
    "@vitejs/plugin-vue": "^5.0",
    "eslint": "^8.56",
    "prettier": "^3.2"
  }
}
```
