import axios from 'axios';

// Create axios instance with base URL from environment variables or default to local development
const apiClient = axios.create({
  baseURL: (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/?$/, '/'),
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  maxRedirects: 5, // Allow following redirects
  validateStatus: status => status >= 200 && status < 500, // Accept 2xx, 3xx, and 4xx status codes
});

// Request interceptor for adding auth token if available
apiClient.interceptors.request.use(
  (config) => {
    // You can add auth token here if needed
    // const token = localStorage.getItem('auth_token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors here (e.g., 401 Unauthorized)
    if (error.response?.status === 401) {
      // Handle unauthorized access
      console.error('Unauthorized access - please login again');
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const api = {
  // General
  getHealth: () => apiClient.get('health'),

  // Workers
  getWorkers: () => apiClient.get('workers'),
  getWorker: (id: number) => apiClient.get(`workers/${id}`),
  createWorker: (workerData: any) => apiClient.post('workers', workerData),
  updateWorker: (id: number, workerData: any) => apiClient.put(`workers/${id}`, workerData),
  deleteWorker: (id: number) => apiClient.delete(`workers/${id}`),
  
  // Shifts
  getShifts: () => apiClient.get('shifts'),
  getShift: (id: number) => apiClient.get(`shifts/${id}`),
  createShift: (shiftData: any) => apiClient.post('shifts', shiftData),
  updateShift: (id: number, shiftData: any) => apiClient.put(`shifts/${id}`, shiftData),
  deleteShift: (id: number) => apiClient.delete(`shifts/${id}`),
};

export default api;
