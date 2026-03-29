<template>
    <div class="page">
        <PageHeader title="编辑资料" />

        <div class="page-content">
            <div class="edit-section">
                <div class="avatar-section" @click="showAvatarOptions = true">
                    <el-avatar :size="80" :src="getAvatarUrl(userStore.user?.avatar)">
                        {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
                    </el-avatar>
                    <span class="avatar-tip">点击更换头像</span>
                </div>

                <div class="form-section">
                    <div class="form-group">
                        <label class="form-label">用户名</label>
                        <input
                            v-model="form.username"
                            class="form-input"
                            placeholder="请输入用户名"
                        />
                    </div>

                    <div class="form-group">
                        <label class="form-label">邮箱</label>
                        <input
                            v-model="form.email"
                            class="form-input"
                            type="email"
                            placeholder="请输入邮箱"
                        />
                    </div>

                    <div class="form-group">
                        <label class="form-label">昵称</label>
                        <input
                            v-model="form.nickname"
                            class="form-input"
                            placeholder="请输入昵称"
                        />
                    </div>

                    <div class="form-group">
                        <label class="form-label">个人简介</label>
                        <textarea
                            v-model="form.bio"
                            class="form-textarea"
                            placeholder="介绍一下自己吧"
                            rows="4"
                        ></textarea>
                    </div>

                    <button
                        class="btn btn-primary btn-block btn-lg"
                        :disabled="saving"
                        @click="saveProfile"
                    >
                        {{ saving ? '保存中...' : '保存' }}
                    </button>
                </div>
            </div>
        </div>

        <el-action-sheet
            v-model="showAvatarOptions"
            :actions="avatarActions"
            @select="handleAvatarAction"
        />
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { updateProfile } from '@/api/user'
import { getAvatarUrl } from '@/utils'
import { useUserStore } from '@/stores/user'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()
const userStore = useUserStore()

const saving = ref(false)
const showAvatarOptions = ref(false)

const form = reactive({
    username: '',
    email: '',
    nickname: '',
    bio: '',
})

const avatarActions = [
    { name: '拍照', value: 'camera' },
    { name: '从相册选择', value: 'gallery' },
    { name: '取消', value: 'cancel' },
]

const handleAvatarAction = action => {
    if (action.value === 'camera') {
        ElMessage.info('拍照功能开发中')
    } else if (action.value === 'gallery') {
        ElMessage.info('相册功能开发中')
    }
    showAvatarOptions.value = false
}

const saveProfile = async () => {
    saving.value = true
    try {
        await updateProfile(form)
        await userStore.fetchUser()
        ElMessage.success('保存成功')
        router.back()
    } catch (e) {
        console.error(e)
        ElMessage.error('保存失败')
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    if (userStore.user) {
        form.username = userStore.user.username || ''
        form.email = userStore.user.email || ''
        form.nickname = userStore.user.nickname || ''
        form.bio = userStore.user.bio || ''
    }
})
</script>

<style scoped>
.edit-section {
    padding: 20px 16px;
}

.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0 30px;
}

.avatar-tip {
    margin-top: 12px;
    font-size: 13px;
    color: var(--text-tertiary);
}

.form-section {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: 16px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group:last-of-type {
    margin-bottom: 24px;
}

.form-label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.form-input {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-color);
    color: var(--text-primary);
    font-size: 14px;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-color);
}

.form-textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-color);
    color: var(--text-primary);
    font-size: 14px;
    resize: none;
    font-family: inherit;
}

.form-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}
</style>
