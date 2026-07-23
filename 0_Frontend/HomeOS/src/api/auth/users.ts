import { api } from '../axiosClient';
import type { AllUsersUser, UserProfile, UserCreateData, UserUpdateData } from './types';


export const createUser = async (userData: UserCreateData): Promise<any> => {
    const response = await api.post('/api/users', userData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' 
        }
    });
    return response.data;
};

export const getUserProfile = async (userId: string): Promise<UserProfile> => {
    const response = await api.get(`/api/users/${userId}`);
    return response.data;
};

export const getAllUsers = async (): Promise<AllUsersUser[]> => {
    const response = await api.get('/api/users');
    return response.data;
}

export const updateUser = async (userData: UserUpdateData): Promise<any> => {
    const response = await api.put('/api/users/me', userData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' 
        }
    });
    return response.data;
};

export const updateUserAdmin = async (userData: UserUpdateData, userId: string): Promise<any> => {
    
    const response = await api.put(`/api/users/${userId}`, userData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' 
        }
    });
    return response.data;
};

export const uploadAvatarFile = async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/users/avatar/me', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' 
        }
    });
    
    return response.data;
};