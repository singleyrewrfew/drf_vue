<template>
    <div class="custom-select"
         :class="{ 'is-open': isOpen, 'has-value': modelValue }"
         ref="selectRef"
    >
        <div
            class="select-trigger"
            role="combobox"
            :aria-expanded="isOpen"
            :aria-haspopup="listboxId"
            tabindex="0"
            @click="toggleDropdown"
            @keydown.enter.prevent="openDropdown"
            @keydown.space.prevent="openDropdown"
            @keydown.down.prevent="openDropdown"
            @keydown.escape.stop="closeDropdown"
        >
            <span class="select-value" v-if="selectedLabel">{{ selectedLabel }}</span>
            <span class="select-placeholder" v-else>{{ placeholder }}</span>
            <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
            </svg>
        </div>

        <transition name="dropdown">
            <ul
                v-show="isOpen"
                class="select-dropdown"
                :id="listboxId"
                role="listbox"
                :aria-activedescendant="activeDescendant"
                ref="dropdownRef"
                tabindex="-1"
                @keydown="handleKeydown"
            >
                <li
                    v-if="showAllOption"
                    id="__all_option__"
                    class="select-option"
                    :class="{ 'is-selected': modelValue === null }"
                    role="option"
                    :aria-selected="modelValue === null"
                    @click="selectOption(null)"
                    @mouseenter="activeIndex = -1"
                    @keydown.enter.prevent="selectOption(null)"
                    @keydown.space.prevent="selectOption(null)"
                >
                    全部
                </li>
                <li
                    v-for="(option, index) in options"
                    :key="getOptionValue(option)"
                    :id="`${listboxId}-opt-${index}`"
                    class="select-option"
                    :class="{ 'is-selected': modelValue === getOptionValue(option), 'is-active': activeIndex === index }"
                    role="option"
                    :aria-selected="modelValue === getOptionValue(option)"
                    @click="selectOption(option)"
                    @mouseenter="activeIndex = index"
                >
                    {{ getOptionLabel(option) }}
                </li>
            </ul>
        </transition>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick, useId } from 'vue'

const props = defineProps({
    /** 当前选中值 */
    modelValue: {
        type: [String, Number],
        default: null
    },
    /** 选项列表（对象数组或字符串数组） */
    options: {
        type: Array,
        default: () => []
    },
    /** 占位文字 */
    placeholder: {
        type: String,
        default: '请选择'
    },
    /** 对象选项的 label 字段名 */
    labelKey: {
        type: String,
        default: 'label'
    },
    /** 对象选项的 value 字段名 */
    valueKey: {
        type: String,
        default: 'value'
    },
    /** 是否显示"全部"选项 */
    showAllOption: {
        type: Boolean,
        default: true
    },
    /** 是否禁用 */
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'change'])

const selectRef = ref(null)
const dropdownRef = ref(null)
const isOpen = ref(false)
const activeIndex = ref(-1)
const listboxId = `custom-select-${useId()}`

/** 当前选中项的显示文字 */
const selectedLabel = computed(() => {
    if (!props.modelValue) return ''
    const option = props.options.find(o => getOptionValue(o) === props.modelValue)
    return option ? getOptionLabel(option) : ''
})

/** 用于 aria-activedescendant 的当前活跃项 ID */
const activeDescendant = computed(() => {
    if (activeIndex.value === -1 && props.showAllOption) return '__all_option__'
    if (activeIndex.value >= 0) return `${listboxId}-opt-${activeIndex.value}`
    return undefined
})

const getOptionLabel = (option) =>
    typeof option === 'object' ? option[props.labelKey] : String(option)

const getOptionValue = (option) =>
    typeof option === 'object' ? option[props.valueKey] : option

/* ---- 操作方法 ---- */

const openDropdown = () => {
    if (props.disabled) return
    isOpen.value = true
}

const closeDropdown = () => {
    isOpen.value = false
    activeIndex.value = -1
}

