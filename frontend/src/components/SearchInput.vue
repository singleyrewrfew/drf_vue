<template>
    <div class="search-input">
        <div class="search-input__inner" :class="{ 'is-focused': isFocused, 'is-disabled': disabled }">
            <!-- 搜索图标 -->
            <svg class="search-input__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 aria-hidden="true">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>

            <input
                ref="inputRef"
                :type="type"
                :value="modelValue"
                :placeholder="placeholder"
                :disabled="disabled"
                class="search-input__field"
                @input="onInput"
                @focus="isFocused = true"
                @blur="onBlur"
                @keyup.enter.prevent="onSearch"
                @keyup.escape="handleClear"
            />

            <!-- 清除按钮 -->
            <button
                v-if="clearable && modelValue"
                type="button"
                class="search-input__clear"
                :aria-label="'清除'"
                @click.stop="handleClear"
            >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const props = defineProps({
    /** 双向绑定值 */
    modelValue: {
        type: String,
        default: ''
    },
    /** 占位文字 */
    placeholder: {
        type: String,
        default: '搜索...'
    },
    /** 输入类型 */
    type: {
        type: String,
        default: 'text'
    },
    /** 是否可清除 */
    clearable: {
        type: Boolean,
        default: true
    },
    /** 是否禁用 */
    disabled: {
        type: Boolean,
        default: false
    },
    /** 防抖延迟（ms），0 表示不防抖 */
    debounce: {
        type: Number,
        default: 300
    }
})

const emit = defineEmits(['update:modelValue', 'search'])

const inputRef = ref(null)
const isFocused = ref(false)

/* ---- 防抖逻辑 ---- */

let debounceTimer = null

/** 带防抖的输入处理 */
const onInput = (e) => {
    const val = e.target.value

    if (props.debounce <= 0) {
        emit('update:modelValue', val)
        return
    }

    // 清除之前的计时器
    if (debounceTimer !== null) clearTimeout(debounceTimer)

    debounceTimer = setTimeout(() => {
        emit('update:modelValue', val)
        debounceTimer = null
    }, props.debounce)
}

/* ---- 操作方法 ---- */

/** 清除内容并聚焦 */
const handleClear = () => {
    // 立即发出空值（不等防抖）
    if (debounceTimer !== null) {
        clearTimeout(debounceTimer)
        debounceTimer = null
    }
    emit('update:modelValue', '')
    inputRef.value?.focus()
}

/** 搜索（立即同步值，不受防抖影响） */
const onSearch = () => {
    // 取消正在进行的防抖
    if (debounceTimer !== null) {
        clearTimeout(debounceTimer)
        debounceTimer = null
    }
    // 立即从 DOM 获取最新值并同步
    const val = inputRef.value?.value ?? ''
    emit('update:modelValue', val)
    emit('search', val)
}

/** 失焦时重置状态 */
const onBlur = () => {
    isFocused.value = false
}

/* ---- 暴露方法 ---- */

defineExpose({ focus: () => inputRef.value?.focus() })

/* ---- 清理 ---- */
onUnmounted(() => {
    if (debounceTimer !== null) clearTimeout(debounceTimer)
})
</script>

<style scoped>
.search-input {
    position: relative;
    width: 100%;
}

/* ---- 内部容器 ---- */
.search-input__inner {
    display: flex;
    align-items: center;
    height: var(--el-component-size, 32px);
    padding: 0 8px;
    background: var(--bg-primary);
    border-radius: var(--radius-sm);
    transition: background-color 0.2s ease;
}

.search-input__inner:hover {
    background: var(--bg-secondary);
}

.is-focused {
    outline: none;
}

/* 禁用态 */
.search-input__inner.is-disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.search-input__inner.is-disabled .search-input__field {
    cursor: not-allowed;
}

/* ---- 图标 ---- */
.search-input__icon {
    width: 14px;
    height: 14px;
    flex-shrink: 0;
    color: var(--text-tertiary);
    margin-right: 6px;
    pointer-events: none;
}

/* ---- 输入框 ---- */
.search-input__field {
    flex: 1;
    min-width: 0;
    border: none;
    outline: none;
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-primary);
    background: transparent;
    padding: 0;
}

.search-input__field::placeholder {
    color: var(--text-tertiary);
}

/* ---- 清除按钮 ---- */
.search-input__clear {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    margin-left: 4px;
    flex-shrink: 0;
    padding: 0;
    border: none;
    border-radius: 50%;
    background: transparent;
    color: var(--text-tertiary);
    cursor: pointer;
    opacity: 0;
    transition:
        opacity 0.15s ease,
        background-color 0.15s ease,
        color 0.15s ease;
}

/* 聚焦或有值时显示清除按钮 */
.is-focused .search-input__clear,
.search-input__inner:hover .search-input__clear {
    opacity: 1;
}

.search-input__clear:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.search-input__clear svg {
    width: 10px;
    height: 10px;
}
</style>
