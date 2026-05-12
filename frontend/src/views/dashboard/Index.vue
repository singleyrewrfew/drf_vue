<template>
    <div class="dashboard">
        <DashboardStats :stats="stats"/>

        <el-row :gutter="20" style="margin-top: 20px">
            <el-col :xs="24" :lg="16">
                <el-card shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <span>{{ isAdmin ? '最新发布内容' : '我的最新发布' }}</span>
                            <ActionButton variant="outline" type="primary" :text="isAdmin ? '查看全部' : '查看我的'"
                                           icon="arrow-right" icon-after
                                           @click="$router.push('/contents')"/>
                        </div>
                    </template>
                    <el-table :data="stats.recent_contents" v-loading="loading">
                        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip/>
                        <el-table-column prop="author_name" label="作者" width="120" v-if="isAdmin"/>
                        <el-table-column prop="view_count" label="浏览量" width="100">
                            <template #default="{ row }">
                                <el-tag type="info" size="small">{{ row.view_count }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="created_at" label="发布时间" width="180"/>
                    </el-table>
                    <el-empty v-if="!loading && stats.recent_contents.length === 0" description="暂无内容"/>
                </el-card>
            </el-col>
            <el-col :xs="24" :lg="8">
                <QuickActionsPanel/>
                <SystemInfoCard
                    v-if="isAdmin"
                    :stats="stats"
                    :health-data="healthData"
                    :loading="healthLoading"
                    @refresh="refreshHealth"
                />
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import {useUserStore} from '@/stores/user'
import ActionButton from '@/components/ActionButton.vue'
import DashboardStats from './components/DashboardStats.vue'
import QuickActionsPanel from './components/QuickActionsPanel.vue'
import SystemInfoCard from './components/SystemInfoCard.vue'
import {fetchStats} from "@/api/stats.js"
import {fetchHealth} from "@/api/health.js"

const userStore = useUserStore()

const loading = ref(false)
const stats = ref({
    contents: 0,
    published: 0,
    drafts: 0,
    comments: 0,
    users: 0,
    media: 0,
    views: 0,
    my_contents: 0,
    my_published: 0,
    my_drafts: 0,
    my_comments: 0,
    my_views: 0,
    recent_contents: [],
})

const isAdmin = computed(() => userStore.isAdmin())

const asyncFetchStats = async () => {
    loading.value = true
    try {
        const {data} = await fetchStats()
        stats.value = {...stats.value, ...data}
    } catch (error) {
        console.error('获取统计数据失败', error)
    } finally {
        loading.value = false
    }
}

const healthLoading = ref(false)
const healthData = ref(null)

const refreshHealth = async () => {
    healthLoading.value = true
    try {
        const {data} = await fetchHealth()
        healthData.value = data
    } catch (error) {
        healthData.value = error.response?.data || null
    } finally {
        healthLoading.value = false
    }
}

onMounted(() => {
    asyncFetchStats()
})
</script>

<style scoped>
.dashboard {
    padding: 0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
