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
 * 解析 JWT Token 的 Payload（不验证签名）
 *
 * JWT 格式：header.payload.signature
 * Payload 是 Base64URL 编码的 JSON，包含 exp（过期时间戳）等声明。
 *
 * @param {string} token - JWT token 字符串
 * @returns {Object|null} 解析后的 payload 对象，格式错误返回 null
 *
 * @example
 * const payload = decodeJWTPayload('eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTAwMDAwMDB9.xxx')
 * // 返回: { exp: 1710000000, ... }
 */
export function decodeJWTPayload(token) {
    try {
        if (!token || typeof token !== 'string') return null
        const parts = token.split('.')
        if (parts.length !== 3) return null
        // Base64URL → Base64 → UTF-8 JSON
        const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
        const jsonPayload = decodeURIComponent(
            atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')
        )
        return JSON.parse(jsonPayload)
    } catch (e) {
        return null
    }
}

/**
 * 检查 JWT Token 是否已过期
 *
 * 解析 token payload 中的 exp 字段（Unix 时间戳，秒），
 * 与当前时间比较。提前 bufferSeconds 秒视为已过期，
 * 避免网络延迟导致请求时刚好过期。
 *
 * @param {string} token - JWT token 字符串
 * @param {number} [bufferSeconds=30] - 过期前多少秒即视为过期（安全缓冲）
 * @returns {boolean} true=已过期或无效, false=未过期
 *
 * @example
 * isTokenExpired('eyJ...')           // 默认 30 秒缓冲
 * isTokenExpired('eyJ...', 60)       // 60 秒缓冲
 * isTokenExpired('invalid-token')    // → true（无效 token 视为过期）
 */
export function isTokenExpired(token, bufferSeconds = 30) {
    if (!token || typeof token !== 'string') return true

    const payload = decodeJWTPayload(token)
    if (!payload || !payload.exp) return true

    // exp 是 Unix 时间戳（秒），Date.now() 是毫秒
    const now = Math.floor(Date.now() / 1000)
    return now >= (payload.exp - bufferSeconds)
}

/**
 * 验证 token 格式是否有效且未过期
 *
 * 综合检查：非空字符串 + 可解析 + 未超过过期时间。
 *
 * @param {string} token - 待验证的 token
 * @param {number} [bufferSeconds=30] - 过期安全缓冲秒数
 * @returns {boolean} token 是否有效且未过期
 */
export function isValidToken(token, bufferSeconds = 30) {
    return typeof token === 'string'
        && token.trim().length > 0
        && !isTokenExpired(token, bufferSeconds)
}
