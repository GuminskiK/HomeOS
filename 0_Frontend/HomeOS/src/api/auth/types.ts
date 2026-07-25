export interface User{
    username: string;
    is_superuser: boolean;
    is_totp_enabled: boolean;
    avatar_url?: string;
}

export interface UserUpdateData {
    username?: string;
    password?: string;
}

export interface UserCreateData {
    username: string;
    password: string;
}

export interface AllUsersUser {
    id: string;
    username: string;
    avatar_url?: string;
}