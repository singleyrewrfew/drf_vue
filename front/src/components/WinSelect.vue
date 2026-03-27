<template>
    <div class="win-select" ref="selectRef">
        <div class="win-select-trigger" @click="toggleDropdown">
            <span class="win-select-value">{{ displayValue || placeholder }}</span>
            <svg class="win-select-arrow" :class="{ 'is-open': isOpen }" viewBox="0 0 1024 1024" width="12" height="12">
                <path fill="currentColor"
                      d="M512 714.667c-17.067 0-32-6.4-44.8-19.2L147.2 375.467c-25.6-25.6-25.6-64 0-89.6s64-25.6 89.6 0L512 561.067l275.2-275.2c25.6-25.6 64-25.6 89.6 0s25.6 64 0 89.6L556.8 695.467c-12.8 12.8-27.733 19.2-44.8 19.2z"/>
            </svg>
        </div>
        <Teleport to="body">
            <Transition name="win-select-fade">
                <div
                    v-if="isOpen"
                    class="win-select-dropdown"
                    :style="dropdownStyle"
                    ref="dropdownRef"
                >
                    <div
                        v-for="option in options"
                        :key="option.value"
                        class="win-select-option"
                        :class="{
              'is-selected': modelValue === option.value,
              'is-disabled': option.disabled 
            }"
                        @click="selectOption(option)"
                    >
                        <span class="win-select-option-indicator" v-if="modelValue === option.value"></span>
                        <span class="win-select-option-text">{{ option.label }}</span>
                    </div>
                    <div v-if="options.length === 0" class="win-select-empty">
                        暂无数据
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup>
import {ref, computed, watch, onMounted, onUnmounted, nextTick} from 'vue'

const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: ''
    },
    options: {
        type: Array,
        default: () => []
    },
    placeholder: {
        type: String,
        default: '请选择'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'change'])

const selectRef = ref(null)
const dropdownRef = ref(null)
const isOpen = ref(false)
const dropdownStyle = ref({})

const displayValue = computed(() => {
    const option = props.options.find(opt => opt.value === props.modelValue)
    return option ? option.label : props.placeholder
})

const toggleDropdown = () => {
    if (props.disabled) return
    isOpen.value = !isOpen.value
    if (isOpen.value) {
        nextTick(() => {
            updatePosition()
        })
    }
}

const selectOption = (option) => {
    if (option.disabled) return
    emit('update:modelValue', option.value)
    emit('change', option.value)
    isOpen.value = false
}

const updatePosition = () => {
    if (!selectRef.value) return

    const rect = selectRef.value.getBoundingClientRect()

    let left = rect.left

    if (left + rect.width > window.innerWidth) {
        left = window.innerWidth - rect.width - 8
    }

    dropdownStyle.value = {
        position: 'fixed',
        top: `${rect.bottom + 4}px`,
        left: `${left}px`,
        width: `${rect.width}px`,
        zIndex: 2000
    }
}

const handleClickOutside = (e) => {
    if (!selectRef.value?.contains(e.target) &&
        !dropdownRef.value?.contains(e.target)) {
        isOpen.value = false
    }
}

const handleScroll = () => {
    if (isOpen.value) {
        updatePosition()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
    window.addEventListener('scroll', handleScroll, true)
    window.addEventListener('resize', handleScroll)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
    window.removeEventListener('scroll', handleScroll, true)
    window.removeEventListener('resize', handleScroll)
})
</script>

<style scoped>
.win-select {
    display: inline-block;
    position: relative;
}

.win-select-trigger {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 8px 12px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
    min-width: 100px;
    user-select: none;
}

.win-select-trigger:hover {
    border-color: var(--primary-color);
}

.win-select-trigger:active {
    transform: scale(0.98);
}

.win-select-value {
    font-size: 14px;
    color: var(--text-primary);
}

.win-select-arrow {
    color: var(--text-secondary);
    transition: transform var(--transition-fast);
    flex-shrink: 0;
}

.win-select-arrow.is-open {
    transform: rotate(180deg);
}

.win-select-dropdown {
    position: fixed;
    z-index: 2000;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-md);
    padding: 4px;
    max-height: 280px;
    overflow-y: auto;
}

.win-select-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: var(--radius-xs);
    cursor: pointer;
    transition: all var(--transition-fast);
    position: relative;
}

.win-select-option:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.win-select-option.is-selected {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.win-select-option.is-disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.win-select-option.is-disabled:hover {
    background: transparent;
    color: var(--text-primary);
}

.win-select-option-indicator {
    position: absolute;
    left: 0;
    top: 4px;
    bottom: 4px;
    width: 3px;
    background: var(--primary-color);
    border-radius: 0 2px 2px 0;
}

.win-select-option-text {
    font-size: 14px;
    flex: 1;
}

.win-select-empty {
    padding: 16px;
    text-align: center;
    color: var(--text-tertiary);
    font-size: 14px;
}

.win-select-fade-enter-active,
.win-select-fade-leave-active {
    transition: all 0.15s ease;
}

.win-select-fade-enter-from,
.win-select-fade-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}
</style>

<style>
.win-select-dropdown {
    position: fixed;
    z-index: 2000;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-md);
    padding: 4px;
    max-height: 280px;
    overflow-y: auto;
}

.win-select-dropdown .win-select-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: var(--radius-xs);
    cursor: pointer;
    transition: all var(--transition-fast);
    position: relative;
    color: var(--text-primary);
}

.win-select-dropdown .win-select-option:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.win-select-dropdown .win-select-option.is-selected {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.win-select-dropdown .win-select-option.is-disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.win-select-dropdown .win-select-option.is-disabled:hover {
    background: transparent;
    color: var(--text-primary);
}

.win-select-dropdown .win-select-option-indicator {
    position: absolute;
    left: 0;
    top: 4px;
    bottom: 4px;
    width: 3px;
    background: var(--primary-color);
    border-radius: 0 2px 2px 0;
}

.win-select-dropdown .win-select-option-text {
    font-size: 14px;
    flex: 1;
}

.win-select-dropdown .win-select-empty {
    padding: 16px;
    text-align: center;
    color: var(--text-tertiary);
    font-size: 14px;
}
</style>
