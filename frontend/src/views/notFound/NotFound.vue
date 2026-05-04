<template>
    <div class="not-found">
        <div class="not-found__content">
            <div class="not-found__icon">404</div>
            <h1 class="not-found__title">页面未找到</h1>
            <p class="not-found__desc">抱歉，您访问的页面不存在或已被移除</p>
            <div class="not-found__actions">
                <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
                <el-button @click="$router.back()">返回上页</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.not-found {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-primary);
}

.not-found__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 48px;
}

.not-found__icon {
    font-size: 120px;
    font-weight: 800;
    line-height: 1;
    color: var(--text-tertiary);
    letter-spacing: -4px;
    margin-bottom: 24px;
    user-select: none;
    font-family: var(--font-sans);
}

.not-found__title {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 12px;
    letter-spacing: -0.5px;
}

.not-found__desc {
    font-size: 15px;
    color: var(--text-secondary);
    margin: 0 0 32px;
    line-height: 1.6;
}

.not-found__actions {
    display: flex;
    gap: 12px;
}
</style>
