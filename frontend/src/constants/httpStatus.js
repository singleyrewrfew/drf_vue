/**
 * HTTP 状态码常量定义模块
 * 
 * 提供全局使用的 HTTP 状态码枚举，按响应类型分类组织。
 * 包含完整的 HTTP/1.1 和 HTTP/2 标准状态码，以及常用的工具函数。
 * 
 * @module constants/httpStatus
 */

/**
 * 信息性响应状态码 (1xx)
 * 
 * 表示请求已被接收，继续处理。
 * 这类响应是临时响应，只包含状态行和某些可选的响应头。
 */
export const INFO_STATUS = {
    CONTINUE: 100,
    SWITCHING_PROTOCOLS: 101,
    PROCESSING: 102,
}

/**
 * 成功响应状态码 (2xx)
 * 
 * 表示请求已成功被服务器接收、理解并接受。
 * 常见的成功状态包括：200 OK、201 Created、204 No Content 等。
 */
export const SUCCESS_STATUS = {
    OK: 200,
    CREATED: 201,
    ACCEPTED: 202,
    NON_AUTHORITATIVE_INFORMATION: 203,
    NO_CONTENT: 204,
    RESET_CONTENT: 205,
    PARTIAL_CONTENT: 206,
    MULTI_STATUS: 207,
    ALREADY_REPORTED: 208,
    IM_USED: 226,
}

/**
 * 重定向状态码 (3xx)
 * 
 * 表示需要客户端采取进一步的操作才能完成请求。
 * 通常用于 URL 重定向、缓存控制等场景。
 */
export const REDIRECT_STATUS = {
    MULTIPLE_CHOICES: 300,
    MOVED_PERMANENTLY: 301,
    FOUND: 302,
    SEE_OTHER: 303,
    NOT_MODIFIED: 304,
    USE_PROXY: 305,
    TEMPORARY_REDIRECT: 307,
    PERMANENT_REDIRECT: 308,
}

/**
 * 客户端错误状态码 (4xx)
 * 
 * 表示客户端可能发生了错误，妨碍了服务器的处理。
 * 常见错误包括：400 请求参数错误、401 未授权、403 禁止访问、404 资源不存在等。
 */
export const CLIENT_ERROR_STATUS = {
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    PAYMENT_REQUIRED: 402,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    METHOD_NOT_ALLOWED: 405,
    NOT_ACCEPTABLE: 406,
    PROXY_AUTHENTICATION_REQUIRED: 407,
    REQUEST_TIMEOUT: 408,
    CONFLICT: 409,
    GONE: 410,
    LENGTH_REQUIRED: 411,
    PRECONDITION_FAILED: 412,
    PAYLOAD_TOO_LARGE: 413,
    URI_TOO_LONG: 414,
    UNSUPPORTED_MEDIA_TYPE: 415,
    RANGE_NOT_SATISFIABLE: 416,
    EXPECTATION_FAILED: 417,
    I_AM_A_TEAPOT: 418,
    MISDIRECTED_REQUEST: 421,
    UNPROCESSABLE_ENTITY: 422,
    LOCKED: 423,
    FAILED_DEPENDENCY: 424,
    TOO_EARLY: 425,
    UPGRADE_REQUIRED: 426,
    PRECONDITION_REQUIRED: 428,
    TOO_MANY_REQUESTS: 429,
    REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
    UNAVAILABLE_FOR_LEGAL_REASONS: 451,
}

/**
 * 服务器错误状态码 (5xx)
 * 
 * 表示服务器在处理请求的过程中有错误或者异常状态发生。
 * 常见错误包括：500 内部服务器错误、502 网关错误、503 服务不可用等。
 */
export const SERVER_ERROR_STATUS = {
    INTERNAL_SERVER_ERROR: 500,
    NOT_IMPLEMENTED: 501,
    BAD_GATEWAY: 502,
    SERVICE_UNAVAILABLE: 503,
    GATEWAY_TIMEOUT: 504,
    HTTP_VERSION_NOT_SUPPORTED: 505,
    VARIANT_ALSO_NEGOTIATES: 506,
    INSUFFICIENT_STORAGE: 507,
    LOOP_DETECTED: 508,
    NOT_EXTENDED: 510,
    NETWORK_AUTHENTICATION_REQUIRED: 511,
}

