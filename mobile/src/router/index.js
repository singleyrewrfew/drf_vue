import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

import MobileLayout from '@/layouts/MobileLayout.vue'
import Home from '@/views/Home.vue'
import Articles from '@/views/Articles.vue'
import Article from '@/views/Article.vue'
import Category from '@/views/Category.vue'
import Tag from '@/views/Tag.vue'
import Search from '@/views/Search.vue'
import Profile from '@/views/Profile.vue'
import ProfileEdit from '@/views/ProfileEdit.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
    {
        path: '/',
        component: MobileLayout,
        children: [
            {
                path: '',
                name: 'Home',
                component: Home,
                meta: { title: '首页', showTabBar: true },
            },
            {
                path: 'articles',
                name: 'Articles',
                component: Articles,
                meta: { title: '文章', showTabBar: true },
            },
            {
                path: 'article/:id',
                name: 'Article',
                component: Article,
                meta: { title: '文章详情' },
            },
            {
                path: 'category/:id_or_slug',
                name: 'Category',
                component: Category,
                meta: { title: '分类' },
            },
            {
                path: 'tag/:id_or_slug',
                name: 'Tag',
                component: Tag,
                meta: { title: '标签' },
            },
            {
                path: 'search',
                name: 'Search',
                component: Search,
                meta: { title: '搜索' },
            },
            {
                path: 'profile',
                name: 'Profile',
                component: Profile,
                meta: { title: '我的', showTabBar: true, requiresAuth: true },
            },
            {
                path: 'profile/edit',
                name: 'ProfileEdit',
                component: ProfileEdit,
                meta: { title: '编辑资料', requiresAuth: true },
            },
        ],
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { title: '登录' },
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { title: '注册' },
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound,
        meta: { title: '页面未找到' },
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

    if (to.meta.requiresAuth && !userStore.isLoggedIn) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
    } else {
        next()
    }
})

export default router
