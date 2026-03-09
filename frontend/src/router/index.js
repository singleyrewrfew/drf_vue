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

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn()) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && userStore.isLoggedIn()) {
    next({ name: 'Dashboard' })
  } else if (to.meta.requiresAdmin && !userStore.isAdmin()) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
