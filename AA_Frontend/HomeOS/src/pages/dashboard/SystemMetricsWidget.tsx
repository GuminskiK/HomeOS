import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { getSystemMetrics} from "@/api/system/metrics.ts";
import type { Metrics } from "@/api/system/types.ts";
import { 
    Activity, Cpu, HardDrive, Thermometer, 
    ArrowDownCircle, ArrowUpCircle 
} from "lucide-react";

export function SystemMetricsWidget() {
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<boolean>(false);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const data = await getSystemMetrics();
                setMetrics(data);
                setError(false);
            } catch (err) {
                console.error("Błąd pobierania metryk:", err);
                setError(true);
            } finally {
                setLoading(false);
            }
        };

        // 1. Pierwsze pobranie przy montowaniu
        fetchMetrics();

        // 2. Polling co 5 sekund (5000 ms)
        const interval = setInterval(fetchMetrics, 5000);

        // 3. Czyszczenie timera przy odmontowaniu
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <Card className="shadow-sm shrink-0">
                <CardContent className="p-4 text-xs text-muted-foreground animate-pulse">
                    Ładowanie metryk systemowych...
                </CardContent>
            </Card>
        );
    }

    if (error || !metrics) {
        return (
            <Card className="shadow-sm shrink-0 border-rose-200 bg-rose-50/50 dark:bg-rose-950/20">
                <CardContent className="p-4 text-xs text-rose-600 dark:text-rose-400">
                    Nie udało się połączyć z mikroserwisem telemetrycznym.
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="shadow-sm shrink-0">
            <CardHeader className="pb-2 pt-4 px-4">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                        <Activity className="w-4 h-4 text-indigo-500" /> Zasoby Host (RPi 5)
                    </CardTitle>
                    {/* Temperatura procesora */}
                    <div className="flex items-center gap-1 text-xs font-semibold text-slate-600 dark:text-slate-300">
                        <Thermometer className={`w-3.5 h-3.5 ${metrics.temperature_c > 65 ? 'text-rose-500' : 'text-emerald-500'}`} />
                        <span>{metrics.temperature_c.toFixed(1)}°C</span>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-3 px-4 pb-4">
                {/* CPU */}
                <div>
                    <div className="flex justify-between text-xs mb-1 font-medium text-muted-foreground">
                        <span className="flex items-center gap-1"><Cpu className="w-3 h-3"/> CPU</span>
                        <span className="font-semibold text-foreground">{metrics.cpu_usage_percent}%</span>
                    </div>
                    <Progress value={metrics.cpu_usage_percent} className="h-1.5" />
                </div>

                {/* RAM */}
                <div>
                    <div className="flex justify-between text-xs mb-1 font-medium text-muted-foreground">
                        <span className="flex items-center gap-1"><HardDrive className="w-3 h-3"/> RAM</span>
                        <span className="font-semibold text-foreground">
                            {metrics.ram_used_gb} GB / {metrics.ram_total_gb} GB ({metrics.ram_usage_percent}%)
                        </span>
                    </div>
                    <Progress value={metrics.ram_usage_percent} className="h-1.5" />
                </div>

                {/* Dysk NVMe */}
                <div>
                    <div className="flex justify-between text-xs mb-1 font-medium text-muted-foreground">
                        <span className="flex items-center gap-1"><HardDrive className="w-3 h-3"/> Dysk</span>
                        <span className="font-semibold text-foreground">{metrics.disk_usage_percent}%</span>
                    </div>
                    <Progress value={metrics.disk_usage_percent} className="h-1.5" />
                </div>

                {/* Prędkość Sieci (Download / Upload) */}
                <div className="pt-2 border-t grid grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center gap-1.5">
                        <ArrowDownCircle className="w-4 h-4 text-emerald-500 shrink-0" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-muted-foreground leading-none">Pobieranie</span>
                            <span className="font-mono font-semibold text-xs mt-0.5">
                                {metrics.network_download_mbs.toFixed(1)} MB/s
                            </span>
                        </div>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <ArrowUpCircle className="w-4 h-4 text-blue-500 shrink-0" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-muted-foreground leading-none">Wysyłanie</span>
                            <span className="font-mono font-semibold text-xs mt-0.5">
                                {metrics.network_upload_mbs.toFixed(1)} MB/s
                            </span>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}