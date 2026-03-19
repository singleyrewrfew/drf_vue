<template>
  <div class="content-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑内容' : '新建内容' }}</span>
          <div class="header-actions">
            <el-tag v-if="autoSaveStatus" :type="autoSaveStatus === 'saving' ? 'warning' : 'success'" size="small">
              {{ autoSaveStatus === 'saving' ? '自动保存中...' : '已自动保存' }}
            </el-tag>
          </div>
        </div>
      </template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入标题" maxlength="200" show-word-limit />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="URL别名" prop="slug">
              <el-input v-model="form.slug" placeholder="留空自动生成" maxlength="200" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="摘要" prop="summary">
          <el-input v-model="form.summary" type="textarea" :rows="3" placeholder="请输入摘要（可选）" maxlength="500" show-word-limit />
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
          <div class="editor-wrapper">
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
              <el-icon class="is-loading"><Loading /></el-icon>
              <span>编辑器加载中...</span>
            </div>
          </div>
        </el-form-item>
        
        <el-divider content-position="left">分类与标签</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="form.category" placeholder="请选择分类" clearable style="width: 100%">
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="标签" prop="tags">
              <el-select v-model="form.tags" multiple placeholder="请选择标签" style="width: 100%">
                <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-if="isAdmin">
          <el-col :span="12">
            <el-form-item label="作者" prop="author">
              <el-select v-model="form.author" placeholder="请选择作者" style="width: 100%">
                <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">封面与设置</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="封面图">
              <el-upload
                class="cover-uploader"
                :action="uploadUrl"
                :headers="uploadHeaders"
                :show-file-list="false"
                :on-success="handleCoverSuccess"
                :before-upload="beforeUpload"
              >
                <img v-if="form.cover_image" :src="form.cover_image" class="cover-image" />
                <div v-else class="cover-placeholder">
                  <el-icon class="cover-uploader-icon"><Plus /></el-icon>
                  <span>点击上传封面</span>
                </div>
              </el-upload>
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
              <el-switch v-model="form.is_top" />
              <span class="form-tip">置顶内容将优先显示在列表顶部</span>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider />
        
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Loading, Upload } from '@element-plus/icons-vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { createContent, updateContent, getContent } from '@/api/content'
import api from '@/api'
import { useUserStore } from '@/stores/user'

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

const editorLoaded = ref(false)
const showPreview = ref(false)
const previewTheme = ref('github')
const codeTheme = ref('github')
const editorHeight = ref('500px')
const autoSaveStatus = ref('')
const autoSaveTimer = ref(null)
const lastSaveContent = ref('')

const form = reactive({
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
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
}

const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'}/media/`)
const uploadHeaders = computed(() => {
  const token = userStore.token
  console.log('上传 Token:', token ? '存在' : '为空')
  return {
    'Authorization': `Bearer ${token}`
  }
})

const beforeUpload = (file) => {
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
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
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
  if (form.content && form.content !== lastSaveContent.value && form.content.length > 100) {
    triggerAutoSave()
  }
}

const handleFileChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const content = e.target.result
    if (form.content) {
      ElMessageBox.confirm(
        '当前编辑器已有内容，是否覆盖？',
        '确认导入',
        {
          confirmButtonText: '覆盖',
          cancelButtonText: '追加',
          type: 'warning',
        }
      ).then(() => {
        form.content = content
        ElMessage.success('文件导入成功')
      }).catch(() => {
        form.content = form.content + '\n\n' + content
        ElMessage.success('文件内容已追加')
      })
    } else {
      form.content = content
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
  if (!form.content || form.content === lastSaveContent.value) return
  
  autoSaveStatus.value = 'saving'
  try {
    const submitData = {
      title: form.title,
      content: form.content,
      summary: form.summary,
      category: form.category,
      tags: form.tags,
      cover_image: form.cover_image,
      status: form.status,
      is_top: form.is_top,
    }
    if (!submitData.category) delete submitData.category
    if (!submitData.cover_image) delete submitData.cover_image
    if (submitData.tags.length === 0) delete submitData.tags
    
    await updateContent(route.params.id, submitData)
    lastSaveContent.value = form.content
    autoSaveStatus.value = 'saved'
    setTimeout(() => {
      autoSaveStatus.value = ''
    }, 2000)
  } catch (error) {
    autoSaveStatus.value = ''
  }
}

const getMediaBaseUrl = () => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
  return apiBaseUrl.replace(/\/api\/?$/, '')
}

const handleCoverSuccess = (response) => {
  if (response.url) {
    const baseUrl = getMediaBaseUrl()
    form.cover_image = response.url.startsWith('http') ? response.url : `${baseUrl}${response.url}`
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await api.get('/categories/')
    categories.value = data.results || data
  } catch (error) {
    console.error(error)
  }
}

const fetchTags = async () => {
  try {
    const { data } = await api.get('/tags/')
    tags.value = data.results || data
  } catch (error) {
    console.error(error)
  }
}

const fetchUsers = async () => {
  if (!isAdmin.value) return
  try {
    const { data } = await api.get('/auth/')
    users.value = data.results || data
  } catch (error) {
    console.error(error)
  }
}

const fetchContent = async () => {
  if (!route.params.id) return
  loading.value = true
  try {
    const { data } = await getContent(route.params.id)
    Object.assign(form, {
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
    const submitData = { ...form }
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
  if (!form.title && !form.content) {
    ElMessage.warning('请至少填写标题或内容')
    return
  }
  loading.value = true
  try {
    const submitData = { ...form, status: 'draft' }
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
  
  setTimeout(() => {
    editorLoaded.value = true
  }, 100)
})

onUnmounted(() => {
  if (autoSaveTimer.value) {
    clearTimeout(autoSaveTimer.value)
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
  color: #303133;
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
  color: #909399;
  background: #f5f7fa;
  border-radius: 8px;
}

.editor-loading .el-icon {
  font-size: 32px;
}

.cover-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 320px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.cover-uploader:hover {
  border-color: #409eff;
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
  color: #8c939d;
}

.cover-image {
  max-width: 100%;
  max-height: 100%;
  display: block;
  object-fit: contain;
}

.cover-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-left: 10px;
}
</style>
