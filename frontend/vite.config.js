/**
 * Vite 构建配置文件
 *
 * 作用：配置 Vue 3 前端项目的开发服务器、代理规则和构建选项
 * 使用：Vite 自动加载此配置文件，无需手动导入
 *
 * 主要配置项：
 *   1. base - 应用部署的基础路径（用于 Django 后台集成）
 *   2. plugins - Vite 插件配置（Vue 支持）
 *   3. resolve.alias - 路径别名配置（简化模块导入）
 *   4. server - 开发服务器配置（端口、API 代理）
 *   5. build - 生产构建配置（输出目录）
 *
 * 开发工作流：
 *   - 运行 npm run dev 启动开发服务器（端口 5173）
 *   - API 请求自动代理到后端 Django 服务（localhost:8000）
 *   - 运行 npm run build 生成生产版本到 dist_backend 目录
 */
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {fileURLToPath, URL} from 'node:url'

/**
 * Vite 配置对象
 *
 * 使用 defineConfig 提供类型提示和更好的 IDE 支持
 */
export default defineConfig({
    /**
     * 应用基础路径
     *
     * 设置为 '/admin/' 以便与 Django 后台路由集成
     * 所有资源引用都会自动添加此前缀
     *
     * 示例：
     *   - HTML 中的 <script src="/admin/assets/index.js">
     *   - CSS 中的 background: url("/admin/images/logo.png")
     *
     * 注意：
     *   - 如果部署在根路径，应改为 '/'
     *   - 需要与 Django 的 STATIC_URL 配置保持一致
     */
    base: '/admin/',

    /**
     * Vite 插件配置
     *
     * 启用 Vue 3 单文件组件（.vue 文件）支持
     * 包括模板编译、样式处理和热模块替换（HMR）
     */
    plugins: [
        vue(),
    ],

    /**
     * 模块解析配置
     *
     * 配置路径别名和模块解析行为
     */
    resolve: {
        /**
         * 路径别名配置
         *
         * 定义 '@' 为 src 目录的别名，简化模块导入路径
         *
         * 使用示例：
         *   - 不使用别名：import Button from '../../components/Button.vue'
         *   - 使用别名：import Button from '@/components/Button.vue'
         *
         * 技术说明：
         *   - fileURLToPath 将 URL 对象转换为文件系统路径
         *   - import.meta.url 是当前模块的 URL
         *   - 这种方式比 __dirname 更符合 ES Module 规范
         */
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },

    /**
     * 开发服务器配置
     *
     * 配置本地开发环境的服务器行为和代理规则
     */
    server: {
        /**
         * 开发服务器端口
         *
         * 设置为 5173（Vite 默认端口）
         * 如果端口被占用，Vite 会自动尝试下一个可用端口
         */
        port: 5173,

        /**
         * 代理配置
         *
         * 将特定路径的请求代理到后端 Django 服务器
         * 解决开发环境的跨域问题（CORS）
         *
         * 工作原理：
         *   1. 前端发起请求到 http://localhost:5173/api/users/
         *   2. Vite 开发服务器拦截该请求
         *   3. 转发到 http://localhost:8000/api/users/
         *   4. 将响应返回给前端
         *
         * 优势：
         *   - 避免跨域问题（浏览器认为请求来自同源）
         *   - 无需在后端配置 CORS
         *   - 保持 API 路径的一致性
         */
        proxy: {
            /**
             * API 请求代理
             *
             * 将所有 /api 开头的请求代理到 Django 后端
             *
             * 示例：
             *   前端：fetch('/api/users/')
             *   实际：http://localhost:8000/api/users/
             */
            '/api': {
                /**
                 * 代理目标地址
                 *
                 * Django 开发服务器的地址和端口
                 */
                target: 'http://localhost:8000',

                /**
                 * 修改请求头中的 Origin 字段为目标 URL
                 *
                 * 设置为 true 可以解决某些后端框架的 CSRF 验证问题
                 * 确保 Host 和 Origin 头与目标服务器一致
                 */
                changeOrigin: true,
            },

            /**
             * 媒体文件代理
             *
             * 将 /media 开头的请求代理到 Django 后端
             * 用于访问用户上传的文件和图片
             *
             * 示例：
             *   前端：<img src="/media/uploads/avatar.jpg">
             *   实际：http://localhost:8000/media/uploads/avatar.jpg
             *
             * 注意：
             *   - 生产环境应使用 Nginx 直接提供媒体文件
             *   - 开发环境通过代理简化配置
             */
            '/media': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },

    /**
     * 生产构建配置
     *
     * 配置执行 npm run build 时的构建行为
     */
    build: {
        /**
         * 输出目录
         *
         * 设置为 'dist_backend' 以便与 Django 项目集成
         *
         * 目录结构：
         *   frontend/
         *   └── dist_backend/       # 构建输出目录
         *       ├── index.html
         *       ├── assets/
         *       │   ├── index.[hash].js
         *       │   └── index.[hash].css
         *       └── ...
         *
         * Django 集成：
         *   - 将此目录配置为 Django 的静态文件目录
         *   - 或使用 WhiteNoise 中间件提供静态文件
         *   - 确保 Django 的 STATICFILES_DIRS 包含此路径
         *
         * 注意：
         *   - 默认值是 'dist'，这里改为 'dist_backend' 以区分
         *   - 每次构建会清空此目录
         */
        outDir: 'dist_backend',
    },
})