/**
 * 常用 HTTP 状态码快捷访问对象
 * 
 * 提供最常用的状态码集合，便于快速引用。
 * 保持向后兼容性，避免破坏现有代码。
 * 
 * @property {number} OK - 200 请求成功
 * @property {number} CREATED - 201 资源创建成功
 * @property {number} NO_CONTENT - 204 请求成功，无返回内容
 * @property {number} MOVED_PERMANENTLY - 301 资源已永久移动
 * @property {number} FOUND - 302 资源临时移动
 * @property {number} NOT_MODIFIED - 304 资源未修改（使用缓存）
 * @property {number} BAD_REQUEST - 400 请求参数错误
 * @property {number} UNAUTHORIZED - 401 未授权，需要登录认证
 * @property {number} FORBIDDEN - 403 禁止访问，权限不足
 * @property {number} NOT_FOUND - 404 请求的资源不存在
 * @property {number} METHOD_NOT_ALLOWED - 405 请求方法不允许
 * @property {number} CONFLICT - 409 资源冲突（如重复创建）
 * @property {number} UNPROCESSABLE_ENTITY - 422 请求格式正确但语义错误
 * @property {number} TOO_MANY_REQUESTS - 429 请求过于频繁，触发限流
 * @property {number} INTERNAL_SERVER_ERROR - 500 服务器内部错误
 * @property {number} BAD_GATEWAY - 502 网关错误（上游服务器无效响应）
 * @property {number} SERVICE_UNAVAILABLE - 503 服务暂时不可用（维护或过载）
 * @property {number} GATEWAY_TIMEOUT - 504 网关超时（上游服务器未及时响应）
 */
export const HTTP_STATUS = {
    // 成功
    OK: SUCCESS_STATUS.OK,
    CREATED: SUCCESS_STATUS.CREATED,
    NO_CONTENT: SUCCESS_STATUS.NO_CONTENT,
    
    // 重定向
    MOVED_PERMANENTLY: REDIRECT_STATUS.MOVED_PERMANENTLY,
    FOUND: REDIRECT_STATUS.FOUND,
    NOT_MODIFIED: REDIRECT_STATUS.NOT_MODIFIED,
    
    // 客户端错误 - 最常用
    BAD_REQUEST: CLIENT_ERROR_STATUS.BAD_REQUEST,
    UNAUTHORIZED: CLIENT_ERROR_STATUS.UNAUTHORIZED,
    FORBIDDEN: CLIENT_ERROR_STATUS.FORBIDDEN,
    NOT_FOUND: CLIENT_ERROR_STATUS.NOT_FOUND,
    METHOD_NOT_ALLOWED: CLIENT_ERROR_STATUS.METHOD_NOT_ALLOWED,
    CONFLICT: CLIENT_ERROR_STATUS.CONFLICT,
    UNPROCESSABLE_ENTITY: CLIENT_ERROR_STATUS.UNPROCESSABLE_ENTITY,
    TOO_MANY_REQUESTS: CLIENT_ERROR_STATUS.TOO_MANY_REQUESTS,
    
    // 服务器错误 - 最常用
    INTERNAL_SERVER_ERROR: SERVER_ERROR_STATUS.INTERNAL_SERVER_ERROR,
    BAD_GATEWAY: SERVER_ERROR_STATUS.BAD_GATEWAY,
    SERVICE_UNAVAILABLE: SERVER_ERROR_STATUS.SERVICE_UNAVAILABLE,
    GATEWAY_TIMEOUT: SERVER_ERROR_STATUS.GATEWAY_TIMEOUT,
}

/**
 * HTTP 状态码中文描述映射表
 * 
 * 将常用的状态码映射为对应的中文描述信息，用于用户友好的错误提示。
 * 使用计算属性名动态生成键值对。
 */
