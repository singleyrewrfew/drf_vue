<template>
    <div class="comments-page">
        <!--
            TablePage: 通用表格页面组件
            - :show-create="false / :show-edit="false 隐藏新建/编辑按钮（只读管理页面）
            - v-model:page / v-model:page-size 双向绑定分页
            - #row-actions 自定义操作插槽：添加审核按钮
        -->
        <TablePage
            ref="tableRef"
            title="评论管理"
            :show-create="false"
            :show-edit="false"
            :data="commentList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!-- 评论内容：支持超长文本省略显示 -->
            <el-table-column prop="content" label="评论内容" min-width="250" show-overflow-tooltip/>
            <!-- 所属文章标题 -->
            <el-table-column prop="article_title" label="所属文章" width="180" show-overflow-tooltip/>
            <!-- 评论类型：主评论或回复 -->
            <el-table-column label="评论类型" width="100">
                <template #default="{ row }">
                    <el-tag :type="row.parent ? 'info' : 'primary'" size="small">
                        {{ row.parent ? '回复' : '主评论' }}
                    </el-tag>
                </template>
            </el-table-column>
            <!-- 评论者名称：非管理员时显示（管理员看到所有用户的评论） -->
            <el-table-column prop="user_name" label="评论者" width="120" v-if="!isAdmin"/>
            <!-- 回复对象：显示被回复的用户名 -->
            <el-table-column label="回复对象" width="120">
                <template #default="{ row }">
                    <span v-if="row.reply_to_name">@{{ row.reply_to_name }}</span>
                    <span v-else style="color: #909399;">-</span>
                </template>
            </el-table-column>
            <!-- 点赞数量 -->
            <el-table-column prop="like_count" label="点赞数" width="90" align="center">
                <template #default="{ row }">
                    <span>{{ row.like_count || 0 }}</span>
                </template>
            </el-table-column>
            <!-- 审核状态：已审核或待审核 -->
            <el-table-column prop="is_approved" label="审核状态" width="100">
                <template #default="{ row }">
                    <el-tag :type="row.is_approved ? 'success' : 'warning'">
                        {{ row.is_approved ? '已审核' : '待审核' }}
                    </el-tag>
                </template>
            </el-table-column>
            <!-- 创建时间 -->
            <el-table-column prop="created_at" label="创建时间" width="180"/>

            <!--
                自定义操作列插槽：
                在内置的编辑/删除按钮之外，添加审核按钮
                仅当评论未审核（is_approved=false）时显示审核按钮
                注意：插槽名为 row-actions（非 actions）
            -->
            <template #row-actions="{ row }">
                <ActionButton
                    v-if="!row.is_approved"
                    icon="approve"
                    text="审核"
                    type="success"
                    @click="handleApprove(row)"
                />
            </template>
        </TablePage>
    </div>
</template>

<script setup>
/**
 * @file 评论管理页面 (Comments Index)
 * @description 管理系统评论的查看、审核和删除操作。
 *              这是一个只读管理页面，不支持新建或编辑评论。
 *
 * 页面功能：
 *   1. 展示评论列表（分页表格）
 *   2. 审核评论（通过按钮，仅未审核时可用）
 *   3. 删除评论（二次确认后执行）
 *   4. 权限区分：管理员查看所有评论，普通用户只看自己的评论
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑
 *   - useDelete: 处理删除操作
 *   - 特殊逻辑：根据用户角色动态调整查询参数
 *
 * @requires vue - Vue 3 核心库（ref, computed, watch, onMounted）
 * @requires element-plus - UI 组件库
 * @requires @/api/comments - 评论相关的 API 接口
 * @requires @/stores/user - 用户状态管理
 * @requires @/composables/usePagination - 分页组合式函数
 * @requires @/composables/useFormSubmit - 删除组合式函数
 * @requires @/components/TablePage.vue - 通用表格页面组件
 * @requires @/components/ApproveButton.vue - 审核按钮组件
 */

// ============================================================================
// 【1】依赖导入
// ============================================================================

