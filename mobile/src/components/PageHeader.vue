<template>
    <header class="page-header">
        <div class="header-left">
            <button v-if="showBack" class="btn-back" @click="handleBack">
                <el-icon>
                    <ArrowLeft/>
                </el-icon>
            </button>
            <slot name="left"/>
        </div>
        <h1 class="page-title">{{ title }}</h1>
        <div class="header-right">
            <slot name="right"/>
        </div>
    </header>
</template>

<script setup>
import {useRouter} from 'vue-router'
import {ArrowLeft} from '@element-plus/icons-vue'

const props = defineProps({
    title: {type: String, default: ''},
    showBack: {type: Boolean, default: true}
})

const router = useRouter()

const handleBack = () => {
    router.back()
}
</script>

<style scoped>
.page-header {
    position: sticky;
    top: 0;
    z-index: var(--z-sticky);
    display: flex;
    align-items: center;
    height: var(--header-height);
    padding: 0 16px;
    background: var(--header-bg);
    border-bottom: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
}

.header-left {
    display: flex;
    align-items: center;
    min-width: 40px;
}

.page-title {
    flex: 1;
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.header-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-width: 40px;
}
</style>
