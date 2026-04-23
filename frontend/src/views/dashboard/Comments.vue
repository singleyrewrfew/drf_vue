<template>
    <div class="comments-page">
        <TablePage
            title="评论管理"
            :show-create="false"
            :show-edit="false"
            :data="commentList"
            :loading="loading"
            :page="pagination.page"
            :page-size="pagination.page_size"
            :total="pagination.total"
            @delete="handleDelete"
            @page-change="handlePageChange"
        >
            <el-table-column prop="content" label="评论内容" min-width="250" show-overflow-tooltip/>
            <el-table-column prop="article_title" label="所属文章" width="180" show-overflow-tooltip/>
            <el-table-column label="评论类型" width="100">
                <template #default="{ row }">
                    <el-tag :type="row.parent ? 'info' : 'primary'" size="small">
                        {{ row.parent ? '回复' : '主评论' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="user_name" label="评论者" width="120" v-if="!isAdmin"/>
            <el-table-column label="回复对象" width="120">
                <template #default="{ row }">
                    <span v-if="row.reply_to_name">@{{ row.reply_to_name }}</span>
                    <span v-else style="color: #909399;">-</span>
                </template>
            </el-table-column>
            <el-table-column prop="like_count" label="点赞数" width="90" align="center">
                <template #default="{ row }">
                    <span>{{ row.like_count || 0 }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="is_approved" label="审核状态" width="100">
                <template #default="{ row }">
                    <el-tag :type="row.is_approved ? 'success' : 'warning'">
                        {{ row.is_approved ? '已审核' : '待审核' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180"/>
            <!-- 自定义操作按钮：审核按钮 -->
            <!-- 只在未审核时显示 -->
            <template #actions="{ row }">
                <ApproveButton
                    v-if="!row.is_approved"
                    @click="handleApprove(row)"
                />
            </template>
        </TablePage>
    </div>
</template>

<script setup>
import {ref, onMounted, reactive} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getComments, approveComment, deleteComment} from '@/api/comments'
import {useUserStore} from '@/stores/user'
import TablePage from '@/components/TablePage.vue'
import ApproveButton from '@/components/ApproveButton.vue'

const pagination = reactive({
    page: 1,
    page_size: 10,
    total: 0,
})

const userStore = useUserStore()
const loading = ref(false)
const commentList = ref([])

const isAdmin = userStore.isAdmin()

const fetchComments = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const params = {
            limit: pagination.page_size,
            offset: offset
        }
        // 非管理员只显示自己的评论
        if (!isAdmin.value) {
            params.my = true
        } else {
            params.all = true
        }
        const {data} = await getComments(params)
        commentList.value = data.results || data
        pagination.total = data.count || commentList.value.length
    } catch (error) {
        ElMessage.error('获取评论列表失败')
    } finally {
        loading.value = false
    }
}

const handleApprove = async (row) => {
    try {
        await approveComment(row.id)
        ElMessage.success('审核通过')
        await fetchComments()
    } catch (error) {
        ElMessage.error('审核失败')
    }
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该评论？', '提示', {type: 'warning'})
    try {
        await deleteComment(row.id)
        ElMessage.success('删除成功')
        await fetchComments()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handlePageChange = ({page, page_size}) => {
    pagination.page = page
    pagination.page_size = page_size
    fetchComments()
}


onMounted(() => {
    fetchComments()
})
</script>

<style scoped>
.comments-page {
    padding: 20px;
}
</style>

