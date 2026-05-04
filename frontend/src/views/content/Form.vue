<template>
    <div class="content-form">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>{{ isEdit ? '编辑内容' : '新建内容' }}</span>
                    <div class="header-actions">
                        <StatusTag v-if="autoSaveStatus"
                                   :type="autoSaveStatus === 'saving' ? 'warning' : 'success'"
                                   :text="autoSaveStatus === 'saving' ? '自动保存中...' : '已自动保存'"
                        />
                    </div>
                </div>
            </template>
            <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
                <el-row :gutter="20">
                    <el-col :span="16">
                        <el-form-item label="标题" prop="title">
                            <el-input v-model="form.title" placeholder="请输入标题" maxlength="200" show-word-limit/>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="URL别名" prop="slug">
                            <el-input v-model="form.slug" placeholder="留空自动生成" maxlength="200"/>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-form-item label="摘要" prop="summary">
                    <el-input v-model="form.summary" type="textarea" :rows="3" placeholder="请输入摘要（可选）"
                              maxlength="500" show-word-limit/>
                </el-form-item>

                <el-form-item label="内容" prop="content">
                    <div class="editor-header">
                        <span class="editor-label">正文内容</span>
                        <el-upload
                            ref="fileUploadRef"
                            :show-file-list="false"
                            :auto-upload="false"
                            :on-change="handleFileChange"
                            accept=".md,.txt,.markdown"
                        >
                            <el-button type="primary" size="small" :icon="Upload">
                                从文件导入
                            </el-button>
                        </el-upload>
                    </div>
                    <div class="editor-wrapper" :class="editorThemeClass">
                        <MdEditor
                            v-if="editorLoaded"
                            v-model="form.content"
                            :toolbars="toolbars"
                            :preview="showPreview"
                            :previewTheme="previewTheme"
                            :codeTheme="codeTheme"
                            :style="{ height: editorHeight }"
                            placeholder="请输入正文内容，支持 Markdown 语法"
                            @onChange="handleContentChange"
                        />
                        <div v-else class="editor-loading">
                            <el-icon class="is-loading">
                                <Loading/>
                            </el-icon>
                            <span>编辑器加载中...</span>
                        </div>
                    </div>
                </el-form-item>

                <el-divider content-position="left">分类与标签</el-divider>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="分类" prop="category">
                            <div class="select-with-button">
                                <el-select v-model="form.category" placeholder="请选择分类" clearable
                                           class="category-select">
                                    <el-option v-for="cat in categories" :key="cat.id" :label="cat.name"
                                               :value="cat.id"/>
                                </el-select>
                                <el-button type="primary" size="small" @click="showCategoryDialog = true">创建
                                </el-button>
                            </div>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="标签" prop="tags">
                            <div class="select-with-button">
                                <el-select v-model="form.tags" multiple placeholder="请选择标签" class="tag-select"
                                           label="name">
                                    <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id"/>
                                </el-select>
                                <el-button type="primary" size="small" @click="showTagDialog = true">创建</el-button>
                            </div>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="20" v-if="isAdmin">
                    <el-col :span="12">
                        <el-form-item label="作者" prop="author">
                            <el-select v-model="form.author" placeholder="请选择作者" style="width: 100%">
                                <el-option v-for="user in users" :key="user.id" :label="user.username"
                                           :value="user.id"/>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-divider content-position="left">封面与设置</el-divider>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="封面图">
                            <div class="cover-wrapper">
                                <div class="cover-uploader" @click="triggerCoverSelect">
                                    <img v-if="coverPreviewUrl" :src="coverPreviewUrl" class="cover-image"/>
                                    <div v-else class="cover-placeholder">
                                        <el-icon class="cover-uploader-icon">
                                            <Plus/>
                                        </el-icon>
                                        <span>点击上传封面</span>
                                    </div>
                                </div>
                                <div v-if="coverPreviewUrl" class="cover-actions">
                                    <button
                                        v-if="pendingCoverFile"
                                        type="button"
                                        class="cover-btn cover-btn-warning"
                                        @click.stop="triggerCoverSelect"
                                    >
                                        <el-icon><Upload /></el-icon>
                                        <span>更换</span>
                                    </button>
                                    <button
                                        type="button"
                                        class="cover-btn cover-btn-danger"
                                        @click.stop="clearCover"
                                    >
                                        <el-icon><Delete /></el-icon>
                                        <span>移除</span>
                                    </button>
                                </div>
                                <div v-if="pendingCoverFile" class="cover-status-bar">
                                    <el-icon class="status-icon"><Clock /></el-icon>
                                    <span>封面图将在提交时上传</span>
                                </div>
                            </div>
                            <input
                                ref="coverInputRef"
                                type="file"
                                accept="image/jpeg,image/png,image/gif,image/webp"
                                style="display: none"
                                @change="handleCoverSelect"
                            />
                            <div class="cover-tip">建议尺寸：1920x1080，支持 jpg/png 格式</div>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="状态" prop="status">
                            <el-radio-group v-model="form.status">
                                <el-radio value="draft">草稿</el-radio>
                                <el-radio value="published">发布</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="置顶">
                            <el-switch v-model="form.is_top"/>
                            <span class="form-tip">置顶内容将优先显示在列表顶部</span>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-divider/>

                <el-form-item>
                    <el-button type="primary" @click="handleSubmit" :loading="loading">
                        {{ isEdit ? '保存修改' : '创建内容' }}
                    </el-button>
                    <el-button @click="handleSaveDraft" :loading="loading" v-if="!isEdit">
                        保存草稿
                    </el-button>
                    <el-button @click="$router.back()">取消</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 创建分类对话框 -->
        <el-dialog v-model="showCategoryDialog" title="创建分类" width="400px">
            <el-form label-width="80px">
                <el-form-item label="分类名称" required>
                    <el-input v-model="newCategoryName" placeholder="请输入分类名称"/>
                </el-form-item>
                <el-form-item label="URL 别名">
                    <el-input v-model="newCategorySlug" placeholder="留空自动生成"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showCategoryDialog = false">取消</el-button>
                <el-button type="primary" @click="createCategory" :loading="creatingCategory">创建</el-button>
            </template>
        </el-dialog>

        <!-- 创建标签对话框 -->
        <el-dialog v-model="showTagDialog" title="创建标签" width="400px">
            <el-form label-width="80px">
                <el-form-item label="标签名称" required>
                    <el-input v-model="newTagName" placeholder="请输入标签名称"/>
                </el-form-item>
                <el-form-item label="URL 别名">
                    <el-input v-model="newTagSlug" placeholder="留空自动生成"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showTagDialog = false">取消</el-button>
                <el-button type="primary" @click="createTag" :loading="creatingTag">创建</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted, onUnmounted, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Plus, Loading, Upload, Delete, Clock} from '@element-plus/icons-vue'
