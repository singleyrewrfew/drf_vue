<template>
    <AuthLayout
        subtitle="欢迎回来，请登录您的账号"
        footer-text="还没有账号？"
        footer-link="/register"
        footer-link-text="立即注册"
    >
        <template #form>
            <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin"
                     class="auth-form">
                <transition-group name="field-fade" appear>
                    <!-- 用户名 -->
                    <el-form-item key="username" prop="username">
                        <div class="form-group">
                            <label class="form-label">用户名</label>
                            <AuthInput
                                v-model="form.username"
                                type="text"
                                placeholder="请输入您的用户名"
                            >
                                <template #icon>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                        <circle cx="12" cy="7" r="4"/>
                                    </svg>
                                </template>
                            </AuthInput>
                        </div>
                    </el-form-item>

                    <!-- 密码 -->
                    <el-form-item key="password" prop="password">
                        <div class="form-group">
                            <label class="form-label">密码</label>
                            <AuthInput
                                v-model="form.password"
                                :type="showPassword ? 'text' : 'password'"
                                placeholder="请输入密码"
                            >
                                <template #icon>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="11" width="18" height="11" rx="2.5" ry="2.5"/>
                                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                    </svg>
                                </template>
                                <template #suffix>
                                    <PasswordToggle v-model="showPassword"/>
                                </template>
                            </AuthInput>
                        </div>
                    </el-form-item>
                </transition-group>

                <!-- 登录按钮 -->
                <ActionButton
                    type="primary" size="normal"
                    :text="loading ? '登录中...' : '登 录'"
                    :icon="loading ? '' : 'arrowRight'"
                    :icon-after="!loading"
                    :disabled="loading"
                    html-type="submit"
                />
            </el-form>
        </template>
    </AuthLayout>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {ElMessage} from 'element-plus'
import {useUserStore} from '@/stores/user'
import AuthLayout from './AuthLayout.vue'
import AuthInput from '@/components/AuthInput.vue'
import PasswordToggle from '@/components/PasswordToggle.vue'
import ActionButton from '@/components/ActionButton.vue'
import { extractErrorMessage } from '@/api/index.js'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const showPassword = ref(false)

const form = reactive({ username: '', password: '' })

const rules = {
    username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
    password: [{required: true, message: '请输入密码', trigger: 'blur'}],
}

onMounted(() => {
    if (route.query.error === 'no_permission') {
        ElMessage.error(route.query.message || '您没有访问后台管理系统的权限，请联系管理员')
    }
})

const handleLogin = async () => {
    await formRef.value.validate()
    loading.value = true
    try {
        const data = await userStore.login(form)
        if (!data.user?.is_staff) {
            await userStore.logout()
            ElMessage.error('您没有访问后台管理系统的权限，请联系管理员')
            return
        }
        ElMessage.success('登录成功')
        await router.push(route.query.redirect || '/dashboard')
    } catch (error) {
        ElMessage.error(extractErrorMessage(error, '登录失败'))
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
/* 字段依次淡入 + 上滑 */
.field-fade-enter-active {
    transition: all 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}
.field-fade-enter-from {
    opacity: 0;
    transform: translateY(8px);
}
/* 第一个字段延迟 0ms，第二个延迟 80ms */
.field-fade-enter-active:nth-child(2) { transition-delay: 0ms; }
.field-fade-enter-active:nth-child(3) { transition-delay: 80ms; }
</style>
