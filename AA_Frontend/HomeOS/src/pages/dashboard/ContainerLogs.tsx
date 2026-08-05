import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Search, Download, Terminal } from 'lucide-react';
import { getContainerLogs } from '@/api/system/containers';
import { useParams } from 'react-router-dom';

// Funkcja do usuwania kodów kolorów ANSI z logów terminala
const cleanAnsiCodes = (str: string) => {
  return str.replace(/[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '');
};

export default function ContainerLogs() {
  const { containerName } = useParams<{ containerName: string }>();
  const [searchTerm, setSearchTerm] = useState('');
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    if (containerName) {
      fetchLogs(containerName);
    }
  }, [containerName]);

  const fetchLogs = async (name: string) => {
    try {
      const response = await getContainerLogs(name);
      setLogs(response);
    } catch (error) {
      console.error('Błąd podczas pobierania logów kontenera:', error);
    }
  };

  // Czyszczenie kodów ANSI z każdej linii i filtrowanie po wyszukiwarce
  const filteredLogs = logs
    .map((line) => cleanAnsiCodes(line))
    .filter((line) => line.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <Card className="w-full h-full flex flex-col shadow-sm border-slate-200 dark:border-slate-800">
      <CardHeader className="pb-4">
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-2xl font-bold tracking-tight flex items-center gap-2">
              <Terminal className="w-6 h-6 text-primary" />
              Logi kontenera: <span className="text-primary font-mono">{containerName}</span>
            </CardTitle>
          </div>
          <Button variant="outline" size="sm" className="hidden sm:flex">
            <Download className="mr-2 h-4 w-4" />
            Eksportuj TXT
          </Button>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col space-y-4 overflow-hidden">
        {/* Wyszukiwarka logów */}
        <div className="flex items-center justify-between">
          <div className="relative w-full sm:max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Filtruj wiersze logów..."
              className="pl-9 bg-slate-50 dark:bg-slate-900"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {/* TERMINAL Z LOGAMI (wyrównany do lewej, UTF-8 i czysty tekst) */}
        <div className="rounded-md border bg-slate-950 text-slate-50 font-mono text-xs sm:text-sm flex-1 overflow-auto p-4 flex flex-col gap-1 shadow-inner text-left">
          {filteredLogs.length > 0 ? (
            filteredLogs.map((logLine, index) => {
              const lower = logLine.toLowerCase();
              const isError = lower.includes('error') || lower.includes('err') || lower.includes('critical');
              const isWarn = lower.includes('warn') || lower.includes('warning');

              return (
                <div
                  key={index}
                  className={`whitespace-pre-wrap break-all leading-relaxed text-left ${
                    isError
                      ? 'text-rose-400 bg-rose-950/40 px-1 rounded'
                      : isWarn
                      ? 'text-amber-400'
                      : 'text-slate-300'
                  }`}
                >
                  {logLine}
                </div>
              );
            })
          ) : (
            <div className="h-full flex items-center justify-center text-slate-500">
              Brak pasujących logów.
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}