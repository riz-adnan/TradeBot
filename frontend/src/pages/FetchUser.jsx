import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// components
import UserDetail from '../components/UserDetail';

// styles
import '../styles/FetchUser.css';

const FetchUser = () => {
    // Initialize state variables and params
    const { id } = useParams();
    const [user, setUser] = useState(null);
    const [fetchError, setFetchError] = useState(null);

    // Fetch data from the API
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/user/${id}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    setUser(null);
                    setFetchError('Failed to fetch user');
                    throw new Error('Failed to fetch user');
                }
                const data = await response.json().then((data) => data.data);
                setFetchError(null);
                setUser(data);
            } catch (error) {
                setFetchError(error.message);
            }
        }
        fetchUser();
    }, []);

    return (
        <div className="fetchuser-container">
            <h1>Fetch User</h1>
            {fetchError && <p>{fetchError}</p>}
            {user && (
                <div className="user">
                    <UserDetail user={user} />
                </div>
            )}
        </div>
    );
}

export default FetchUser;