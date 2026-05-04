<template>
    <div class="content-page">
        <!--
            TablePage: 通用表格页面组件
            - :show-edit="false 内置编辑按钮不需要（使用自定义操作列）
            - v-model:page / v-model:page-size 双向绑定分页
            - #header 自定义头部：标题 + 新建按钮 + 搜索表单
            - #row-actions 自定义操作列：查看/编辑/发布/删除
        -->
        <TablePage
            ref="tableRef"
            title="内容管理"
            :show-create="false"
            :show-edit="false"
            :actions-width="260"
            :data="contentList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :default-page-size="10"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!--
                自定义卡片头部：
                包含标题、新建按钮（跳转到创建页）和搜索筛选区域
            -->
            <template #header>
                <div>
                    <div class="card-header">
                        <span>内容管理</span>
                        <!-- 新建内容：跳转到富文本编辑器页面（非弹窗表单） -->
                        <ActionButton text="新建内容" icon="plus" size="normal" spin-icon @click="$router.push('/contents/create')"/>
                    </div>
                    <!-- 搜索筛选区域 -->
                    <el-form :inline="true" :model="searchForm" class="search-form">
                        <!-- 按状态筛选：草稿/已发布/已归档 -->
                        <el-form-item label="状态" prop="status">
                            <CustomSelect
                                v-model="searchForm.status"
                                :options="statusOptions"
                                placeholder="全部"
                                style="width: 120px"
                            />
                        </el-form-item>
                        <!-- 按分类筛选：下拉选择分类 -->
                        <el-form-item label="分类" prop="category">
                            <CustomSelect
                                v-model="searchForm.category"
                                :options="categories"
                                label-key="name"
                                value-key="id"
                                placeholder="全部"
                                style="width: 150px"
                            />
                        </el-form-item>
                        <!-- 关键词搜索：按标题模糊匹配 -->
                        <el-form-item label="搜索" prop="search">
                            <SearchInput
                                v-model="searchForm.search"
                                placeholder="标题搜索"
                                @search="handleSearch"
                                style="width: 220px"
                            />
                        </el-form-item>
                        <el-form-item>
                            <ActionButton variant="outline" type="text" icon="reset" text="重置" size="normal" @click="handleReset"/>
                            <ActionButton icon="search" text="搜索" size="normal" stop @click="handleSearch" style="margin-left: 12px"/>
                        </el-form-item>
                    </el-form>
                </div>
            </template>

            <!-- 文章标题：支持超长标题省略显示 -->
            <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip/>
            <!-- 作者名称 -->
            <el-table-column prop="author_name" label="作者" width="120"/>
            <!-- 所属分类 -->
            <el-table-column prop="category_name" label="分类" width="120"/>
            <!-- 标签列表：多标签展示 -->
            <el-table-column label="标签" width="200">
                <template #default="{ row }">
                    <div class="tag-list">
                        <el-tag
                            v-for="tag in row.tags"
                            :key="tag.id"
                            size="small"
                            effect="plain"
                            class="content-tag"
                        >
                            {{ tag.name }}
                        </el-tag>
                        <span v-if="!row.tags || row.tags.length === 0" class="no-tags">-</span>
                    </div>
                </template>
            </el-table-column>
            <!-- 发布状态：草稿/已发布/已归档，用不同颜色区分 -->
            <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                    <StatusTag :type="statusMap[row.status]?.type" :text="statusMap[row.status]?.label"/>
                </template>
            </el-table-column>
            <!-- 浏览量统计 -->
            <el-table-column prop="view_count" label="浏览量" width="100"/>
            <!-- 创建时间 -->
            <el-table-column prop="created_at" label="创建时间" width="180"/>

            <!--
                自定义操作列：
                - 查看按钮（仅已发布的文章可见）
                - 编辑按钮（跳转到编辑页面）
                - 发布按钮（仅草稿可见）
                - 删除按钮（由 TablePage 内置处理）
                注意：插槽名为 row-actions（非 actions），内容追加到内置按钮之后
            -->
            <template #row-actions="{ row }">
                <!-- 查看文章（新窗口打开前台页面） -->
                <ActionButton
                    v-if="row.status === 'published'"
                    icon="eye"
                    text="查看"
                    type="info"
                    @click="handleView(row)"
                />
                <!-- 编辑文章（跳转到编辑页面） -->
                <ActionButton icon="edit" text="编辑" @click="handleEdit(row)"/>
                <!-- 发布文章（将草稿变为已发布状态） -->
                <ActionButton
                    v-if="row.status === 'draft'"
                    icon="publish"
                    text="发布"
                    type="success"
                    @click="handlePublish(row)"
                />
            </template>
        </TablePage>
    </div>
</template>

