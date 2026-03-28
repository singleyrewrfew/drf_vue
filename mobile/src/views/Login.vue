<template>
    <div class="page">
        <AuthBackground />
        <PageHeader title="登录"/>

        <div class="page-content">
            <div class="login-form">
                <div class="form-group">
                    <input
                        v-model="form.username"
                        class="form-input"
                        placeholder="用户名"
                    />
                </div>

                <div class="form-group">
                    <input
                        v-model="form.password"
                        class="form-input"
                        type="password"
                        placeholder="密码"
                    />
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
import {ref, reactive} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {useUserStore} from '@/stores/user'
import PageHeader from '@/components/PageHeader.vue'
import AuthBackground from '@/components/AuthBackground.vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const form = reactive({
    username: '',
    password: ''
})

const handleLogin = async () => {
    loading.value = true
    try {
        await userStore.login(form)
        ElMessage.success('登录成功')
        router.replace('/')
    } catch (e) {
        console.error(e)
        ElMessage.error('用户名或密码错误')
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
</style>
