<template>
  <el-form-item :label="label" :prop="prop" class="auth-field">
    <el-input
      :model-value="modelValue"
      :type="type"
      :placeholder="placeholder"
      :prefix-icon="iconComponent"
      :show-password="showPassword"
      size="default"
      @update:model-value="$emit('update:modelValue', $event)"
    />
    <slot></slot>
  </el-form-item>
</template>

<script setup>
import { computed } from 'vue'
import {
  User,
  Lock,
  Message,
  Phone,
  Location,
  Link as LinkIcon
} from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    required: true
  },
  prop: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  showPassword: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])

const iconMap = {
  user: User,
  lock: Lock,
  message: Message,
  phone: Phone,
  location: Location,
  link: LinkIcon
}

const iconComponent = computed(() => iconMap[props.icon] || null)
</script>

<style scoped>
.auth-field {
  margin-bottom: 14px;
}

.auth-field:last-child {
  margin-bottom: 0;
}

.auth-field :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 5px;
  font-size: 12px;
}

.auth-field :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  padding: 2px 9px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
  background: var(--bg-primary);
}

.auth-field :deep(.el-input__wrapper:hover) {
  border-color: var(--border-dark);
  background: var(--bg-secondary);
}

.auth-field :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.15);
  background: var(--card-bg);
}

.auth-field :deep(.el-input__inner) {
  height: 32px;
  line-height: 32px;
  font-size: 13px;
}

.auth-field :deep(.el-input__prefix) {
  display: flex;
  align-items: center;
}

.auth-field :deep(.el-input__icon) {
  width: 15px;
  height: 15px;
  font-size: 15px;
}
</style>
