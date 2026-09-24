import { OverallPerformanceStatus } from './performance.js';
export interface LeaderboardEntryDTO {
    rank: number;
    student_id: string;
    display_name: string;
    student_identifier: string;
    overall_score: number;
    status: OverallPerformanceStatus;
    achieved_at: string;
    is_current_user: boolean;
}
export interface LeaderboardResponseDTO {
    batch_id: string | null;
    batch_name: string | null;
    total_students: number;
    entries: LeaderboardEntryDTO[];
    current_user_entry: LeaderboardEntryDTO | null;
}
//# sourceMappingURL=leaderboard.d.ts.map