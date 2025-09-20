import shared from "@styles/shared.module.css";
import type { HistoryProps } from "@/types";


const History = ({ historyData }: HistoryProps) => {
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);

        dateString = date.toLocaleString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
        })

        return dateString;
    }

    return (
        <ul className={shared.widgetList}>
            {
                historyData.map((entry, index) => (
                    <li key={index}>
                        <span className={shared.boldText}>
                            {formatDate(entry.date)}
                        </span>
                         - {entry.username}
                    </li>
                ))
            } 
        </ul>
    );
}

export default History;