const toggleDropdown = () => {
    if (props.disabled) return
    isOpen.value ? closeDropdown() : openDropdown()
}

const selectOption = (option) => {
    const value = option !== null ? getOptionValue(option) : null
    emit('update:modelValue', value)
    emit('change', value)
    closeDropdown()
}

/* ---- 键盘导航 ---- */

watch(isOpen, async (val) => {
    if (val) {
        await nextTick()
        // 聚焦到当前选中的选项
        const idx = props.options.findIndex(o => getOptionValue(o) === props.modelValue)
        const offset = props.showAllOption ? 0 : -1
        activeIndex.value = idx >= 0 ? idx : offset
        dropdownRef.value?.focus()
    }
})

const handleKeydown = (e) => {
    if (!isOpen.value) return
    const maxIndex = props.options.length - 1
    const offset = props.showAllOption ? 1 : 0

    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault()
            if (activeIndex.value < maxIndex) activeIndex.value++
            break
        case 'ArrowUp':
            e.preventDefault()
            if (activeIndex.value > (props.showAllOption ? -1 : 0)) activeIndex.value--
            break
        case 'Enter':
        case ' ':
            e.preventDefault()
            if (activeIndex.value === -1 && props.showAllOption) selectOption(null)
            else if (activeIndex.value >= 0) selectOption(props.options[activeIndex.value])
            break
        case 'Escape':
            closeDropdown()
            break
    }
}

/* ---- 点击外部关闭 ---- */

const handleClickOutside = (e) => {
    if (selectRef.value && !selectRef.value.contains(e.target)) {
        closeDropdown()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.custom-select {
    position: relative;
    width: 100%;
    font-family: var(--font-sans);
}

/* ---- 触发器 ---- */
.select-trigger {
    display: flex;
    align-items: center;
    height: var(--el-component-size, 32px);
    padding: 0 10px;
    background: var(--bg-primary);
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
    user-select: none;
    gap: 6px;
}

.select-trigger:hover {
    background: var(--bg-secondary, #f0f2f5);
}

.is-open > .select-trigger,
.select-trigger:focus-visible {
    outline: none;
    box-shadow: none;
}

.select-trigger:disabled,
.custom-select[disabled] .select-trigger {
    opacity: 0.5;
    cursor: not-allowed;
}

/* ---- 值 / 占位符 ---- */
.select-value {
    flex: 1;
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.select-placeholder {
    flex: 1;
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-placeholder, #a8abb2);
}

/* ---- 箭头图标 ---- */
.select-arrow {
    width: 12px;
    height: 12px;
    flex-shrink: 0;
    color: var(--text-quaternary, #c0c4cc);
    transition: transform 0.25s ease, color 0.2s ease;
}

.is-open > .select-trigger .select-arrow {
    transform: rotate(180deg);
}

/* ---- 下拉面板 ---- */
.select-dropdown {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    z-index: calc(var(--el-index-popper, 2000) + 10);
    padding: 4px;
    background: var(--card-bg);
    border: none;
    border-radius: var(--radius-sm);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    overflow-y: auto;
    max-height: 220px;
    outline: none;
    margin: 0;
    list-style: none;
}

/* ---- 选项 ---- */
.select-option {
    padding: 6px 10px;
    font-size: 13px;
    line-height: 20px;
    color: var(--text-primary);
    border-radius: var(--radius-xs);
    cursor: pointer;
    transition:
        background-color 0.15s ease,
        color 0.15s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.select-option:hover,
.select-option.is-active {
    background: var(--bg-secondary, #f0f2f5);
}

.select-option.is-selected {
    color: var(--primary-color);
    font-weight: 600;
    background: var(--primary-bg, #ecf5ff);
}

.select-option:hover.is-selected {
    background: var(--primary-bg-lighter, #d9ecff);
}

/* ---- 过渡动画 ---- */
.dropdown-enter-active,
.dropdown-leave-active {
    transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from,
.dropdown-leave-to {
    opacity: 0;
    transform: translateY(-6px) scale(0.96);
}
</style>
