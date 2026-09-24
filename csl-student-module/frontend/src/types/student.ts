export interface StudentProfile {
  name: string;
  email: string;
  student_id: string;
  course: string | null;
  batch: string | null;
}

export interface StudentCourseInfo {
  id: number;
  name: string;
  code: string;
}

export interface StudentBatchInfo {
  id: number;
  name: string;
}

export interface StudentSubSkill {
  id: number;
  name: string;
  status: string;
}

export interface StudentSkill {
  id: number;
  name: string;
  category: string;
  status: string;
  subskills: StudentSubSkill[];
}

export interface StudentSkillsResponse {
  course: StudentCourseInfo | null;
  batch: StudentBatchInfo | null;
  skills: StudentSkill[];
}

