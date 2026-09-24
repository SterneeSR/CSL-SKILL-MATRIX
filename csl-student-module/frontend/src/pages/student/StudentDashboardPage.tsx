import { useEffect, useState } from 'react';
import { getStudentProfile } from '../../api/student';
import type { StudentProfile } from '../../types/student';

/**
 * Student dashboard placeholder. Shows the student's course/batch from the
 * profile API; performance, skills and activities use "—" placeholders until
 * those modules exist. No fake data.
 */
export function StudentDashboardPage() {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getStudentProfile()
      .then((data) => {
        if (!cancelled) setProfile(data);
      })
      .catch(() => {
        if (!cancelled) setError(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error || !profile) {
    return <p>Unable to load profile.</p>;
  }

  return (
    <div>
      <h2>Welcome back, {profile.name}.</h2>
      <p>Course: {profile.course ?? 'Not assigned'}</p>
      <p>Batch: {profile.batch ?? 'Not assigned'}</p>
      <p>Overall Performance: —</p>
      <p>Skills: —</p>
      <p>Pending Activities: —</p>
    </div>
  );
}
