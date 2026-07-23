import { Button } from "@/components/ui/button.tsx"
import { Card, CardTitle, CardFooter, CardContent} from "@/components/ui/card"
import { useNavigate } from 'react-router-dom';
import { api } from "@/api/axiosClient";
import { useState } from "react";
import ProfileSettings from "./ProfileSettings";
import ProfileSecurity from "./ProfileSecurity";
import ProfileAPIKeys from "./ProfileAPIKeys";

type Tab =  'settings' | 'security' | 'apikeys' | 'preferences';

export default function Profile() {

    const navigate = useNavigate();

    const [activeTab, setActiveTab] = useState<Tab>('settings');

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
                            variant={activeTab === 'settings' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('settings')}
                        >
                            Settings
                        </Button>
                        <Button 
                            variant={activeTab === 'security' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('security')}
                        >
                            Security
                        </Button>
                        <Button 
                            variant={activeTab === 'apikeys' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('apikeys')}
                        >
                            APIKeys
                        </Button>
                        <Button 
                            variant={activeTab === 'preferences' ? 'default' : 'outline'} 
                            onClick={() => setActiveTab('preferences')}
                        >
                            Preferences
                        </Button>
                    </CardContent>
                </Card>
                
            </div>
            
            <div className="flex [flex:7] flex-col gap-6 h-full">
                <Card className="flex-[3] flex h-full">

                    {activeTab === 'settings' && (
                        <ProfileSettings />
                    )}
                    {activeTab === 'security' && (
                        <ProfileSecurity />
                    )}
                    {activeTab === 'apikeys' && (
                        <ProfileAPIKeys />
                    )}
                    {activeTab === 'preferences' && (
                        <div>
                            <h2 className="text-2xl font-bold mb-4">Preferences</h2>
                            <p className="text-gray-600">TODO - Future implementation</p>
                        </div>
                    )}
                </Card> 
            </div>

        </div>
    )
}