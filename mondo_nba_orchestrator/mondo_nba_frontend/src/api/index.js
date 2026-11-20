import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export const productsApi = {
  list: (params) => api.get('products/', { params }),
  get: (id) => api.get(`products/${id}/`),
}

export const cartApi = {
  list: () => api.get('cart/'),
  add: (data) => api.post('cart/', data),
  update: (id, data) => api.patch(`cart/${id}/`, data),
  remove: (id) => api.delete(`cart/${id}/`),
}

export const commentsApi = {
  list: (params) => api.get('comments/', { params }),
  add: (data) => api.post('comments/', data),
}

export const paymentsApi = {
  list: () => api.get('payments/'),
  create: (data) => api.post('payments/', data),
}

export const authApi = {
  login: (credentials) => api.post('auth/login/', credentials),
  register: (data) => api.post('auth/register/', data),
}

export default api