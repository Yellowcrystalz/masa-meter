import MeterWidget from "@components/widgets/MeterWidget/MeterWidget";
import HistoryWidget from "@components/widgets/HistoryWidget.tsx/HistoryWidget";
import StatWidget from "@components/widgets/StatWidget/StatWidget";
import SushiPicWidget from "../widgets/SushiPicWidget/SushiPicWidget";
import AchievementWidget from "../widgets/AchievementWidget/AchievementWidget";
import AboutWidget from "../widgets/AboutWidget/AboutWidget";
import styles from "@components/WidgetGrid/WidgetGrid.module.css";


const WidgetGrid = () => {
    return (
        <div className={styles.widgetGrid}>
            <MeterWidget />
            <HistoryWidget />
            <StatWidget />
            <SushiPicWidget />
            <AchievementWidget />
            <AboutWidget />
        </div>
    );
}

export default WidgetGrid;