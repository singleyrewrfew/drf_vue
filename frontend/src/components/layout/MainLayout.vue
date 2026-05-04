<template>
    <el-container class="main-layout">
        <el-aside :width="isCollapsed ? '72px' : '240px'" class="aside" :class="{ collapsed: isCollapsed }">
            <div class="sidebar">
                <div class="logo" :class="{ collapsed: isCollapsed }">
                    <div class="logo-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                            <path d="M2 17l10 5 10-5"/>
                            <path d="M2 12l10 5 10-5"/>
                        </svg>
                    </div>
                    <h2 class="logo-title" :class="{ collapsed: isCollapsed }">CMS 管理</h2>
                </div>
                <nav class="nav-menu" ref="navMenuRef">
                    <div class="menu-indicator" :style="indicatorStyle"/>
                    <template v-for="(menuSection, sectionIndex) in menuSections" :key="sectionIndex">
                        <div class="menu-section" v-show="!isCollapsed">
                            <span class="menu-section-title">{{ menuSection.section }}</span>
                        </div>
                        <router-link
                            v-for="item in menuSection.items"
                            :key="item.path"
                            :to="item.path"
                            class="menu-item"
                            :class="{ active: activeMenu === item.path, collapsed: isCollapsed }"
                            :title="isCollapsed ? item.label : ''"
                        >
                            <div class="menu-item-icon">
                                <el-icon><component :is="item.icon"/></el-icon>
                            </div>
                            <span class="menu-item-text">{{ item.label }}</span>
                        </router-link>
                    </template>
                </nav>
                <div class="sidebar-footer">
                    <div class="user-card" :class="{ collapsed: isCollapsed }">
                        <div class="avatar-wrapper" @click="toggleCollapse"
                             :title="isCollapsed ? '展开侧边栏' : '收起侧边栏'">
                            <el-avatar :size="40"
                                       :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)">
                                <el-icon><UserFilled/></el-icon>
                            </el-avatar>
                            <div class="collapse-icon">
                                <el-icon>
                                    <ArrowLeft v-if="!isCollapsed"/>
                                    <ArrowRight v-else/>
                                </el-icon>
                            </div>
                        </div>
                        <div class="user-info" v-show="!isCollapsed">
                            <span class="user-name">{{ userStore.user?.username }}</span>
                            <span class="user-role">{{ userStore.user?.role_name || '用户' }}</span>
                        </div>
                        <el-dropdown trigger="click" placement="top-start" v-show="!isCollapsed" @click.stop>
                            <div class="user-actions" @click.stop title="设置">
                                <el-icon><Setting/></el-icon>
                            </div>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item @click="$router.push('/profile')">个人设置</el-dropdown-item>
                                    <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </div>
                </div>
            </div>
        </el-aside>
        <el-container>
            <el-header class="header">
                <div class="header-left">
                    <span class="current-page">{{ currentPageTitle }}</span>
                </div>
                <div class="header-right">
                    <button class="theme-toggle" @click="toggleTheme"
                            :title="themeStore.theme === 'light' ? '切换到暗色模式' : '切换到亮色模式'">
                        <el-icon v-if="themeStore.theme === 'light'"><Moon/></el-icon>
                        <el-icon v-else><Sunny/></el-icon>
                    </button>
                </div>
            </el-header>
            <el-main class="main">
                <router-view/>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import {ref, computed, watch, onMounted, nextTick} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user'
import {useThemeStore} from '@/stores/theme'
import {
    Odometer,
    Document,
    Folder,
    PriceTag,
    Picture,
    ChatDotRound,
    User,
    UserFilled,
    Setting,
    Key,
    Lock,
    ArrowLeft,
    ArrowRight,
    Moon,
    Sunny
} from '@element-plus/icons-vue'
import {getAvatarUrl} from '@/utils'

