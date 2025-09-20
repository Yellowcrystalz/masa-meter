import Header from "@components/Header/Header.tsx";
import WidgetGrid from "@components/WidgetGrid/WidgetGrid.tsx";
import styles from "./App.module.css"

const App = () => {

    return (
        <div className={styles.app}>
            <Header />
            <WidgetGrid />
        </div>
    );
}

export default App;