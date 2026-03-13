import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { guest: true },
  },
  {
    path: '/',
    component: () => import('@/components/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
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
        meta: { requiresAdmin: true },
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('@/views/system/Role.vue'),
        meta: { requiresAdmin: true },
      },
      {
        path: 'permissions',
        name: 'Permissions',
        component: () => import('@/views/system/Permission.vue'),
        meta: { requiresAdmin: true },
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/user/Profile.vue'),
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/auth/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 调试信息
  console.log('Router guard:', {
    to: to.path,
    isLoggedIn: userStore.isLoggedIn(),
    user: userStore.user,
    canAccessBackend: userStore.canAccessBackend(),
    is_staff: userStore.user?.is_staff,
  })

  // 如果需要认证但未登录
  if (to.meta.requiresAuth && !userStore.isLoggedIn()) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // 如果已登录但没有后台访问权限
  if (to.meta.requiresAuth && userStore.isLoggedIn() && !userStore.canAccessBackend()) {
    console.log('No backend access, clearing and redirecting to login')
    // 先清除登录状态
    userStore.token = ''
    userStore.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh')
    // 然后跳转到登录页
    return next({ name: 'Login', query: { error: 'no_permission' } })
  }

  // 如果是访客页面但已登录且有后台权限
  if (to.meta.guest && userStore.isLoggedIn() && userStore.canAccessBackend()) {
    return next({ name: 'Dashboard' })
  }

  // 如果需要管理员权限但不是管理员
  if (to.meta.requiresAdmin && !userStore.isAdmin()) {
    return next({ name: 'Dashboard' })
  }

  next()
})

export default router
