<template>
    <div class="login-container">
        <!-- 背景 -->
        <div class="login-background">
            <div class="bg-shape bg-shape-1"></div>
            <div class="bg-shape bg-shape-2"></div>
            <div class="bg-shape bg-shape-3"></div>
        </div>
        <!-- 登录卡片 -->
        <div class="login-card">
            <div class="login-header">
                <div class="logo">
                    <div class="logo-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                            <path d="M2 17l10 5 10-5"/>
                            <path d="M2 12l10 5 10-5"/>
                        </svg>
                    </div>
                    <h1>CMS 管理</h1>
                </div>
                <p class="subtitle">欢迎回来，请登录您的账号</p>
            </div>
            <!--
            :model="form" —— 表单数据对象
            :rules="rules" —— 校验规则（验证器）
            -->
            <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin" class="login-form">
                <el-form-item prop="username">
                    <div class="form-group">
                        <label class="form-label">用户名</label>
                        <div class="input-wrapper">
                            <div class="input-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                    <circle cx="12" cy="7" r="4"/>
                                </svg>
                            </div>
                            <input v-model="form.username" type="text" placeholder="请输入用户名" class="form-input"/>
                        </div>
                    </div>
                </el-form-item>

                <el-form-item prop="password">
                    <div class="form-group">
                        <label class="form-label">密码</label>
                        <div class="input-wrapper">
                            <div class="input-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                </svg>
                            </div>
                            <input v-model="form.password" :type="showPassword ? 'text' : 'password'"
                                   placeholder="请输入密码" class="form-input"/>
                            <div class="input-suffix" @click="showPassword = !showPassword">
                                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                     stroke-width="2">
                                    <path
                                        d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                                    <line x1="1" y1="1" x2="23" y2="23"/>
                                </svg>
                                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                    <circle cx="12" cy="12" r="3"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </el-form-item>

                <button type="submit" class="login-btn" :disabled="loading">
                    <span v-if="!loading">登录</span>
                    <span v-else class="loading-spinner"></span>
                </button>
            </el-form>

            <div class="login-footer">
                <p>还没有账号？
                    <router-link to="/register">立即注册</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, reactive} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {ElMessage} from 'element-plus'
import {useUserStore} from '@/stores/user'

//router 是用来 操作路由（跳转、前进、后退）
const router = useRouter()
//route 是用来 读取当前页面地址信息（路径、参数、查询串）
const route = useRoute()
// 用户状态管理
const userStore = useUserStore()

/*
登录表单引用
与模板 ref="formRef" 同名
挂载前：formRef.value === undefined
onMounted 后：formRef.value → 表单实例
*/
const formRef = ref()
// 按钮状态
const loading = ref(false)
// 密码是否显示
const showPassword = ref(false)
// 登录表单数据
const form = reactive({
    username: '',
    password: '',
})

// 校验规则
const rules = {
    username: [{required: true, message: '请输入用户名', trigger: 'blur'}],  // blur：输入框失去焦点时校验
    password: [{required: true, message: '请输入密码', trigger: 'blur'}],
}

onMounted(() => {
    /*
    组件挂载后（页面刚打开）
    检查 URL 里是否有查询参数 ?error=no_permission
    如果有，就用 Element Plus 弹出红色错误提示
    优先显示路由带的 message 参数，没有就用默认文案
    */
    if (route.query.error === 'no_permission') {
        ElMessage.error(route.query.message || '您没有访问后台管理系统的权限，请联系管理员')
    }
})

// 处理登录
const handleLogin = async () => {
    // 1. 表单校验（Element Plus）
    await formRef.value.validate()
    // 2. 开启加载状态（防重复提交）
    /*按钮置灰、显示 “登录中...”，防止用户重复点击提交*/
    loading.value = true
    try {
        // 3. 调用Pinia的userStore登录Action
        const data = await userStore.login(form)

        // 4. 权限判断：是否是后台管理员（is_staff）
        if (!data.user?.is_staff) {
            // 无权限 → 强制登出、提示、终止
            await userStore.logout()
            ElMessage.error('您没有访问后台管理系统的权限，请联系管理员')
            return
        }
        // 5. 登录+权限都成功 → 提示+跳转
        ElMessage.success('登录成功')
        const redirect = route.query.redirect || '/dashboard'
        await router.push(redirect)
    } catch (error) {
        // 6. 捕获所有错误：表单校验失败/接口报错
        ElMessage.error(error.response?.data?.error || '登录失败')
    } finally {
        // 7. 无论成功/失败，关闭loading
        loading.value = false
    }
}
</script>

<style scoped>
.login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    position: relative;
    overflow: hidden;
    padding: 20px;
}

.login-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
}

.bg-shape {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
}

.bg-shape-1 {
    width: 600px;
    height: 600px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    top: -200px;
    right: -200px;
    animation: float 20s ease-in-out infinite;
}

.bg-shape-2 {
    width: 400px;
    height: 400px;
    background: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
    bottom: -100px;
    left: -100px;
    animation: float 15s ease-in-out infinite reverse;
}

.bg-shape-3 {
    width: 300px;
    height: 300px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: pulse 10s ease-in-out infinite;
}

@keyframes float {
    0%, 100% {
        transform: translate(0, 0);
    }
    50% {
        transform: translate(30px, 30px);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.1;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.1);
        opacity: 0.15;
    }
}

.login-card {
    width: 100%;
    max-width: 420px;
    background: var(--card-bg);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
}

.login-header {
    text-align: center;
    margin-bottom: 32px;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 12px;
}

.logo-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
}

.logo-icon svg {
    width: 28px;
    height: 28px;
    color: #fff;
}

.logo h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.input-wrapper {
    display: flex;
    align-items: center;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.input-wrapper:focus-within {
    background: var(--bg-primary);
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px var(--primary-bg);
}

.input-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    flex-shrink: 0;
}

.input-icon svg {
    width: 20px;
    height: 20px;
}

.form-input {
    flex: 1;
    height: 48px;
    border: none;
    background: transparent;
    font-size: 15px;
    color: var(--text-primary);
    outline: none;
}

.form-input::placeholder {
    color: var(--text-tertiary);
}

.input-suffix {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: color 0.3s ease;
    flex-shrink: 0;
}

.input-suffix:hover {
    color: var(--primary-color);
}

.input-suffix svg {
    width: 20px;
    height: 20px;
}

.login-btn {
    height: 50px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
    position: relative;
    overflow: hidden;
}

.login-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.login-btn:hover::before {
    left: 100%;
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 120, 212, 0.5);
}

.login-btn:active {
    transform: translateY(0);
}

.login-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
}

.loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    display: inline-block;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.login-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border-color);
}

.login-footer p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

.login-footer a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.login-footer a:hover {
    color: var(--primary-hover);
}

:deep(.el-form-item) {
    margin-bottom: 0;
}

:deep(.el-form-item__error) {
    padding-top: 4px;
    padding-left: 12px;
}
</style>
