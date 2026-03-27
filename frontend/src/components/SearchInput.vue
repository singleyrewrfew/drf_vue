<template>
    <div class="search-input-wrapper">
        <div class="search-input-container" :class="{ focused: isFocused }">
            <div class="search-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
            </div>
            <input
                ref="inputRef"
                :type="type"
                :value="modelValue"
                :placeholder="placeholder"
                class="search-input"
                @input="$emit('update:modelValue', $event.target.value)"
                @focus="handleFocus"
                @blur="handleBlur"
                @keyup.enter="$emit('search')"
            />
            <button v-if="modelValue" class="clear-btn" @click="handleClear">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import {ref} from 'vue'

const emit = defineEmits(['update:modelValue', 'search'])
const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: '搜索...'
    },
    type: {
        type: String,
        default: 'text'
    }
})

const inputRef = ref(null)
const isFocused = ref(false)

const handleFocus = () => {
    isFocused.value = true
}

const handleBlur = () => {
    isFocused.value = false
}

const handleClear = () => {
    emit('update:modelValue', '')
    inputRef.value?.focus()
}
</script>

<style scoped>
.search-input-wrapper {
    position: relative;
}

.search-input-container {
    position: relative;
    display: flex;
    align-items: center;
    background: var(--bg-primary);
    border-radius: var(--radius-sm);
    overflow: hidden;
    transition: all 0.15s ease;
    border: 1px solid var(--border-color);
}

.search-input-container:hover {
    border-color: var(--border-dark);
}

.search-input-container.focused {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-bg);
}

.search-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    transition: all 0.15s ease;
    flex-shrink: 0;
}

.search-icon svg {
    width: 14px;
    height: 14px;
}

.search-input-container.focused .search-icon {
    color: var(--primary-color);
}

.search-input {
    flex: 1;
    height: 32px;
    border: none;
    outline: none;
    font-size: 14px;
    color: var(--text-primary);
    background: transparent;
    padding-right: 8px;
}

.search-input::placeholder {
    color: var(--text-tertiary);
}

.clear-btn {
    width: 24px;
    height: 24px;
    margin-right: 4px;
    border: none;
    background: transparent;
    color: var(--text-tertiary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-xs);
    transition: all 0.15s ease;
}

.clear-btn:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.clear-btn svg {
    width: 12px;
    height: 12px;
}
</style>