const RAW_MENU = [
    {
        section: '主菜单',
        items: [
            {path: '/dashboard', icon: Odometer, label: '仪表盘'},
            {path: '/contents', icon: Document, label: '内容管理'},
            {path: '/categories', icon: Folder, label: '分类管理'},
            {path: '/tags', icon: PriceTag, label: '标签管理'},
            {path: '/media', icon: Picture, label: '媒体管理'},
            {path: '/comments', icon: ChatDotRound, label: '评论管理'},
        ]
    },
    {
        section: '系统管理',
        requireAdmin: true,
        items: [
            {path: '/users', icon: User, label: '用户管理'},
            {path: '/roles', icon: Key, label: '角色管理'},
            {path: '/permissions', icon: Lock, label: '权限管理'},
        ]
    }
]

// 额外页面标题（不在菜单中的页面）
const EXTRA_TITLES = {
    '/contents/create': '新建内容',
    '/profile': '个人设置',
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const isCollapsed = ref(false)
const navMenuRef = ref(null)

// Win11 NavigationView SelectionIndicator — 基于 WinUI 源码还原
//
// 原理（来源：Uno Platform / microsoft-ui-xaml）：
//   动画时长: 600ms
//   缓动曲线:
//     Frame1 (位移/缩放中段): cubic-bezier(0.9, 0.1, 1.0, 0.2)
//     Frame2 (结束减速):     cubic-bezier(0.1, 0.9, 0.2, 1.0)
//     Step easing 在起始阶段制造"瞬跳"效果 (IsFinalStepSingleFrame)
//   Scale: beginSize / targetSize → 不同尺寸项间自然拉伸/压缩
//   CenterPoint: 独立 200ms 过渡，控制缩放锚点
//   Opacity: 旧指示器保持到 ~33% 时间点后渐隐
const indicatorStyle = ref({ top: '0px', height: '0px', opacity: 0 })

// 匹配 WinUI 的动画参数
const DURATION_MS = 400    // web 下 600ms 偏慢，用 400ms 更敏捷
const TARGET_H = 26

const updateIndicator = (animate = true) => {
    nextTick(() => {
        if (!navMenuRef.value) return
        const activeItem = navMenuRef.value.querySelector('.menu-item.active')
        if (!activeItem) { indicatorStyle.value.opacity = 0; return }

        const el = navMenuRef.value.querySelector('.menu-indicator')
        const menuRect = navMenuRef.value.getBoundingClientRect()
        const itemRect = activeItem.getBoundingClientRect()
        const newTop = itemRect.top - menuRect.top + (itemRect.height - TARGET_H) / 2

        // 首次 / 收起展开 / 无动画标记 → 直接到位
        if (!animate || !el || indicatorStyle.value.opacity !== 1) {
            Object.assign(indicatorStyle.value, { top: `${newTop}px`, height: `${TARGET_H}px`, opacity: 1 })
            return
        }

        const oldTop = parseFloat(indicatorStyle.value.top)
        const distance = Math.abs(newTop - oldTop)

        // 相邻项切换距离太近，直接滑动无拉扯
        if (distance < 8) {
            indicatorStyle.value.top = `${newTop}px`
            return
        }

        // ====== Win11 三阶段动画 ======
        //
        // 阶段 1 [0ms]：瞬跳拉伸 —— 模拟 StepEasingFunction 的 IsFinalStepSingleFrame
        //   height 瞬间增大，模拟"头部被粘住、尾部被拉长"
        //   这一步必须绕过 Vue 响应式，用 DOM 直接操作 + 强制重绘
        //
        // 阶段 2 [0→400ms]：CSS transition 接管 —— top 滑向目标 + height 收缩回正常
        //   使用 WinUI Frame1 曲线 cubic-bezier(0.9, 0.1, 1.0, 0.2)
        //   top 先行（快）→ height 后跟（稍慢+延迟）= 拉扯感

        el.style.transition = 'none'

        // WinUI 中 Scale = beginSize / targetSize，同尺寸项时 scale ≈ 1
        // 我们用 height 拉伸模拟：拉伸量与距离成正比，但有上限
        const stretchAmount = Math.min(distance * 0.4, TARGET_H * 0.7)
        el.style.height = `${TARGET_H + stretchAmount}px`

        // ★ 关键：强制浏览器同步重绘，确保拉伸帧被绘制
        void el.offsetHeight

        requestAnimationFrame(() => {
            // 恢复 transition → 后续赋值会触发 CSS 动画
            el.style.transition = ''

            // 同时设置 top 和 height → CSS 各自按自己的 timing-function 独立过渡
            // top 快（Frame1），height 慢一点且延迟（Frame2）→ 产生"头先到尾后追"的拉扯
            indicatorStyle.value.top = `${newTop}px`
            indicatorStyle.value.height = `${TARGET_H}px`
        })
    })
}

// 根据权限过滤菜单 + 自动生成标题映射
const menuSections = computed(() =>
    RAW_MENU.filter(s => !s.requireAdmin || userStore.isAdmin())
)

const pageTitles = computed(() => {
    const map = {}
    menuSections.value.forEach(s => s.items.forEach(i => { map[i.path] = i.label }))
    return { ...map, ...EXTRA_TITLES }
})

const toggleCollapse = () => { isCollapsed.value = !isCollapsed.value }
const toggleTheme = () => { themeStore.toggleTheme() }
const activeMenu = computed(() => route.path)

const currentPageTitle = computed(() => {
    const path = route.path
    if (path.includes('/contents/edit/')) return '编辑内容'
    return pageTitles.value[path] || 'CMS 管理'
})

const handleLogout = async () => {
    try { await userStore.logout() }
    catch (error) { console.error('Logout error:', error) }
    finally { router.replace({ name: 'Login' }) }
}

watch(activeMenu, () => updateIndicator(true))
watch(isCollapsed, () => updateIndicator(false))
onMounted(() => updateIndicator(false))
</script>

<style scoped>
.main-layout {
    height: 100vh;
    background: var(--bg-color);
}

/* ---- 侧边栏 ---- */
.aside {
    background: var(--sidebar-bg);
    overflow: hidden;
    transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border-right: 1px solid var(--sidebar-border);
}

.sidebar {
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* ---- Logo ---- */
.logo {
    height: 40px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 12px 12px;
}

.logo.collapsed { justify-content: center; padding: 20px 16px 12px; }

.logo-icon {
    width: 36px; height: 36px;
    background: var(--primary-color);
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.logo.collapsed .logo-icon { width: 40px; height: 40px; }

.logo-icon svg { width: 20px; height: 20px; color: #fff; }
.logo.collapsed .logo-icon svg { width: 18px; height: 18px; }

.logo h2 {
    margin: 0;
    font-size: 15px; font-weight: 600;
    color: var(--sidebar-text);
    white-space: nowrap;
    transition: opacity 0.2s ease, width 0.25s ease 0.05s;
    overflow: hidden;
}
.logo-title.collapsed { opacity: 0; width: 0; }

/* ---- 导航菜单 ---- */
.nav-menu {
    flex: 1;
    padding: 4px 8px;
    overflow-y: auto;
    position: relative;
}
.aside.collapsed .nav-menu { padding: 4px 4px; }

.nav-menu::-webkit-scrollbar { width: 0; }

/* Win11 NavigationView SelectionIndicator — 基于微软 WinUI 源码还原 */
.menu-indicator {
    position: absolute;
    left: 6px;
    width: 3px;
    border-radius: 3px;
    background: var(--primary-color);
    pointer-events: none;
    opacity: 0;
    z-index: 1;

    /*
     * WinUI 源码中的三阶段缓动（来源：Uno Platform / microsoft-ui-xaml）：
     *
     *   StepEasingFunction (起始): IsFinalStepSingleFrame=true
     *     → JS 层用 DOM 直接操作 + 强制重绘模拟
     *
     *   Frame1 — cubic-bezier(0.9, 0.1, 1.0, 0.2)  用于 Offset/位移
     *     → 映射到 top：快速起步，缓慢收尾（"头部先滑过去"）
     *
     *   Frame2 — cubic-bezier(0.1, 0.9, 0.2, 1.0)  用于 Scale/缩放
     *     → 映射到 height：慢速起步，快速收尾（"尾部后追上来"）
     *
     *   top 比 height 快 50ms 且无延迟 → 制造拉扯感
     */
    transition:
        top     0.36s cubic-bezier(0.9, 0.1, 1.0, 0.2),
        height  0.40s cubic-bezier(0.1, 0.9, 0.2, 1.0) 0.03s,
        opacity  0.15s ease;
}

.menu-section {
    margin-top: 16px; margin-bottom: 4px;
    padding: 0 16px; height: 20px;
    display: flex; align-items: center;
}
.menu-section:first-child { margin-top: 8px; }
.menu-section-title { font-size: 12px; font-weight: 400; color: var(--sidebar-text-secondary); }

/* ---- 菜单项 ---- */
.menu-item {
    display: flex; align-items: center; gap: 16px;
    height: 40px; padding: 0 12px; margin: 2px 0;
    border-radius: var(--radius-sm); color: var(--sidebar-text);
    text-decoration: none;
    transition: background-color 0.15s ease, color 0.15s ease;
    position: relative;
}
.menu-item.collapsed { justify-content: center; padding: 0 16px; gap: 0; }

.menu-item:hover { background: var(--sidebar-hover-bg); }
.menu-item.active { background: var(--sidebar-active-bg); color: var(--primary-color); }

.menu-item-icon { width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.menu-item-icon .el-icon { font-size: 18px; }

.menu-item-text {
    font-size: 14px; font-weight: 400; white-space: nowrap;
    transition: opacity 0.2s ease 0.05s, width 0.25s ease 0.05s;
    overflow: hidden;
}
.menu-item.collapsed .menu-item-text { opacity: 0; width: 0; }

/* ---- 底部用户区 ---- */
.sidebar-footer {
    padding: 8px;
    border-top: 1px solid var(--sidebar-border);
}

.user-card {
    display: flex; align-items: center; gap: 12px;
    padding: 8px; border-radius: var(--radius-sm);
    cursor: pointer; position: relative;
}
.user-card.collapsed { justify-content: center; padding: 8px; gap: 0; }

.user-card:hover { background: var(--sidebar-hover-bg); }

.avatar-wrapper { position: relative; flex-shrink: 0; width: 36px; height: 36px; }
.avatar-wrapper :deep(.el-avatar) { width: 36px !important; height: 36px !important; min-width: 36px; min-height: 36px; }

.collapse-icon {
    position: absolute; top: -4px; right: -4px;
    width: 16px; height: 16px;
    background: var(--primary-color); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    opacity: 0; transform: scale(0.8);
    transition: opacity 0.15s ease, transform 0.15s ease;
}
.user-card:hover .collapse-icon { opacity: 1; transform: scale(1); }
.collapse-icon .el-icon { font-size: 10px; color: #fff; }

.user-info {
    flex: 1; display: flex; flex-direction: column; gap: 2px;
    min-width: 0; overflow: hidden;
    transition: opacity 0.2s ease 0.05s, width 0.25s ease 0.05s;
}
.user-name { font-size: 13px; font-weight: 600; color: var(--sidebar-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 12px; color: var(--sidebar-text-secondary); }

.user-actions {
    width: 28px; height: 28px; border-radius: var(--radius-xs);
    display: flex; align-items: center; justify-content: center;
    color: var(--sidebar-text-secondary); cursor: pointer;
    transition: background 0.1s ease;
}
.user-actions:hover { background: var(--sidebar-hover-bg); color: var(--sidebar-text); }

/* ---- 头部 ---- */
.header {
    background: var(--card-bg);
    box-shadow: none;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px;
    border-bottom: 1px solid var(--border-color);
    height: 48px;
}

.header-left { display: flex; align-items: center; gap: 8px; }
.current-page { font-size: 14px; font-weight: 600; color: var(--text-primary); }

.header-right { display: flex; align-items: center; gap: 8px; }

.theme-toggle {
    width: 32px; height: 32px; border-radius: var(--radius-sm);
    background: transparent; border: none;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; color: var(--text-secondary);
    transition: background 0.15s ease, color 0.15s ease;
}
.theme-toggle:hover { background: var(--bg-secondary); color: var(--text-primary); }

/* ---- 主内容区 ---- */
.main {
    background: var(--bg-color);
    padding: 20px;
}
</style>
