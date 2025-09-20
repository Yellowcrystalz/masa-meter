import shared from "@styles/shared.module.css";
import type { LeadeboardProps } from "@/types";

const Leaderboard = ({ leaderboardData }: LeadeboardProps) => {
    const emojiList = [
        "\u{1F947}",
        "\u{1F948}",
        "\u{1F949}",
        "\u{1F3C5}",
        "\u{1F3C5}",
    ]
    return (
        <ul className={shared.widgetList}>
            {
                leaderboardData.slice(0, 5).map((entry, index) => (
                    <li key={index}>
                        {emojiList[index]}
                        <span className={shared.boldText}>
                            {entry.username}
                        </span>
                        {" "}- {entry.count}
                    </li>
                ))
            }
        </ul>
    );
}

export default Leaderboard;