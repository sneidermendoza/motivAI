import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { ApiResponse, AuthResponse, User, TrainingPlan, Conversation, Progress } from '@/types/api';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token JWT a las peticiones
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

// Interceptor para manejar errores y refresh token
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    // Solo intentar refresh si el error es 401 y no es un intento de login
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== '/token/' // No intentes refresh si es el login
    ) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post<{ access: string }>(`${process.env.NEXT_PUBLIC_API_URL}/token/refresh/`, {
          refresh: refreshToken,
        });
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access}`;
        }
        return api(originalRequest);
      } catch (error) {
        // Si falla el refresh, redirigir a la landing
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
        return Promise.reject(error);
      }
    }
    // Si es un error de login u otro error, solo rechaza la promesa (no recarga la página)
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: async (data: { username: string; email: string; password: string; password2: string }) => {
    const response = await api.post<ApiResponse<User>>('/users/register/', data);
    return response.data;
  },

  login: async (data: { username: string; password: string }) => {
    const response = await api.post<AuthResponse>('/token/', data);
    return response.data;
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    await api.post('/users/logout/', { refresh: refreshToken });
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getProfile: async () => {
    const response = await api.get<ApiResponse<User>>('/users/profile/me/');
    return response.data;
  },

  resetPassword: async (data: { email: string }) => {
    const response = await api.post<ApiResponse<{ reset_token?: string }>>('/users/password-reset/', data);
    return response.data;
  },

  setPassword: async (data: { password: string; token: string; email: string }) => {
    const response = await api.post<ApiResponse<any>>('/users/password-reset/confirm/', data);
    return response.data;
  },
};

// Plans API
export const plansApi = {
  getPlans: async () => {
    const response = await api.get<ApiResponse<TrainingPlan[]>>('/plans/planentrenamiento/');
    return response.data;
  },

  createPlan: async (data: any) => {
    const response = await api.post<ApiResponse<TrainingPlan>>('/plans/planentrenamiento/', data);
    return response.data;
  },

  generatePlan: async (data: any) => {
    const response = await api.post<ApiResponse<TrainingPlan>>('/plans/planentrenamiento/generate/', data);
    return response.data;
  },

  markRoutineAsCompleted: async (routineId: number, data?: { fecha_realizacion: string }) => {
    const response = await api.post<ApiResponse<any>>(`/plans/rutinas/${routineId}/realizar/`, data);
    return response.data;
  },
};

// Conversation API
export const conversationApi = {
  getConversations: async () => {
    const response = await api.get<ApiResponse<Conversation[]>>('/conversation/conversations/');
    return response.data;
  },

  createConversation: async () => {
    const response = await api.post<ApiResponse<Conversation>>('/conversation/conversations/');
    return response.data;
  },

  respondToConversation: async (conversationId: number, data: { question_id: number; raw_text: string }) => {
    const response = await api.post<ApiResponse<Conversation>>(
      `/conversation/conversations/${conversationId}/respond/`,
      data
    );
    return response.data;
  },
};

// Progress API
export const progressApi = {
  getProgress: async () => {
    const response = await api.get<ApiResponse<Progress[]>>('/progress/');
    return response.data;
  },

  createProgress: async (data: Omit<Progress, 'id' | 'usuario'>) => {
    const response = await api.post<ApiResponse<Progress>>('/progress/', data);
    return response.data;
  },
};

export default api; 