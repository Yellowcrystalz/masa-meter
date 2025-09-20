import shared from "@styles/shared.module.css";
import type { LeaderboardEntry } from "@/types";
import Leaderboard from "@components/widgets/StatWidget/Leaderboard";
import { useEffect, useState } from "react";

const StatWidget = () => {
    const [leaderboardData, setLeaderboardData] = useState<LeaderboardEntry[]>([]);

    useEffect(() => {
        const updateLeaderboard = () => {
            fetch("http://localhost:8000/api/leaderboard")
                .then((response) => response.json())
                .then((data: LeaderboardEntry[]) => {
                    let tempData: LeaderboardEntry[] = [];

                    for (let i = 0; i < 5; i++) {
                        tempData.push(data[i]);
                    }

                    setLeaderboardData(tempData);
                })
                .catch(error => console.error(error));
        }

        updateLeaderboard();
        const interval = setInterval(updateLeaderboard, 30000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <div className={shared.widget}>
                <h1 className={shared.widgetTitle}>Stats</h1>
                <Leaderboard leaderboardData={leaderboardData}/> 
            </div>
        </div>
    );
}

export default StatWidget;