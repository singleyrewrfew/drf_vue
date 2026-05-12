<template>
    <el-card shadow="hover">
        <template #header>
            <span>快捷操作</span>
        </template>
        <div class="quick-actions">
            <QuickActionCard title="新建内容" type="primary" @click="$router.push('/contents/create')">
                <EditPen/>
            </QuickActionCard>
            <QuickActionCard title="上传媒体" type="success" @click="$router.push('/media')">
                <Upload/>
            </QuickActionCard>
            <QuickActionCard title="个人设置" type="warning" @click="$router.push('/profile')">
                <Setting/>
            </QuickActionCard>
            <template v-if="isAdmin">
                <QuickActionCard title="分类管理" type="info" @click="$router.push('/categories')">
                    <Folder/>
                </QuickActionCard>
                <QuickActionCard title="标签管理" type="primary" @click="$router.push('/tags')">
                    <PriceTag/>
                </QuickActionCard>
                <QuickActionCard title="评论管理" type="success" @click="$router.push('/comments')">
                    <ChatDotRound/>
                </QuickActionCard>
            </template>
            <template v-else-if="isEditor">
                <QuickActionCard title="内容管理" type="info" @click="$router.push('/contents')">
                    <Document/>
                </QuickActionCard>
            </template>
        </div>
    </el-card>
</template>

<script setup>
import {computed} from 'vue'
import {
    EditPen,
    Upload,
    Setting,
    Folder,
    PriceTag,
    ChatDotRound,
    Document
} from '@element-plus/icons-vue'
import {useUserStore} from '@/stores/user'
import QuickActionCard from '@/components/QuickActionCard.vue'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin())
const isEditor = computed(() => userStore.isEditor())
</script>

<style scoped>
.quick-actions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

@media (max-width: 768px) {
    .quick-actions {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
