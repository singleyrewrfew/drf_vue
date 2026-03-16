<template>
  <div class="custom-select" :class="{ focused: isOpen, 'has-value': modelValue }" ref="selectRef">
    <div class="select-trigger" @click="toggleDropdown">
      <span class="select-value" v-if="selectedLabel">{{ selectedLabel }}</span>
      <span class="select-placeholder" v-else>{{ placeholder }}</span>
      <div class="select-arrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>
    </div>
    <transition name="dropdown">
      <div class="select-dropdown" v-show="isOpen">
        <div class="dropdown-item" :class="{ selected: !modelValue }" @click="selectOption(null)">
          全部
        </div>
        <div
          v-for="option in options"
          :key="getOptionValue(option)"
          class="dropdown-item"
          :class="{ selected: modelValue === getOptionValue(option) }"
          @click="selectOption(option)"
        >
          {{ getOptionLabel(option) }}
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: null
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: '请选择'
  },
  labelKey: {
    type: String,
    default: 'label'
  },
  valueKey: {
    type: String,
    default: 'value'
  }
})

const emit = defineEmits(['update:modelValue'])

const selectRef = ref(null)
const isOpen = ref(false)

const selectedLabel = computed(() => {
  if (!props.modelValue) return ''
  const option = props.options.find(o => getOptionValue(o) === props.modelValue)
  return option ? getOptionLabel(option) : ''
})

const getOptionLabel = (option) => {
  return typeof option === 'object' ? option[props.labelKey] : option
}

const getOptionValue = (option) => {
  return typeof option === 'object' ? option[props.valueKey] : option
}

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option ? getOptionValue(option) : null)
  isOpen.value = false
}

const handleClickOutside = (e) => {
  if (selectRef.value && !selectRef.value.contains(e.target)) {
    isOpen.value = false
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
}

.select-trigger {
  display: flex;
  align-items: center;
  height: 32px;
  padding: 0 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s ease;
}

.select-trigger:hover {
  border-color: var(--border-dark);
}

.custom-select.focused .select-trigger {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-bg);
}

.select-value {
  font-size: 14px;
  color: var(--text-primary);
  flex: 1;
}

.select-placeholder {
  font-size: 14px;
  color: var(--text-tertiary);
  flex: 1;
}

.select-arrow {
  width: 14px;
  height: 14px;
  color: var(--text-tertiary);
  transition: all 0.15s ease;
  flex-shrink: 0;
  margin-left: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-select.focused .select-arrow {
  transform: rotate(180deg);
  color: var(--primary-color);
}

.select-arrow svg {
  width: 100%;
  height: 100%;
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-item {
  padding: 8px 12px;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.1s ease;
}

.dropdown-item:hover {
  background: var(--bg-secondary);
}

.dropdown-item.selected {
  background: var(--primary-bg);
  color: var(--primary-color);
  font-weight: 500;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.15s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
