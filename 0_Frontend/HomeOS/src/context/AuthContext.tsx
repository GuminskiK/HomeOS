// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { api } from '../api/axiosClient';

interface User {
  username: string;
  is_superuser: boolean;
  is_totp_enabled: boolean;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (updatedData: User) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchUserProfile = useCallback(async () => {
    try {
      const response = await api.get<User>('/api/users/me'); 
      setUser(response.data);
      return response.data;
    } catch (error) {
      setUser(null);
      return null;
    }
  }, []);

  useEffect(() => {
    const checkSession = async () => {
      await fetchUserProfile();
      setIsLoading(false);
    };
    checkSession();
  }, [fetchUserProfile]);

  useEffect(() => {
    const handleUnauthorized = () => {
      // Serwer powiedział, że nie mamy już sesji.
      // Czyścimy stan użytkownika. To sprawi, że ProtectedRoute zrobi redirect.
      setUser(null); 
    };

    // Zaczynamy nasłuchiwać
    window.addEventListener('auth:unauthorized', handleUnauthorized);

    // Sprzątamy po sobie, gdyby komponent został odmontowany
    return () => {
      window.removeEventListener('auth:unauthorized', handleUnauthorized);
    };
  }, []);

  const login = useCallback(async () => {
    await fetchUserProfile();
  }, [fetchUserProfile]);

  const logout = useCallback(async () => {
    setUser(null);
  }, []);

  const updateUser = useCallback((updatedData: User) => {
    setUser(updatedData);
  }, []);

  const contextValue = useMemo(() => ({
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    updateUser
  }), [user, isLoading, login, logout, updateUser]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};