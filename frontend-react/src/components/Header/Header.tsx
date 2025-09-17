import { useState } from "react";

import styles from "@components/Header/Header.module.css";
import logo from "@assets/images/masa_logo_small_light.png";
import closeIcon from "@assets/images/close-icon.svg";
import menuIcon from "@assets/images/menu-icon.svg";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
        <header className={styles.header}>
            <div className={styles.logoBox}>
                <img src={logo} className={styles.logo} />
                <h1>Home</h1>
            </div>


            <button
                onClick={() => setIsOpen(true)}
            >
                <img src={menuIcon} className={styles.logo}/>
            </button>
        </header>

        <nav
            className={`${styles.navMenu} ${isOpen ? styles.active : ""}`}
        >
            <ul>
                <button 
                    onClick={() => setIsOpen(false)}
                >
                    <img src={closeIcon} className={styles.logo}/>
                </button>

                <li><a href="#">Home</a></li>
                <li><a href="#">Counter</a></li>
                <li><a href="#">History</a></li>
                <li><a href="#">Stats</a></li>
                <li><a href="#">Timeline</a></li>
                <li><a href="#">Achievements</a></li>
                <li><a href="#">About</a></li>
            </ul>
        </nav>
        <hr />
        </>
    );
}

export default Header;
