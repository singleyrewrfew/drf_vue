import api from './index.js'

// 获取仪表盘统计数据
export const fetchStats = () => api.get('/auth/stats/')
