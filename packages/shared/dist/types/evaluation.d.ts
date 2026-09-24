export type EvaluationStatus = 'EVALUATED' | 'RE_EVALUATED' | 'ESCALATED_TO_ADMIN';
export interface EvaluationDTO {
    id: string;
    submission_id: string;
    tutor_id: string;
    obtained_marks: number;
    percentage: number;
    feedback: string | null;
    tutor_re_eval_count: number;
    evaluation_status: EvaluationStatus;
    evaluated_at: string;
}
export interface EvaluationHistoryDTO {
    id: string;
    evaluation_id: string;
    evaluator_id: string;
    evaluator_role: 'TUTOR' | 'ADMIN';
    previous_marks: number;
    new_marks: number;
    reason: string;
    recorded_at: string;
}
export interface SkillEvidenceDTO {
    id: string;
    student_id: string;
    sub_skill_id: string;
    evaluation_id: string;
    normalized_score: number;
    validity_expires_at: string | null;
    is_expired: boolean;
    recorded_at: string;
}
//# sourceMappingURL=evaluation.d.ts.map