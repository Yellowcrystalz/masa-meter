export type LeaderboardEntry = {
    username: string;
    count: number;
}

export type LeadeboardProps = {
    leaderboardData: LeaderboardEntry[];
}

export type HistoryEntry = {
    date: string;
    username: string;
}

export type HistoryProps = {
    historyData: HistoryEntry[];
}

export type AchievementEntry = {
    achievement_name: string;
    description: string,
    emoji: string,
    username: string;
}

export type AchievementProps = {
    achievementData: AchievementEntry[];
}