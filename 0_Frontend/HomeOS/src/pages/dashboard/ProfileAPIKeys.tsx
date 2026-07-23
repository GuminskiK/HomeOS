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
import { Dialog, DialogClose, DialogContent, DialogFooter, DialogTrigger, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Field, FieldGroup } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

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

export default function ProfileAPIKeys(){
    return (
        <div className="flex flex-col h-full m-10 text-left">
            <div className="text-3xl font-bold mb-4">Your apikeys</div>

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
                    <TableCell><Button variant="outline">Turn OFF</Button></TableCell>
                </TableRow>
                ))}
            </TableBody>
            </Table>
            
            <Dialog>
            <form>
              <DialogTrigger asChild>
                <Button className="w-1/2 mt-5" variant="outline">Create API Key</Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-sm">
                <DialogHeader>
                  <DialogTitle>Create API Key</DialogTitle>
                </DialogHeader>
                <FieldGroup>
                  <Field>
                    <Label htmlFor="name-1">Name</Label>
                    <Input id="name-1" name="name" placeholder="Username" />
                  </Field>
                </FieldGroup>
                <DialogFooter>
                  <DialogClose asChild>
                    <Button variant="outline">Cancel</Button>
                  </DialogClose>
                  <Button type="submit">Create API Key</Button>
                </DialogFooter>
              </DialogContent>
            </form>
          </Dialog>
        </div>
  )
}