<script setup>
/**
 * @file 内容管理页面 (Content Index)
 * @description 管理系统文章/内容的列表查看和快捷操作界面。
 *              这是一个"列表+搜索+快捷操作"类型的页面，不支持在当前页创建或编辑内容，
 *              而是跳转到专门的富文本编辑器页面。
 *
 * 页面功能：
 *   1. 展示内容列表（分页表格，含搜索筛选）
 *   2. 搜索筛选（按状态/分类/关键词过滤）
 *   3. 新建内容（跳转到创建页面）
 *   4. 编辑内容（跳转到编辑页面）
 *   5. 查看内容（新窗口打开前台页面）
 *   6. 发布内容（将草稿一键发布）
 *   7. 删除内容（二次确认后执行）
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑（支持额外查询参数传递）
 *   - useDelete: 处理删除操作
 *
 * 特殊设计说明：
 *   - 使用 #header 自定义插槽整合了标题栏和搜索区域
 *   - 使用 #row-actions 自定义插槽追加自定义操作按钮（内置按钮之后）
 *   - 创建/编辑操作通过 router.push 跳转到独立页面（非弹窗表单）
 *
 * @requires vue - Vue 3 核心库（reactive, watch, onMounted, ref）
 * @requires vue-router - Vue Router（页面跳转）
 * @requires element-plus - UI 组件库
 * @requires @/api/content - 内容相关的 API 接口
 * @requires @/api - 通用 API 实例（用于获取分类列表）
 * @requires @/composables/usePagination - 分页组合式函数
 * @requires @/composables/useFormSubmit - 删除组合式函数
 * @requires @/components/TablePage.vue - 通用表格页面组件
 * @requires @/components/CreateButton.vue - 新建按钮组件
 * @requires @/components/EditButton.vue - 编辑按钮组件
 * @requires @/components/ViewButton.vue - 查看按钮组件
 * @requires @/components/PublishButton.vue - 发布按钮组件
 * @requires @/components/SearchButton.vue - 搜索按钮组件
 * @requires @/components/ResetButton.vue - 重置按钮组件
 * @requires @/components/SearchInput.vue - 搜索输入框组件
 * @requires @/components/CustomSelect.vue - 自定义下拉选择组件
 */

// ============================================================================
// 【1】依赖导入
// ============================================================================

/** Vue 响应式 API */
import {reactive, watch, onMounted, ref} from 'vue'

/** Vue Router（用于页面导航） */
import {useRouter} from 'vue-router'

/** Element Plus */
import {ElMessage} from 'element-plus'

/**
 * API 接口
 * - getContents: 获取内容列表（支持分页和多种筛选参数）
 * - deleteContent: 删除指定内容
 * - publishContent: 将草稿内容发布为正式状态
 */
import {getContents, deleteContent, publishContent} from '@/api/content'

/** 通用 API 实例（用于获取分类下拉数据） */
import api from '@/api'

/** Composables */
import {usePagination} from '@/composables/usePagination'
import {useDelete} from '@/composables/useFormSubmit'

/** 业务组件 */
import TablePage from '@/components/TablePage.vue'
import ActionButton from '@/components/ActionButton.vue'
import SearchInput from '@/components/SearchInput.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import StatusTag from '@/components/StatusTag.vue'


// ============================================================================
// 【2】Composables 初始化
// ============================================================================

/** Vue Router 实例 */
const router = useRouter()

