<template>
    <div class="search-filter">
        <SearchInput
            v-if="showSearch"
            v-model="searchValue"
            :placeholder="searchPlaceholder"
            @search="handleSearch"
        />
        <CustomSelect
            v-for="filter in filters"
            :key="filter.key"
            v-model="filterValues[filter.key]"
            :options="filter.options"
            :placeholder="filter.placeholder"
            :label-key="filter.labelKey || 'label'"
            :value-key="filter.valueKey || 'value'"
        />
        <ActionButton v-if="showSearch" icon="search" text="搜索" size="normal" stop @click="handleSearch"/>
        <ActionButton variant="outline" type="text" icon="reset" text="重置" size="normal" @click="handleReset"/>
    </div>
</template>

<script setup>
import {ref, reactive, watch} from 'vue'
import SearchInput from '@/components/SearchInput.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import ActionButton from '@/components/ActionButton.vue'

const props = defineProps({
    showSearch: {
        type: Boolean,
        default: true
    },
    searchPlaceholder: {
        type: String,
        default: '搜索...'
    },
    search: {
        type: String,
        default: ''
    },
    filters: {
        type: Array,
        default: () => []
    },
    modelValue: {
        type: Object,
        default: () => ({})
    }
})

const emit = defineEmits(['update:search', 'update:modelValue', 'search', 'reset'])

const searchValue = ref(props.search)
const filterValues = reactive({...props.modelValue})

watch(() => props.search, (val) => {
    searchValue.value = val
})

watch(() => props.modelValue, (val) => {
    Object.assign(filterValues, val)
}, {deep: true})

watch(filterValues, (val) => {
    emit('update:modelValue', {...val})
}, {deep: true})

watch(searchValue, (val) => {
    emit('update:search', val)
})

const handleSearch = () => {
    emit('search', {
        search: searchValue.value,
        filters: {...filterValues}
    })
}

const handleReset = () => {
    searchValue.value = ''
    Object.keys(filterValues).forEach(key => {
        filterValues[key] = null
    })
    emit('update:search', '')
    emit('update:modelValue', {})
    emit('reset')
}
</script>

<style scoped>
.search-filter {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}

.search-filter > .search-input-wrapper {
    width: 200px;
}

.search-filter > .custom-select {
    width: 150px;
}
</style>
