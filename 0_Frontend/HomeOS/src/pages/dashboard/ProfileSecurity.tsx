import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
const invoices = [
  {
    Session: "INV001",
    Device: "Laptop",
    IP: "192.168.1.1"
  },
  {
    Session: "INV002",
    Device: "Pending",
    IP: "$150.00",
  },
]

export default function ProfileSecurity(){
    return (
        <div className="flex flex-col h-full m-10 text-left">
            <div className="text-3xl font-bold mb-4">Your sessions</div>

            <Table>
            <TableHeader>
                <TableRow>
                <TableHead className="w-[100px]">Session</TableHead>
                <TableHead>Device</TableHead>
                <TableHead>IP Address</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {invoices.map((invoice) => (
                <TableRow key={invoice.Session}>
                    <TableCell className="font-medium">{invoice.Session}</TableCell>
                    <TableCell>{invoice.Device}</TableCell>
                    <TableCell>{invoice.IP}</TableCell>
                    <TableCell><Button variant="outline">Logout</Button></TableCell>
                </TableRow>
                ))}
            </TableBody>
            </Table>
        </div>
  )
}