export interface UserUpdateData {
    username?: string;
    password?: string;
}

export interface UserCreateData {
    username: string;
    password: string;
}

export interface UserProfile {
    username: string;
    avatarUrl?: string;
}

export interface AllUsersUser {
    id: string;
    username: string;
    avatarUrl?: string;
}