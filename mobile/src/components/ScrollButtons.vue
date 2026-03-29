<template>
    <div v-show="visible" class="scroll-buttons">
        <button class="scroll-btn" title="回到顶部" @click="scrollToTop">
            <el-icon>
                <ArrowUp />
            </el-icon>
        </button>
        <button class="scroll-btn" title="滚动到底部" @click="scrollToBottom">
            <el-icon>
                <ArrowDown />
            </el-icon>
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

const visible = ref(false)

const findScrollElement = () => {
    const pageContent = document.querySelector('.page-content')
    if (pageContent && pageContent.scrollHeight > pageContent.clientHeight) {
        return pageContent
    }
    return document.documentElement
}

const checkScroll = () => {
    const el = findScrollElement()
    visible.value = el.scrollTop > 100
}

const scrollToTop = () => {
    const el = findScrollElement()
    el.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToBottom = () => {
    const el = findScrollElement()
    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
}

onMounted(() => {
    const el = findScrollElement()
    el.addEventListener('scroll', checkScroll)
    window.addEventListener('scroll', checkScroll, true)
    checkScroll()
})

onUnmounted(() => {
    const el = findScrollElement()
    el.removeEventListener('scroll', checkScroll)
    window.removeEventListener('scroll', checkScroll, true)
})
</script>

<style scoped>
.scroll-buttons {
    position: fixed;
    right: 16px;
    bottom: calc(var(--tab-bar-height) + var(--safe-area-bottom) + 16px);
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: var(--z-sticky);
}

.scroll-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--card-bg);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    transition: all var(--transition-fast);
}

.scroll-btn:active {
    transform: scale(0.95);
    background: var(--bg-secondary);
}

:global(.dark) .scroll-btn,
:global([data-theme='dark']) .scroll-btn {
    background: var(--bg-tertiary);
    color: var(--text-secondary);
}
</style>