import {MdEditor} from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import {createContent, updateContent, getContent} from '@/api/content'
import api from '@/api'
import {useUserStore} from '@/stores/user'
import {useThemeStore} from '@/stores/theme'
import StatusTag from '@/components/StatusTag.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const isEdit = computed(() => !!route.params.id)
const isAdmin = computed(() => userStore.user?.role_code === 'admin' || userStore.user?.is_superuser)
const editorThemeClass = computed(() => ({
    'md-editor-dark': themeStore.theme === 'dark'
}))
const formRef = ref()
const loading = ref(false)
const categories = ref([])
const tags = ref([])
const users = ref([])

const editorLoaded = ref(false)
const showPreview = ref(false)
const previewTheme = ref('github')
const codeTheme = ref('github')
const editorHeight = ref('500px')
const autoSaveStatus = ref('')
const autoSaveTimer = ref(null)
const lastSaveContent = ref('')
const showCategoryDialog = ref(false)
const showTagDialog = ref(false)
const newCategoryName = ref('')
const newCategorySlug = ref('')
const newTagName = ref('')
const newTagSlug = ref('')
const creatingCategory = ref(false)
const creatingTag = ref(false)

const coverInputRef = ref(null)
const pendingCoverFile = ref(null)
const coverPreviewUrl = ref('')

