<template>
    <BaseDialog
        :visible="visible"
        :title="dialogTitle"
        :width="width"
        @update:visible="(val) => emit('update:show', val)"
        @close="handleClose"
    >
        <el-form ref="formRef" :model="modelValue" :rules="rules" :label-width="labelWidth" v-bind="$attrs">
            <slot></slot>
        </el-form>

        <template #footer>
            <ActionButton variant="outline" type="text" :text="cancelText" icon="reset" size="normal" @click="handleCancel"/>
            <ActionButton :text="submitText" icon="approve" size="normal" stop @click="handleSubmit" :disabled="loading"/>
        </template>
    </BaseDialog>
</template>

<script setup>
import {ref, computed} from 'vue'
import BaseDialog from './BaseDialog.vue'
import ActionButton from '@/components/ActionButton.vue'

const props = defineProps({
    modelValue: {type: Object, required: true},
    show: {type: Boolean, default: false},
    isEdit: {type: Boolean, default: false},
    createTitle: {type: String, default: '新建'},
    editTitle: {type: String, default: '编辑'},
    width: {type: [String, Number], default: 500},
    labelWidth: {type: [String, Number], default: '80px'},
    rules: {type: Object, default: () => ({})},
    loading: {type: Boolean, default: false},
    cancelText: {type: String, default: '取消'},
    submitText: {type: String, default: '确定'}
})

const emit = defineEmits(['update:show', 'submit', 'cancel', 'close'])

const visible = computed({
    get: () => props.show,
    set: (val) => emit('update:show', val)
})

const formRef = ref()
const dialogTitle = computed(() => props.isEdit ? props.editTitle : props.createTitle)

const handleSubmit = async () => {
    try {
        await formRef.value.validate()
        emit('submit', props.modelValue)
    } catch {}
}

const handleCancel = () => {
    visible.value = false
    emit('cancel')
}

const handleClose = () => {
    formRef.value?.resetFields()
    emit('close')
}

defineExpose({validate: () => formRef.value?.validate(), resetFields: () => formRef.value?.resetFields()})
</script>
