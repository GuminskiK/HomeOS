import React, { useState, useEffect, useCallback } from 'react';
import { getContainersStatus, controlContainer} from "@/api/system/containers.ts";
import type { ContainerStatus } from "@/api/system/types.ts";
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, Play, RotateCw, Server, Square } from 'lucide-react';

export function ContainersSection() {
    const [containers, setContainers] = useState<ContainerStatus[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const fetchContainers = useCallback(async () => {
        try {
            const data = await getContainersStatus();
            setContainers(data);
        } catch (err) {
            console.error("Błąd pobierania kontenerów:", err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchContainers();
        
        // Polling kontenerów np. co 15 sekund
        const interval = setInterval(fetchContainers, 15000);
        return () => clearInterval(interval);
    }, [fetchContainers]);

    // Przykładowa obsługa akcji kontenera
    const handleContainerAction = async (container_name: string, action: 'start' | 'stop' | 'restart') => {
        try {
            await controlContainer(container_name, action);

            // Odświeżamy listę natychmiast po wykonaniu akcji
            await fetchContainers();
        } catch (err) {
            console.error(`Błąd podczas ${action}:`, err);
        }
    };

    return (
            <div className="flex-1 overflow-y-auto pr-2 pb-2">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {containers.map((container) => (
                        <Card key={container.id} className="flex flex-col shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
                            <CardContent className="p-5 flex flex-col items-center justify-center flex-1">
                                {/* Statyczna ikona usługi z Lucide */}
                                <div className="p-4 rounded-full mb-3 transition-transform group-hover:scale-105 bg-indigo-500/10">
                                    <Server className="w-8 h-8 text-indigo-500" />
                                </div>
                                
                                {/* Nazwa i Status */}
                                <h3 className="font-semibold text-base tracking-tight">{container.name}</h3>
                                
                                {/* Wyświetlenie obrazu jako zwykły tekst */}
                                <span className="text-[11px] text-muted-foreground font-mono mt-0.5 truncate max-w-[200px]" title={container.image}>
                                    {container.image}
                                </span>

                                <div className="flex items-center gap-1.5 mt-2">
                                    <span className={`w-2 h-2 rounded-full ${container.state === 'running' ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                                    <span className="text-xs text-muted-foreground font-medium">
                                        {container.status}
                                    </span>
                                </div>
                            </CardContent>
                            
                            {/* Pasek akcji (Footer) */}
                            <CardFooter className="p-2 border-t bg-muted/20 flex justify-center gap-1">
                                <Button 
                                    variant="ghost" 
                                    size="icon" 
                                    className="h-8 w-8 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-100" 
                                    title="Start"
                                    onClick={() => handleContainerAction(container.name, 'start')}
                                >
                                    <Play className="w-4 h-4" />
                                </Button>
                                
                                <Button 
                                    variant="ghost" 
                                    size="icon" 
                                    className="h-8 w-8 text-rose-600 hover:text-rose-700 hover:bg-rose-100" 
                                    title="Stop"
                                    onClick={() => handleContainerAction(container.name, 'stop')}
                                >
                                    <Square className="w-4 h-4" />
                                </Button>
                                
                                <Button 
                                    variant="ghost" 
                                    size="icon" 
                                    className="h-8 w-8 text-amber-600 hover:text-amber-700 hover:bg-amber-100" 
                                    title="Restart"
                                    onClick={() => handleContainerAction(container.name, 'restart')}
                                >
                                    <RotateCw className="w-4 h-4" />
                                </Button>
                                
                                <div className="w-px h-4 bg-border mx-1 self-center" />
                                
                                <Button 
                                    variant="ghost" 
                                    size="icon" 
                                    className="h-8 w-8 text-slate-500 hover:text-slate-700" 
                                    title="Logi"
                                    onClick={() => window.open(`/dashboard/containers/${container.name}/logs`, '_blank')}
                                >
                                    <FileText className="w-4 h-4" />
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
    )
}