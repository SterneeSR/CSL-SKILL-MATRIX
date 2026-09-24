import { apiClient } from './client';
import type { StudentProfile, StudentSkillsResponse } from '../types/student';

/**
 * Fetch the profile of the currently authenticated student.
 * The backend determines the student from the session; no ID is sent.
 */
export async function getStudentProfile(): Promise<StudentProfile> {
  const res = await apiClient.get<StudentProfile>('/student/profile/');
  return res.data;
}

/**
 * Fetch required skills and subskills for the currently authenticated student.
 */
export async function getStudentSkills(): Promise<StudentSkillsResponse> {
  const res = await apiClient.get<StudentSkillsResponse>('/student/skills/');
  return res.data;
}

