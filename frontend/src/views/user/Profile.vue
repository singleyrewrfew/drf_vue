<template>
    <div class="profile-page">
        <div class="profile-header">
            <h1 class="page-title">个人设置</h1>
            <p class="page-subtitle">管理您的账户信息和安全设置</p>
        </div>

        <div class="profile-content">
            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                    </div>
                    <div class="card-title">
                        <h3>个人信息</h3>
                        <p>您的头像和基本资料</p>
                    </div>
                </div>

                <div class="card-body">
                    <div class="avatar-section">
                        <div class="avatar-wrapper">
                            <el-avatar :size="100"
                                       :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)"/>
                        </div>
                        <div class="avatar-actions">
                            <el-upload
                                class="avatar-upload"
                                :action="uploadUrl"
                                :headers="uploadHeaders"
                                :show-file-list="false"
                                :on-success="handleAvatarSuccess"
                                :on-error="handleAvatarError"
                                name="file"
                                :before-upload="beforeAvatarUpload"
                            >
                                <UploadButtonSmall>上传头像</UploadButtonSmall>
                            </el-upload>
                            <UploadButtonSmall @click="showMediaDialog = true">从媒体库选择</UploadButtonSmall>
                        </div>
                    </div>

                    <div class="info-list">
                        <div class="info-item">
                            <div class="info-label">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                    <circle cx="12" cy="7" r="4"/>
                                </svg>
                                <span>用户名</span>
                            </div>
                            <div class="info-value">{{ userStore.user?.username }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path
                                        d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                    <polyline points="22,6 12,13 2,6"/>
                                </svg>
                                <span>邮箱</span>
                            </div>
                            <div class="info-value">{{ userStore.user?.email }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                </svg>
                                <span>角色</span>
                            </div>
                            <div class="info-value">
                <span class="role-tag" :class="userStore.user?.role_code || 'user'">
                  {{ userStore.user?.role_name || '未分配' }}
                </span>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                                    <line x1="16" y1="2" x2="16" y2="6"/>
                                    <line x1="8" y1="2" x2="8" y2="6"/>
                                    <line x1="3" y1="10" x2="21" y2="10"/>
                                </svg>
                                <span>注册时间</span>
                            </div>
                            <div class="info-value">{{ userStore.user?.created_at }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon success">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                    </div>
                    <div class="card-title">
                        <h3>修改邮箱</h3>
                        <p>更新您的邮箱地址</p>
                    </div>
                </div>

                <div class="card-body">
                    <el-form ref="formRef" :model="form" :rules="rules" class="profile-form">
                        <el-form-item prop="email">
                            <div class="form-group">
                                <label class="form-label">新邮箱</label>
                                <div class="input-wrapper">
                                    <div class="input-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path
                                                d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                            <polyline points="22,6 12,13 2,6"/>
                                        </svg>
                                    </div>
                                    <input v-model="form.email" type="email" placeholder="请输入新邮箱"
                                           class="form-input"/>
                                </div>
                            </div>
                        </el-form-item>
                        <div class="form-actions">
                            <ConfirmButton text="保存修改" @click="handleUpdateProfile" :disabled="loading"/>
                        </div>
                    </el-form>
                </div>
            </div>

            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon warning">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                        </svg>
                    </div>
                    <div class="card-title">
                        <h3>修改密码</h3>
                        <p>定期更换密码可以提高账户安全性</p>
                    </div>
                </div>

                <div class="card-body">
                    <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" class="profile-form">
                        <el-form-item prop="old_password">
                            <div class="form-group">
                                <label class="form-label">原密码</label>
                                <div class="input-wrapper">
                                    <div class="input-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                        </svg>
                                    </div>
                                    <input v-model="passwordForm.old_password"
                                           :type="showOldPassword ? 'text' : 'password'" placeholder="请输入原密码"
                                           class="form-input"/>
                                    <div class="input-suffix" @click="showOldPassword = !showOldPassword">
                                        <svg v-if="showOldPassword" viewBox="0 0 24 24" fill="none"
                                             stroke="currentColor" stroke-width="2">
                                            <path
                                                d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                                            <line x1="1" y1="1" x2="23" y2="23"/>
                                        </svg>
                                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                             stroke-width="2">
                                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                            <circle cx="12" cy="12" r="3"/>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </el-form-item>
                        <el-form-item prop="new_password">
                            <div class="form-group">
                                <label class="form-label">新密码</label>
                                <div class="input-wrapper">
                                    <div class="input-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                        </svg>
                                    </div>
                                    <input v-model="passwordForm.new_password"
                                           :type="showNewPassword ? 'text' : 'password'" placeholder="请输入新密码"
                                           class="form-input"/>
                                    <div class="input-suffix" @click="showNewPassword = !showNewPassword">
                                        <svg v-if="showNewPassword" viewBox="0 0 24 24" fill="none"
                                             stroke="currentColor" stroke-width="2">
                                            <path
                                                d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                                            <line x1="1" y1="1" x2="23" y2="23"/>
                                        </svg>
                                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                             stroke-width="2">
                                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                            <circle cx="12" cy="12" r="3"/>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </el-form-item>
                        <el-form-item prop="new_password_confirm">
                            <div class="form-group">
                                <label class="form-label">确认新密码</label>
                                <div class="input-wrapper">
                                    <div class="input-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                        </svg>
                                    </div>
                                    <input v-model="passwordForm.new_password_confirm"
                                           :type="showConfirmPassword ? 'text' : 'password'"
                                           placeholder="请再次输入新密码" class="form-input"/>
                                    <div class="input-suffix" @click="showConfirmPassword = !showConfirmPassword">
                                        <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none"
                                             stroke="currentColor" stroke-width="2">
                                            <path
                                                d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                                            <line x1="1" y1="1" x2="23" y2="23"/>
                                        </svg>
                                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                             stroke-width="2">
                                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                            <circle cx="12" cy="12" r="3"/>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </el-form-item>
                        <div class="form-actions">
                            <button type="button" class="save-btn warning" @click="handleChangePassword"
                                    :disabled="passwordLoading">
                                <span v-if="!passwordLoading">修改密码</span>
                                <span v-else class="loading-spinner"></span>
                            </button>
                        </div>
                    </el-form>
                </div>
            </div>
        </div>

        <el-dialog
            v-model="showMediaDialog"
            title="从媒体库选择头像"
            width="800px"
            :close-on-click-modal="false"
        >
            <SearchInput v-model="mediaSearch" placeholder="搜索媒体文件" style="margin-bottom: 16px"/>
            <div class="media-list-container">
                <div class="media-grid" v-loading="mediaLoading">
                    <div
                        v-for="media in filteredMedia"
                        :key="media.id"
                        class="media-card"
                        :class="{ selected: selectedMedia?.id === media.id }"
                        @click="selectedMedia = media"
                    >
                        <img :src="getMediaUrl(media.url)" class="media-image"/>
                        <div class="media-info">
                            <span class="media-name">{{ media.filename }}</span>
                        </div>
                    </div>
                </div>
                <el-empty v-if="!mediaLoading && filteredMedia.length === 0" description="暂无媒体文件"/>
            </div>
            <template #footer>
                <ResetButton text="取消" @click="showMediaDialog = false"/>
                <ConfirmButton text="确定" @click="handleMediaSelect" :disabled="!selectedMedia"/>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {useUserStore} from '@/stores/user'
import {updateProfile, changePassword} from '@/api/user'
import {getAvatarUrl} from '@/utils'
import api from '@/api'
import UploadButtonSmall from '@/components/UploadButtonSmall.vue'
import ConfirmButton from '@/components/ConfirmButton.vue'
import ResetButton from '@/components/ResetButton.vue'
import SearchInput from '@/components/SearchInput.vue'

const userStore = useUserStore()
const formRef = ref()
const passwordFormRef = ref()
const loading = ref(false)
const passwordLoading = ref(false)
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const form = reactive({
    email: '',
})

const passwordForm = reactive({
    old_password: '',
    new_password: '',
    new_password_confirm: '',
})

const rules = {
    email: [
        {required: true, message: '请输入邮箱', trigger: 'blur'},
        {type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur'},
    ],
}

const validatePassword = (rule, value, callback) => {
    if (value !== passwordForm.new_password) {
        callback(new Error('两次密码不一致'))
    } else {
        callback()
    }
}

const passwordRules = {
    old_password: [{required: true, message: '请输入原密码', trigger: 'blur'}],
    new_password: [
        {required: true, message: '请输入新密码', trigger: 'blur'},
        {min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur'},
    ],
    new_password_confirm: [
        {required: true, message: '请确认新密码', trigger: 'blur'},
        {validator: validatePassword, trigger: 'blur'},
    ],
}

const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL || '/api'}/media/`)
const uploadHeaders = computed(() => {
    const token = userStore.token
    return {
        'Authorization': `Bearer ${token}`
    }
})

const beforeAvatarUpload = (file) => {
    const token = userStore.token
    if (!token) {
        ElMessage.error('请先登录')
        return false
    }
    const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type)
    if (!isValidType) {
        ElMessage.error('只能上传 JPG/PNG/GIF/WEBP 格式的图片')
        return false
    }
    const isLt2M = file.size / 1024 / 1024 < 2
    if (!isLt2M) {
        ElMessage.error('头像大小不能超过 2MB')
        return false
    }
    return true
}

const showMediaDialog = ref(false)
const mediaLoading = ref(false)
const mediaList = ref([])
const mediaSearch = ref('')
const selectedMedia = ref(null)

const getMediaUrl = (file) => {
    if (!file) return ''
    if (file.startsWith('http')) return file
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    return `${baseUrl.replace('/api', '')}${file}`
}

const fetchMedia = async () => {
    mediaLoading.value = true
    try {
        const {data} = await api.get('/media/', {params: {limit: 50}})
        mediaList.value = data.results || data
    } catch (error) {
        console.error('获取媒体列表失败:', error)
    } finally {
        mediaLoading.value = false
    }
}

const filteredMedia = computed(() => {
    let images = mediaList.value.filter(media => {
        return media.is_image || (media.file_type && media.file_type.startsWith('image/'))
    })

    if (mediaSearch.value) {
        images = images.filter(media =>
            (media.filename || media.name || '')?.toLowerCase().includes(mediaSearch.value.toLowerCase())
        )
    }

    return images
})

const handleMediaSelect = async () => {
    if (!selectedMedia.value) return

    try {
        let avatarPath = selectedMedia.value.url

        if (avatarPath && avatarPath.startsWith('http')) {
            const mediaIndex = avatarPath.indexOf('/media/')
            if (mediaIndex !== -1) {
                avatarPath = avatarPath.substring(mediaIndex)
            }
        }

        if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
            avatarPath = '/media/' + avatarPath
        }

        if (!avatarPath) {
            ElMessage.error('未找到媒体路径')
            return
        }

        await updateProfile({avatar_url: avatarPath})
        await userStore.fetchProfile(true)
        ElMessage.success('头像更新成功')
        showMediaDialog.value = false
        selectedMedia.value = null
        mediaSearch.value = ''
    } catch (error) {
        ElMessage.error(error.response?.data?.message || '头像更新失败')
    }
}

const handleAvatarSuccess = async (response) => {
    if (response && response.url) {
        try {
            let avatarPath = response.url
            if (avatarPath && avatarPath.startsWith('http')) {
                const mediaIndex = avatarPath.indexOf('/media/')
                if (mediaIndex !== -1) {
                    avatarPath = avatarPath.substring(mediaIndex)
                }
            }

            if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
                avatarPath = '/media/' + avatarPath
            }

            await updateProfile({avatar_url: avatarPath})
            await userStore.fetchProfile(true)
            ElMessage.success('头像更新成功')
        } catch (error) {
            ElMessage.error(error.response?.data?.message || '头像更新失败')
        }
    } else {
        ElMessage.error('头像上传失败：未返回媒体信息')
    }
}

const handleAvatarError = () => {
    ElMessage.error('头像上传失败')
}

const handleUpdateProfile = async () => {
    try {
        await formRef.value.validate()
    } catch (error) {
        return
    }

    loading.value = true
    try {
        await updateProfile(form)
        // 强制从后端重新获取用户信息
        await userStore.fetchProfile(true)
        ElMessage.success('邮箱修改成功')
        form.email = userStore.user?.email || ''
    } catch (error) {
        console.error('修改邮箱失败:', error)
        ElMessage.error(error.response?.data?.message || error.response?.data?.detail || '修改失败')
    } finally {
        loading.value = false
    }
}

const handleChangePassword = async () => {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    try {
        await changePassword(passwordForm)
        ElMessage.success('密码修改成功')
        Object.assign(passwordForm, {
            old_password: '',
            new_password: '',
            new_password_confirm: '',
        })
    } catch (error) {
        ElMessage.error(error.response?.data?.message || '密码修改失败')
    } finally {
        passwordLoading.value = false
    }
}

onMounted(() => {
    form.email = userStore.user?.email || ''
    fetchMedia()
})
</script>

<style scoped>
.profile-page {
    padding: 0;
    max-width: 900px;
    margin: 0 auto;
}

.profile-header {
    margin-bottom: 24px;
}

.page-title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
}

.page-subtitle {
    margin: 4px 0 0;
    font-size: 14px;
    color: var(--text-secondary);
}

.profile-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.profile-card {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    overflow: hidden;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
}

.card-icon {
    width: 44px;
    height: 44px;
    background: var(--primary-color);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.card-icon svg {
    width: 22px;
    height: 22px;
    color: #fff;
}

.card-icon.success {
    background: var(--success-color);
}

.card-icon.warning {
    background: var(--warning-color);
}

.card-title h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.card-title p {
    margin: 2px 0 0;
    font-size: 13px;
    color: var(--text-secondary);
}

.card-body {
    padding: 20px;
}

.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border-light);
}

.avatar-wrapper {
    position: relative;
    cursor: pointer;
}

.avatar-wrapper :deep(.el-avatar) {
    border: 3px solid var(--card-bg);
    box-shadow: var(--shadow-md);
}

.avatar-actions {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

.avatar-upload {
    display: inline-flex;
}

.info-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.info-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
}

.info-label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-secondary);
    font-size: 14px;
}

.info-label svg {
    width: 16px;
    height: 16px;
    color: var(--text-tertiary);
}

.info-value {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 500;
}

.role-tag {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.role-tag.admin {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.role-tag.editor {
    background: var(--warning-bg);
    color: var(--warning-color);
}

.role-tag.user {
    background: var(--bg-tertiary);
    color: var(--text-secondary);
}

.profile-form {
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
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    transition: all 0.15s ease;
}

.input-wrapper:focus-within {
    background: var(--bg-primary);
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-bg);
}

.input-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    flex-shrink: 0;
}

.input-icon svg {
    width: 16px;
    height: 16px;
}

.form-input {
    flex: 1;
    height: 40px;
    border: none;
    background: transparent;
    font-size: 14px;
    color: var(--text-primary);
    outline: none;
}

.form-input::placeholder {
    color: var(--text-tertiary);
}

.input-suffix {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: color 0.15s ease;
    flex-shrink: 0;
}

.input-suffix:hover {
    color: var(--primary-color);
}

.input-suffix svg {
    width: 16px;
    height: 16px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    padding-top: 8px;
}

.save-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 20px;
    border: none;
    border-radius: var(--radius-sm);
    background: var(--primary-color);
    color: #fff;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
}

.save-btn:hover {
    background: var(--primary-hover);
}

.save-btn.warning {
    background: var(--warning-color);
}

.save-btn.warning:hover {
    background: var(--warning-hover);
}

.save-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

:deep(.el-form-item) {
    margin-bottom: 0;
}

:deep(.el-form-item__error) {
    padding-top: 4px;
    padding-left: 12px;
}

.media-list-container {
    max-height: 400px;
    overflow-y: auto;
}

.media-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.media-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.15s ease;
}

.media-card:hover {
    border-color: var(--primary-color);
}

.media-card.selected {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-bg);
}

.media-image {
    width: 100%;
    height: 100px;
    object-fit: contain;
    background: var(--bg-secondary);
}

.media-info {
    padding: 8px;
    text-align: center;
}

.media-name {
    font-size: 12px;
    color: var(--text-secondary);
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

@media (max-width: 768px) {
    .media-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .info-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
}
</style>
