<template>
    <div class="dashboard-stats">
        <template v-if="isAdmin">
            <el-row :gutter="20" class="stat-row">
                <el-col :xs="12" :sm="6">
                    <StatCard :value="stats.contents" label="内容总数" type="primary" icon="Document" clickable>
                        <template #footer>已发布 {{ stats.published }} · 草稿 {{ stats.drafts }}</template>
                    </StatCard>
                </el-col>
                <el-col :xs="12" :sm="6">
                    <StatCard :value="stats.comments" label="评论总数" type="success" icon="ChatDotRound">
                        <template #footer>用户互动数据</template>
                    </StatCard>
                </el-col>
                <el-col :xs="12" :sm="6">
                    <StatCard :value="stats.users" label="用户总数" type="warning" icon="User">
                        <template #footer>注册用户</template>
                    </StatCard>
                </el-col>
                <el-col :xs="12" :sm="6">
                    <StatCard :value="formatNumber(stats.views)" label="总浏览量" type="danger" icon="View">
                        <template #footer>累计访问</template>
                    </StatCard>
                </el-col>
            </el-row>
        </template>

        <template v-else>
            <el-row :gutter="20" class="stat-row">
                <el-col :xs="12" :sm="8">
                    <StatCard :value="stats.my_contents || 0" label="我的内容" type="primary" icon="Document" clickable>
                        <template #footer>已发布 {{ stats.my_published || 0 }} · 草稿 {{ stats.my_drafts || 0 }}</template>
                    </StatCard>
                </el-col>
                <el-col :xs="12" :sm="8">
                    <StatCard :value="formatNumber(stats.my_views || 0)" label="我的浏览量" type="success" icon="View">
                        <template #footer>累计访问</template>
                    </StatCard>
                </el-col>
                <el-col :xs="12" :sm="8">
                    <StatCard :value="stats.my_comments || 0" label="我的评论" type="warning" icon="ChatDotRound">
                        <template #footer>互动数据</template>
                    </StatCard>
                </el-col>
            </el-row>
        </template>
    </div>
</template>

<script setup>
import {computed} from 'vue'
import {useUserStore} from '@/stores/user'
import StatCard from '@/components/StatCard.vue'

const props = defineProps({
    stats: {
        type: Object,
        required: true
    }
})

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin())

const formatNumber = (num) => {
    if (num >= 10000) return (num / 10000).toFixed(1) + 'w'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k'
    return num
}
</script>

<style scoped>
.stat-row {
    margin-bottom: 16px;
}
</style>