const updateEditorTheme = () => {
    const isDark = themeStore.theme === 'dark'
    previewTheme.value = isDark ? 'mk-cute' : 'github'
    codeTheme.value = isDark ? 'one-dark' : 'github'
}

const form = ref({
    title: '',
    slug: '',
    summary: '',
    content: '',
    category: null,
    tags: [],
    cover_image: '',
    status: 'draft',
    is_top: false,
    author: null,
})

const rules = {
    title: [{required: true, message: '请输入标题', trigger: 'blur'}],
    content: [{required: true, message: '请输入内容', trigger: 'blur'}],
}

const toolbars = [
    'bold',
    'underline',
    'italic',
    '-',
    'title',
    'strikeThrough',
    'quote',
    'unorderedList',
    'orderedList',
    '-',
    'codeRow',
    'code',
    'link',
    'image',
    'table',
    '-',
    'revoke',
    'next',
    '=',
    'pageFullscreen',
    'fullscreen',
    'preview',
]

const handleContentChange = () => {
    if (form.value.content && form.value.content !== lastSaveContent.value && form.value.content.length > 100) {
        triggerAutoSave()
    }
}

const handleFileChange = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        const content = e.target.result
        if (form.value.content) {
            ElMessageBox.confirm(
                '当前编辑器已有内容，是否覆盖？',
                '确认导入',
                {
                    confirmButtonText: '覆盖',
                    cancelButtonText: '追加',
                    type: 'warning',
                }
            ).then(() => {
                form.value.content = content
                ElMessage.success('文件导入成功')
            }).catch(() => {
                form.value.content = form.value.content + '\n\n' + content
                ElMessage.success('文件内容已追加')
            })
        } else {
            form.value.content = content
            ElMessage.success('文件导入成功')
        }
    }
    reader.onerror = () => {
        ElMessage.error('文件读取失败')
    }
    reader.readAsText(file.raw)
}

const triggerAutoSave = () => {
    if (autoSaveTimer.value) {
        clearTimeout(autoSaveTimer.value)
    }
    autoSaveTimer.value = setTimeout(() => {
        if (isEdit.value) {
            autoSave()
        }
    }, 3000)
}

const autoSave = async () => {
    if (!form.value.content || form.value.content === lastSaveContent.value) return

    autoSaveStatus.value = 'saving'
    try {
        const submitData = {
            title: form.value.title,
            content: form.value.content,
            summary: form.value.summary,
            category: form.value.category,
            tags: form.value.tags,
            cover_image: form.value.cover_image,
            status: form.value.status,
            is_top: form.value.is_top,
        }
        if (!submitData.category) delete submitData.category
        if (!submitData.cover_image) delete submitData.cover_image
        if (submitData.tags.length === 0) delete submitData.tags

        await updateContent(route.params.id, submitData)
        lastSaveContent.value = form.value.content
        autoSaveStatus.value = 'saved'
        setTimeout(() => {
            autoSaveStatus.value = ''
        }, 2000)
    } catch (error) {
        autoSaveStatus.value = ''
    }
}

const triggerCoverSelect = () => {
    coverInputRef.value?.click()
}

const handleCoverSelect = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type)
    if (!isValidType) {
        ElMessage.error('只能上传 JPG/PNG/GIF/WEBP 格式的图片')
        event.target.value = ''
        return
    }

    const isLt10M = file.size / 1024 / 1024 < 10
    if (!isLt10M) {
        ElMessage.error('图片大小不能超过 10MB')
        event.target.value = ''
        return
    }

    if (coverPreviewUrl.value && coverPreviewUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(coverPreviewUrl.value)
    }

    pendingCoverFile.value = file
    coverPreviewUrl.value = URL.createObjectURL(file)
    form.value.cover_image = ''
    event.target.value = ''
}

