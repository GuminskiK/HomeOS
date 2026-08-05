import React, { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Search, Download, Terminal, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import type { Log } from '@/api/system/types.ts';
import { getLogs } from '@/api/system/logs';

// --- POMOCNICZE FUNKCJE ---
const getLevelBadge = (level: string) => {
  switch (level) {
    case 'ERROR':
      return <Badge variant="destructive" className="flex gap-1 items-center w-20 justify-center"><AlertCircle className="w-3 h-3"/> {level}</Badge>;
    case 'WARN':
      return <Badge variant="outline" className="text-yellow-600 border-yellow-600 flex gap-1 items-center w-20 justify-center"><AlertTriangle className="w-3 h-3"/> {level}</Badge>;
    case 'INFO':
      return <Badge variant="secondary" className="text-blue-600 bg-blue-100 hover:bg-blue-200 flex gap-1 items-center w-20 justify-center"><Info className="w-3 h-3"/> {level}</Badge>;
    case 'DEBUG':
      return <Badge variant="outline" className="text-gray-500 w-20 justify-center"><Terminal className="w-3 h-3 mr-1"/> {level}</Badge>;
    default:
      return <Badge>{level}</Badge>;
  }
};

export default function SystemLogs() {
  const [searchTerm, setSearchTerm] = useState('');
  const [levelFilter, setLevelFilter] = useState<string>('ALL');
  const [serviceFilter, setServiceFilter] = useState<string>('ALL');

  const [logs, setLogs] = useState<Log[]>([]);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const response = await getLogs();
      setLogs(response);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Card className="w-full h-full flex flex-col shadow-sm border-slate-200 dark:border-slate-800">
      <CardHeader className="pb-4">
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-2xl font-bold tracking-tight">System Logs</CardTitle>
          </div>
          <Button variant="outline" size="sm" className="hidden sm:flex">
            <Download className="mr-2 h-4 w-4" />
            Eksportuj CSV
          </Button>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col space-y-4">
        {/* TOOLBAR: Filtry i wyszukiwarka */}
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="relative w-full sm:max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Szukaj w logach (np. ip=172.19...)"
              className="pl-9 bg-slate-50 dark:bg-slate-900"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex gap-2 w-full sm:w-auto">
            <Select value={serviceFilter} onValueChange={setServiceFilter}>
              <SelectTrigger className="w-full sm:w-[160px] md:w-[180px]">
                <SelectValue placeholder="Wszystkie serwisy" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">Wszystkie serwisy</SelectItem>
                <SelectItem value="homeos-auth">homeos-auth</SelectItem>
                <SelectItem value="homeos-system">homeos-system</SelectItem>
                <SelectItem value="homeos-files">homeos-files</SelectItem>
                <SelectItem value="homeos-gateway">homeos-gateway</SelectItem>
              </SelectContent>
            </Select>

            <Select value={levelFilter} onValueChange={setLevelFilter}>
              <SelectTrigger className="w-full sm:w-[140px]">
                <SelectValue placeholder="Poziom logu" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">Wszystkie</SelectItem>
                <SelectItem value="INFO">INFO</SelectItem>
                <SelectItem value="WARN">WARN</SelectItem>
                <SelectItem value="ERROR">ERROR</SelectItem>
                <SelectItem value="DEBUG">DEBUG</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* TABELA LOGÓW */}
        <div className="rounded-md border flex-1 overflow-hidden">
          <Table>
            <TableHeader className="bg-slate-50 dark:bg-slate-900/50">
              <TableRow>
                <TableHead className="w-[180px]">Timestamp</TableHead>
                <TableHead className="w-[100px]">Level</TableHead>
                <TableHead className="w-[150px]">Serwis</TableHead>
                <TableHead>Wiadomość</TableHead>
                <TableHead className="hidden md:table-cell">Metadane</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {logs.length > 0 ? (
                logs.map((log) => (
                  <TableRow key={log.id} className="font-mono text-sm hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <TableCell className="text-muted-foreground">
                      {new Date(log.created_at).toLocaleTimeString('pl-PL', { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' })}
                      <span className="text-xs ml-2 text-slate-400">{new Date(log.created_at).toLocaleDateString('pl-PL')}</span>
                    </TableCell>
                    <TableCell>{getLevelBadge(log.event_type)}</TableCell>
                    <TableCell className="font-medium text-slate-700 dark:text-slate-300">
                      {log.container}
                    </TableCell>
                    <TableCell className="text-slate-900 dark:text-slate-100">
                      {log.details}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                    Brak logów pasujących do kryteriów.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}