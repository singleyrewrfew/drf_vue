/**
 * 评论认证组合式函数
 */

import { useUserStore } from '@/stores/user'
import { message } from '@/utils/message'
import { useRouter } from 'vue-router'

export function useCommentAuth() {
    const userStore = useUserStore()
    const router = useRouter()

    const requireAuth = (action = '操作') => {
        if (!userStore.isLoggedIn) {
            message.authRequired(action, () => {
                router.push('/login')
            })
            return false
        }
        return true
    }

    const checkLikeAuth = callback => {
        if (requireAuth('点赞')) {
            callback()
        }
    }

    const checkCommentAuth = callback => {
        if (requireAuth('评论')) {
            callback()
        }
    }

    return {
        requireAuth,
        checkLikeAuth,
        checkCommentAuth,
    }
}
