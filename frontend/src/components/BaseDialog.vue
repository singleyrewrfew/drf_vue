<template>
    <Teleport to="body">
        <Transition :name="transitionName">
            <div v-if="visible" class="dialog-overlay" @click.self="handleOverlayClick">
                <div class="dialog-container" :style="{ width: computedWidth }">
                    <!-- 头部 -->
                    <div class="dialog-header">
                        <h3 class="dialog-title">
                            <slot name="title">{{ title }}</slot>
                        </h3>
                        <button v-if="closable" class="dialog-close" @click="handleClose" type="button">
                            <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="16" height="16">
                                <path fill="currentColor" d="M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12 45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512 557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12 512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z"/>
                            </svg>
                        </button>
                    </div>

                    <!-- 内容区 -->
                    <div class="dialog-body">
                        <slot></slot>
                    </div>

                    <!-- 底部 -->
                    <div v-if="$slots.footer || showDefaultFooter" class="dialog-footer">
                        <slot name="footer"></slot>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({
    modelValue: {type: Boolean, default: false},
    visible: {type: Boolean, default: null},
    title: {type: String, default: ''},
    width: {type: [String, Number], default: 500},
    closable: {type: Boolean, default: true},
    closeOnClickOverlay: {type: Boolean, default: true},
    showDefaultFooter: {type: Boolean, default: false},
    transitionName: {type: String, default: 'dialog-fade'},
})

const emit = defineEmits(['update:modelValue', 'update:visible', 'close'])

const isVisible = computed(() => props.visible ?? props.modelValue)

const computedWidth = computed(() =>
    typeof props.width === 'number' ? props.width + 'px' : props.width
)

const handleClose = () => {
    if (props.visible !== null) {
        emit('update:visible', false)
    } else {
        emit('update:modelValue', false)
    }
    emit('close')
}

const handleOverlayClick = () => {
    if (props.closeOnClickOverlay) handleClose()
}

defineExpose({handleClose})
</script>

<style scoped>
.dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 3000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.dialog-container {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), 0 10px 20px rgba(0, 0, 0, 0.15);
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.dialog-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    flex-shrink: 0;
}

.dialog-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.dialog-close {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    transition: all 0.2s ease;
}

.dialog-close:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.dialog-body {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    min-height: 0;
}

.dialog-footer {
    padding: 12px 20px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    flex-shrink: 0;
}

.dialog-fade-enter-active,
.dialog-fade-leave-active { transition: opacity 0.25s ease; }
.dialog-fade-enter-active .dialog-container,
.dialog-fade-leave-active .dialog-container { transition: transform 0.25s ease, opacity 0.25s ease; }
.dialog-fade-enter-from,
.dialog-fade-leave-to { opacity: 0; }
.dialog-fade-enter-from .dialog-container,
.dialog-fade-leave-to .dialog-container { transform: scale(0.95) translateY(-10px); opacity: 0; }
</style>
