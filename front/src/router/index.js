import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

export const ROUTE_NAMES = {
  HOME: 'Home',
  ARTICLES: 'Articles',
  ARTICLE: 'Article',
  ARTICLE_BY_SLUG: 'ArticleBySlug',
  CATEGORY: 'Category',
  TAG: 'Tag',
  SEARCH: 'Search',
  PROFILE: 'Profile',
  LOGIN: 'Login',
  REGISTER: 'Register',
  NOT_FOUND: 'NotFound'
}

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/FrontLayout.vue'),
    children: [
      {
        path: '',
        name: ROUTE_NAMES.HOME,
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'articles',
        name: ROUTE_NAMES.ARTICLES,
        component: () => import('@/views/Articles.vue'),
        meta: { title: '文章列表' }
      },
      {
        path: 'article/:id',
        name: ROUTE_NAMES.ARTICLE,
        component: () => import('@/views/Article.vue'),
        meta: { title: '文章详情' }
      },
      {
        path: 'article/slug/:slug',
        name: ROUTE_NAMES.ARTICLE_BY_SLUG,
        component: () => import('@/views/Article.vue'),
        meta: { title: '文章详情' }
      },
      {
        path: 'category/:id_or_slug',
        name: ROUTE_NAMES.CATEGORY,
        component: () => import('@/views/Category.vue'),
        meta: { title: '分类' }
      },
      {
        path: 'tag/:id_or_slug',
        name: ROUTE_NAMES.TAG,
        component: () => import('@/views/Tag.vue'),
        meta: { title: '标签' }
      },
      {
        path: 'search',
        name: ROUTE_NAMES.SEARCH,
        component: () => import('@/views/Search.vue'),
        meta: { title: '搜索' }
      },
      {
        path: 'profile',
        name: ROUTE_NAMES.PROFILE,
        component: () => import('@/views/Profile.vue'),
        meta: { requiresAuth: true, title: '个人中心' }
      },
    ],
  },
  {
    path: '/login',
    name: ROUTE_NAMES.LOGIN,
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', guestOnly: true }
  },
  {
    path: '/register',
    name: ROUTE_NAMES.REGISTER,
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册', guestOnly: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: ROUTE_NAMES.NOT_FOUND,
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.title) {
    document.title = `${to.meta.title} - CMS`
  }
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: ROUTE_NAMES.LOGIN, query: { redirect: to.fullPath } })
    return
  }
  
  if (to.meta.guestOnly && userStore.isLoggedIn) {
    next({ name: ROUTE_NAMES.HOME })
    return
  }
  
  next()
})

export default router
