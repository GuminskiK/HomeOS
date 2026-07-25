import { Button } from "@/components/ui/button"
import { Card, CardTitle, CardContent } from "@/components/ui/card"
import { useState, useRef } from "react";
import ProfileSettings from "./ProfileSettings";
import ProfileSecurity from "./ProfileSecurity";
import ProfileAPIKeys from "./ProfileAPIKeys";

import { getUserProfile, uploadAvatarFile } from "@/api/auth/users"; 
import { useAuth } from '@/context/AuthContext'

type Tab = 'settings' | 'security' | 'apikeys' | 'preferences';

export default function Profile() {
    const { user: profile, updateUser } = useAuth();
    const [activeTab, setActiveTab] = useState<Tab>('settings');
    const [isUploading, setIsUploading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleAvatarClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        setIsUploading(true);
        try {
            const data = await uploadAvatarFile(file);
            console.log("Wgrywanie zakończone sukcesem:", data);
            
            const get_data = await getUserProfile("me");
            updateUser(get_data)

        } catch (error) {
            console.error("Błąd podczas wgrywania:", error);
        } finally {
            setIsUploading(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    }

    const getAvatarSrc = (url: string) => {
        return `${url}?t=${Date.now()}`;
    };

    return(
        <div className="w-full h-screen flex justify-center items-center gap-12 p-8 box-border">
            
            <div className="flex [flex:3] flex-col gap-6 h-full">
                <Card className="flex flex-col items-center h-full">
                    <div className="flex flex-col items-center w-full">
                        <div 
                            className={`w-32 h-32 bg-gray-300 mt-10 rounded-full overflow-hidden cursor-pointer hover:opacity-80 transition-opacity flex items-center justify-center relative ${isUploading ? 'opacity-50' : ''}`}
                            onClick={handleAvatarClick}
                            title="Kliknij, aby zmienić awatar"
                        >
                            {isUploading ? (
                                <span className="text-gray-700 text-sm font-semibold z-10 absolute">Wgrywanie...</span>
                            ) : null}

                            {profile?.avatar_url ? (
                                <img 
                                    src={getAvatarSrc(profile.avatar_url)} 
                                    alt={`${profile.username} avatar`} 
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                !isUploading && <span className="text-gray-500 text-sm">Brak zdjęcia</span>
                            )}
                        </div>
                        
                        <input 
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileChange}
                            accept="image/*"
                            className="hidden"
                        />

                        {/* Nazwa użytkownika */}
                        <CardTitle className="text-lg font-semibold mt-5 mb-5">
                            {profile?.username || "Nieznany"}
                        </CardTitle>
                    </div>

                    {/* Reszta Twojego kodu... */}
                    <CardContent className="flex flex-col gap-2 w-full border-t border-gray-600 p-4">
                        <Button variant={activeTab === 'settings' ? 'default' : 'outline'} onClick={() => setActiveTab('settings')}>
                            Settings
                        </Button>
                        <Button variant={activeTab === 'security' ? 'default' : 'outline'} onClick={() => setActiveTab('security')}>
                            Security
                        </Button>
                        <Button variant={activeTab === 'apikeys' ? 'default' : 'outline'} onClick={() => setActiveTab('apikeys')}>
                            APIKeys
                        </Button>
                        <Button variant={activeTab === 'preferences' ? 'default' : 'outline'} onClick={() => setActiveTab('preferences')}>
                            Preferences
                        </Button>
                    </CardContent>
                </Card>
            </div>
            
            <div className="flex [flex:7] flex-col gap-6 h-full">
                <Card className="flex-[3] flex h-full p-6">
                    {activeTab === 'settings' && <ProfileSettings />}
                    {activeTab === 'security' && <ProfileSecurity />}
                    {activeTab === 'apikeys' && <ProfileAPIKeys />}
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