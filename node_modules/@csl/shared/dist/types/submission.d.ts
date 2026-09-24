export type SubmissionStatus = 'SUBMITTED' | 'WITHDRAWN' | 'FAILED';
export interface SubmissionDTO {
    id: string;
    activity_id: string;
    student_id: string;
    submission_url_or_file: string | null;
    notes: string | null;
    withdrawal_count: number;
    remaining_withdrawals: number;
    submission_status: SubmissionStatus;
    submitted_at: string;
    withdrawn_at: string | null;
}
//# sourceMappingURL=submission.d.ts.map