import { ElMessage } from 'element-plus'
import { ERROR_MESSAGES, ERROR_CODES } from '@/constants/errorMessages'

export function useErrorHandler() {
  const getErrorMessage = (error) => {
    if (!error) return ERROR_MESSAGES.UNKNOWN

    if (error.code === ERROR_CODES.NETWORK_ERROR) {
      return ERROR_MESSAGES.NETWORK_ERROR
    }

    if (error.code === ERROR_CODES.TIMEOUT) {
      return ERROR_MESSAGES.TIMEOUT
    }

    const status = error.response?.status
    switch (status) {
      case ERROR_CODES.UNAUTHORIZED:
        return ERROR_MESSAGES.UNAUTHORIZED
      case ERROR_CODES.FORBIDDEN:
        return ERROR_MESSAGES.FORBIDDEN
      case ERROR_CODES.NOT_FOUND:
        return ERROR_MESSAGES.NOT_FOUND
      case ERROR_CODES.SERVER_ERROR:
        return ERROR_MESSAGES.SERVER_ERROR
      case ERROR_CODES.VALIDATION_ERROR:
        return error.response?.data?.message || ERROR_MESSAGES.VALIDATION_ERROR
      default:
        return error.response?.data?.message || error.message || ERROR_MESSAGES.UNKNOWN
    }
  }

  const handleError = (error, customMessage = null) => {
    console.error('Error occurred:', error)

    const message = customMessage || getErrorMessage(error)

    if (error.response?.status !== ERROR_CODES.UNAUTHORIZED) {
      ElMessage.error(message)
    }

    return message
  }

  const handleApiError = (error, fallbackMessage = '操作失败') => {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      handleError(error, fallbackMessage)
    }
  }

  return {
    getErrorMessage,
    handleError,
    handleApiError
  }
}
