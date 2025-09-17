import logo from "@assets/images/masa_logo_big_light.png"
import { useEffect, useState } from "react";

const MeterWidget = () => {
    const [meter, setMeter] = useState(0);

    useEffect(() => {
        const updateMeter = () => {
            fetch("http://localhost:8000/api/meter")
                .then((response) => response.json())
                .then((data) => setMeter(data[0].meter))
                .catch(error => console.error(error));
        }

        updateMeter()
        const interval = setInterval(updateMeter, 5000);
        
        return () => clearInterval(interval);
    }, []);
    
    return (
        <>
            <img src={logo} alt="" />
            <h1>{meter}</h1>
        </>
    );
}

export default MeterWidget;
