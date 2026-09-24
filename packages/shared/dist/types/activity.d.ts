export type ActivityType = 'ASSESSMENT' | 'TASK' | 'PROJECT';
export interface ActivityDTO {
    id: string;
    course_id: string;
    sub_skill_id: string;
    sub_skill_name: string;
    skill_name: string;
    category_name: string;
    title: string;
    instructions: string;
    activity_type: ActivityType;
    max_marks: number;
    is_max_marks_locked: boolean;
    deadline: string;
    is_reopened: boolean;
    reopened_deadline: string | null;
    effective_deadline: string;
    submission_status: 'NOT_SUBMITTED' | 'SUBMITTED' | 'WITHDRAWN' | 'FAILED';
    is_evaluated: boolean;
    obtained_marks: number | null;
    percentage: number | null;
    feedback: string | null;
    withdrawal_count: number;
    can_withdraw: boolean;
    can_submit: boolean;
}
//# sourceMappingURL=activity.d.ts.map