import { Button } from "@/components/ui/button.tsx";
import { Card } from "@/components/ui/card";
import { useNavigate } from 'react-router-dom';
import { useAuth } from "@/context/AuthContext";

export default function Dashboard() {
    const navigate = useNavigate();
    const { logout } = useAuth();

    const handleLogout = async () => {
        try {
            const success = await logout();
            if (success) {
                navigate('/');
            }
        } catch (error) {
            console.error('Error occurred while logging out:', error);
        }
    };

    return (
        <div className="w-full h-screen flex justify-center items-center gap-12 p-8 box-border">
            <div className="flex [flex:3] flex-col gap-6 h-full">
                <Card className="flex-[2] flex items-center justify-center">Text</Card> 
                <Card className="flex-[4] flex items-center justify-center">Text</Card>
                <Card className="flex-[3] flex items-center justify-center">Text</Card>
            </div>
            
            <div className="flex [flex:7] flex-col gap-6 h-full">
                <Card className="flex-[3] flex items-center justify-center gap-2">
                    <Button onClick={() => navigate('/profile')}>Profile</Button>
                    <Button onClick={handleLogout}>Logout</Button>
                    <Button onClick={() => navigate('/admin')}>Admin Panel</Button>
                </Card> 
                <Card className="flex-[7] flex items-center justify-center">Text</Card>
            </div>
        </div>
    );
}