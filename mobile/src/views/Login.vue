<template>
    <div class="page">
        <AuthBackground />
        <PageHeader title="登录" />

        <div class="page-content">
            <div class="login-form">
                <div class="form-group">
                    <input
                        v-model="form.username"
                        class="form-input"
                        :class="{ 'is-invalid': errors.username }"
                        placeholder="用户名"
                        @blur="validateUsername"
                    />
                    <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
                </div>

                <div class="form-group">
                    <input
                        v-model="form.password"
                        class="form-input"
                        :class="{ 'is-invalid': errors.password }"
                        type="password"
                        placeholder="密码"
                        @blur="validatePassword"
                    />
                    <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
                </div>

                <button
                    class="btn btn-primary btn-block btn-lg"
                    :disabled="loading || !form.username || !form.password"
                    @click="handleLogin"
                >
                    {{ loading ? '登录中...' : '登录' }}
                </button>

                <div class="form-footer">
                    <span class="form-footer-text">还没有账号？</span>
                    <router-link to="/register" class="form-footer-link">立即注册</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import PageHeader from '@/components/PageHeader.vue'
import AuthBackground from '@/components/AuthBackground.vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const form = reactive({
    username: '',
    password: '',
})

const errors = reactive({
    username: '',
    password: '',
})

const validateUsername = () => {
    if (!form.username.trim()) {
        errors.username = '请输入用户名'
        return false
    }
    if (form.username.length < 3) {
        errors.username = '用户名至少 3 个字符'
        return false
    }
    errors.username = ''
    return true
}

const validatePassword = () => {
    if (!form.password) {
        errors.password = '请输入密码'
        return false
    }
    if (form.password.length < 6) {
        errors.password = '密码至少 6 个字符'
        return false
    }
    errors.password = ''
    return true
}

const handleLogin = async () => {
    // 先验证所有字段
    const isUsernameValid = validateUsername()
    const isPasswordValid = validatePassword()

    if (!isUsernameValid || !isPasswordValid) {
        return
    }

    loading.value = true
    try {
        await userStore.login(form)
        ElMessage.success('登录成功')
        router.replace('/')
    } catch (e) {
        console.error(e)
        // 清除密码但不清空用户名，方便用户重试
        form.password = ''
        ElMessage.error('用户名或密码错误，请重试')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-form {
    padding: 40px 20px;
}

.form-group {
    margin-bottom: 16px;
}

.form-input {
    width: 100%;
    padding: 14px 16px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 15px;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-color);
    background: var(--bg-primary);
}

.form-input.is-invalid {
    border-color: #f56c6c;
}

.error-message {
    margin-top: 6px;
    font-size: 12px;
    color: #f56c6c;
}
</style>
