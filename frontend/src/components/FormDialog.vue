<template>
    <el-dialog v-model="visible" :title="dialogTitle" :width="width" destroy-on-close @close="handleClose">
        <el-form ref="formRef" :model="modelValue" :rules="rules" :label-width="labelWidth" v-bind="$attrs">
            <slot></slot>
        </el-form>
        <template #footer>
            <ActionButton variant="outline" type="text" :text="cancelText" icon="reset" size="normal" @click="handleCancel"/>
            <ActionButton :text="submitText" icon="approve" size="normal" stop @click="handleSubmit" :disabled="loading"/>
        </template>
    </el-dialog>
</template>

<script setup>
import {ref, computed, watch} from 'vue'
import ActionButton from '@/components/ActionButton.vue'

const props = defineProps({
    modelValue: {
        type: Object,
        required: true
    },
    show: {
        type: Boolean,
        default: false
    },
    isEdit: {
        type: Boolean,
        default: false
    },
    createTitle: {
        type: String,
        default: '新建'
    },
    editTitle: {
        type: String,
        default: '编辑'
    },
    width: {
        type: [String, Number],
        default: '500px'
    },
    labelWidth: {
        type: [String, Number],
        default: '80px'
    },
    rules: {
        type: Object,
        default: () => ({})
    },
    loading: {
        type: Boolean,
        default: false
    },
    cancelText: {
        type: String,
        default: '取消'
    },
    submitText: {
        type: String,
        default: '确定'
    }
})

const emit = defineEmits(['update:show', 'submit', 'cancel', 'close'])

const visible = computed({
    get: () => props.show,
    set: (val) => emit('update:show', val)
})

const formRef = ref()

const dialogTitle = computed(() => {
    return props.isEdit ? props.editTitle : props.createTitle
})

const handleSubmit = async () => {
    try {
        await formRef.value.validate()
        emit('submit', props.modelValue)
    } catch (error) {
        // 验证失败
    }
}

const handleCancel = () => {
    visible.value = false
    emit('cancel')
}

const handleClose = () => {
    formRef.value?.resetFields()
    emit('close')
}

const validate = () => formRef.value?.validate()
const resetFields = () => formRef.value?.resetFields()

defineExpose({validate, resetFields, formRef})
</script>
