<template>
  <div class="content-form">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑内容' : '新建内容' }}</span>
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
          <el-input v-model="form.content" type="textarea" :rows="15" placeholder="请输入正文内容" />
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
        
        <el-divider content-position="left">封面与设置</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="封面图">
              <el-upload
                class="cover-uploader"
                :action="uploadUrl"
                :headers="headers"
                :show-file-list="false"
                :on-success="handleCoverSuccess"
              >
                <img v-if="form.cover_image" :src="form.cover_image" class="cover-image" />
                <div v-else class="cover-placeholder">
                  <el-icon class="cover-uploader-icon"><Plus /></el-icon>
                  <span>点击上传封面</span>
                </div>
              </el-upload>
              <div class="cover-tip">建议尺寸: 1920x1080，支持 jpg/png 格式</div>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { createContent, updateContent, getContent } from '@/api/content'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const categories = ref([])
const tags = ref([])

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  summary: '',
  content: '',
  category: '',
  tags: [],
  cover_image: '',
  is_top: false,
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
}

const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'}/media/`)
const headers = computed(() => ({ Authorization: `Bearer ${userStore.token}` }))

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

const fetchContent = async () => {
  if (!isEdit.value) return
  try {
    const { data } = await getContent(route.params.id)
    Object.assign(form, {
      title: data.title,
      summary: data.summary,
      content: data.content,
      category: data.category,
      tags: data.tags.map((t) => t.id),
      cover_image: data.cover_image,
      is_top: data.is_top,
    })
  } catch (error) {
    ElMessage.error('获取内容失败')
    router.back()
  }
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    const submitData = { ...form }
    if (!submitData.category) {
      delete submitData.category
    }
    if (!submitData.cover_image) {
      delete submitData.cover_image
    }
    if (submitData.tags.length === 0) {
      delete submitData.tags
    }
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
  await formRef.value.validate()
  loading.value = true
  try {
    const submitData = { ...form, status: 'draft' }
    if (!submitData.category) {
      delete submitData.category
    }
    if (!submitData.cover_image) {
      delete submitData.cover_image
    }
    if (submitData.tags.length === 0) {
      delete submitData.tags
    }
    await createContent(submitData)
    ElMessage.success('草稿保存成功')
    router.push('/contents')
  } catch (error) {
    ElMessage.error('保存草稿失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchContent()
})
</script>

<style scoped>
.content-form {
  padding: 20px;
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
