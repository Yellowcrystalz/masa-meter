import shared from "@styles/shared.module.css";
import type { AchievementEntry } from "@/types";
import Achievement from "./Achievement";
import { useEffect, useState } from "react";


const AchievementWidget = () => {
    const [achievementData, setAchievementData] = useState<AchievementEntry[]>([]);

    useEffect(()=> {
        const updateAchievement = () => {
            fetch("http://localhost:8000/api/achievements")
                .then((response) => response.json())
                .then((data: AchievementEntry[]) => (setAchievementData(data)))
                .catch(error => console.error(error));
        }

        updateAchievement();
        const interval = setInterval(updateAchievement, 30000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <div className={shared.widget}>
                <h1 className={shared.widgetTitle}>Achievements</h1>
                <Achievement achievementData={achievementData}/>
            </div>
        </div>
    );
}

export default AchievementWidget;