/**
 * 分页列表管理实例
 *
 * 与标准 CRUD 页面的区别：fetchData 函数会自动合并当前的搜索条件。
 *
 * @type {Object}
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     *
     * 自动合并以下搜索参数到 API 请求中：
     *   - status: 文章状态（draft/published/archived）
     *   - category: 分类 ID
     *   - search: 关键词搜索（按标题模糊匹配）
     *
     * @param {Object} params - 由 usePagination 提供的分页参数 {limit, offset}
     * @returns {Promise<Object>} DRF 格式的响应数据
     */
    async (params) => {
        // 合并搜索条件到请求参数
        if (searchForm.status) params.status = searchForm.status
        if (searchForm.category) params.category = searchForm.category
        if (searchForm.search) params.search = searchForm.search.trim()

        const {data} = await getContents(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref
// ============================================================================

/** @type {Ref<Array>} 内容列表数据 */
const contentList = pagination.data

/** @type {Ref<boolean>} 加载状态 */
const loading = pagination.loading

/** @type {Ref<number>} 当前页码 */
const page = pagination.page

/** @type {Ref<number>} 每页显示条数 */
const pageSize = pagination.pageSize

/** @type {Ref<number>} 总记录数 */
const total = pagination.total

/**
 * 刷新数据的快捷方法
 * @returns {Promise<void>}
 */
const refreshData = () => pagination.fetchData()

/**
 * 删除操作管理实例
 *
 * @type {Object}
 */
const delOp = useDelete(
    async (id) => await deleteContent(id),
    {message: '确定删除该内容？'}
)


// ============================================================================
// 【3】搜索表单与辅助数据
// ============================================================================

/**
 * 搜索/筛选条件表单
 *
 * 所有字段变化后需手动调用 handleSearch 触发重新查询。
 *
 * @type {Object} 响应式对象
 * @property {string|null} status=null - 状态筛选（draft/published/archived/null=全部）
 * @property {number|null} category=null - 分类 ID 筛选（null=全部分类）
 * @property {string} search='' - 关键词搜索（按标题模糊匹配）
 */
const searchForm = reactive({
    status: null,
    category: null,
    search: '',
})

/**
 * 内容状态映射表（用于表格中的 Tag 显示）
 *
 * @type {Object.<string, Object>}
 * @property {string} draft.label='草稿' - 草稿状态的文字
 * @property {string} draft.type='info' - 草稿状态的 Tag 颜色类型
 * @property {string} published.label='已发布' - 已发布状态的文字
 * @property {string} published.type='success' - 已发布状态的 Tag 颜色类型
 * @property {string} archived.label='已归档' - 已归档状态的文字
 * @property {string} archived.type='warning' - 已归档状态的 Tag 颜色类型
 */
const statusMap = {
    draft: {label: '草稿', type: 'info'},
    published: {label: '已发布', type: 'success'},
    archived: {label: '已归档', type: 'warning'},
}

/**
 * 状态下拉选项
 *
 * @type {Array.<{label: string, value: string}>}
 */
const statusOptions = [
    {label: '草稿', value: 'draft'},
    {label: '已发布', value: 'published'},
    {label: '已归档', value: 'archived'},
]

/**
 * 分类列表（用于分类筛选下拉的数据源）
 * 在组件挂载时一次性加载。
 *
 * @type {Ref<Array>}
 */
const categories = ref([])


// ============================================================================
// 【4】事件处理函数
// ============================================================================

/**
 * 执行搜索
 *
 * 重置页码到第 1 页，然后触发数据刷新。
 * fetchData 会自动合并 searchForm 中的当前筛选条件。
 *
 * @returns {void}
 */
const handleSearch = () => {
    page.value = 1
    // watch([page, pageSize]) 会自动触发 refreshData()
}

/**
 * 重置所有筛选条件并刷新
 *
 * 清空状态/分类/关键词三个筛选项，重置到第 1 页，然后刷新数据。
 *
 * @returns {void}
 */
const handleReset = () => {
    searchForm.status = null
    searchForm.category = null
    searchForm.search = ''
    page.value = 1
    // watch([page, pageSize]) 会自动触发 refreshData()
}

/**
 * 编辑内容（跳转到编辑页面）
 *
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 内容 ID
 */
const handleEdit = (row) => {
    router.push(`/contents/${row.id}/edit`)
}

/**
 * 查看内容（新窗口打开前台展示页）
 *
 * 仅对已发布的内容可见。打开新的浏览器标签页访问前台 URL。
 *
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 内容 ID
 */
const handleView = (row) => {
    const frontUrl = import.meta.env.VITE_FRONT_URL || window.location.origin
    window.open(`${frontUrl}/article/${row.id}`, '_blank')
}

/**
 * 发布内容（将草稿变为已发布状态）
 *
 * 调用后端接口将指定内容的状态从 draft 改为 published，
 * 成功后刷新列表以更新状态显示。
 *
 * @async
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 要发布的内容 ID
 * @returns {Promise<void>}
 */
const handlePublish = async (row) => {
    try {
        await publishContent(row.id)
        ElMessage.success('发布成功')
        await refreshData()
    } catch (error) {
        ElMessage.error('发布失败')
    }
}


// ============================================================================
// 【5】分页变化监听与生命周期
// ============================================================================

/** TablePage 组件引用 */
const tableRef = ref(null)

/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 *
 * 合并监听避免切换 pageSize 时产生双重 API 请求。
 */
watch([page, pageSize], () => {
    refreshData()
})

/**
 * 组件挂载后加载初始数据
 *
 * 同时加载两个独立数据源：
 *   1. 内容列表（带默认筛选条件的分页数据）
 *   2. 分类列表（用于搜索区域的分类下拉选择）
 */
onMounted(() => {
    refreshData()
    fetchCategories()
})

/**
 * 获取分类列表（用于搜索筛选的下拉选项）
 *
 * @async
 * @returns {Promise<void>}
 */
const fetchCategories = async () => {
    try {
        const {data} = await api.get('/categories/')
        categories.value = data.results || data
    } catch (error) {
        console.error('获取分类列表失败:', error)
    }
}
</script>

<style scoped>
/**
 * 内容管理页面样式
 */
.content-page {
    padding: 20px;
}

/** 卡片头部布局（标题 + 新建按钮左右分布） */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

/** 搜索表单区域 */
.search-form {
    margin-bottom: 8px;
}

/** 标签列表容器（支持换行排列） */
.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
    min-height: 24px;
}

/** 单个标签样式微调 */
.content-tag {
    margin: 2px;
}

/** 无标签时的占位符 */
.no-tags {
    color: #909399;
    font-size: 14px;
}
</style>

<style>
/**
 * 全局样式（非 scoped）：确保自定义 Select 下拉面板的层级正确
 */
.content-select-popper {
    z-index: 9999 !important;
}
</style>
