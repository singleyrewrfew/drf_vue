<template>
    <div class="select-with-create">
        <el-select
            :model-value="modelValue"
            :placeholder="placeholder"
            :multiple="multiple"
            :clearable="clearable"
            :disabled="disabled"
            class="select-el"
            @change="$emit('update:modelValue', $event)"
        >
            <el-option v-for="item in options" :key="item[valueKey]" :label="item[labelKey]" :value="item[valueKey]"/>
        </el-select>
        <el-button type="primary" size="default" @click="$emit('create')">{{ createBtnText }}</el-button>
    </div>
</template>

<script setup>
/**
 * 选择器 + 创建按钮复合组件
 *
 * 用于「从现有选项中选择 或 快速新建」的场景，
 * 如分类选择、标签选择、作者分配等。
 */
defineProps({
    modelValue: {type: [String, Number, Array], default: null},
    options: {type: Array, required: true, default: () => []},
    labelKey: {type: String, default: 'name'},
    valueKey: {type: String, default: 'id'},
    placeholder: {type: String, default: '请选择'},
    multiple: {type: Boolean, default: false},
    clearable: {type: Boolean, default: true},
    disabled: {type: Boolean, default: false},
    createBtnText: {type: String, default: '创建'},
})

defineEmits(['update:modelValue', 'create'])
</script>

<style scoped>
.select-with-create {
    display: flex;
    gap: 8px;
    align-items: center;
    width: 100%;
}

.select-el {
    /* flex: 1 自动填充剩余空间，无需硬编码宽度 */
    flex: 1;
    min-width: 0; /* 防止内容溢出 */
}
</style>
