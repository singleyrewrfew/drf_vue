/**
 * 评论认证组合式函数
 * 
 * 封装评论相关操作的登录验证逻辑，避免代码重复
 */

import { useUserStore } from '@/stores/user'
import { message } from '@/utils/message'
import { useRouter } from 'vue-router'

export function useCommentAuth() {
  const userStore = useUserStore()
  const router = useRouter()

  /**
   * 检查是否已登录，未登录则提示并跳转
   * @param {string} action - 操作名称
   * @returns {boolean} - 是否已登录
   */
  const requireAuth = (action = '操作') => {
    if (!userStore.isLoggedIn) {
      message.authRequired(action, () => {
        router.push('/login')
      })
      return false
    }
    return true
  }

  /**
   * 点赞操作的认证检查
   * @param {Function} callback - 认证通过后的回调
   */
  const checkLikeAuth = (callback) => {
    if (requireAuth('点赞')) {
      callback()
    }
  }

  /**
   * 评论操作的认证检查
   * @param {Function} callback - 认证通过后的回调
   */
  const checkCommentAuth = (callback) => {
    if (requireAuth('评论')) {
      callback()
    }
  }

  return {
    requireAuth,
    checkLikeAuth,
    checkCommentAuth
  }
}
