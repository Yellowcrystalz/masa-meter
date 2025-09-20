import shared from "@styles/shared.module.css";
import type { HistoryEntry } from "@/types.ts";
import History from "./History";
import { useEffect, useState } from "react";


const HistoryWidget = () => {
    const [historyData, setHistoryData] = useState<HistoryEntry[]>([]);

    useEffect(() => {
        const updateHistory = () => {
            fetch("/api/history")
                .then((response) => response.json())
                .then((data: HistoryEntry[]) => {
                    let tempData: HistoryEntry[] = [];

                    for (let i = 1; i <= 5; i++) {
                        tempData.push(data[data.length - i]);
                    }

                    setHistoryData(tempData);
                })
                .catch(error => console.error(error));
        }

        updateHistory();
        const interval = setInterval(updateHistory, 30000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <div className={shared.widget}>
                <h1 className={shared.widgetTitle}>History</h1>
                <History historyData={historyData}/>
            </div>
        </div>
    );
}

export default HistoryWidget;