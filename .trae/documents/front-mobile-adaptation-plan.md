# 前台移动端适配计划

## 一、适配概述

### 1.1 项目结构

```
front/
├── src/
│   ├── layouts/
│   │   └── FrontLayout.vue    # 主布局组件
│   ├── views/
│   │   ├── Home.vue           # 首页
│   │   ├── Articles.vue       # 文章列表
│   │   ├── Article.vue        # 文章详情
│   │   ├── Category.vue       # 分类页
│   │   ├── Tag.vue            # 标签页
│   │   ├── Search.vue         # 搜索页
│   │   ├── Login.vue          # 登录页
│   │   ├── Register.vue       # 注册页
│   │   └── Profile.vue        # 个人中心
│   └── assets/styles/
│       ├── variables.css      # CSS 变量
│       └── main.css           # 全局样式
```

### 1.2 适配目标

| 断点 | 宽度范围 | 设备类型 |
|------|----------|----------|
| xs | < 576px | 手机竖屏 |
| sm | 576px - 768px | 手机横屏/小平板 |
| md | 768px - 992px | 平板 |
| lg | 992px - 1200px | 小屏电脑 |
| xl | > 1200px | 桌面电脑 |

---

## 二、适配任务清单

### 阶段一：全局样式适配

#### 任务 1.1：添加移动端断点变量
**文件：** `assets/styles/variables.css`

**新增内容：**
```css
:root {
  /* 移动端断点 */
  --breakpoint-xs: 576px;
  --breakpoint-sm: 768px;
  --breakpoint-md: 992px;
  --breakpoint-lg: 1200px;
  
  /* 移动端专用变量 */
  --mobile-header-height: 56px;
  --mobile-padding: 16px;
  --mobile-card-padding: 16px;
}
```

#### 任务 1.2：添加全局移动端样式
**文件：** `assets/styles/main.css`

**新增内容：**
```css
/* 移动端全局适配 */
@media (max-width: 768px) {
  html {
    font-size: 14px;
  }
  
  body {
    -webkit-tap-highlight-color: transparent;
  }
  
  .container {
    padding: 0 var(--mobile-padding);
  }
}
```

---

### 阶段二：布局组件适配

#### 任务 2.1：FrontLayout.vue 导航栏适配
**文件：** `layouts/FrontLayout.vue`

**适配内容：**
1. 导航栏高度调整（64px → 56px）
2. Logo 缩小
3. 导航菜单隐藏，改为汉堡菜单
4. 搜索框改为图标触发
5. 用户菜单改为下拉菜单

**修改点：**
- 添加移动端菜单按钮
- 添加移动端抽屉菜单组件
- 搜索框改为弹窗形式

#### 任务 2.2：移动端抽屉菜单
**新建组件：** `components/MobileMenu.vue`

**功能：**
- 从右侧滑入的抽屉菜单
- 包含导航链接
- 包含用户信息和操作
- 支持主题切换

---

### 阶段三：页面适配

#### 任务 3.1：Home.vue 首页适配
**文件：** `views/Home.vue`

**适配内容：**
1. Hero 区域高度调整
2. 文章卡片改为单列布局
3. 分类标签横向滚动
4. 侧边栏移到底部或隐藏

#### 任务 3.2：Articles.vue 文章列表适配
**文件：** `views/Articles.vue`

**适配内容：**
1. 页面标题缩小
2. 文章卡片改为垂直布局（封面在上）
3. 侧边栏隐藏，改为筛选按钮
4. 分页组件简化

**修改示例：**
```css
@media (max-width: 768px) {
  .article-item {
    flex-direction: column;
  }
  
  .article-cover {
    width: 100%;
    height: 180px;
  }
  
  .sidebar {
    display: none;
  }
}
```

#### 任务 3.3：Article.vue 文章详情适配
**文件：** `views/Article.vue`

**适配内容：**
1. 文章标题字号调整（32px → 24px）
2. 内容区域 padding 调整
3. 侧边栏（目录、相关文章）移到底部
4. 评论区表单适配
5. 图片自适应宽度

