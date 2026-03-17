# 前台系统代码审查计划

## 审查范围
- 目录: `front/src/`
- 审查日期: 2026-03-17
- 审查重点: 重复代码、组件化设计、性能隐患、潜在错误

---

## 一、重复实现的业务逻辑模块

### 问题 1: 工具函数重复定义 (高优先级)

**问题描述**: 多个视图文件中重复定义了相同的工具函数

**涉及文件及代码位置**:

| 函数名 | 重复位置 |
|--------|----------|
| `getCoverUrl` | Home.vue:207-211, Articles.vue:184-188, Category.vue, Tag.vue, Search.vue |
| `getArticleUrl` | Home.vue:213-215, Articles.vue:190-192, Category.vue, Tag.vue, Search.vue |
| `formatDate` | Home.vue:223-227, Articles.vue:194-198, Profile.vue:221-224 |
| `getAvatarUrl` | Home.vue:217-221, Profile.vue:144-148, FrontLayout.vue:187-191 |

**代码示例** (Home.vue):
```javascript
const getCoverUrl = (coverImage) => {
  if (!coverImage) return 'https://picsum.photos/800/400?random=' + Math.random()
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const getArticleUrl = (article) => {
  return `/article/${article.slug || article.id}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
```

**优化建议**:
1. 创建 `front/src/utils/index.js` 统一存放工具函数
2. 各视图文件从工具模块导入使用

**预期收益**: 减少约 50+ 行重复代码，便于统一维护和修改

---

### 问题 2: 硬编码的 API 基础 URL (高优先级)

**问题描述**: `http://localhost:8001` 在多个文件中硬编码

