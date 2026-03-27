<template>
    <div class="password-input-wrapper">
        <div class="input-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
        </div>
        <input
            :type="showPassword ? 'text' : 'password'"
            :value="modelValue"
            :placeholder="placeholder"
            class="form-input"
            @input="$emit('update:modelValue', $event.target.value)"
            @focus="$emit('focus')"
            @blur="$emit('blur')"
        />
        <div class="input-suffix" @click="togglePassword">
            <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                    d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
            </svg>
        </div>
    </div>
</template>

<script setup>
import {ref} from 'vue'

defineEmits(['update:modelValue', 'focus', 'blur'])

defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: '请输入密码'
    }
})

const showPassword = ref(false)

const togglePassword = () => {
    showPassword.value = !showPassword.value
}
</script>

<style scoped>
.password-input-wrapper {
    display: flex;
    align-items: center;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    transition: all 0.15s ease;
}

.password-input-wrapper:focus-within {
    background: var(--bg-primary);
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-bg);
}

.input-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    flex-shrink: 0;
}

.input-icon svg {
    width: 16px;
    height: 16px;
}

.form-input {
    flex: 1;
    height: 40px;
    border: none;
    background: transparent;
    font-size: 14px;
    color: var(--text-primary);
    outline: none;
}

.form-input::placeholder {
    color: var(--text-tertiary);
}

.input-suffix {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: color 0.15s ease;
    flex-shrink: 0;
}

.input-suffix:hover {
    color: var(--primary-color);
}

.input-suffix svg {
    width: 16px;
    height: 16px;
}
</style>
