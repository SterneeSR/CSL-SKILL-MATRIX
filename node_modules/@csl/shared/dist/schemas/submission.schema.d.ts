import { z } from 'zod';
export declare const CreateSubmissionSchema: z.ZodObject<{
    submission_url_or_file: z.ZodString;
    notes: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    submission_url_or_file: string;
    notes?: string | undefined;
}, {
    submission_url_or_file: string;
    notes?: string | undefined;
}>;
export type CreateSubmissionInput = z.infer<typeof CreateSubmissionSchema>;
//# sourceMappingURL=submission.schema.d.ts.map