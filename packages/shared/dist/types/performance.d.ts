export type OverallPerformanceStatus = 'NOT_COMPLETE' | 'COMPLETE';
export interface StudentOverallPerformanceDTO {
    student_id: string;
    current_overall_score: number | null;
    status: OverallPerformanceStatus;
    required_skills_count: number;
    proficient_skills_count: number;
    completed_skills_count: number;
    achieved_at: string;
    updated_at: string;
}
//# sourceMappingURL=performance.d.ts.map