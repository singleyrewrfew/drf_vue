module.exports = {
    root: true,
    env: {
        browser: true,
        es2021: true,
        node: true,
    },
    extends: ['eslint:recommended', 'plugin:vue/vue3-recommended', 'plugin:prettier/recommended'],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    rules: {
        // Vue 特定规则
        'vue/multi-word-component-names': 'off', // 允许单字组件名

        // Prettier 集成
        'prettier/prettier': 'error',

        // 代码质量规则
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

        // 最佳实践
        'no-unused-vars': [
            'warn',
            {
                varsIgnorePattern: '^_|^props$|^emit$',
                argsIgnorePattern: '^_',
            },
        ],

        // Vue 模板规则
        'vue/no-v-html': 'warn', // 警告而不是错误（因为我们需要 v-html 渲染 Markdown）
        'vue/attribute-hyphenation': ['error', 'always'],
        'vue/component-definition-name-casing': ['error', 'PascalCase'],
    },
}
