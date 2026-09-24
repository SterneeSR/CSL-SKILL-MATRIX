import { ProficiencyLevel } from '../constants/proficiency.js';
export interface SkillCategory {
    id: string;
    name: string;
    description: string | null;
    skills?: Skill[];
}
export interface Skill {
    id: string;
    category_id: string;
    name: string;
    description: string | null;
    category?: SkillCategory;
    sub_skills?: SubSkill[];
}
export interface SubSkill {
    id: string;
    skill_id: string;
    name: string;
    description: string | null;
}
export interface CourseRequiredSkill {
    id: string;
    course_id: string;
    skill_id: string;
    is_required: boolean;
}
export type SkillCompletionStatus = 'PROVISIONAL' | 'COMPLETE';
export interface StudentSubSkillScoreDTO {
    sub_skill_id: string;
    sub_skill_name: string;
    current_score: number | null;
    is_assessed: boolean;
    latest_evaluated_at: string | null;
}
export interface StudentSkillScoreDTO {
    skill_id: string;
    skill_name: string;
    category_name: string;
    is_required: boolean;
    current_score: number | null;
    proficiency_level: ProficiencyLevel | null;
    status: SkillCompletionStatus;
    sub_skills: StudentSubSkillScoreDTO[];
}
export interface SkillMatrixCategoryDTO {
    category_id: string;
    category_name: string;
    skills: StudentSkillScoreDTO[];
}
//# sourceMappingURL=skill.d.ts.map