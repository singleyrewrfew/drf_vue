<template>
    <div class="content-form">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>{{ isEdit ? '编辑内容' : '新建内容' }}</span>
                    <div class="header-actions">
                        <StatusTag v-if="autoSaveStatus === 'saving'" type="warning" icon="Loading" text="保存中..."/>
                        <StatusTag v-else-if="autoSaveStatus === 'saved'" type="success" icon="CircleCheck" text="已保存"/>
                        <StatusTag v-else-if="autoSaveStatus === 'local'" type="info" icon="Document" text="本地缓存"/>
                    </div>
                </div>
            </template>
            <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
                <el-row :gutter="20">
                    <el-col :span="16">
                        <el-form-item label="标题" prop="title">
                            <el-input id="title" v-model="form.title" placeholder="请输入标题" maxlength="200" show-word-limit/>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="URL别名" prop="slug">
                            <el-input id="slug" v-model="form.slug" placeholder="留空自动生成" maxlength="200"/>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-form-item label="摘要" prop="summary">
                    <el-input id="summary" v-model="form.summary" type="textarea" :rows="3" placeholder="请输入摘要（可选）"
                              maxlength="500" show-word-limit/>
                </el-form-item>

                <el-form-item label="内容" prop="content">
                    <div class="editor-header">
                        <span class="editor-label">正文内容</span>
                        <el-upload ref="fileUploadRef" :show-file-list="false" :auto-upload="false" :on-change="handleFileChange"
                                   accept=".md,.txt,.markdown">
                            <ActionButton type="primary" text="从文件导入" icon="upload" size="small"/>
                        </el-upload>
                    </div>
                    <div class="editor-wrapper" :class="editorThemeClass()">
                        <MdEditor v-if="editorLoaded" id="content" v-model="form.content" :toolbars="toolbars" :preview="showPreview"
                                  :previewTheme="previewTheme" :codeTheme="codeTheme" :style="{ height: editorHeight }"
                                  placeholder="请输入正文内容，支持 Markdown 语法" @onChange="(val) => handleContentChange(val)"/>
                        <div v-else class="editor-loading">
                            <el-icon class="is-loading"><Loading/></el-icon>
                            <span>编辑器加载中...</span>
                        </div>
                    </div>
                </el-form-item>

                <el-divider content-position="left">分类与标签</el-divider>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="分类" prop="category">
                            <SelectWithCreate v-model="form.category" :options="categories" placeholder="请选择分类"
                                              @create="showCategoryDialog = true"/>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="标签" prop="tags">
                            <SelectWithCreate v-model="form.tags" :options="tags" :multiple="true" placeholder="请选择标签"
                                              @create="showTagDialog = true"/>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="20" v-if="isAdmin">
                    <el-col :span="12">
                        <el-form-item label="作者" prop="author">
                            <el-select id="author" v-model="form.author" placeholder="请选择作者" class="full-width-select">
                                <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id"/>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-divider content-position="left">封面与设置</el-divider>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="封面图" prop="cover_image">
                            <div class="cover-upload-wrapper">
                                <ImageUploader v-model="form.cover_image"
                                               placeholder-text="点击上传封面"
                                               replace-text="更换"
                                               remove-text="移除"
                                               :max-size-m-b="10"
                                               tip="支持 JPG/PNG/GIF/WEBP，建议尺寸 1200x630"
                                               @file-selected="(file) => pendingCoverFile = file"
                                               ref="imageUploaderRef">
                                    <template #actions>
                                        <ActionButton icon="folder" size="small" class="media-btn" @click="showMediaSelector = true">媒体库</ActionButton>
                                    </template>
                                </ImageUploader>
                            </div>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <div class="form-item-custom">
                            <label for="status" class="form-label">状态</label>
                            <div class="radio-wrapper">
                                <input type="radio" id="status" name="status" :checked="form.status === 'published'"
                                       class="sr-only"
                                       tabindex="-1" aria-hidden="true"/>
                                <el-radio-group v-model="form.status" @change="(val) => form.status = val">
                                    <el-radio value="draft">草稿</el-radio>
                                    <el-radio value="published">发布</el-radio>
                                </el-radio-group>
                            </div>
                        </div>
                        <el-form-item label="置顶" prop="is_top">
                            <el-switch id="is_top" v-model="form.is_top"/>
                            <span class="form-tip">置顶内容将优先显示在列表顶部</span>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-divider/>

                <el-form-item class="form-actions">
                    <ActionButton icon="approve" :text="isEdit ? '保存修改' : '创建内容'" size="normal" stop
                               @click="handleSubmit" :loading="loading"/>
                    <ActionButton variant="outline" type="text" icon="save" text="保存草稿" size="normal" stop
                               @click="handleSaveDraft" :loading="loading" v-if="!isEdit"/>
                    <ActionButton variant="outline" type="text" icon="reset" text="取消" size="normal" @click="$router.back()"/>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 创建分类对话框 -->
        <FormDialog v-model="categoryForm" v-model:show="showCategoryDialog" create-title="创建分类" width="400px"
                   label-width="80px" :rules="categoryRules" :loading="creatingCategory"
                   @submit="() => handleCreateCategory(categories)">
            <el-form-item label="分类名称" prop="name"><el-input id="name" v-model="categoryForm.name" placeholder="请输入分类名称"/></el-form-item>
            <el-form-item label="URL 别名" prop="slug"><el-input id="slug" v-model="categoryForm.slug" placeholder="留空自动生成"/></el-form-item>
        </FormDialog>

        <!-- 创建标签对话框 -->
        <FormDialog v-model="tagForm" v-model:show="showTagDialog" create-title="创建标签" width="400px"
                   label-width="80px" :rules="tagRules" :loading="creatingTag"
                   @submit="() => handleCreateTag(tags)">
            <el-form-item label="标签名称" prop="name"><el-input id="name" v-model="tagForm.name" placeholder="请输入标签名称"/></el-form-item>
            <el-form-item label="URL 别名" prop="slug"><el-input id="slug" v-model="tagForm.slug" placeholder="留空自动生成"/></el-form-item>
        </FormDialog>

        <!-- 媒体库选择 -->
        <MediaSelectorDialog v-model:visible="showMediaSelector" @select="handleMediaSelect"/>

        <!-- 草稿恢复提示条（恢复后显示） -->
        <DraftRestoreBar :visible="draftRestored" :saved-at="draftRestoreTime"/>

        <!-- 草稿恢复对话框 -->
        <BaseDialog :visible="hasDraft" title="发现未保存的草稿" width="450px"
                   @update:visible="(val) => { if (!val) discardDraft() }">
            <div class="draft-restore-hint">
                <p>检测到您上次编辑的内容尚未保存，是否恢复？</p>
                <div v-if="draftData" class="draft-preview">
                    <div class="draft-info"><strong>标题：</strong>{{ draftData.title || '(空)' }}</div>
                    <div class="draft-info"><strong>字数：</strong>{{ (draftData.content || '').length }} 字</div>
                    <div class="draft-info"><strong>保存时间：</strong>{{ formatDraftTime(draftData.savedAt) }}</div>
                </div>
            </div>
            <template #footer>
                <ActionButton variant="outline" type="text" text="放弃草稿" icon="delete" size="normal" @click="discardDraft"/>
                <ActionButton text="恢复草稿" icon="refresh" size="normal" stop @click="handleRestoreDraft"/>
            </template>
        </BaseDialog>
    </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted, onUnmounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Loading, CircleCheck, Document} from '@element-plus/icons-vue'
