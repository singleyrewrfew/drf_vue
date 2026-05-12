<template>
    <BaseDialog
        :visible="visible"
        :title="title"
        :width="width"
        :close-on-click-overlay="closeOnClickOverlay"
        @update:visible="(val) => emit('update:visible', val)"
        @close="handleClose"
    >
        <slot></slot>
        <template #footer>
            <slot name="footer"></slot>
        </template>
    </BaseDialog>
</template>

<script setup>
import BaseDialog from './BaseDialog.vue'

defineProps({
    visible: {type: Boolean, default: false},
    title: {type: String, default: '对话框'},
    width: {type: [String, Number], default: 800},
    closeOnClickOverlay: {type: Boolean, default: true}
})

const emit = defineEmits(['update:visible', 'close'])

const handleClose = () => {
    emit('update:visible', false)
    emit('close')
}
</script>
