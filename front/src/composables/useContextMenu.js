import { ref, reactive } from 'vue'

export function useContextMenu() {
  const visible = ref(false)
  const position = reactive({ x: 0, y: 0 })
  const items = ref([])

  const show = (event, menuItems) => {
    event.preventDefault()
    event.stopPropagation()

    position.x = Math.min(event.clientX, window.innerWidth - 200)
    position.y = Math.min(event.clientY, window.innerHeight - 300)
    
    items.value = menuItems
    visible.value = true
  }

  const hide = () => {
    visible.value = false
  }

  return {
    visible,
    position,
    items,
    show,
    hide
  }
}
