import shared from "@styles/shared.module.css";
import styles from "./SushiPicWidget.module.css";
import { useEffect, useState } from "react";


const SushiPicWidget = () => {
    const [url, setUrl] = useState("");

    useEffect(() => {
        fetch("/api/sushi-pic")
            .then((response) => response.json())
            .then((data) => {
                setUrl(data.sushi_pic_url);
            })
            .catch(error => console.error(error));
    }, [])

    return (
        <div>
            <div className={shared.widget}>
                <h1 className={shared.widgetTitle}>Sushi Pic</h1>
                <div className={styles.picContainer}>
                    <img src={url} alt="Sushi Pic" className={styles.sushiPic}/>
                </div>
            </div>
        </div>
    );
}

export default SushiPicWidget;