<template>
    <div class="mobile-app">
        <router-view v-slot="{ Component }">
            <transition name="fade-slide" mode="out-in">
                <component :is="Component"/>
            </transition>
        </router-view>
    </div>
</template>

<script setup>
</script>

<style>
.mobile-app {
    min-height: 100vh;
    min-height: 100dvh;
    background: var(--bg-color);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.2s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateX(10px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateX(-10px);
}
</style>