import {MdEditor} from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

import {createContent, updateContent, getContent} from '@/api/content'
import api from '@/api'
import {useUserStore} from '@/stores/user'
import {logger} from '@/utils/logger.js'

import StatusTag from '@/components/StatusTag.vue'
import ActionButton from '@/components/ActionButton.vue'
import FormDialog from '@/components/FormDialog.vue'
import BaseDialog from '@/components/BaseDialog.vue'
import SelectWithCreate from '@/components/SelectWithCreate.vue'
import DraftRestoreBar from '@/components/DraftRestoreBar.vue'
import ImageUploader from '@/components/ImageUploader.vue'
import MediaSelectorDialog from './components/MediaSelectorDialog.vue'
import {useCategoryTagForm} from '@/composables/useCategoryTagForm.js'
import {useContentEditor} from '@/composables/useContentEditor.js'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isEdit = computed(() => !!route.params.id)
const isAdmin = computed(() => userStore.user?.role_code === 'admin' || userStore.user?.is_superuser)

const formRef = ref()
const loading = ref(false)
const categories = ref([])
const tags = ref([])
const users = ref([])
const imageUploaderRef = ref(null)
const pendingCoverFile = ref(null)
const showMediaSelector = ref(false)

const form = ref({
    title: '', slug: '', summary: '', content: '',
    category: null, tags: [], cover_image: '',
    status: 'draft', is_top: false, author: null,
})

