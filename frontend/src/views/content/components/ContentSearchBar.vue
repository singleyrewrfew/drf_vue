<template>
    <div class="content-search-bar">
        <div class="card-header">
            <span>{{ title }}</span>
            <ActionButton text="新建内容" icon="plus" size="normal" spin-icon @click="$router.push('/contents/create')"/>
        </div>
        <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="状态" prop="status">
                <CustomSelect
                    v-model="searchForm.status"
                    :options="CONTENT_STATUS_OPTIONS"
                    placeholder="全部"
                    style="width: 120px"
                />
            </el-form-item>
            <el-form-item label="分类" prop="category">
                <CustomSelect
                    v-model="searchForm.category"
                    :options="categories"
                    label-key="name"
                    value-key="id"
                    placeholder="全部"
                    style="width: 150px"
                />
            </el-form-item>
            <el-form-item label="搜索" prop="search">
                <SearchInput
                    v-model="searchForm.search"
                    placeholder="标题搜索"
                    @search="$emit('search')"
                    style="width: 220px"
                />
            </el-form-item>
            <el-form-item>
                <ActionButton variant="outline" type="text" icon="reset" text="重置" size="normal" @click="handleReset"/>
                <ActionButton icon="search" text="搜索" size="normal" stop @click="$emit('search')" style="margin-left: 12px"/>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import ActionButton from '@/components/ActionButton.vue'
import SearchInput from '@/components/SearchInput.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import {CONTENT_STATUS_OPTIONS} from '@/constants/contentConfig.js'

const props = defineProps({
    title: {
        type: String,
        default: '内容管理'
    },
    categories: {
        type: Array,
        default: () => []
    },
    searchForm: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['update:searchForm', 'search', 'reset'])

const handleReset = () => {
    props.searchForm.status = null
    props.searchForm.category = null
    props.searchForm.search = ''
    emit('reset')
}
</script>

<style scoped>
.content-search-bar {
    width: 100%;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.search-form {
    margin-bottom: 8px;
}
</style>
