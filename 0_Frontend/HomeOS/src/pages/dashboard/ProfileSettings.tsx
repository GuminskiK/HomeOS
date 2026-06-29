import { Button } from "@/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Card, CardTitle, CardFooter, CardContent} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Eye, EyeOff } from "lucide-react"
import { useState } from "react"

export default function ProfileSettings() {
    
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)

    return(
        <div className="flex flex-col m-10 gap-10">
            <FieldGroup>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-name">Name</FieldLabel>
                    <Input className="w-full" id="fieldgroup-name" placeholder="Jordan Lee" />
                </Field>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-password">Password</FieldLabel>
                    <div className="relative">
                        <Input
                        className="w-full"
                        id="fieldgroup-password"
                        type={showPassword ? "text" : "password"} 
                        placeholder="password"
                        />
                        <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        >
                        {showPassword ? (
                            <Eye className="h-4 w-4" />
                        ) : (
                            <EyeOff className="h-4 w-4" />
                        )}
                        </button>
                    </div>
                </Field>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-password-confirm">Confirm Password</FieldLabel>
                    <div className="relative">
                        <Input
                        className="w-full"
                        id="fieldgroup-password-confirm"
                        type={showConfirmPassword ? "text" : "password"} 
                        placeholder="password"
                        />
                        <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                        aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                        >
                        {showConfirmPassword ? (
                            <Eye className="h-4 w-4" />
                        ) : (
                            <EyeOff className="h-4 w-4" />
                        )}
                        </button>
                    </div>
                </Field>                 
                <Field>
                    <FieldLabel htmlFor="picture">Avatar</FieldLabel>
                    <Input id="picture" type="file" className="file:mr-4 file:hover:cursor-pointer" />
                </Field>
                <Field orientation="horizontal">
                    <Button type="reset" variant="outline">
                    Reset
                    </Button>
                    <Button type="submit">Submit</Button>
                </Field>
            </FieldGroup>
            
            <div className="flex flex-row gap-4 justify-start items-center">
                
                <Card className="flex flex-col items-center p-4 w-full">
                    <div>TwoFactor Authentication: Enabled</div>
                    <Button className="w-1/2">Disable</Button>
                </Card>
            </div>
        </div>
    )
}