**修改示例：**
```css
@media (max-width: 768px) {
  .article-main {
    padding: 20px 16px;
  }
  
  .article-header h1 {
    font-size: 24px;
  }
  
  .sidebar {
    position: static;
    margin-top: 32px;
  }
}
```

#### 任务 3.4：Category.vue / Tag.vue 适配
**文件：** `views/Category.vue`, `views/Tag.vue`

**适配内容：**
1. 页面标题缩小
2. 文章列表适配
3. 侧边栏处理

#### 任务 3.5：Search.vue 搜索页适配
**文件：** `views/Search.vue`

**适配内容：**
1. 搜索框全宽
2. 搜索结果列表适配
3. 筛选条件折叠

#### 任务 3.6：Login.vue / Register.vue 适配
**文件：** `views/Login.vue`, `views/Register.vue`

**适配内容：**
1. 表单卡片全宽
2. 输入框适配
3. 按钮全宽
4. 背景动画简化或隐藏

#### 任务 3.7：Profile.vue 个人中心适配
**文件：** `views/Profile.vue`

**适配内容：**
1. 用户信息卡片适配
2. 表单适配
3. 操作按钮适配

---

### 阶段四：组件适配

#### 任务 4.1：文章卡片组件适配
**影响文件：** `Home.vue`, `Articles.vue`

**适配内容：**
- 封面图片尺寸调整
- 标题字号调整
- 元信息（作者、日期等）换行处理

#### 任务 4.2：评论组件适配
**文件：** `Article.vue`

**适配内容：**
- 评论输入框全宽
- 回复列表缩进调整
- 点赞/回复按钮大小调整

#### 任务 4.3：分页组件适配
**影响文件：** 所有列表页面

**适配内容：**
- 简化分页按钮
- 隐藏页码数量选择器
- 使用"加载更多"按钮替代

---

## 三、执行顺序

### 第一步：全局样式
1. 更新 `variables.css` 添加移动端变量
2. 更新 `main.css` 添加移动端全局样式

### 第二步：布局组件
1. 创建 `MobileMenu.vue` 抽屉菜单组件
2. 更新 `FrontLayout.vue` 添加移动端导航

### 第三步：核心页面
1. 适配 `Articles.vue` 文章列表
2. 适配 `Article.vue` 文章详情
3. 适配 `Home.vue` 首页

### 第四步：其他页面
1. 适配 `Category.vue` / `Tag.vue`
2. 适配 `Search.vue`
3. 适配 `Login.vue` / `Register.vue`
4. 适配 `Profile.vue`

### 第五步：细节优化
1. 触摸反馈优化
2. 滚动性能优化
3. 图片懒加载优化

---

## 四、CSS 适配规范

### 4.1 媒体查询写法

```css
/* 推荐：移动优先 */
.component {
  /* 移动端默认样式 */
  padding: 16px;
}

@media (min-width: 768px) {
  .component {
    /* 平板及以上 */
    padding: 24px;
  }
}

@media (min-width: 992px) {
  .component {
    /* 桌面端 */
    padding: 32px;
  }
}
```

### 4.2 常用适配模式

```css
/* 隐藏/显示 */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
}
@media (min-width: 769px) {
  .mobile-only { display: none !important; }
}

/* 弹性布局 */
@media (max-width: 768px) {
  .flex-row { flex-direction: column; }
}

/* 间距调整 */
@media (max-width: 768px) {
  .section { padding: 16px; }
  .card { padding: 16px; }
  .gap-24 { gap: 12px; }
}
```

---

## 五、预期效果

### 5.1 移动端体验提升
- 导航便捷（汉堡菜单）
- 内容易读（字号、间距合适）
- 操作便捷（按钮大小合适）
- 加载快速（图片懒加载）

### 5.2 保持桌面端体验
- 不影响现有桌面端布局
- 渐进增强，优雅降级

---

## 六、测试清单

- [ ] iPhone SE (375px)
- [ ] iPhone 12/13 (390px)
- [ ] iPhone 14 Pro Max (430px)
- [ ] iPad Mini (768px)
- [ ] iPad Pro (1024px)
- [ ] 横屏模式
- [ ] 暗色模式
- [ ] 触摸交互
- [ ] 滚动性能
