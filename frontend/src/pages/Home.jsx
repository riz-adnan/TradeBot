import { useState, useEffect } from 'react';
import '../styles/Home.css';

// components
import UserCard from '../components/UserCard';

const Home = ({ account }) => {
    // Initialize state variables
    const [fetchError, setFetchError] = useState(null);
    const [users, setUsers] = useState(null);

    // Fetch data from the API
    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await fetch('http://localhost:8000/user/', {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG5hbkBnbWFpbC5jb20iLCJleHAiOjE3MjMwMTkyMzF9.IdAev0io3wGwxOD6VZg41N8I8TGZFFiR2_YQrfHUSN0',
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch users');
                }
                const data = await response.json().then((data) => data.data);
                setUsers(data);
            } catch (error) {
                setFetchError(error.message);
            }            
        };
        fetchUsers();
    }, []);

    return (
        <div className="home-container">
            <div className='starting-content'>
                <img src="./Logo.png" alt="TradeQuest" />
                <p>
                    Welcome to the Trade Bot! Here you can view all the users that are currently using the Trade Bot. 
                    Can trade in the market (for hackathon, only paper money). Update the users and trades.
                </p>
            </div>
            <h1>Trade Bot Users</h1>
            {fetchError && <p>{fetchError}</p>}
            {users && (
                <div className="users">
                    <div className="user-grid">
                        {users.map((user, key) => (
                            <UserCard key={key} idx={key} user={user} account={account} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Home;