<template>
  <SidebarContainer title="热门标签" :icon="PriceTag">
    <div class="tag-cloud">
      <el-tag
        v-for="tag in displayTags"
        :key="tag.id"
        class="tag-item"
        type="info"
        effect="plain"
        @click="handleClick(tag)"
      >
        #{{ tag.name }}
      </el-tag>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { PriceTag } from '@element-plus/icons-vue'
import SidebarContainer from './SidebarContainer.vue'

const props = defineProps({
  tags: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 20
  }
})

const router = useRouter()

const displayTags = computed(() => {
  return props.tags.slice(0, props.maxItems)
})

const handleClick = (tag) => {
  router.push(`/tag/${tag.slug || tag.id}`)
}
</script>

<style scoped>
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all var(--transition-fast);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
}

.tag-item:hover {
  background: var(--primary-color) !important;
  color: #fff !important;
  border-color: transparent !important;
}
</style>
