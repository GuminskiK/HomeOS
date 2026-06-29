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
    Username: "INV001",
    Role: "Laptop",
    Status: "Active"
  },
  {
    Username: "INV002",
    Role: "Pending",
    Status: "Inactive",
  },
]

export default function ManageUsers(){
    return (
        <div className="flex flex-col h-full m-10 text-left">
            <div className="text-3xl font-bold mb-4">Manage Users</div>

            <Table>
            <TableHeader>
                <TableRow>
                <TableHead className="w-[100px]">Username</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Status</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {invoices.map((invoice) => (
                <TableRow key={invoice.Username}>
                    <TableCell className="font-medium">{invoice.Username}</TableCell>
                    <TableCell>{invoice.Role}</TableCell>
                    <TableCell>{invoice.Status}</TableCell>
                    <TableCell><Button variant="outline">See more</Button></TableCell>
                </TableRow>
                ))}
            </TableBody>
            </Table>
        </div>
  )
}