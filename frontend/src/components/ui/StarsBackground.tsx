'use client';

import { useState, useEffect } from 'react';

const generateBoxShadow = (n: number) => {
    let value = '';
    for (let i = 0; i < n; i++) {
        value += `${Math.random() * 2000}px ${Math.random() * 2000}px #FFF`;
        if (i < n - 1) value += ', ';
    }
    return value;
};

export function StarsBackground() {
    const [shadowsSmall, setShadowsSmall] = useState('');
    const [shadowsMedium, setShadowsMedium] = useState('');
    const [shadowsBig, setShadowsBig] = useState('');

    useEffect(() => {
        setShadowsSmall(generateBoxShadow(700));
        setShadowsMedium(generateBoxShadow(200));
        setShadowsBig(generateBoxShadow(100));
    }, []);

    if (!shadowsSmall) return null; // Evitar renderizado hasta que esté listo en cliente

    return (
        <div className="universe-bg fixed inset-0 pointer-events-none z-[-1]">
            <div
                className="star-layer w-[1px] h-[1px] rounded-full opacity-70 animate-[animStar_100s_linear_infinite]"
                style={{ boxShadow: shadowsSmall }}
            />
            <div
                className="star-layer w-[2px] h-[2px] rounded-full opacity-90 animate-[animStar_150s_linear_infinite]"
                style={{ boxShadow: shadowsMedium }}
            />
            <div
                className="star-layer w-[3px] h-[3px] rounded-full opacity-100 animate-[animStar_200s_linear_infinite]"
                style={{ boxShadow: shadowsBig }}
            />
        </div>
    );
}
