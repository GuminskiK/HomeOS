"use client" // Wymagane w Next.js App Router dla useState/useEffect

import { useState, useEffect } from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"

type Session = {
  session_id: string;
  created_at: string;
  device: string;
  ip: string;
}

export default function ProfileSecurity() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await fetch(`/api/sessions/me`);
      if (!response.ok) throw new Error("Błąd podczas pobierania sesji");
      
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/sessions/${sessionId}`, {
        method: "DELETE", 
      });

      if (!response.ok) throw new Error("Nie udało się wylogować sesji");

      setSessions((prevSessions) => 
        prevSessions.filter((session) => session.session_id !== sessionId)
      );
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col h-full m-10 text-left">
      <div className="text-3xl font-bold mb-4">Your sessions</div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">ID Sesji</TableHead>
            <TableHead>Device</TableHead>
            <TableHead>IP Address</TableHead>
            <TableHead className="text-right">Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center">
                Ładowanie sesji...
              </TableCell>
            </TableRow>
          ) : sessions.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center">
                Brak aktywnych sesji.
              </TableCell>
            </TableRow>
          ) : (
            sessions.map((session) => (
              <TableRow key={session.session_id}>
                <TableCell className="font-medium">{session.session_id}</TableCell>
                <TableCell>{new Date(session.created_at).toLocaleString()}</TableCell>
                <TableCell>{session.device}</TableCell>
                <TableCell>{session.ip}</TableCell>
                <TableCell className="text-right">
                  <Button 
                    variant="outline" 
                    onClick={() => handleLogout(session.session_id)}
                  >
                    Logout
                  </Button>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}