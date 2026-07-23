import React, { useEffect } from 'react';
import { api } from '../../api/axiosClient.ts';
import { Button } from "@/components/ui/button.tsx"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input.tsx"
import { Label } from "@/components/ui/label.tsx"
import { useNavigate } from 'react-router-dom';
import { useAuth  } from '../../context/AuthContext.tsx';
import { PasswordInput } from '@/components/custom/PasswordInput.tsx';

export default function Login() {
    const navigate = useNavigate();
    const { isAuthenticated, isLoading } = useAuth();
    const { login } = useAuth();

    useEffect(() => {
    if (!isLoading && isAuthenticated) {
        navigate('/dashboard', { replace: true });
    }
    }, [isAuthenticated, isLoading, navigate]);


    const handleLogin = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const username = formData.get("username") as string;
        const password = formData.get("password") as string; // TO NADAL DZIAŁA IDEALNIE!

        try {
            const response = await login(username, password);

            if (response.status === 200) {
                navigate('/dashboard'); 
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
    <div className="flex min-h-screen items-center justify-center bg-background">
        <Card className="w-full max-w-sm">
        <CardHeader>
            <CardTitle>
                <div className="text-2xl font-bold text-center">HomeOS</div>
            </CardTitle>
        </CardHeader>
        <CardContent>
            <form onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                <Label htmlFor="username">Username</Label>
                <Input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="username"
                    required
                />
                </div>
                
                <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
                
                <PasswordInput 
                    id="password"
                    name="password"
                    required 
                />
                </div>
            </div>

            <Button type="submit" className="w-full self-center mt-6">
                Login
            </Button>
            </form>
        </CardContent>
        </Card>
    </div>
    );
}