const clearCover = () => {
    if (coverPreviewUrl.value && coverPreviewUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(coverPreviewUrl.value)
    }
    pendingCoverFile.value = null
    coverPreviewUrl.value = ''
    form.value.cover_image = ''
}

const uploadCoverImage = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    const token = userStore.accessToken

    const response = await fetch(`${baseUrl}/media/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    })

    if (!response.ok) {
        throw new Error('封面图上传失败')
    }

    const result = await response.json()
    const mediaData = result.data || result

    if (mediaData.url) {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
        const mediaBaseUrl = apiBaseUrl.replace(/\/api\/?$/, '')
        return mediaData.url.startsWith('http') ? mediaData.url : `${mediaBaseUrl}${mediaData.url}`
    }

    throw new Error('响应格式错误')
}

const fetchCategories = async () => {
    try {
        const {data} = await api.get('/categories/')
        categories.value = data.results || data
    } catch (error) {
        console.error(error)
    }
}

const fetchTags = async () => {
    try {
        const {data} = await api.get('/tags/')
        tags.value = data.results || data
    } catch (error) {
        console.error(error)
    }
}

const createCategory = async () => {
    if (!newCategoryName.value.trim()) {
        ElMessage.warning('请输入分类名称')
        return
    }
    creatingCategory.value = true
    try {
        const payload = {
            name: newCategoryName.value.trim(),
            slug: newCategorySlug.value.trim() || undefined,
        }
        const {data} = await api.post('/categories/', payload)
        ElMessage.success('分类创建成功')
        showCategoryDialog.value = false
        newCategoryName.value = ''
        newCategorySlug.value = ''
        categories.value = [...categories.value, data]
        form.value.category = data.id
    } catch (error) {
        ElMessage.error('创建分类失败')
        console.error(error)
    } finally {
        creatingCategory.value = false
    }
}

const createTag = async () => {
    if (!newTagName.value.trim()) {
        ElMessage.warning('请输入标签名称')
        return
    }
    creatingTag.value = true
    try {
        const payload = {
            name: newTagName.value.trim(),
            slug: newTagSlug.value.trim() || undefined,
        }
        const {data} = await api.post('/tags/', payload)
        ElMessage.success('标签创建成功')
        showTagDialog.value = false
        newTagName.value = ''
        newTagSlug.value = ''
        tags.value = [...tags.value, data]
        if (!form.value.tags) form.value.tags = []
        form.value.tags.push(data.id)
    } catch (error) {
        ElMessage.error('创建标签失败')
        console.error(error)
    } finally {
        creatingTag.value = false
    }
}

const fetchUsers = async () => {
    if (!isAdmin.value) return
    try {
        const {data} = await api.get('/auth/')
        users.value = data.results || data
    } catch (error) {
        console.error(error)
    }
}

const fetchContent = async () => {
    if (!route.params.id) return
    loading.value = true
    try {
        const {data} = await getContent(route.params.id)
        Object.assign(form.value, {
            title: data.title,
            slug: data.slug,
            summary: data.summary,
            content: data.content,
            category: data.category,
            tags: data.tags?.map(t => t.id) || [],
            cover_image: data.cover_image,
            status: data.status,
            is_top: data.is_top,
            author: data.author?.id || data.author,
        })
        if (data.cover_image) {
            coverPreviewUrl.value = data.cover_image
        }
        lastSaveContent.value = data.content
    } catch (error) {
        ElMessage.error('获取内容失败')
    } finally {
        loading.value = false
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return
    await formRef.value.validate()
    loading.value = true
    try {
        let coverImageUrl = form.value.cover_image

        if (pendingCoverFile.value) {
            try {
                coverImageUrl = await uploadCoverImage(pendingCoverFile.value)
            } catch (error) {
                ElMessage.error('封面图上传失败')
                loading.value = false
                return
            }
        }

        const submitData = {...form.value, cover_image: coverImageUrl}
        if (!submitData.category) delete submitData.category
        if (!submitData.cover_image) delete submitData.cover_image
        if (submitData.tags.length === 0) delete submitData.tags
        if (!isAdmin.value || !submitData.author) delete submitData.author

        if (isEdit.value) {
            await updateContent(route.params.id, submitData)
            ElMessage.success('保存成功')
        } else {
            await createContent(submitData)
            ElMessage.success('创建成功')
        }
        router.push('/contents')
    } catch (error) {
        ElMessage.error(isEdit.value ? '保存失败' : '创建失败')
    } finally {
        loading.value = false
    }
}

const handleSaveDraft = async () => {
    if (!form.value.title && !form.value.content) {
        ElMessage.warning('请至少填写标题或内容')
        return
    }
    loading.value = true
    try {
        let coverImageUrl = form.value.cover_image

        if (pendingCoverFile.value) {
            try {
                coverImageUrl = await uploadCoverImage(pendingCoverFile.value)
            } catch (error) {
                ElMessage.error('封面图上传失败')
                loading.value = false
                return
            }
        }

        const submitData = {...form.value, status: 'draft', cover_image: coverImageUrl}
        if (!submitData.category) delete submitData.category
        if (!submitData.cover_image) delete submitData.cover_image
        if (submitData.tags.length === 0) delete submitData.tags
        if (!isAdmin.value || !submitData.author) delete submitData.author

        if (isEdit.value) {
            await updateContent(route.params.id, submitData)
            ElMessage.success('草稿保存成功')
        } else {
            await createContent(submitData)
            ElMessage.success('草稿保存成功')
            router.push('/contents')
        }
    } catch (error) {
        ElMessage.error('保存草稿失败')
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    await Promise.all([
        fetchCategories(),
        fetchTags(),
        fetchUsers(),
        fetchContent(),
    ])

    updateEditorTheme()

    setTimeout(() => {
        editorLoaded.value = true
    }, 100)
})

watch(() => themeStore.theme, () => {
    updateEditorTheme()
})

onUnmounted(() => {
    if (autoSaveTimer.value) {
        clearTimeout(autoSaveTimer.value)
    }
    if (coverPreviewUrl.value && coverPreviewUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(coverPreviewUrl.value)
    }
})
</script>

<style scoped>
.content-form {
    padding: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.editor-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.editor-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.select-with-button {
    display: flex;
    gap: 8px;
    align-items: center;
    width: 100%;
}

.select-with-button .el-select,
.select-with-button .category-select,
.select-with-button .tag-select {
    width: calc(100% - 60px);
}

.editor-wrapper {
    width: 100%;
}

.editor-loading {
    height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--text-tertiary);
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
}

.editor-loading .el-icon {
    font-size: 32px;
}

.cover-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.cover-uploader {
    border: 1px dashed var(--border-color);
    border-radius: var(--radius-sm);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    width: 320px;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-tertiary);
    transition: border-color var(--transition-fast);
}

.cover-uploader:hover {
    border-color: var(--primary-color);
}

.cover-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.cover-uploader-icon {
    font-size: 32px;
    color: var(--text-tertiary);
}

.cover-image {
    max-width: 100%;
    max-height: 100%;
    display: block;
    object-fit: contain;
}

.cover-actions {
    display: flex;
    gap: 8px;
}

.cover-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: none;
    border-radius: var(--radius-xs);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
}

.cover-btn .el-icon {
    font-size: 12px;
}

.cover-btn-warning {
    background: var(--warning-color, #e6a23c);
    color: #fff;
}

.cover-btn-warning:hover {
    background: var(--warning-hover, #ebb563);
}

.cover-btn-danger {
    background: var(--danger-color);
    color: #fff;
}

.cover-btn-danger:hover {
    background: var(--danger-hover);
}

.cover-status-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--warning-bg, #fdf6ec);
    border-radius: var(--radius-sm);
    font-size: 12px;
    color: var(--warning-color, #e6a23c);
}

.cover-status-bar .status-icon {
    font-size: 14px;
}

[data-theme="dark"] .cover-status-bar {
    background: rgba(230, 162, 60, 0.1);
}

.cover-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 8px;
}

.form-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-left: 10px;
}

/* Markdown 编辑器主题适配 */
[data-theme="dark"] .md-editor {
    background: var(--bg-primary) !important;
    border-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper {
    background: var(--bg-primary) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper h1,
[data-theme="dark"] .md-editor-preview-wrapper h2,
[data-theme="dark"] .md-editor-preview-wrapper h3,
[data-theme="dark"] .md-editor-preview-wrapper h4,
[data-theme="dark"] .md-editor-preview-wrapper h5,
[data-theme="dark"] .md-editor-preview-wrapper h6 {
    color: var(--text-primary) !important;
    border-bottom-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper p,
[data-theme="dark"] .md-editor-preview-wrapper li,
[data-theme="dark"] .md-editor-preview-wrapper blockquote {
    color: var(--text-secondary) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper code {
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper pre {
    background: var(--bg-secondary) !important;
    border-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper table td,
[data-theme="dark"] .md-editor-preview-wrapper table th {
    border-color: var(--border-color) !important;
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper table tr:nth-child(2n) {
    background: var(--bg-tertiary) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper hr {
    background-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-preview-wrapper a {
    color: var(--primary-color) !important;
}

/* 编辑器工具栏主题适配 */
[data-theme="dark"] .md-editor-toolbar {
    background: var(--bg-primary) !important;
    border-bottom-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-toolbar-item {
    color: var(--text-secondary) !important;
}

[data-theme="dark"] .md-editor-toolbar-item:hover {
    background: var(--bg-secondary) !important;
    color: var(--primary-color) !important;
}

[data-theme="dark"] .md-editor-toolbar-item.active {
    background: var(--primary-bg) !important;
    color: var(--primary-color) !important;
}

[data-theme="dark"] .md-editor-divider {
    background: var(--border-color) !important;
}

/* 编辑器输入区域主题适配 */
[data-theme="dark"] .md-editor-input-wrapper {
    background: var(--bg-primary) !important;
}

[data-theme="dark"] .md-editor-input-wrapper textarea {
    color: var(--text-primary) !important;
    background: var(--bg-primary) !important;
}

/* 代码块主题适配 */
[data-theme="dark"] .md-editor-code-block-language {
    color: var(--text-secondary) !important;
}

/* CodeMirror 滚动区域主题适配 */
[data-theme="dark"] .cm-scroller {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-scroller .cm-content {
    color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-scroller .cm-line {
    color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-scroller ::selection {
    background: var(--primary-bg-hover) !important;
}

[data-theme="dark"] .cm-activeLine {
    background: var(--bg-tertiary) !important;
}

[data-theme="dark"] .cm-activeLineGutter {
    background: var(--bg-secondary) !important;
}

[data-theme="dark"] .cm-gutters {
    background: var(--bg-primary) !important;
    border-right-color: var(--border-color) !important;
    color: var(--text-tertiary) !important;
}

[data-theme="dark"] .cm-cursor {
    border-left-color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-matchingBracket {
    background: var(--primary-bg) !important;
}

[data-theme="dark"] .cm-foldPlaceholder {
    background: var(--bg-secondary) !important;
    border-color: var(--border-color) !important;
    color: var(--text-secondary) !important;
}

/* 强制覆盖 md-editor-v3 的编辑器主题 */
[data-theme="dark"] .md-editor-input-wrapper .cm-editor {
    background: var(--bg-primary) !important;
}

[data-theme="dark"] .md-editor-input-wrapper .cm-editor .cm-scroller {
    background: var(--bg-primary) !important;
}

[data-theme="dark"] .md-editor-input-wrapper .cm-focused {
    outline: none !important;
}

/* 亮色模式下的样式保证 */
.md-editor-input-wrapper .cm-editor .cm-scroller {
    background: #ffffff !important;
}

.md-editor-input-wrapper .cm-content {
    color: #24292f !important;
}

/* 全局样式 - 强制主题适配 */
.md-editor-dark {
    --md-bk-color: #252526 !important;
    --md-bk-color-outstand: #2d2d2d !important;
    --md-bk-hover-color: #383838 !important;
    --md-border-color: #3a3a3a !important;
    --md-modal-color: #1e1e1e !important;
    --md-bar-color: #2d2d2d !important;
    --md-bar-border-color: #3a3a3a !important;
    --md-icon-color: #b4b4b4 !important;
    --md-icon-hover-color: #ffffff !important;
    --md-text-color: #ffffff !important;
    --md-text-active-color: #0078d4 !important;
    --md-text-unchecked-color: #b4b4b4 !important;
    --md-scrollbar-bg-color: transparent !important;
    --md-scrollbar-thumb-color: #424242 !important;
    --md-scrollbar-thumb-hover-color: #4f4f4f !important;
}

.md-editor-dark .cm-scroller {
    --cm-readonly-bg: #252526 !important;
    background-color: #252526 !important;
}

.md-editor-dark .cm-gutters {
    background-color: #252526 !important;
    border-right: 1px solid #3a3a3a !important;
}

.md-editor-dark .cm-lineNumbers {
    color: #858585 !important;
}

.md-editor-dark .cm-activeLineGutter {
    background-color: #2d2d2d !important;
}

.md-editor-dark .cm-cursorLayer {
    caret-color: #ffffff !important;
}

.md-editor-dark .cm-selectionBackground,
.md-editor-dark ::selection {
    background: rgba(0, 120, 212, 0.3) !important;
}

.md-editor-dark .cm-focused .cm-cursor {
    border-left-color: #ffffff !important;
}
</style>

<style>
/* 全局样式 - 用于覆盖 md-editor-v3 的主题 */
[data-theme="dark"] .md-editor {
    background: var(--bg-primary) !important;
    border-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-toolbar {
    background: var(--bg-primary) !important;
    border-bottom-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-toolbar-item {
    color: var(--text-secondary) !important;
}

[data-theme="dark"] .md-editor-toolbar-item:hover {
    background: var(--bg-secondary) !important;
    color: var(--primary-color) !important;
}

[data-theme="dark"] .md-editor-divider {
    background-color: var(--border-color) !important;
}

[data-theme="dark"] .md-editor-input-wrapper,
[data-theme="dark"] .md-editor-input-wrapper * {
    background: var(--bg-primary) !important;
}

[data-theme="dark"] .cm-scroller {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-content,
[data-theme="dark"] .cm-line {
    color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-gutters {
    background: var(--bg-primary) !important;
    border-right-color: var(--border-color) !important;
    color: var(--text-tertiary) !important;
}

[data-theme="dark"] .cm-cursor {
    border-left-color: var(--text-primary) !important;
}

[data-theme="dark"] .cm-activeLine {
    background: var(--bg-tertiary) !important;
}

[data-theme="dark"] .cm-activeLineGutter {
    background: var(--bg-secondary) !important;
}

[data-theme="dark"] ::selection {
    background: var(--primary-bg-hover) !important;
}

/* 强制应用暗色主题到 CodeMirror */
.md-editor-dark .cm-editor,
.md-editor-dark .cm-scroller,
.md-editor-dark .cm-content,
.md-editor-dark .cm-line {
    background-color: #252526 !important;
    color: #c5c5c5 !important;
}

.md-editor-dark .cm-gutters {
    background-color: #1e1e1e !important;
    border-right-color: #3a3a3a !important;
    color: #858585 !important;
}

.md-editor-dark .cm-cursor {
    border-left-color: #ffffff !important;
}
</style>
