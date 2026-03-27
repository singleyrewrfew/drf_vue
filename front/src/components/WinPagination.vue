<template>
    <div class="win-pagination">
        <span class="win-pagination-total" v-if="showTotal">共 {{ total }} 条</span>

        <button
            class="win-pagination-btn"
            :disabled="currentPage === 1"
            @click="handlePrev"
        >
            <svg viewBox="0 0 1024 1024" width="12" height="12">
                <path fill="currentColor"
                      d="M672 192L384 512l288 320c12.8 14.4 12.8 36.8 0 51.2-14.4 12.8-36.8 12.8-51.2 0L304 537.6c-12.8-14.4-12.8-36.8 0-51.2l316.8-345.6c14.4-12.8 36.8-12.8 51.2 0 12.8 14.4 12.8 36.8 0 51.2z"/>
            </svg>
        </button>

        <div class="win-pagination-pager">
            <button
                v-for="page in pages"
                :key="page"
                class="win-pagination-pager-item"
                :class="{ 'is-active': currentPage === page }"
                @click="handlePageChange(page)"
            >
                {{ page }}
            </button>
        </div>

        <button
            class="win-pagination-btn"
            :disabled="currentPage >= pageCount"
            @click="handleNext"
        >
            <svg viewBox="0 0 1024 1024" width="12" height="12">
                <path fill="currentColor"
                      d="M352 192l288 320-288 320c-12.8 14.4-12.8 36.8 0 51.2 14.4 12.8 36.8 12.8 51.2 0L720 537.6c12.8-14.4 12.8-36.8 0-51.2L403.2 140.8c-14.4-12.8-36.8-12.8-51.2 0-12.8 14.4-12.8 36.8 0 51.2z"/>
            </svg>
        </button>

        <div class="win-pagination-sizes" v-if="showSizes">
            <WinSelect
                v-model="currentSize"
                :options="sizeOptions"
                @change="handleSizeChange"
            />
        </div>
    </div>
</template>

<script setup>
import {ref, computed, watch} from 'vue'
import WinSelect from './WinSelect.vue'

const props = defineProps({
    total: {
        type: Number,
        default: 0
    },
    pageSize: {
        type: Number,
        default: 10
    },
    currentPage: {
        type: Number,
        default: 1
    },
    pageSizes: {
        type: Array,
        default: () => [10, 20, 50, 100]
    },
    pagerCount: {
        type: Number,
        default: 5
    },
    showTotal: {
        type: Boolean,
        default: true
    },
    showSizes: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits(['update:currentPage', 'update:pageSize', 'current-change', 'size-change'])

const currentSize = ref(props.pageSize)

const pageCount = computed(() => Math.ceil(props.total / currentSize.value))

const sizeOptions = computed(() =>
    props.pageSizes.map(size => ({
        label: `${size} 条/页`,
        value: size
    }))
)

const pages = computed(() => {
    const pages = []
    const total = pageCount.value
    const current = props.currentPage
    const count = props.pagerCount

    let start = Math.max(1, current - Math.floor(count / 2))
    let end = Math.min(total, start + count - 1)

    if (end - start < count - 1) {
        start = Math.max(1, end - count + 1)
    }

    for (let i = start; i <= end; i++) {
        pages.push(i)
    }

    return pages
})

const handlePrev = () => {
    if (props.currentPage > 1) {
        emit('update:currentPage', props.currentPage - 1)
        emit('current-change', props.currentPage - 1)
    }
}

const handleNext = () => {
    if (props.currentPage < pageCount.value) {
        emit('update:currentPage', props.currentPage + 1)
        emit('current-change', props.currentPage + 1)
    }
}

const handlePageChange = (page) => {
    if (page !== props.currentPage) {
        emit('update:currentPage', page)
        emit('current-change', page)
    }
}

const handleSizeChange = (size) => {
    currentSize.value = size
    emit('update:pageSize', size)
    emit('size-change', size)
    if (props.currentPage !== 1) {
        emit('update:currentPage', 1)
        emit('current-change', 1)
    }
}

watch(() => props.pageSize, (val) => {
    currentSize.value = val
})
</script>

<style scoped>
.win-pagination {
    display: flex;
    align-items: center;
    gap: 8px;
}

.win-pagination-total {
    font-size: 14px;
    color: var(--text-secondary);
}

.win-pagination-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.win-pagination-btn:hover:not(:disabled) {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.win-pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.win-pagination-pager {
    display: flex;
    gap: 4px;
}

.win-pagination-pager-item {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    height: 32px;
    padding: 0 8px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 14px;
    color: var(--text-primary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.win-pagination-pager-item:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.win-pagination-pager-item.is-active {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: #fff;
}

.win-pagination-sizes {
    margin-left: 8px;
}
</style>
