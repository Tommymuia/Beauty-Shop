import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (email, password) => api.post('/auth/register', { email, password }),
  login: (email, password) => api.post('/auth/login', { email, password }),
  getProfile: () => api.get('/auth/me'),
  updateProfile: (profileData) => api.put('/auth/me', profileData),
};

export const productsAPI = {
  getAll: (params) => api.get('/products', { params }),
  getById: (id) => api.get(`/products/${id}`),
  create: (productData) => api.post('/products/', productData),
  update: (id, productData) => api.put(`/products/${id}`, productData),
  delete: (id) => api.delete(`/products/${id}`),
};

export const cartAPI = {
  getCart: () => api.get('/cart/'),
  addItem: (productId, quantity) => api.post('/cart/', { product_id: productId, quantity }),
  updateItem: (itemId, quantity) => api.put(`/cart/${itemId}`, { quantity }),
  removeItem: (itemId) => api.delete(`/cart/${itemId}`),
  clearCart: () => api.delete('/cart/'),
};

export const ordersAPI = {
  create: (orderData) => api.post('/orders/', orderData),
  checkout: (phoneNumber, cartItems) => api.post('/orders/checkout', { 
    phone_number: phoneNumber,
    cart_items: cartItems 
  }),
  getUserOrders: () => api.get('/orders/'),
  getAllOrders: () => api.get('/orders/all'),
  getById: (orderId) => api.get(`/orders/${orderId}`),
  updateStatus: (orderId, status) => api.put(`/orders/${orderId}/status`, { status }),
};

export const usersAPI = {
  getAll: () => api.get('/users/'),
  create: (userData) => api.post('/users/', userData),
  update: (userId, userData) => api.put(`/users/${userId}`, userData),
  delete: (userId) => api.delete(`/users/${userId}`),
};

export const reviewsAPI = {
  getByProduct: (productId) => api.get(`/reviews/product/${productId}`),
  create: (reviewData) => api.post('/reviews/', reviewData),
};

export default api;
