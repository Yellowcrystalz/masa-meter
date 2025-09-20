import shared from "@styles/shared.module.css";


const AboutWidget = () => {
    return (
        <div>
            <div className={shared.widget}>
                <h1 className={shared.widgetTitle}>About</h1>
                <ul className={shared.widgetList}>
                    <li><span className={shared.boldText}>Developer #1</span> - yellowcrystalz</li>
                    <li><span className={shared.boldText}>Developer #2</span> - d.a.n.n_</li>
                    <li><span className={shared.boldText}>Web Designer #1</span> - yellowcrystalz</li>
                    <li><span className={shared.boldText}>Web Designer #2</span> - tania</li>
                    <li><span className={shared.boldText}>Artist</span> - saotitaneater</li>
                </ul>
            </div>
        </div>
    );
}

export default AboutWidget;