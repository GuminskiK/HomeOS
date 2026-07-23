import { api } from "@/api/axiosClient";

export const loginApi = async (username: string, password: string) => {
  const response = await api.post(
    '/api/auth/login', 
    { username, password }, 
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  return response.data;
};

export const logoutApi = async () => {
  const response = await api.post('/api/auth/logout');
  return response;
};