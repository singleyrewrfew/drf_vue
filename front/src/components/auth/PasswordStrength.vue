<template>
  <div v-if="password" class="password-strength">
    <div class="strength-bar">
      <span :class="{ active: strength >= 1 }"></span>
      <span :class="{ active: strength >= 2 }"></span>
      <span :class="{ active: strength >= 3 }"></span>
      <span :class="{ active: strength >= 4 }"></span>
    </div>
    <span class="strength-text" :class="strengthClass">{{ strengthText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  password: {
    type: String,
    default: ''
  }
})

const strength = computed(() => {
  const pwd = props.password
  if (!pwd) return 0

  let score = 0
  if (pwd.length >= 6) score++
  if (pwd.length >= 10) score++
  if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++
  if (/[0-9]/.test(pwd) && /[^A-Za-z0-9]/.test(pwd)) score++

  return score
})

const strengthText = computed(() => {
  const texts = ['', '弱', '中', '强', '很强']
  return texts[strength.value]
})

const strengthClass = computed(() => {
  const classes = ['', 'weak', 'medium', 'strong', 'very-strong']
  return classes[strength.value]
})
</script>

<style scoped>
.password-strength {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.strength-bar {
  display: flex;
  gap: 3px;
}

.strength-bar span {
  width: 28px;
  height: 3px;
  border-radius: 2px;
  background: var(--border-color);
  transition: all var(--transition-fast);
}

.strength-bar span.active {
  background: var(--danger-color);
}

.strength-bar span:nth-child(2).active {
  background: var(--warning-color);
}

.strength-bar span:nth-child(3).active {
  background: var(--success-light);
}

.strength-bar span:nth-child(4).active {
  background: var(--success-color);
}

.strength-text {
  font-size: 11px;
  font-weight: 500;
}

.strength-text.weak {
  color: var(--danger-color);
}

.strength-text.medium {
  color: var(--warning-color);
}

.strength-text.strong {
  color: var(--success-light);
}

.strength-text.very-strong {
  color: var(--success-color);
}
</style>
