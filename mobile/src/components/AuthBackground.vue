<template>
    <div class="bg-animation">
        <div class="bg-gradient"></div>
        <div class="bg-shapes">
            <span v-for="i in 5" :key="i" :style="getShapeStyle(i)"></span>
        </div>
    </div>
</template>

<script setup>
/**
 * 认证页面背景动画组件
 *
 * 用于 Login/Register 等认证相关页面
 * 提供统一的渐变背景和浮动动画效果
 */

const getShapeStyle = index => {
    const positions = [
        { top: '10%', left: '20%' },
        { top: '30%', left: '60%' },
        { top: '50%', left: '40%' },
        { top: '70%', left: '80%' },
        { top: '90%', left: '30%' },
    ]
    const delays = [0, 2, 4, 6, 8]

    return {
        ...positions[index - 1],
        animationDelay: `${delays[index - 1]}s`,
    }
}
</script>

<style scoped>
.bg-animation {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
}

.bg-gradient {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-shapes span {
    position: absolute;
    display: block;
    opacity: 0.1;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: float 15s infinite;
}

.bg-shapes span:nth-child(1) {
    width: 80px;
    height: 80px;
}

.bg-shapes span:nth-child(2) {
    width: 60px;
    height: 60px;
}

.bg-shapes span:nth-child(3) {
    width: 100px;
    height: 100px;
}

.bg-shapes span:nth-child(4) {
    width: 70px;
    height: 70px;
}

.bg-shapes span:nth-child(5) {
    width: 90px;
    height: 90px;
}

@keyframes float {
    0%,
    100% {
        transform: translateY(0) rotate(0deg);
    }
    50% {
        transform: translateY(-20px) rotate(180deg);
    }
}
</style>
