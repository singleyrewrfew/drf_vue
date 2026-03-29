<template>
    <div class="page">
        <AuthBackground />
        <PageHeader title="注册" />

        <div class="page-content">
            <div class="register-form">
                <div class="form-group">
                    <input v-model="form.username" class="form-input" placeholder="用户名" />
                </div>

                <div class="form-group">
                    <input
                        v-model="form.email"
                        class="form-input"
                        type="email"
                        placeholder="邮箱"
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

                <div class="form-group">
                    <input
                        v-model="form.password2"
                        class="form-input"
                        type="password"
                        placeholder="确认密码"
                    />
                </div>

                <button
                    class="btn btn-primary btn-block btn-lg"
                    :disabled="loading || !isFormValid"
                    @click="handleRegister"
                >
                    {{ loading ? '注册中...' : '注册' }}
                </button>

                <div class="form-footer">
                    <span class="form-footer-text">已有账号？</span>
                    <router-link to="/login" class="form-footer-link">立即登录</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/user'
import PageHeader from '@/components/PageHeader.vue'
import AuthBackground from '@/components/AuthBackground.vue'

const router = useRouter()

const loading = ref(false)
const form = reactive({
    username: '',
    email: '',
    password: '',
    password2: '',
})

const isFormValid = computed(() => {
    return form.username && form.email && form.password && form.password === form.password2
})

const handleRegister = async () => {
    if (form.password !== form.password2) {
        ElMessage.error('两次密码不一致')
        return
    }

    loading.value = true
    try {
        await register({
            username: form.username,
            email: form.email,
            password: form.password,
        })
        ElMessage.success('注册成功，请登录')
        router.push('/login')
    } catch (e) {
        console.error(e)
        ElMessage.error('注册失败，请重试')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.register-form {
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