/**
 * Vue 响应式 API
 * - ref: 创建响应式引用（TablePage 组件引用等）
 * - computed: 创建计算属性（isAdmin 权限判断）
 * - watch: 监听分页变化自动刷新数据
 * - onMounted: 生命周期钩子（挂载后加载数据）
 */
import {ref, computed, watch, onMounted} from 'vue'

/** Element Plus 消息提示 */
import {ElMessage} from 'element-plus'

/**
 * API 接口
 * - getComments: 获取评论列表（支持权限过滤参数）
 * - approveComment: 审核通过指定评论
 * - deleteComment: 删除指定评论
 */
import {getComments, approveComment, deleteComment} from '@/api/comments'

/** Pinia 用户 Store（获取当前用户角色信息） */
import {useUserStore} from '@/stores/user'

/**
 * Composables
 *
 * usePagination: 封装分页逻辑，自动处理 offset/limit 和 DRF 响应格式
 * useDelete: 封含删除确认+请求+提示的完整流程
 */
import {usePagination} from '@/composables/usePagination'
import {useDelete} from '@/composables/useFormSubmit'

/** 业务组件 */
import TablePage from '@/components/TablePage.vue'
import ActionButton from '@/components/ActionButton.vue'


// ============================================================================
// 【2】Composables 初始化
// ============================================================================

/** 当前登录用户的 Pinia Store */
const userStore = useUserStore()

/**
 * 当前用户是否为管理员（计算属性）
 *
 * 用途：
 *   - 管理员：查看所有评论（params.all=true），不显示"评论者"列
 *   - 普通用户：只看自己的评论（params.my=true），显示评论者列
 *
 * @returns {boolean}
 */
const isAdmin = userStore.isAdmin()

/**
 * 分页列表管理实例
 *
 * 与标准 CRUD 页面的区别在于 fetchData 函数需要根据用户角色
 * 动态调整查询参数（my/all）。
 *
 * @type {Object} usePagination 的返回值
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     *
     * 根据当前用户角色决定查询范围：
     *   - 管理员：查询所有评论（all=true）
     *   - 普通用户：只查自己的评论（my=true）
     *
     * @param {Object} params - 分页参数 {limit, offset}
     * @returns {Promise<Object>} DRF 格式的响应数据
     */
    async (params) => {
        // 根据角色添加权限过滤参数
        if (!isAdmin.value) {
            params.my = true       // 普通用户：只看自己的
        } else {
            params.all = true      // 管理员：看全部
        }

        const {data} = await getComments(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref（模板自动解包必需）
// ============================================================================

/** @type {Ref<Array>} 评论列表数据 */
const commentList = pagination.data

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
 * @type {Object} useDelete 的返回值
 * @property {Function} handleDelete(id, onSuccess?) - 执行带确认的删除操作
 */
const delOp = useDelete(
    async (id) => await deleteComment(id),
    {message: '确定删除该评论？'}
)


// ============================================================================
// 【3】事件处理函数
// ============================================================================

/**
 * 审核通过评论
 *
 * 将指定的评论标记为"已审核"状态。
 * 仅当评论当前为"待审核"状态时，表格中的审核按钮才会可见。
 *
 * 执行流程：
 *   1. 调用 approveComment API
 *   2. 显示成功消息
 *   3. 重新加载列表以更新状态
 *
 * @async
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 评论 ID
 * @returns {Promise<void>}
 */
const handleApprove = async (row) => {
    try {
        await approveComment(row.id)
        ElMessage.success('审核通过')
        await refreshData()
    } catch (error) {
        ElMessage.error('审核失败')
    }
}


// ============================================================================
// 【4】分页变化监听与生命周期
// ============================================================================

/** TablePage 组件引用 */
const tableRef = ref(null)

/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 */
watch([page, pageSize], () => {
    refreshData()
})

/**
 * 组件挂载后加载第一页评论数据
 */
onMounted(() => {
    refreshData()
})
</script>

<style scoped>
/**
 * 评论页面样式
 */
.comments-page {
    padding: 20px;
}
</style>
