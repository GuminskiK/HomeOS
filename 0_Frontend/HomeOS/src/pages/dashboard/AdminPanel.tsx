import { Button } from "@/components/ui/button.tsx"
import { Card, CardTitle, CardFooter, CardContent} from "@/components/ui/card"
import { useNavigate } from 'react-router-dom';
import { api } from "@/api/axiosClient";
import { useState } from "react";
import ManageUsers from "./ManageUsers";


type Tab =  'manage_users' | 'logs';

export default function AdminPanel() {

    const navigate = useNavigate();

    const [activeTab, setActiveTab] = useState<Tab>('manage_users');

    return(
        <div className="w-full h-screen flex justify-center items-center gap-12 p-8 box-border">
        

            <div className="flex [flex:3] flex-col gap-6 h-full">
                <Card className="flex items-center h-full">
                    <div>
                        <div className="w-32 h-32 bg-gray-300 mt-10 rounded-full"></div>
                        <CardTitle className="text-lg font-semibold mt-5">Name</CardTitle>
                    </div>
                    <CardContent className="flex flex-col gap-2 w-full h-f border-t border-gray-600 p-4">
                        <Button 
                            variant={activeTab === 'manage_users' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('manage_users')}
                        >
                            Manage Users
                        </Button>
                        <Button 
                            variant={activeTab === 'logs' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('logs')}
                        >
                            Logs
                        </Button>
                    </CardContent>
                </Card>
                
            </div>
            
            <div className="flex [flex:7] flex-col gap-6 h-full">
                <Card className="flex-[3] flex h-full">

                    {activeTab === 'manage_users' && (
                        <ManageUsers />
                    )}
                    {activeTab === 'logs' && (
                        <div>
                            <h2 className="text-2xl font-bold mb-4">Logs</h2>
                            <p className="text-gray-600">TODO - Future implementation</p>
                        </div>
                    )}
                </Card> 
            </div>

        </div>
    )
}