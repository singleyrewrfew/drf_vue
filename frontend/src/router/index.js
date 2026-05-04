/**
 * Vue Router 路由配置
 *
 * 定义应用的所有路由规则、权限守卫和导航逻辑。
 * 支持基于角色的访问控制（RBAC）和动态路由跳转。
 */
import {createRouter, createWebHistory} from 'vue-router'
import {useUserStore} from '@/stores/user'
import {refreshToken} from '@/utils/tokenRefresh'

/**
 * 路由规则配置
 */
const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/auth/Login.vue'),
        meta: {guest: true},
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/auth/Register.vue'),
        meta: {guest: true},
    },
    {
        path: '/',
        component: () => import('@/components/layout/MainLayout.vue'),
        meta: {requiresAuth: true},
        children: [
            {
                path: '',
                redirect: '/dashboard',
            },
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('@/views/dashboard/Index.vue'),
            },
            {
                path: 'contents',
                name: 'Contents',
                component: () => import('@/views/content/Index.vue'),
            },
            {
                path: 'contents/create',
                name: 'ContentCreate',
                component: () => import('@/views/content/Form.vue'),
            },
            {
                path: 'contents/:id/edit',
                name: 'ContentEdit',
                component: () => import('@/views/content/Form.vue'),
            },
            {
                path: 'categories',
                name: 'Categories',
                component: () => import('@/views/category/Index.vue'),
            },
            {
                path: 'tags',
                name: 'Tags',
                component: () => import('@/views/category/Tags.vue'),
            },
            {
                path: 'media',
                name: 'Media',
                component: () => import('@/views/dashboard/Media.vue'),
            },
            {
                path: 'comments',
                name: 'Comments',
                component: () => import('@/views/dashboard/Comments.vue'),
            },
            {
                path: 'users',
                name: 'Users',
                component: () => import('@/views/user/Index.vue'),
                meta: {requiresAdmin: true},
            },
            {
                path: 'roles',
                name: 'Roles',
                component: () => import('@/views/system/Role.vue'),
                meta: {requiresAdmin: true},
            },
            {
                path: 'permissions',
                name: 'Permissions',
                component: () => import('@/views/system/Permission.vue'),
                meta: {requiresAdmin: true},
            },
            {
                path: 'profile',
                name: 'Profile',
                component: () => import('@/views/user/Profile.vue'),
            },
        ],
    },
    /**
     * 404 通配符路由
     *
     * 匹配所有未定义的路径，显示 NotFound 页面。
     * pathMatch 参数捕获完整的路径信息。
     */
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/notFound/NotFound.vue'),
    },
]

/**
 * 创建路由器实例
 *
 * 使用 History 模式，基础路径为 /admin/。
 */
const router = createRouter({
    history: createWebHistory('/admin/'),
    routes,
})

/**
 * 全局前置路由守卫
 *
 * 在每次路由跳转前执行，进行权限验证和导航控制。
 *
 * 权限检查流程：
 * 1. 需要认证但未登录（无 token 或 token 过期且刷新失败）→ 跳转登录页
 * 2. Token 存在但已过期 → 尝试自动刷新，成功则放行，失败跳转登录
 * 3. 已登录但无后台权限 → 清除状态并跳转到登录页
 * 4. 访客页面且已登录 → 重定向到仪表盘或停留
 * 5. 需要管理员权限但非管理员 → 重定向到仪表盘
 *
 * @param {import('vue-router').RouteLocationNormalized} to - 目标路由
 * @param {import('vue-router').RouteLocationNormalizedLoaded} from - 当前路由
 * @param {Function} next - 导航控制函数
 */
router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    // ===== 需要 Auth 的路由处理 =====
    if (to.meta.requiresAuth) {
        // 场景 A：token 完全不存在 → 直接跳转登录
        if (!userStore.accessToken) {
            return next({name: 'Login', query: {redirect: to.fullPath}})
        }

        // 场景 B：token 存在但已过期 → 尝试自动刷新
        if (userStore.isAccessTokenExpired()) {
            try {
                await refreshToken()
                // 刷新成功，继续后续权限检查（不 return，往下走）
            } catch {
                // refresh token 也失效了 → 清除状态并跳转登录
                await userStore.logout()
                return next({name: 'Login', query: {redirect: to.fullPath}})
            }
        }

        // 场景 C：token 有效但仍需验证后台访问权限
        if (!userStore.canAccessBackend()) {
            await userStore.logout()
            return next({name: 'Login', query: {error: 'no_permission'}})
        }
    }

    // ===== 访客页面且已登录 =====
    if (to.meta.guest && userStore.isLoggedIn()) {
        if (userStore.canAccessBackend()) {
            return next({name: 'Dashboard'})
        }
    }

    // ===== 管理员权限校验 =====
    if (to.meta.requiresAdmin && !userStore.isAdmin()) {
        return next({name: 'Dashboard'})
    }

    next()
})

export default router