const rules = {
    title: [{required: true, message: '请输入标题', trigger: 'blur'}],
    content: [{required: true, message: '请输入内容', trigger: 'blur'}],
}

const {
    editorLoaded, showPreview, previewTheme, codeTheme, editorHeight,
    autoSaveStatus, toolbars, editorThemeClass, handleContentChange,
    initLastContent, hasDraft, draftData,
    checkLocalDraft, restoreDraft, discardDraft, clearDraftStorage,
} = useContentEditor(form)

const draftRestored = ref(false)
const draftRestoreTime = ref(0)

const handleRestoreDraft = () => {
    if (draftData.value?.savedAt) {
        draftRestoreTime.value = draftData.value.savedAt
    }
    restoreDraft()
    draftRestored.value = true
    setTimeout(() => { draftRestored.value = false }, 5000)
}

const {
    showCategoryDialog, showTagDialog, creatingCategory, creatingTag,
    categoryForm, tagForm, categoryRules, tagRules,
    handleCreateCategory, handleCreateTag,
} = useCategoryTagForm(
    (id) => { form.value.category = id },
    (id) => { if (!form.value.tags) form.value.tags = []; form.value.tags.push(id) }
)

const handleFileChange = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        if (form.value.content) {
            ElMessageBox.confirm('当前编辑器已有内容，是否覆盖？', '确认导入', {
                confirmButtonText: '覆盖', cancelButtonText: '追加', type: 'warning',
            }).then(() => { form.value.content = e.target.result; ElMessage.success('文件导入成功') })
              .catch(() => { form.value.content += '\n\n' + e.target.result; ElMessage.success('文件内容已追加') })
        } else { form.value.content = e.target.result; ElMessage.success('文件导入成功') }
    }
    reader.onerror = () => ElMessage.error('文件读取失败')
    reader.readAsText(file.raw)
}

const handleMediaSelect = (media) => {
    form.value.cover_image = media.url
}

const uploadCoverImage = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    const token = userStore.accessToken
    const response = await fetch(`${baseUrl}/media/`, {
        method: 'POST', headers: {'Authorization': `Bearer ${token}`}, body: formData,
    })
    if (!response.ok) throw new Error('封面图上传失败')
    const result = await response.json()
    const mediaData = result.data || result
    if (mediaData.url) {
        const mediaBaseUrl = baseUrl.replace(/\/api\/?$/, '')
        return mediaData.url.startsWith('http') ? mediaData.url : `${mediaBaseUrl}${mediaData.url}`
    }
    throw new Error('响应格式错误')
}

const buildSubmitData = async () => {
    let coverImageUrl = form.value.cover_image
    if (pendingCoverFile.value) coverImageUrl = await uploadCoverImage(pendingCoverFile.value)
    const data = {...form.value, cover_image: coverImageUrl}
    if (!data.category) delete data.category
    if (!data.cover_image) delete data.cover_image
    if (data.tags.length === 0) delete data.tags
    if (!isAdmin.value || !data.author) delete data.author
    return data
}

const handleSubmit = async () => {
    if (!formRef.value) return
    await formRef.value.validate()
    loading.value = true
    
    try {
        const submitData = await buildSubmitData()
        
        if (isEdit.value) {
            await updateContent(route.params.id, submitData)
            ElMessage.success('保存成功')
        } else {
            await createContent(submitData)
            ElMessage.success('创建成功')
        }
        
        try {
            clearDraftStorage()
        } catch (e) {
            logger.warn('清除草稿失败', e)
        }

        router.push('/contents')

    } catch (error) {
        logger.error('提交失败', error)
        ElMessage.error(isEdit.value ? '保存失败' : '创建失败')
    } finally {
        loading.value = false
    }
}

