<template>
    <div class="auth-input-wrap" :class="{ 'is-disabled': disabled }">
        <!-- 左侧图标插槽 -->
        <div class="ai-icon">
            <slot name="icon"/>
        </div>

        <!-- 输入框 -->
        <input
            ref="inputRef"
            :type="type"
            :value="modelValue"
            :placeholder="placeholder"
            :disabled="disabled"
            :maxlength="maxlength"
            class="ai-input"
            @input="$emit('update:modelValue', $event.target.value)"
            @focus="$emit('focus', $event)"
            @blur="$emit('blur', $event)"
        />

        <!-- 右侧插槽（suffix / password toggle 等，由外部传入） -->
        <div v-if="$slots.suffix" class="ai-suffix">
            <slot name="suffix"/>
        </div>

        <!-- 底部微光条 -->
        <span class="ai-glow"/>
    </div>
</template>

<script setup>
import {ref} from 'vue'

defineProps({
    modelValue:  { type: [String, Number], default: '' },
    type:        { type: String, default: 'text' },
    placeholder: { type: String, default: '' },
    disabled:    { type: Boolean, default: false },
    maxlength:   { type: [String, Number], default: undefined },
})

defineEmits(['update:modelValue', 'focus', 'blur'])

const inputRef = ref(null)

defineExpose({ focus: () => inputRef.value?.focus() })
</script>

<style scoped>
.auth-input-wrap {
    display: flex;
    align-items: center;
    position: relative;
    background: var(--bg-secondary, #FAFAFA);
    border: 1.5px solid var(--border-color, #E5E5E5);
    border-radius: var(--radius-md, 8px);
    overflow: hidden;
    transition:
        background 0.28s cubic-bezier(0.4, 0, 0.2, 1),
        border-color 0.28s cubic-bezier(0.4, 0, 0.2, 1),
        box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 聚焦态 */
.auth-input-wrap:focus-within {
    border-color: var(--primary-color, #0078D4);
    box-shadow:
        0 0 0 3px var(--primary-bg, rgba(0, 120, 212, 0.08)),
        0 4px 16px -4px rgba(0, 120, 212, 0.18);
}

.auth-input-wrap:focus-within .ai-icon {
    color: var(--primary-color, #0078D4);
}

.auth-input-wrap:focus-within .ai-glow {
    opacity: 1;
}

/* 禁用态 */
.auth-input-wrap.is-disabled {
    opacity: 0.55;
    cursor: not-allowed;
}
.auth-input-wrap.is-disabled .ai-input {
    cursor: not-allowed;
}

/* ---- 图标区 ---- */
.ai-icon {
    width: 38px; height: 38px;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-tertiary, #8A8A8A);
    flex-shrink: 0;
    transition: color 0.28s ease;
}

.ai-icon :deep(svg) {
    width: 16px; height: 16px;
}

/* ---- 输入框 ---- */
.ai-input {
    flex: 1;
    height: 38px;
    border: none;
    background: transparent;
    font-size: 14px;
    font-weight: 400;
    color: var(--text-primary, #1A1A1A);
    outline: none;
    caret-color: var(--primary-color, #0078D4);
}

.ai-input::placeholder { color: var(--text-disabled, #ABABAB); }

/* ---- 后缀区 ---- */
.ai-suffix {
    display: flex; align-items: center; justify-content: center;
    min-width: 36px;
    flex-shrink: 0;
}

/* ---- 底部微光条 ---- */
.ai-glow {
    position: absolute;
    bottom: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary-color, #0078D4), transparent);
    opacity: 0;
    transition: opacity 0.28s ease;
    pointer-events: none;
}
</style>
