import {api} from "@/api/axiosClient";
import { useAuth } from "@/context/AuthContext";


export const loginToGetSession = async (username: string, password: string): Promise<any> => {
    
    const { login } = useAuth();
    
    const response = await api.post('/api/auth/login', 
        { username, password }, 
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );

    await login();

    return response.data;
};

export const logoutFromSession = async (): Promise<any> => {
    const { logout } = useAuth();

    const response = await api.post('/api/auth/logout');

    if (response.status === 200) {
        await logout();
    }

    return response.data;
};