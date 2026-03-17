# 前端代码冗余优化计划

## 一、问题概述

通过对前端代码的全面检查，发现以下主要冗余问题：

| 类别 | 重复文件数 | 估计重复代码行数 | 优化后可减少 |
|------|-----------|-----------------|-------------|
| 登录/注册页面 | 2 | ~300行 | ~250行 |
| 分页逻辑 | 8 | ~200行 | ~160行 |
| 表单提交逻辑 | 5 | ~100行 | ~80行 |
| 删除确认逻辑 | 6 | ~60行 | ~50行 |
| 样式代码 | 7+ | ~150行 | ~120行 |
| 工具函数 | 3 | ~20行 | ~15行 |
| **总计** | - | **~830行** | **~675行** |

---

## 二、优化任务清单

### 阶段一：创建组合式函数（Composables）

#### 任务 1.1：创建 `usePagination.js` 分页逻辑
**影响文件：** 8个列表页面
- `views/category/Index.vue`
- `views/category/Tags.vue`
- `views/content/Index.vue`
- `views/dashboard/Comments.vue`
- `views/dashboard/Media.vue`
- `views/user/Index.vue`
- `views/system/Role.vue`
- `views/system/Permission.vue`

**实现内容：**
```javascript
// composables/usePagination.js
export function usePagination(fetchFn, options = {}) {
  const page = ref(1)
  const pageSize = ref(options.defaultPageSize || 20)
  const total = ref(0)
  const loading = ref(false)
  const data = ref([])
  
  const fetchData = async (params = {}) => { ... }
  const handleSizeChange = () => { ... }
  const handleCurrentChange = () => { ... }
  const reset = () => { ... }
  
  return { page, pageSize, total, loading, data, fetchData, handleSizeChange, handleCurrentChange, reset }
}
```

#### 任务 1.2：创建 `useFormSubmit.js` 表单提交逻辑
**影响文件：** 5个表单页面

**实现内容：**
```javascript
// composables/useFormSubmit.js
export function useFormSubmit(createFn, updateFn, options = {}) {
  const isEdit = ref(false)
  const editingId = ref(null)
  const loading = ref(false)
  const visible = ref(false)
  
  const openCreate = () => { ... }
  const openEdit = (id, data) => { ... }
  const submit = async (formData) => { ... }
  const close = () => { ... }
  
  return { isEdit, editingId, loading, visible, openCreate, openEdit, submit, close }
}
```

#### 任务 1.3：创建 `useDialog.js` 对话框状态管理
**实现内容：**
```javascript
// composables/useDialog.js
export function useDialog() {
  const visible = ref(false)
  const open = () => { visible.value = true }
  const close = () => { visible.value = false }
  const toggle = () => { visible.value = !visible.value }
  return { visible, open, close, toggle }
}
```

---

### 阶段二：创建公共组件

#### 任务 2.1：创建认证页面公共组件
**新建文件：**
- `components/auth/AuthLayout.vue` - 认证页面布局（背景动画+卡片容器）
- `components/auth/AuthInput.vue` - 带图标的输入框组件
- `components/PasswordInput.vue` - 密码输入框（含显示/隐藏切换）

**影响文件：**
- `views/auth/Login.vue`
- `views/auth/Register.vue`
- `views/user/Profile.vue`

#### 任务 2.2：创建 `StatusTag.vue` 状态标签组件
**影响文件：**
- `views/content/Index.vue`
- `views/user/Index.vue`
- `views/dashboard/Comments.vue`

**实现内容：**
```vue
<StatusTag type="success">已发布</StatusTag>
<StatusTag type="warning">草稿</StatusTag>
<StatusTag type="danger">已禁用</StatusTag>
```

#### 任务 2.3：创建 `MediaSelector.vue` 媒体选择器组件
**影响文件：**
- `views/user/Profile.vue`
- `views/content/Form.vue`

---

### 阶段三：统一全局样式

#### 任务 3.1：添加全局公共样式到 `styles/components.css`
**新增样式：**
```css
/* 卡片头部 */
.card-header { ... }

/* 操作按钮区域 */
.action-buttons { ... }

/* 表单输入框 */
.form-input-wrapper { ... }
.form-input-icon { ... }
.form-input { ... }
.form-input-suffix { ... }

/* 页面标题 */
.page-header { ... }
.page-title { ... }
.page-subtitle { ... }
```

#### 任务 3.2：移除各组件中的重复样式
**影响文件：** 7+ 个组件文件

---

### 阶段四：统一工具函数

#### 任务 4.1：完善 `utils/index.js`
**新增函数：**
```javascript
// 确认删除对话框
export async function confirmDelete(message = '确定删除该项？') { ... }

// 带 loading 的异步操作
export async function withLoading(fn, loadingRef) { ... }

// 统一的媒体 URL 处理
export function getMediaUrl(file) { ... }
```

#### 任务 4.2：移除各文件中重复的工具函数定义
**影响文件：**
- `views/user/Profile.vue`
- `views/content/Form.vue`

---

### 阶段五：重构现有页面使用公共组件

#### 任务 5.1：重构列表页面使用 `TablePage` 组件
**影响文件：**
- `views/category/Index.vue`
- `views/category/Tags.vue`
- `views/content/Index.vue`
- `views/dashboard/Comments.vue`
- `views/dashboard/Media.vue`
- `views/user/Index.vue`

#### 任务 5.2：重构表单页面使用 `FormDialog` 组件
**影响文件：**
- `views/category/Index.vue`
- `views/category/Tags.vue`
- `views/user/Index.vue`

---

## 三、执行顺序

1. **第一步：创建组合式函数**
   - 创建 `composables/usePagination.js`
   - 创建 `composables/useFormSubmit.js`
   - 创建 `composables/useDialog.js`

2. **第二步：创建公共组件**
   - 创建 `components/PasswordInput.vue`
   - 创建 `components/StatusTag.vue`
   - 创建 `components/auth/AuthLayout.vue`
   - 创建 `components/auth/AuthInput.vue`

3. **第三步：统一全局样式**
   - 创建 `styles/components.css`
   - 移除各组件重复样式

4. **第四步：完善工具函数**
   - 更新 `utils/index.js`
   - 移除重复定义

5. **第五步：重构现有页面**
   - 重构列表页面
   - 重构表单页面
   - 重构认证页面

---

## 四、预期效果

- **代码量减少：** 约 675 行重复代码
- **维护性提升：** 公共逻辑统一管理
- **一致性提升：** UI 组件风格统一
- **开发效率：** 新页面可快速复用组件

---

## 五、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 重构过程中功能异常 | 中 | 逐个页面重构，每步测试 |
| 公共组件设计不合理 | 低 | 参考现有良好实践 |
| 样式冲突 | 低 | 使用 scoped 样式隔离 |
