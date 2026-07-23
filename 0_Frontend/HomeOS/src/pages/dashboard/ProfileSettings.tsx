import { Button } from "@/components/ui/button"
import {
  Field,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Card} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {PasswordInput} from "@/components/custom/PasswordInput"
import { useState } from "react"
import { uploadAvatarFile } from "@/api/auth/users"

export default function ProfileSettings() {

    const [isUploading, setIsUploading] = useState(false);
    
    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        setIsUploading(true);
        try {
            const data = await uploadAvatarFile(file);
            
            console.log("Wgrywanie zakończone sukcesem:", data);
        } catch (error) {
            console.error("Błąd podczas wgrywania:", error);
        } finally {
            setIsUploading(false);
        }
    }


    return(
        <div className="flex flex-col m-10 gap-10">
            <FieldGroup>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-name">Name</FieldLabel>
                    <Input className="w-full" id="fieldgroup-name" placeholder="Jordan Lee" />
                </Field>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-password">Password</FieldLabel>
                    <PasswordInput 
                        id="password"
                        name="password"
                        required 
                    />
                </Field>
                <Field>
                    <FieldLabel htmlFor="fieldgroup-confirm-password">Confirm Password</FieldLabel>
                    <PasswordInput 
                        id="confirm-password"
                        name="confirm-password"
                        required 
                    />
                </Field>                 
                <Field>
                    <FieldLabel htmlFor="picture">Avatar</FieldLabel>
                    {isUploading ? 'Wgrywanie...' : 'Zmień awatar'}
                    <Input id="picture" type="file" className="file:mr-4 file:hover:cursor-pointer" accept="image/png, image/jpeg, image/webp" onChange={handleFileChange}
                        disabled={isUploading} />
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