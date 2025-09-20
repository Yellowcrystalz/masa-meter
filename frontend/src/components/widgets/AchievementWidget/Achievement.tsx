import shared from "@styles/shared.module.css";
import type { AchievementProps } from "@/types";


const Achievement = ({ achievementData }: AchievementProps) => {
    return (
        <ul className={shared.widgetList}>
            {
                achievementData.map((entry, index) => (
                    <li key={index}>
                        {entry.emoji}
                        <span title={entry.description} className={shared.boldText}>
                            {entry.achievement_name}
                        </span>
                        {" "}- {entry.username}
                    </li>
                ))
            }
        </ul>
    );
}

export default Achievement;