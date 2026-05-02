import api from './index'

export const fetchHealth = () => api.get('/health/')
