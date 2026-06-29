import React, { useState } from 'react';
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
import { Eye, EyeOff } from "lucide-react"
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const [showPassword, setShowPassword] = useState(false)
    const navigate = useNavigate();
    
    const handleLogin = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const username = formData.get("username") as string;
        const password = formData.get("password") as string;

        try {
            const response = await api.post('/api/auth/login', 
                {
                    username: username,
                    password: password
                }, 
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }
            );

            if (response.status === 200) {
                navigate('/dashboard'); 
            }
        return response.data;
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
    <div className="flex min-h-screen items-center justify-center bg-background">
        <Card className="w-full max-w-sm">
        <CardHeader>
            <CardTitle>
                <div className="text-2xl font-bold text-center">
                    HomeOS
                </div>
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
                <div className="relative">
                    <Input 
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"} 
                    className="pr-10"
                    required 
                    />
                    <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                    {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                    ) : (
                        <Eye className="h-4 w-4" />
                    )}
                    </button>
                </div>
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
};
