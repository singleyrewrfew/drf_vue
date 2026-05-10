<template>
  <SidebarContainer title="分类导航">
    <div class="category-list">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="category-item"
        :class="{ active: activeId === cat.id }"
        @click="handleClick(cat)"
      >
        <div class="category-left">
          <span class="category-dot"></span>
          <span class="category-name">{{ cat.name }}</span>
        </div>
        <span class="category-count">{{ cat.content_count || 0 }}</span>
      </div>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { useRouter } from 'vue-router'
import SidebarContainer from './SidebarContainer.vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  activeId: {
    type: [Number, String],
    default: null
  },
  selectable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])
const router = useRouter()

const handleClick = cat => {
  if (props.selectable) {
    emit('select', cat)
  } else {
    router.push(`/category/${cat.slug || cat.id}`)
  }
}
</script>

<style scoped>
.category-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  color: var(--ink-medium, #595959);
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: var(--tracking-normal, 0.05em);
}

.category-item:hover {
  background: rgba(45, 90, 74, 0.08);
  color: var(--primary-color, #2d5a4a);
}

.category-item.active {
  background: var(--primary-color, #2d5a4a);
  color: #fff;
}

.category-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--ink-light, #8c8c8c);
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.category-item:hover .category-dot {
  background: var(--primary-color, #2d5a4a);
  box-shadow: 0 0 4px rgba(45, 90, 74, 0.3);
}

.category-item.active .category-dot {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.5);
}

.category-name {
  font-weight: 500;
}

.category-count {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  background: var(--bg-primary, #f5f2eb);
  color: var(--ink-light, #8c8c8c);
  border-radius: var(--radius-xs);
  border: 1px solid var(--paper-aged, #ddd6c8);
  min-width: 24px;
  text-align: center;
  font-family: 'SimSun', serif;
  transition: all var(--transition-fast);
}

.category-item:hover .category-count {
  background: var(--primary-light, #e8f0ec);
  color: var(--primary-color, #2d5a4a);
  border-color: var(--primary-color, #2d5a4a);
}

.category-item.active .category-count {
  background: rgba(255, 255, 255, 0.15) !important;
  color: #fff !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
}

[data-theme='dark'] .category-item {
  color: var(--text-secondary, #c4beb0);
}

[data-theme='dark'] .category-item:hover {
  background: rgba(74, 157, 130, 0.12);
  color: var(--primary-color, #4a9d82);
}

[data-theme='dark'] .category-item.active {
  background: var(--primary-color, #4a9d82);
  color: #fff;
}

[data-theme='dark'] .category-dot {
  background: var(--text-tertiary, #8c8578);
}

[data-theme='dark'] .category-count {
  background: var(--bg-tertiary, #252219);
  color: var(--text-tertiary, #8c8578);
  border-color: var(--border-color, #3d3830);
}
</style>