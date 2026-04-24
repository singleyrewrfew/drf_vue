import {createRouter, createWebHistory} from 'vue-router'
import {useUserStore} from '@/stores/user'

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
        meta: {guest: true},  // 标记：仅访客
    },
    {
        path: '/',
        component: () => import('@/components/layout/MainLayout.vue'),
        meta: {requiresAuth: true},  // 标记：需登录
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
    /* Vue 3 专用语法，用来匹配任意 URL
      :pathMatch：自定义参数名，被捕获的路径会存在 $route.params.pathMatch 里。
      (.*)：正则表达式，匹配任意字符（包括 /）。
      末尾的 *：表示参数可重复 0 次或多次，能正确捕获多级路径（/a/b/c）。
    */
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/notFound/NotFound.vue'),
    },
]

const router = createRouter({
    // 配置路由历史模式（History模式，URL不带#）
    history: createWebHistory('/admin/'),
    routes,  // 路由规则数组
})

/* Vue Router 全局前置守卫的异步写法，核心用于：路由跳转前，执行异步操作
to：即将进入的目标路由（如 to.path、to.meta）Vue Router
from：当前正要离开的路由Vue Router
next：必须调用的函数，决定导航是否放行
*/
router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    // 如果需要认证但未登录
    // 前提：路由配置时必须定义 meta: { requiresAuth: true }
    if (to.meta.requiresAuth && !userStore.isLoggedIn()) {
        return next({name: 'Login', query: {redirect: to.fullPath}})
    }

    // 如果已登录但没有后台访问权限，且访问的是需要认证的页面
    if (to.meta.requiresAuth && userStore.isLoggedIn() && !userStore.canAccessBackend()) {
        // 先清除登录状态
        await userStore.logout()
        // 然后跳转到登录页
        return next({name: 'Login', query: {error: 'no_permission'}})
    }

    // 如果是访客页面（如登录/注册页）且已登录
    if (to.meta.guest && userStore.isLoggedIn()) {
        // 如果有后台权限，跳转到后台
        if (userStore.canAccessBackend()) {
            return next({name: 'Dashboard'})
        }
        // 如果没有后台权限，停留在登录页（让用户重新登录）
    }

    // 如果需要管理员权限但不是管理员
    if (to.meta.requiresAdmin && !userStore.isAdmin()) {
        return next({name: 'Dashboard'})
    }

    next()
})

export default router
