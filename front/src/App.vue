<template>
    <router-view/>

    <div class="scroll-buttons">
        <button
            @click="scrollToTop"
            class="scroll-btn scroll-top"
            title="回到顶部"
        >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 15l-6-6-6 6"/>
            </svg>
        </button>
        <button
            @click="scrollToBottom"
            class="scroll-btn scroll-bottom"
            title="滚动到底部"
        >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
            </svg>
        </button>
    </div>
</template>

<script setup>
const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
}

const scrollToBottom = () => {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
    })
}
</script>

<style>
.scroll-buttons {
    position: fixed;
    right: 24px;
    bottom: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 1000;
}

.scroll-btn {
    width: 40px;
    height: 40px;
    padding: 0;
    margin: 0;
    border-radius: 6px;
    background: var(--card-bg, #fff);
    border: 1px solid var(--border-color, #e4e7ed);
    color: var(--text-primary, #303133);
    box-shadow: var(--shadow-sm, 0 2px 8px rgba(0, 0, 0, 0.08));
    transition: all var(--transition-fast, 0.2s ease);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.scroll-btn:hover {
    background: var(--primary-bg, rgba(0, 120, 212, 0.1));
    border-color: var(--primary-color, #0078D4);
    color: var(--primary-color, #0078D4);
    box-shadow: var(--shadow-md, 0 4px 12px rgba(0, 0, 0, 0.12));
}

.scroll-btn:active {
    transform: scale(0.95);
}

.scroll-btn svg {
    width: 18px;
    height: 18px;
    transition: transform var(--transition-fast, 0.2s ease);
}

.scroll-top:hover svg {
    transform: translateY(-2px);
}

.scroll-bottom:hover svg {
    transform: translateY(2px);
}

@media (max-width: 768px) {
    .scroll-buttons {
        right: 16px;
        bottom: 140px;
    }

    .scroll-btn {
        width: 36px;
        height: 36px;
    }

    .scroll-btn svg {
        width: 16px;
        height: 16px;
    }
}
</style>
