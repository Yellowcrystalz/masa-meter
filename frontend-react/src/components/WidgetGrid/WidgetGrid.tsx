import MeterWidget from "@components/widgets/MeterWidget/MeterWidget.tsx"
import styles from "@components/WidgetGrid/WidgetGrid.module.css";

const WidgetGrid = () => {
    return (
        <div className={styles.widgetGrid}>
            <MeterWidget />
            <MeterWidget />
            <MeterWidget />
            <MeterWidget />
            <MeterWidget />
            <MeterWidget />
        </div>
    );
}

export default WidgetGrid;