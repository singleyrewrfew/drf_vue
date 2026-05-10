<template>
  <SidebarContainer title="热门标签">
    <div class="tag-cloud">
      <span
        v-for="tag in displayTags"
        :key="tag.id"
        class="tag-item"
        @click="handleClick(tag)"
      >
        {{ tag.name }}
      </span>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
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

const handleClick = tag => {
  router.push(`/tag/${tag.slug || tag.id}`)
}
</script>

<style scoped>
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: all var(--transition-fast);
  border-radius: var(--radius-xs);
  padding: 5px 12px;
  font-size: 13px;
  background: var(--bg-primary, #f5f2eb);
  color: var(--ink-medium, #595959);
  border: 1px solid var(--paper-aged, #ddd6c8);
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: var(--tracking-normal, 0.05em);
  position: relative;
}

.tag-item::before {
  content: '#';
  color: var(--vermilion-color, #c53d43);
  opacity: 0.6;
  margin-right: 2px;
}

.tag-item:hover {
  background: var(--vermilion-light, #fce4e4) !important;
  color: var(--vermilion-color, #c53d43) !important;
  border-color: var(--vermilion-color, #c53d43) !important;
  transform: translateY(-1px);
  box-shadow:
    0 2px 4px rgba(197, 61, 67, 0.15),
    inset 0 0 0 1px rgba(255, 255, 255, 0.3);
}

[data-theme='dark'] .tag-item {
  background: var(--bg-tertiary, #252219);
  color: var(--text-secondary, #c4beb0);
  border-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .tag-item:hover {
  background: rgba(232, 90, 96, 0.15) !important;
  color: var(--danger-color, #e85a60) !important;
  border-color: var(--danger-color, #e85a60) !important;
}
</style>