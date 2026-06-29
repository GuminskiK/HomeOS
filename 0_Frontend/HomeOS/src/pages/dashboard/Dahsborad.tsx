import { Button } from "@/components/ui/button.tsx"
import { Card} from "@/components/ui/card"
import { useNavigate } from 'react-router-dom';
import { api } from "@/api/axiosClient";

export default function Dashboard() {

    const navigate = useNavigate();

    const handleLogout = async () => {
        try{
            const response = await api.post('/api/auth/logout')

            if (response.status === 200) {
                navigate('/');
            }

        } catch (error) {
            console.error('Error occurred while logging out:', error);
        }
    }

    return (
        // h-screen (100vh) + p-8 daje idealny margines wewnętrzny z każdej strony bez scrolla
        <div className="w-full h-screen flex justify-center items-center gap-12 p-8 box-border">
        
        {/* Kolumna lewa (zajmuje 30% szerokości dzięki flex-[3]) */}
        <div className="flex [flex:3] flex-col gap-6 h-full">
            <Card className="flex-[2] flex items-center justify-center">Text</Card> 
            <Card className="flex-[4] flex items-center justify-center">Text</Card>
            <Card className="flex-[3] flex items-center justify-center">Text</Card>
        </div>
        
        {/* Kolumna prawa (zajmuje 70% szerokości dzięki flex-[7]) */}
        <div className="flex [flex:7] flex-col gap-6 h-full">
            <Card className="flex-[3] flex items-center justify-center">
                <Button onClick={() => navigate('/profile')}>Profile</Button>
                <Button onClick={handleLogout}>Logout</Button>
                <Button onClick={() => navigate('/admin')}>Admin Panel</Button>
            </Card> 
            <Card className="flex-[7] flex items-center justify-center">Text</Card>
        </div>

        </div>
    )
}