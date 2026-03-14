# Element Plus 美化样式说明

## 文件位置
`frontend/src/styles/element-override.css`

## 已引入方式
已在 `frontend/src/main.js` 中引入：
```javascript
import './styles/element-override.css'
```

## 美化内容

### 1. CSS 变量定义
- 主题色：`#409eff` (蓝色)
- 成功色：`#67c23a` (绿色)
- 警告色：`#e6a23c` (橙色)
- 危险色：`#f56c6c` (红色)
- 信息色：`#909399` (灰色)
- 圆角：基础 8px，小 4px，圆 16px
- 字体：Inter, PingFang SC, Microsoft YaHei

### 2. 按钮美化
- 统一圆角 8px
- 添加阴影效果
- Hover 时上移 1px
- 增强阴影效果

### 3. 卡片美化
- 圆角 12px
- 移除边框
- 添加柔和阴影
- Hover 时阴影加深

### 4. 输入框美化
- 圆角 8px
- Focus 时显示主题色边框
- Hover 时边框加深
- 平滑过渡动画

### 5. 表格美化
- 圆角 8px
- 移除边框
- 表头灰色背景
- 斑马纹行
- Hover 高亮效果

### 6. 对话框美化
- 圆角 12px
- 添加阴影
- 头部/底部边框分隔
- 优化内边距

### 7. 分页美化
- 居中对齐
- 圆角按钮
- Hover 主题色

### 8. 标签美化
- 圆角 4px
- 移除边框
- 柔和背景色

### 9. 消息提示美化
- 圆角 8px
- 移除边框
- 添加阴影
- 优化内边距

### 10. 下拉菜单美化
- 圆角 8px
- 添加阴影
- 移除边框
- Hover 高亮

### 11. 菜单美化
- 移除右边框
- Hover 高亮
- Active 状态主题色

### 12. 其他组件
- 标签页、开关、复选框、单选框
- 头像、徽章、面包屑
- 警告框、抽屉、上传
- 气泡提示、树形控件
- 穿梭框、步骤条、时间轴
- 日历、评分、滑块
- 颜色选择器、级联选择器
- 时间选择器、日期选择器
- 数字输入框、回到顶部
- 骨架屏、图片、空状态
- 结果页、分割线、描述列表
- 统计数值、引导提示

## 自定义修改

### 修改主题色
在 `element-override.css` 顶部修改 CSS 变量：
```css
:root {
  --el-color-primary: #你的主题色;
}
```

### 修改圆角
```css
:root {
  --el-border-radius-base: 12px;
  --el-border-radius-small: 6px;
}
```

### 修改字体
```css
:root {
  --el-font-family: '你的字体', sans-serif;
}
```

### 单独修改某个组件
在 `element-override.css` 中找到对应组件的样式，直接修改即可。

## 注意事项

1. **样式优先级**：此文件在 Element Plus 默认样式之后引入，会覆盖默认样式
2. **作用范围**：全局生效，影响所有 Element Plus 组件
3. **兼容性**：支持所有现代浏览器
4. **性能**：使用 CSS 变量，性能良好

## 效果预览

- 按钮悬停有上浮效果
- 卡片有柔和阴影
- 输入框 Focus 时主题色边框
- 表格 Hover 高亮
- 对话框圆角阴影
- 所有组件统一圆角风格

## 移除美化

如需移除美化效果，在 `main.js` 中删除以下行：
```javascript
import './styles/element-override.css'
```