**涉及文件**:
- [Home.vue:210](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/views/Home.vue#L210)
- [Articles.vue:187](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/views/Articles.vue#L187)
- [Profile.vue:147](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/views/Profile.vue#L147)
- [FrontLayout.vue:190](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/layouts/FrontLayout.vue#L190)

**代码示例**:
```javascript
return `http://localhost:8001${coverImage}`
```

**优化建议**:
1. 使用环境变量 `import.meta.env.VITE_API_BASE_URL` (已在 api/index.js 中配置)
2. 或创建统一的 URL 构建函数

**预期收益**: 便于环境切换，避免生产环境部署问题

---

## 二、未被抽离为公共组件的功能代码

### 问题 3: 登录/注册页面大量重复代码 (中优先级)

**问题描述**: Login.vue 和 Register.vue 存在高度相似的代码结构

**重复内容**:
1. 背景动画 HTML 结构 (bg-animation, bg-gradient, bg-shapes)
2. 背景动画 CSS 样式 (约 120 行)
3. 社交登录按钮 HTML 和 CSS (约 50 行)
4. fadeInUp 动画定义
5. 表单样式

**代码示例** (Login.vue 和 Register.vue 几乎相同的背景动画):
```html
<div class="bg-animation">
  <div class="bg-gradient"></div>
  <div class="bg-shapes">
    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
  </div>
</div>
```

**优化建议**:
1. 创建 `AuthLayout.vue` 公共布局组件
2. 将背景动画抽取为独立 CSS 或组件
3. 创建 `SocialLoginButtons.vue` 组件

---

### 问题 4: 文章卡片组件重复实现 (中优先级)

**问题描述**: 文章卡片在 Home.vue 和 Articles.vue 中有不同的实现

**Home.vue 文章卡片**: 网格布局，带封面图
**Articles.vue 文章卡片**: 列表布局，横向排列

**优化建议**:
1. 创建 `ArticleCard.vue` 组件，支持不同布局模式 (grid/list)
2. 通过 props 控制显示样式

---

### 问题 5: 侧边栏组件重复 (中优先级)

**问题描述**: 热门文章、分类导航、热门标签侧边栏在多个页面重复

**涉及文件**:
- Home.vue (侧边栏)
- Articles.vue (侧边栏)

**优化建议**:
1. 创建 `SidebarHotArticles.vue` 组件
2. 创建 `SidebarCategories.vue` 组件
3. 创建 `SidebarTags.vue` 组件
4. 创建 `SidebarAuthors.vue` 组件

---

## 三、模块间功能重叠或冗余逻辑

### 问题 6: WinDropdown 和 WinSelect 组件功能重叠 (低优先级)

**问题描述**: 两个组件都实现了下拉菜单功能，存在代码重复

**重复代码**:
- 点击外部关闭逻辑
- 位置计算逻辑
- Teleport 到 body
- 动画效果

**优化建议**:
1. 提取公共的下拉定位逻辑到 composable
2. 或合并为一个更通用的组件

---

### 问题 7: CSS 动画重复定义 (低优先级)

**问题描述**: fadeInUp 动画在多个文件中重复定义

**涉及文件**:
- Login.vue:261-270
- Register.vue:340-349
- Articles.vue:353-362
- Profile.vue:395-404
- variables.css:144-153 (已有全局定义)

**代码示例**:
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**优化建议**:
1. 删除各组件中的重复定义
2. 统一使用 variables.css 中的全局动画类

---

## 四、组件化设计问题

### 问题 8: 缺少公共 UI 组件库 (中优先级)

**问题描述**: 项目创建了自定义组件 (WinDropdown, WinPagination, WinSelect)，但缺少更多可复用组件

**建议创建的组件**:
1. `ArticleCard.vue` - 文章卡片
2. `Avatar.vue` - 用户头像 (带 URL 处理)
3. `EmptyState.vue` - 空状态展示
4. `LoadingSkeleton.vue` - 加载骨架屏
5. `SidebarCard.vue` - 侧边栏卡片容器

---

## 五、语法错误、逻辑漏洞及性能隐患

### 问题 9: 调试代码残留 (高优先级)

**问题描述**: stores/user.js 中存在大量 console.log 调试语句

**涉及文件**: [front/src/stores/user.js:56-79](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/stores/user.js#L56)

**代码示例**:
```javascript
console.log('前台：Starting profile check timer')
console.log('前台：Checking profile for updates...')
console.log('前台：Old user:', user.value)
console.log('前台：New user:', data)
console.log('前台：User info changed, updating...')
console.log('前台：No changes detected')
console.log('前台：Profile check timer set to run every 5 seconds')
```

**优化建议**: 删除所有调试日志

---

### 问题 10: Profile 检查频率过高 (高优先级)

**问题描述**: 用户信息检查定时器间隔为 5 秒，频率过高

**涉及文件**: [front/src/stores/user.js:78](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/stores/user.js#L78)

**代码示例**:
```javascript
}, 5000)  // 每 5 秒检查一次
```

**优化建议**:
1. 将间隔调整为 30 秒或更长
2. 或改用 WebSocket 实现实时更新
3. 或仅在用户主动操作时检查

**预期收益**: 减少不必要的 API 请求，降低服务器负载

---

### 问题 11: 并行请求过多 (中优先级)

**问题描述**: Home.vue 的 fetchData 函数同时发起 5 个并行请求

**涉及文件**: [front/src/views/Home.vue:235-241](file:///c:/Users/ZQY/Desktop/drf_vue/front/src/views/Home.vue#L235)

**代码示例**:
```javascript
const [featuredRes, latestRes, hotRes, catRes, tagRes] = await Promise.all([
  getContents({ status: 'published', is_top: true, limit: 5 }),
  getContents({ status: 'published', offset: offset, limit: pageSize.value }),
  getContents({ status: 'published', ordering: '-view_count', limit: 8 }),
  getCategories(),
  getTags(),
])
```

**优化建议**:
1. 考虑后端提供聚合 API
2. 或使用缓存策略减少重复请求

---

### 问题 12: 错误处理不一致 (低优先级)

**问题描述**: 不同组件的错误处理方式不统一

**示例**:
- Home.vue: 检查 `e.response?.status !== 401`
- Articles.vue: 仅显示错误消息
- Profile.vue: 简单的 try-catch

**优化建议**:
1. 创建统一的错误处理工具函数
2. 在 API 拦截器中统一处理常见错误

---

## 六、实施优先级

### 高优先级 (立即处理)
1. **问题 1**: 创建工具函数模块，消除重复代码
2. **问题 2**: 修复硬编码 URL
3. **问题 9**: 删除调试代码
4. **问题 10**: 降低 Profile 检查频率

### 中优先级 (近期处理)
5. **问题 3**: 重构登录/注册页面
6. **问题 4**: 创建 ArticleCard 组件
7. **问题 5**: 抽取侧边栏组件
8. **问题 8**: 建立公共组件库
9. **问题 11**: 优化并行请求

### 低优先级 (后续处理)
10. **问题 6**: 重构下拉组件
11. **问题 7**: 清理重复 CSS 动画
12. **问题 12**: 统一错误处理

---

## 七、预期优化效果

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 重复代码行数 | ~200+ 行 | ~20 行 |
| 硬编码 URL | 6 处 | 0 处 |
| 调试日志 | 7 处 | 0 处 |
| API 请求频率 | 5秒/次 | 30秒/次 |
| 公共组件数 | 3 个 | 8+ 个 |

---

## 八、实施步骤

### 第一阶段: 工具函数抽取
1. 创建 `front/src/utils/index.js`
2. 迁移 getCoverUrl, getAvatarUrl, getArticleUrl, formatDate
3. 更新所有视图文件的导入

### 第二阶段: 修复关键问题
1. 修复硬编码 URL
2. 删除调试代码
3. 调整 Profile 检查间隔

### 第三阶段: 组件抽取
1. 创建 ArticleCard 组件
2. 创建侧边栏组件
3. 重构登录/注册页面

### 第四阶段: 代码清理
1. 删除重复 CSS 动画
2. 统一错误处理
3. 优化 API 请求策略
