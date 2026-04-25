/**
 * 认证配置常量
 * 
 * 集中管理所有与认证相关的配置项，确保前后端认证方式一致。
 * 如果后端修改认证方案，只需在此处修改即可。
 * 
 * @module constants/authConfig
 */

/**
 * JWT 认证配置
 * 
 * 与后端 Django REST Framework SimpleJWT 配置保持一致
 * 后端配置位置：backend/config/settings.py -> SIMPLE_JWT
 */
export const AUTH_CONFIG = {
    /**
     * JWT Token 类型前缀
     * 
     * 对应后端的 AUTH_HEADER_TYPES 配置
     * 常见值：'Bearer'、'JWT'、'Token'
     * 
     * 后端配置示例：
     * SIMPLE_JWT = {
     *     'AUTH_HEADER_TYPES': ('Bearer',),
     * }
     */
    TOKEN_TYPE: 'Bearer',

    /**
     * Access Token 在 localStorage 中的存储键名
     */
    ACCESS_TOKEN_KEY: 'access',

    /**
     * Refresh Token 在 localStorage 中的存储键名
     */
    REFRESH_TOKEN_KEY: 'refresh',

    /**
     * 用户信息在 localStorage 中的存储键名
     */
    USER_INFO_KEY: 'user',

    /**
     * 认证请求头的名称
     * 
     * 对应后端的 AUTH_HEADER_NAME 配置（默认为 HTTP_AUTHORIZATION）
     */
    AUTH_HEADER_NAME: 'Authorization',
}

/**
 * 构建完整的 Authorization 头值
 * 
 * 根据配置的 token type 和实际的 token 值，生成符合规范的认证头。
 * 
 * @param {string} token - JWT access token
 * @returns {string} 格式化的认证头值，如 "Bearer eyJhbGciOiJIUzI1NiIs..."
 * 
 * @example
 * const authHeader = buildAuthHeader('eyJhbGci...')
 * // 返回: "Bearer eyJhbGci..."
 */
export function buildAuthHeader(token) {
    return `${AUTH_CONFIG.TOKEN_TYPE} ${token}`
}

/**
 * 从 Authorization 头中提取 token
 * 
 * 解析认证头字符串，去除 token type 前缀，返回纯 token 值。
 * 
 * @param {string} authHeaderValue - Authorization 头的完整值
 * @returns {string|null} 提取的 token，如果格式不正确则返回 null
 * 
 * @example
 * extractTokenFromHeader('Bearer eyJhbGci...')
 * // 返回: "eyJhbGci..."
 */
export function extractTokenFromHeader(authHeaderValue) {
    if (!authHeaderValue) {
        return null
    }

    const parts = authHeaderValue.split(' ')
    if (parts.length !== 2 || parts[0] !== AUTH_CONFIG.TOKEN_TYPE) {
        return null
    }

    return parts[1]
}

/**
 * 验证 token 格式是否有效
 * 
 * 检查 token 是否为非空字符串且符合基本格式要求。
 * 
 * @param {string} token - 待验证的 token
 * @returns {boolean} token 是否有效
 */
export function isValidToken(token) {
    return typeof token === 'string' && token.trim().length > 0
}