const handleSaveDraft = async () => {
    if (!form.value.title && !form.value.content) { ElMessage.warning('请至少填写标题或内容'); return }
    loading.value = true
    
    try {
        const submitData = {...(await buildSubmitData()), status: 'draft'}
        
        if (isEdit.value) {
            await updateContent(route.params.id, submitData)
            ElMessage.success('草稿保存成功')
        } else {
            await createContent(submitData)
            ElMessage.success('草稿保存成功')
            router.push('/contents')
        }
        
        try {
            clearDraftStorage()
        } catch (e) {
            logger.warn('清除草稿失败', e)
        }

    } catch (error) {
        logger.error('保存草稿失败', error)
        ElMessage.error('保存草稿失败')
    } finally { 
        loading.value = false
    }
}

const fetchCategories = async () => { try { const {data} = await api.get('/categories/'); categories.value = data.results || data } catch {} }
const fetchTags = async () => { try { const {data} = await api.get('/tags/'); tags.value = data.results || data } catch {} }
const fetchUsers = async () => { if (!isAdmin.value) return; try { const {data} = await api.get('/auth/'); users.value = data.results || data } catch {} }

const fetchContent = async () => {
    if (!route.params.id) return
    loading.value = true
    try {
        const {data} = await getContent(route.params.id)
        Object.assign(form.value, {
            title: data.title, slug: data.slug, summary: data.summary, content: data.content,
            category: data.category, tags: data.tags?.map(t => t.id) || [],
            cover_image: data.cover_image, status: data.status, is_top: data.is_top,
            author: data.author?.id || data.author,
        })
        initLastContent(data.content)
    } catch { ElMessage.error('获取内容失败') } finally { loading.value = false }
}

const formatDraftTime = (timestamp) => {
    if (!timestamp) return ''
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date
    if (diff < 60000) return '刚刚'
    if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
    return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(async () => {
    await Promise.all([fetchCategories(), fetchTags(), fetchUsers(), fetchContent()])
    setTimeout(() => { editorLoaded.value = true }, 100)
    if (!route.params.id) {
        checkLocalDraft()
    }
})
</script>

<style scoped>
.content-form {padding: 20px}
.card-header {display: flex; justify-content: space-between; align-items: center}
.header-actions {display: flex; align-items: center; gap: 12px}
.editor-header {display: flex; align-items: center; gap: 12px; margin-bottom: 12px}
.editor-label {font-size: 14px; font-weight: 500; color: var(--text-primary)}
.select-with-button {display: flex; gap: 8px; align-items: center; width: 100%}
.editor-wrapper {width: 100%}
.editor-loading {height: 500px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; color: var(--text-tertiary); background: var(--bg-tertiary); border-radius: var(--radius-md)}
.form-tip {font-size: 12px; color: var(--text-tertiary); margin-left: 8px}
.form-item-custom {display: flex; align-items: center; margin-bottom: 18px}
.form-label {width: 100px; text-align: right; font-size: 14px; color: var(--text-primary); padding-right: 12px; box-sizing: border-box; flex-shrink: 0}
.cover-upload-wrapper {display: flex; flex-direction: column; gap: 8px; align-items: flex-start}
.cover-upload-wrapper .media-btn {width: 100%}
.draft-restore-hint p {margin: 0 0 12px; color: var(--text-secondary); font-size: 14px}
.draft-preview {background: var(--bg-tertiary); border-radius: var(--radius-sm); padding: 12px}
.draft-info {font-size: 13px; color: var(--text-secondary); padding: 4px 0}
.draft-info strong {color: var(--text-primary)}
.form-actions :deep(.el-form-item__content) {display: flex; gap: 12px; align-items: center}

/* ---- 工具类 ---- */
.full-width-select {width: 100%}
.radio-wrapper {position: relative; display: inline-flex}
.sr-only {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
    pointer-events: none;
}
</style>
