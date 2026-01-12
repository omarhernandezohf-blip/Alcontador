'use client';

import { useMemo } from 'react';

const generateBoxShadow = (n: number) => {
    let value = '';
    for (let i = 0; i < n; i++) {
        value += `${Math.random() * 2000}px ${Math.random() * 2000}px #FFF`;
        if (i < n - 1) value += ', ';
    }
    return value;
};

export function StarsBackground() {
    const shadowsSmall = useMemo(() => generateBoxShadow(700), []);
    const shadowsMedium = useMemo(() => generateBoxShadow(200), []);
    const shadowsBig = useMemo(() => generateBoxShadow(100), []);

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
