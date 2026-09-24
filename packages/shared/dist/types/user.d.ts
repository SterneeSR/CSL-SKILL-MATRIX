export type UserRole = 'STUDENT' | 'TUTOR' | 'ADMIN';
export type AccountStatus = 'PENDING' | 'ACTIVE' | 'REJECTED';
export interface User {
    id: string;
    email: string;
    role: UserRole;
    account_status: AccountStatus;
    created_at: string;
    updated_at: string;
}
export interface StudentProfile {
    id: string;
    user_id: string;
    first_name: string;
    last_name: string;
    student_identifier: string;
    batch_id: string | null;
    approved_at: string | null;
    rejected_at: string | null;
    rejection_reason: string | null;
}
export interface Course {
    id: string;
    code: string;
    title: string;
    description: string | null;
}
export interface Batch {
    id: string;
    course_id: string;
    name: string;
    start_date: string;
    end_date: string;
    course?: Course;
}
export interface StudentAuthResponse {
    access_token: string;
    user: {
        id: string;
        email: string;
        role: UserRole;
        account_status: AccountStatus;
        profile: {
            id: string;
            first_name: string;
            last_name: string;
            student_identifier: string;
            batch_id: string | null;
            batch?: Batch;
        };
    };
}
//# sourceMappingURL=user.d.ts.map