/**
 * 媒体文件处理工具函数（扩展）
 * 
 * 包含媒体特有的工具函数（头像处理、图片验证等）
 * 通用函数（getMediaUrl、formatFileSize）从 utils/index.js re-export
 */

/** 从主工具库导入通用函数 */
export { getMediaUrl, formatFileSize } from './index.js'

/**
 * 标准化头像路径（从完整 URL 提取相对路径）
 *
 * @param {string} avatarPath - 原始头像路径
 * @returns {string} 标准化后的相对路径
 */
export const normalizeAvatarPath = (avatarPath) => {
    if (!avatarPath) return ''
    
    let path = avatarPath
    if (path.startsWith('http')) {
        const mediaIndex = path.indexOf('/media/')
        if (mediaIndex !== -1) {
            path = path.substring(mediaIndex)
        }
    }

    if (!path.startsWith('/')) {
        path = `/${path}`
    }

    return path
}

/**
 * 验证图片文件是否符合上传要求
 *
 * @param {File} file - 待上传的文件对象
 * @param {Object} options - 配置选项
 * @param {number} [options.maxSizeMB=2] - 最大文件大小（MB）
 * @param {string[]} [options.allowedTypes] - 允许的 MIME 类型
 * @returns {{ valid: boolean, error: string|null }} 验证结果
 */
export const validateImageFile = (file, options = {}) => {
    const {
        maxSizeMB = 2,
        allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    } = options

    if (!allowedTypes.includes(file.type)) {
        return {
            valid: false,
            error: `只能上传 ${allowedTypes.map(t => t.split('/')[1].toUpperCase()).join('/')} 格式的图片`
        }
    }

    const maxSizeBytes = maxSizeMB * 1024 * 1024
    if (file.size > maxSizeBytes) {
        return {
            valid: false,
            error: `文件大小不能超过 ${maxSizeMB}MB`
        }
    }

    return { valid: true, error: null }
}
