import { useState } from "react";

import styles from "@components/Header/Header.module.css";
import logo from "@assets/images/masa_logo_small_light.png";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
        <header className={styles.header}>
            <button
                className={styles.menuButton}
                onClick={() => setIsOpen(true)}
            >
                <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                        <path d="M4 18L20 18" stroke="#535960" stroke-width="2" stroke-linecap="round"></path>
                        <path d="M4 12L20 12" stroke="#535960" stroke-width="2" stroke-linecap="round"></path>
                        <path d="M4 6L20 6" stroke="#535960" stroke-width="2" stroke-linecap="round"></path>
                    </g>
                </svg>
            </button>

            <a href="" className={styles.logo}>
                <img src={logo} className={styles.logo} />
            </a>

            <span>Dashboard</span>
        </header>

        <nav
            className={`${styles.navMenu} ${isOpen ? styles.active : ""}`}
        >
                <div className={styles.navHeader}>
                    <a href="" className={styles.logo}>
                        <img src={logo} className={styles.logo} />
                    </a>
                    <button 
                        className={styles.closeButton}
                        onClick={() => setIsOpen(false)}
                    >
                        <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <path
                                    d="M20.7457 3.32851C20.3552 2.93798 19.722 2.93798 19.3315 3.32851L12.0371 10.6229L4.74275 3.32851C4.35223 2.93798 3.71906 2.93798 3.32854 3.32851C2.93801 3.71903 2.93801 4.3522 3.32854 4.74272L10.6229 12.0371L3.32856 19.3314C2.93803 19.722 2.93803 20.3551 3.32856 20.7457C3.71908 21.1362 4.35225 21.1362 4.74277 20.7457L12.0371 13.4513L19.3315 20.7457C19.722 21.1362 20.3552 21.1362 20.7457 20.7457C21.1362 20.3551 21.1362 19.722 20.7457 19.3315L13.4513 12.0371L20.7457 4.74272C21.1362 4.3522 21.1362 3.71903 20.7457 3.32851Z" fill="#535960"
                                />
                            </g>
                        </svg>
                    </button>
                </div>
            <ul className={styles.navList}>
                <li><a href="">Home</a></li>
                <li><a href="">Counter</a></li>
                <li><a href="">History</a></li>
                <li><a href="">Stats</a></li>
                <li><a href="">Timeline</a></li>
                <li><a href="">Achievements</a></li>
                <li><a href="">About</a></li>
            </ul>
        </nav>
        </>
    );
}

export default Header;