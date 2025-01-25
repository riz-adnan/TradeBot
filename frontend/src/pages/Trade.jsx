import React, { useState } from 'react';
import '../styles/Trade.css';

const Trade = ({ account }) => {
    const [isTrading, setIsTrading] = useState(false);

    const startTrade = async () => {
        try {
            setIsTrading(true);
            const response = await fetch('http://localhost:8000/trading/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${account.token}`
                }
            });
        } catch (error) {
            console.error('Error', error);
        }
    }

    const stopTrade = async () => {
        setIsTrading(false);
    }

    return (
        <main className='trade-container'>
            {isTrading === false ? <button onClick={startTrade}>Start Trade</button>
            : <button onClick={stopTrade}>Stop Trade</button>}
        </main>
    )
}

export default Trade;
