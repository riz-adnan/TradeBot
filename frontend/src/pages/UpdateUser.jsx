import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';

// styles
import '../styles/AddUser.css';

const UpdateUser = ({ account }) => {
    // Initialize state variables, params and functions
    const { id } = useParams();
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repassword, setRepassword] = useState('');
    const [publicApiKey, setPublicApiKey] = useState('');
    const [privateApiKey, setPrivateApiKey] = useState('');
    const [baseUrl, setBaseUrl] = useState('');
    const [formError, setFormError] = useState('');

    // Functions
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || !password || !repassword || !publicApiKey || !privateApiKey || !baseUrl) {
            setFormError('Please provide all fields');
            return;
        }
        if (password !== repassword) {
            setFormError('Passwords do not match');
            return;
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/user/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${account.token}`
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    api_key_private: privateApiKey,
                    api_key_public: publicApiKey,
                    base_url: baseUrl
                })
            });

            if (response.ok) {
                navigate('/');
            } else {
                const errorData = await response.json();
                setFormError(errorData.message);
            }
        } catch (error) {
            console.error('Error:', error);
            setFormError('An error occurred while adding the user');
        }
    }
    
    useEffect(() => {
        const fetchUser = async () => {
            try {
                console.log(`The address is: http://127.0.0.1:8000/user/${id}`);
                const response = await fetch(`http://127.0.0.1:8000/user/${id}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error(`Failed to fetch ${id} data`);
                    // navigate('/', { replace: true });
                }
                const data = await response.json().then((data) => data.data);
                setEmail(data.email);
                setPublicApiKey(data.api_key_public);
                setPrivateApiKey(data.api_key_private);
                setBaseUrl(data.base_url);
            } catch (error) {
                setFormError(error.message);
            }
        }
        fetchUser();
    }, [id, navigate])

    return (
        <div className="add-user-container">
            <h1 className="text-center my-3">{id}</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} />
                <label htmlFor="name">Password</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} />
                <label htmlFor="name">Re-enter Password</label>
                <input
                    type="password"
                    id="repassword"
                    value={repassword}
                    onChange={(e) => setRepassword(e.target.value)} />
                <label htmlFor="public_api">Public API Key</label>
                <input
                    type="password"
                    id="publicApiKey"
                    value={publicApiKey}
                    onChange={(e) => setPublicApiKey(e.target.value)} />
                <label htmlFor="private_api">Private API Key</label>
                <input
                    type="password"
                    id="privateApiKey"
                    value={privateApiKey}
                    onChange={(e) => setPrivateApiKey(e.target.value)} />
                <label htmlFor="base_url">URL of the Trading Portal</label>
                <input
                    type="text"
                    id="baseUrl"
                    value={baseUrl}
                    onChange={(e) => setBaseUrl(e.target.value)} />
                <button type="submit">Update User</button>
            </form>

            {formError && <p className="error">{formError}</p>}
        </div>
    );
}

export default UpdateUser;