export const STATUS_CODE_DESCRIPTIONS = {
    // 2xx
    [SUCCESS_STATUS.OK]: '请求成功',
    [SUCCESS_STATUS.CREATED]: '资源创建成功',
    [SUCCESS_STATUS.NO_CONTENT]: '请求成功，无返回内容',
    
    // 3xx
    [REDIRECT_STATUS.MOVED_PERMANENTLY]: '资源已永久移动',
    [REDIRECT_STATUS.FOUND]: '资源临时移动',
    [REDIRECT_STATUS.NOT_MODIFIED]: '资源未修改',
    
    // 4xx
    [CLIENT_ERROR_STATUS.BAD_REQUEST]: '请求参数错误',
    [CLIENT_ERROR_STATUS.UNAUTHORIZED]: '未授权，需要登录',
    [CLIENT_ERROR_STATUS.FORBIDDEN]: '禁止访问',
    [CLIENT_ERROR_STATUS.NOT_FOUND]: '资源不存在',
    [CLIENT_ERROR_STATUS.METHOD_NOT_ALLOWED]: '请求方法不允许',
    [CLIENT_ERROR_STATUS.CONFLICT]: '资源冲突',
    [CLIENT_ERROR_STATUS.UNPROCESSABLE_ENTITY]: '请求格式正确但语义错误',
    [CLIENT_ERROR_STATUS.TOO_MANY_REQUESTS]: '请求过于频繁',
    
    // 5xx
    [SERVER_ERROR_STATUS.INTERNAL_SERVER_ERROR]: '服务器内部错误',
    [SERVER_ERROR_STATUS.BAD_GATEWAY]: '网关错误',
    [SERVER_ERROR_STATUS.SERVICE_UNAVAILABLE]: '服务不可用',
    [SERVER_ERROR_STATUS.GATEWAY_TIMEOUT]: '网关超时',
}

/**
 * 获取 HTTP 状态码的中文描述
 * 
 * 根据状态码返回对应的中文描述信息。如果状态码不在描述表中，
 * 则返回默认的"未知状态码"提示。
 * 
 * @param {number} code - HTTP 状态码（如 200, 404, 500 等）
 * @returns {string} 状态码对应的中文描述信息
 * 
 * @example
 * getStatusDescription(200) // '请求成功'
 * getStatusDescription(404) // '资源不存在'
 * getStatusDescription(999) // '未知状态码'
 */
export function getStatusDescription(code) {
    return STATUS_CODE_DESCRIPTIONS[code] || '未知状态码'
}

/**
 * 判断是否为成功的 HTTP 状态码
 * 
 * 检查给定的状态码是否属于 2xx 范围（200-299），
 * 表示请求已成功被服务器处理。
 * 
 * @param {number} code - HTTP 状态码
 * @returns {boolean} 如果是 2xx 状态码返回 true，否则返回 false
 * 
 * @example
 * isSuccessStatus(200) // true
 * isSuccessStatus(201) // true
 * isSuccessStatus(404) // false
 */
export function isSuccessStatus(code) {
    return code >= 200 && code < 300
}

/**
 * 判断是否为客户端错误的 HTTP 状态码
 * 
 * 检查给定的状态码是否属于 4xx 范围（400-499），
 * 表示客户端请求存在错误（如参数错误、未授权、资源不存在等）。
 * 
 * @param {number} code - HTTP 状态码
 * @returns {boolean} 如果是 4xx 状态码返回 true，否则返回 false
 * 
 * @example
 * isClientError(400) // true
 * isClientError(404) // true
 * isClientError(200) // false
 */
export function isClientError(code) {
    return code >= 400 && code < 500
}

/**
 * 判断是否为服务器错误的 HTTP 状态码
 * 
 * 检查给定的状态码是否属于 5xx 范围（500-599），
 * 表示服务器在处理请求时发生了错误或异常。
 * 
 * @param {number} code - HTTP 状态码
 * @returns {boolean} 如果是 5xx 状态码返回 true，否则返回 false
 * 
 * @example
 * isServerError(500) // true
 * isServerError(503) // true
 * isServerError(404) // false
 */
export function isServerError(code) {
    return code >= 500 && code < 600
}

// 默认导出常用状态码（保持向后兼容）
export default HTTP_STATUS
