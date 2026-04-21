import api from './index'

// 获取评论列表（带分页 / 筛选）
export const getComments = (params = {}) => api.get('/comments/', { params })
// 评论审核
export const approveComment = (id) => api.post(`/comments/${id}/approve/`)
// 删除评论
export const deleteComment = (id) => api.delete(`/comments/${id}/`)
