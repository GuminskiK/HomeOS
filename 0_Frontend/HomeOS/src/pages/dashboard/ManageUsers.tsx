import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Dialog, DialogClose, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Field, FieldGroup } from "@/components/ui/field"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { PasswordInput } from "@/components/custom/PasswordInput"

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
          
          <Dialog>
            <form>
              <DialogTrigger asChild>
                <Button className="w-1/2 mt-5" variant="outline">Create User</Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-sm">
                <DialogHeader>
                  <DialogTitle>Create User</DialogTitle>
                </DialogHeader>
                <FieldGroup>
                  <Field>
                    <Label htmlFor="name-1">Name</Label>
                    <Input id="name-1" name="name" placeholder="Username" />
                  </Field>
                  <Field>
                    <Label htmlFor="password-1">Password</Label>
                      <PasswordInput 
                          id="password"
                          name="password"
                          required 
                      />
                  </Field>
                  <Field>
                    <Label htmlFor="confirm-password-1">Confirm Password</Label>
                      <PasswordInput 
                          id="confirm-password"
                          name="confirm-password"
                          required 
                      />
                  </Field>
                </FieldGroup>
                <DialogFooter>
                  <DialogClose asChild>
                    <Button variant="outline">Cancel</Button>
                  </DialogClose>
                  <Button type="submit">Create User</Button>
                </DialogFooter>
              </DialogContent>
            </form>
          </Dialog>
      </div>
  )
}