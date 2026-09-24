import { apiClient } from './client';
import type { StudentProfile } from '../types/student';

/**
 * Fetch the profile of the currently authenticated student.
 * The backend determines the student from the session; no ID is sent.
 */
export async function getStudentProfile(): Promise<StudentProfile> {
  const res = await apiClient.get<StudentProfile>('/student/profile/');
  return res.data;
}
