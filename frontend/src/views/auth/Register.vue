<template>
    <AuthLayout
        subtitle="创建您的账号"
        footer-text="已有账号？"
        footer-link="/login"
        footer-link-text="立即登录"
    >
        <template #form>
            <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleRegister"
                     class="auth-form">
                <transition-group name="reg-field" appear>
                    <!-- 用户名 -->
                    <el-form-item key="username" prop="username">
                        <div class="form-group">
                            <label class="form-label">用户名</label>
                            <AuthInput
                                v-model="form.username"
                                type="text"
                                placeholder="设置您的用户名"
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

                    <!-- 邮箱 -->
                    <el-form-item key="email" prop="email">
                        <div class="form-group">
                            <label class="form-label">邮箱</label>
                            <AuthInput
                                v-model="form.email"
                                type="email"
                                placeholder="example@mail.com"
                            >
                                <template #icon>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="2" y="4" width="20" height="16" rx="2.5" ry="2.5"/>
                                        <polyline points="22,7 13,14 2,7"/>
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
                                :type="showPwd ? 'text' : 'password'"
                                placeholder="至少 6 位字符"
                            >
                                <template #icon>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="11" width="18" height="11" rx="2.5" ry="2.5"/>
                                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                    </svg>
                                </template>
                                <template #suffix>
                                    <PasswordToggle v-model="showPwd"/>
                                </template>
                            </AuthInput>
                        </div>
                    </el-form-item>

                    <!-- 确认密码 -->
                    <el-form-item key="confirm" prop="password_confirm">
                        <div class="form-group">
                            <label class="form-label">确认密码</label>
                            <AuthInput
                                v-model="form.password_confirm"
                                :type="showConfirmPwd ? 'text' : 'password'"
                                placeholder="再次输入密码"
                            >
                                <template #icon>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                    </svg>
                                </template>
                                <template #suffix>
                                    <PasswordToggle v-model="showConfirmPwd"/>
                                </template>
                            </AuthInput>
                        </div>
                    </el-form-item>
                </transition-group>

                <!-- 注册按钮 -->
                <ActionButton
                    type="primary" size="normal"
                    :text="loading ? '注册中...' : '注 册'"
                    :icon="loading ? '' : 'plus'"
                    :disabled="loading"
                    html-type="submit"
                />
            </el-form>
        </template>
    </AuthLayout>
</template>

<script setup>
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {register} from '@/api/user'
import AuthLayout from './AuthLayout.vue'
import AuthInput from '@/components/AuthInput.vue'
import PasswordToggle from '@/components/PasswordToggle.vue'
import ActionButton from '@/components/ActionButton.vue'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const showPwd = ref(false)
const showConfirmPwd = ref(false)

const form = reactive({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
})

const validatePassword = (rule, value, callback) => {
    if (!value) callback(new Error('请确认密码'))
    else if (value !== form.password) callback(new Error('两次密码不一致'))
    else callback()
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
    try {
        await formRef.value.validate()
    } catch (error) {
        ElMessage.error('请检查表单填写是否正确')
        return
    }
    loading.value = true
    try {
        await register(form)
        ElMessage.success('注册成功，请登录')
        formRef.value.resetFields()
        Object.assign(form, {username: '', email: '', password: '', password_confirm: ''})
        await router.push({name: 'Login'})
    } catch (error) {
        const errData = error.response?.data
        if (errData) {
            const msg = errData.message || errData.detail ||
                (typeof errData === 'object' ? Object.values(errData)?.[0]?.[0] : null)
            ElMessage.error(msg || '注册失败')
        } else {
            ElMessage.error('注册失败，请稍后重试')
        }
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
/* 注册页四字段依次淡入 */
.reg-field-enter-active {
    transition: all 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}
.reg-field-enter-from {
    opacity: 0;
    transform: translateY(8px);
}
/* 级联延迟：每项递增 65ms */
.reg-field-enter-active:nth-child(2) { transition-delay: 0ms;   }
.reg-field-enter-active:nth-child(3) { transition-delay: 65ms;  }
.reg-field-enter-active:nth-child(4) { transition-delay: 130ms; }
.reg-field-enter-active:nth-child(5) { transition-delay: 195ms; }
</style>
