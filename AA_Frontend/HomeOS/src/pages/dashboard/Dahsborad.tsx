import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useNavigate } from 'react-router-dom';
import { useAuth } from "@/context/AuthContext";
import { 
    Clock, Cpu, HardDrive, TerminalSquare, 
    Play, Square, RotateCw, FileText, 
    LogOut, ShieldAlert, User, Activity,
    Globe, Shield, Server, Folder, Share2
} from "lucide-react";
import { ContainersSection } from './ContainersSection';
import ClockWidget from './ClockWidget';
import { SystemMetricsWidget } from './SystemMetricsWidget';


export default function Dashboard() {
    const navigate = useNavigate();
    const { logout, user: profile } = useAuth(); 
    
    // Prosta symulacja uprawnień 
    const isAdmin = profile?.is_superuser === true || false; 

    const handleLogout = async () => {
        try {
            const success = await logout();
            if (success) navigate('/');
        } catch (error) {
            console.error('Błąd podczas wylogowywania:', error);
        }
    };
    
    const getAvatarSrc = (url: string) => url;

    return (
        <div className="w-full max-w-7xl mx-auto h-screen flex justify-center items-center gap-8 p-8 box-border">
            
            {/* LEWY PANEL - Wzorem Profile.tsx (Tylko dla admina) */}
            {isAdmin && (
                <div className="w-[300px] shrink-0 flex flex-col gap-6 h-full py-10">
                    
                    {/* Zegar */}
                    <ClockWidget />

                    {/* Zużycie Zasobów */}
                    <SystemMetricsWidget />
                </div>
            )}

            {/* PRAWY PANEL - flex-1 (Aplikacje i top bar) */}
            <div className="flex-1 min-w-0 flex flex-col gap-6 h-full py-10">
                
                {/* Cienki pasek górny z Avatarem */}
                <Card className="flex flex-row items-center justify-between p-3 shadow-sm shrink-0">
                    {/* Sekcja Użytkownika */}
                    <div 
                        className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
                        onClick={() => navigate('/profile')}
                        title="Przejdź do profilu"
                    >
                        <div className="w-9 h-9 bg-gray-300 rounded-full overflow-hidden flex items-center justify-center border border-gray-600">
                            {profile?.avatar_url ? (
                                <img 
                                    src={getAvatarSrc(profile.avatar_url)} 
                                    alt="Avatar" 
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <User className="w-5 h-5 text-gray-500" />
                            )}
                        </div>
                        <span className="font-semibold text-sm">
                            {profile?.username || "Użytkownik"}
                        </span>
                    </div>

                    {/* Przyciski Akcji */}
                    <div className="flex items-center gap-1">
                        {isAdmin && (
                            <Button variant="ghost" size="sm" onClick={() => navigate('/admin')} className="h-8">
                                <ShieldAlert className="w-4 h-4 mr-2" />
                                <span className="hidden sm:inline">Admin</span>
                            </Button>
                        )}
                        <Button variant="ghost" size="sm" onClick={handleLogout} className="h-8 text-rose-500 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950">
                            <LogOut className="w-4 h-4 sm:mr-2" />
                            <span className="hidden sm:inline">Wyloguj</span>
                        </Button>
                    </div>
                </Card>

                {/* Siatka Kontenerów z scrollowaniem w razie dużej liczby usług */}
                <ContainersSection />
            </div>
        </div>
    );
}