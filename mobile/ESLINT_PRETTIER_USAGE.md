# ESLint & Prettier 配置说明

## 📋 已添加的工具

### ESLint
- **作用**: 代码质量检查，发现和修复语法错误、最佳实践问题
- **配置**: `.eslintrc.cjs`
- **忽略文件**: `.eslintignore`

### Prettier
- **作用**: 代码格式化，统一代码风格
- **配置**: `.prettierrc.json`

## 🚀 使用方法

### 1. 运行代码检查
```bash
npm run lint
```
自动检查并修复所有 Vue、JS 文件的 ESLint 错误

### 2. 格式化代码
```bash
npm run format
```
格式化 `src/` 目录下所有支持的文件

### 3. VS Code 自动格式化（推荐）

安装了以下扩展后，保存文件时会自动格式化：
- ESLint (dbaeumer.vscode-eslint)
- Prettier - Code formatter (esbenp.prettier-vscode)

**VS Code 扩展推荐：**
```bash
# 在 VS Code 中搜索并安装
- ESLint
- Prettier - Code formatter
- Volar (Vue 开发)
```

## ⚙️ 配置说明

### ESLint 规则亮点
- ✅ 允许单字组件名 (`vue/multi-word-component-names`: off)
- ✅ 允许使用 `v-html` (仅警告，因为需要渲染 Markdown)
- ✅ 忽略以 `_` 开头的未使用变量
- ✅ 自动修复格式问题

### Prettier 配置
- 行宽：100 字符
- 缩进：4 个空格
- 引号：单引号
- 分号：无分号
- 尾随逗号：ES5 标准（对象、数组有尾随逗号）

## 💡 常见问题

### Q: 如何临时禁用某行的 ESLint 检查？
```javascript
// eslint-disable-next-line
const x = anyValue // 这行不会报错

/* eslint-disable */
// 这里的所有代码都不会被 ESLint 检查
/* eslint-enable */
```

### Q: 如何禁用某个文件的检查？
在 `.eslintignore` 文件中添加文件路径

### Q: 格式化后代码变化很大怎么办？
第一次运行时可能会有大量改动，这是正常的。之后的提交就会保持一致了。

## 🎯 最佳实践

1. **保存时自动格式化** - 配置 VS Code 在保存时自动运行 ESLint 和 Prettier
2. **提交前检查** - 在 git commit 前运行 `npm run lint` 和 `npm run format`
3. **团队协作** - 确保团队成员使用相同的配置（配置文件已提交到版本控制）

## 📝 Git Hooks（可选）

如果需要，可以添加 pre-commit hook 自动检查和格式化：

```bash
# 安装 husky
npm install -D husky
npx husky install

# 添加 pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm run format"
```

这样每次 commit 前都会自动检查和格式化代码！
