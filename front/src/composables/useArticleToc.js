import { ref } from 'vue'

export function useArticleToc() {
    const activeHeadingId = ref('')
    const showTocDrawer = ref(false)
    
    const scrollToHeading = (id) => {
        const element = document.getElementById(id)
        if (element) {
            const headerHeight = 72
            const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
            window.scrollTo({
                top: elementPosition - headerHeight - 16,
                behavior: 'smooth'
            })
        }
    }
    
    const handleTocClick = (id) => {
        showTocDrawer.value = false
        activeHeadingId.value = id
        scrollToHeading(id)
    }
    
    const openTocDrawer = () => {
        showTocDrawer.value = true
    }
    
    const closeTocDrawer = () => {
        showTocDrawer.value = false
    }
    
    return {
        activeHeadingId,
        showTocDrawer,
        scrollToHeading,
        handleTocClick,
        openTocDrawer,
        closeTocDrawer
    }
}
