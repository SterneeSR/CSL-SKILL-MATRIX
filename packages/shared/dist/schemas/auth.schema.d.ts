import { z } from 'zod';
export declare const RegisterStudentSchema: z.ZodObject<{
    first_name: z.ZodString;
    last_name: z.ZodString;
    email: z.ZodString;
    password: z.ZodString;
    student_identifier: z.ZodString;
    batch_id: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    student_identifier: string;
    batch_id?: string | undefined;
}, {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    student_identifier: string;
    batch_id?: string | undefined;
}>;
export type RegisterStudentInput = z.infer<typeof RegisterStudentSchema>;
export declare const LoginSchema: z.ZodObject<{
    email: z.ZodString;
    password: z.ZodString;
}, "strip", z.ZodTypeAny, {
    email: string;
    password: string;
}, {
    email: string;
    password: string;
}>;
export type LoginInput = z.infer<typeof LoginSchema>;
//# sourceMappingURL=auth.schema.d.ts.map