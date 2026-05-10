<template>
  <div class="demo-page">
    <!-- 右键点击区域 -->
    <div
      class="right-click-area"
      @contextmenu.prevent="handleRightClick($event)"
    >
      <p>🖱️ 在此区域右键点击，查看自定义菜单</p>
    </div>

    <!-- 自定义右键菜单 -->
    <ContextMenu
      :visible="contextMenu.visible"
      :items="contextMenu.items"
      :position="contextMenu.position"
      @select="contextMenu.handleSelect"
      @close="contextMenu.hide"
    />
  </div>
</template>

<script setup>
import ContextMenu from '@/components/common/ContextMenu.vue'
import { useContextMenu } from '@/composables/useContextMenu'

const contextMenu = useContextMenu()

const handleRightClick = (event) => {
  const menuItems = [
    { label: '返回首页', icon: '🏠', action: 'home' },
    { label: '刷新页面', icon: '🔄', action: 'refresh', shortcut: 'F5' },
    { divider: true },
    { label: '复制链接', icon: '📋', action: 'copy', shortcut: 'Ctrl+C' },
    { label: '分享文章', icon: '📤', action: 'share' },
    { divider: true },
    {
      label: '更多操作',
      icon: '⚙️',
      children: [
        { label: '收藏本文', icon: '⭐', action: 'favorite' },
        { label: '添加书签', icon: '🔖', action: 'bookmark' },
        { label: '打印页面', icon: '🖨️', action: 'print' }
      ]
    },
    { divider: true },
    { label: '查看源码', icon: '💻', action: 'source' },
  ]
  
  contextMenu.show(event, menuItems, (item) => {
    console.log('选中了:', item)
    
    // 根据不同动作执行相应逻辑
    switch (item.action) {
      case 'home':
        window.location.href = '/'
        break
      case 'refresh':
        window.location.reload()
        break
      case 'copy':
        navigator.clipboard.writeText(window.location.href)
        alert('链接已复制！')
        break
      case 'source':
        alert('查看源码功能')
        break
      default:
        console.log('执行动作:', item.action)
    }
  })
}
</script>

<style scoped>
.demo-page {
  padding: 40px;
}

.right-click-area {
  padding: 60px;
  background: var(--paper-cream, #ede8dc);
  border: 2px dashed var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-sm, 4px);
  text-align: center;
  cursor: context-menu;
  font-family: "KaiTi", "STKaiti", serif;
  font-size: 16px;
  color: var(--ink-medium, #595959);
  transition: all 0.3s ease;
}

.right-click-area:hover {
  border-color: var(--vermilion-color, #c53d43);
  background: linear-gradient(135deg, #f8f5f0 0%, #ede8dc 100%);
}
</style>
