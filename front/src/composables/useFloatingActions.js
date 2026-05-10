import { ref, readonly } from 'vue'

const extraButtons = ref([])

export function useFloatingActions() {
  function registerButton(config) {
    const buttonId = config.id || `btn-${Date.now()}`

    if (!extraButtons.value.find(btn => btn.id === buttonId)) {
      extraButtons.value.push({
        id: buttonId,
        ...config
      })
    }

    return () => removeButton(buttonId)
  }

  function removeButton(buttonId) {
    const index = extraButtons.value.findIndex(btn => btn.id === buttonId)
    if (index > -1) {
      extraButtons.value.splice(index, 1)
    }
  }

  function clearAllButtons() {
    extraButtons.value = []
  }

  return {
    extraButtons: readonly(extraButtons),
    registerButton,
    removeButton,
    clearAllButtons
  }
}
