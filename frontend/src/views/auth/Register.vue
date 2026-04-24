<template>
    <div class="register-container">
        <div class="register-background">
            <div class="bg-shape bg-shape-1"></div>
            <div class="bg-shape bg-shape-2"></div>
            <div class="bg-shape bg-shape-3"></div>
        </div>
        <div class="register-card">
            <div class="register-header">
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
                <p class="subtitle">创建您的账号</p>
            </div>

            <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleRegister" class="register-form">
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

                <el-form-item prop="email">
                    <div class="form-group">
                        <label class="form-label">邮箱</label>
                        <div class="input-wrapper">
                            <div class="input-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path
                                        d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                    <polyline points="22,6 12,13 2,6"/>
                                </svg>
                            </div>
                            <input v-model="form.email" type="email" placeholder="请输入邮箱" class="form-input"/>
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

                <el-form-item prop="password_confirm">
                    <div class="form-group">
                        <label class="form-label">确认密码</label>
                        <div class="input-wrapper">
                            <div class="input-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                </svg>
                            </div>
                            <input v-model="form.password_confirm" :type="showPasswordConfirm ? 'text' : 'password'"
                                   placeholder="请再次输入密码" class="form-input"/>
                            <div class="input-suffix" @click="showPasswordConfirm = !showPasswordConfirm">
                                <svg v-if="!showPasswordConfirm" viewBox="0 0 24 24" fill="none" stroke="currentColor"
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

                <button type="submit" class="register-btn" :disabled="loading">
                    <span v-if="!loading">注册</span>
                    <span v-else class="loading-spinner"></span>
                </button>
            </el-form>

            <div class="register-footer">
                <p>已有账号？
                    <router-link to="/login">立即登录</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {register} from '@/api/user'

// 处理路由跳转
const router = useRouter()

const formRef = ref()
const loading = ref(false)
const showPassword = ref(false)
const showPasswordConfirm = ref(false)
const form = reactive({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
})

const validatePassword = (rule, value, callback) => {
    if (value !== form.password) {
        callback(new Error('两次密码不一致'))
    } else {
        callback()
    }
}

const rules = {
    username: [
        {required: true, message: '请输入用户名', trigger: 'blur'},
        {min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur'},
    ],
    email: [
        {required: true, message: '请输入邮箱', trigger: 'blur'},
        {type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur'},
    ],
    password: [
        {required: true, message: '请输入密码', trigger: 'blur'},
        {min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur'},
    ],
    password_confirm: [
        {required: true, message: '请确认密码', trigger: 'blur'},
        {validator: validatePassword, trigger: 'blur'},
    ],
}

const handleRegister = async () => {
    // 校验表单
    await formRef.value.validate()
    loading.value = true
    try {
        await register(form)
        ElMessage.success('注册成功，请登录')
        await router.push('/login')
    } catch (error) {
        ElMessage.error(error.response?.data?.detail || '注册失败')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.register-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    position: relative;
    overflow: hidden;
    padding: 20px;
}

.register-background {
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
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
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

.register-card {
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

.register-header {
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

.register-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
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

.register-btn {
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
    margin-top: 8px;
}

.register-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.register-btn:hover::before {
    left: 100%;
}

.register-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 120, 212, 0.5);
}

.register-btn:active {
    transform: translateY(0);
}

.register-btn:disabled {
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

.register-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border-color);
}

.register-footer p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

.register-footer a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.register-footer a:hover {
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
