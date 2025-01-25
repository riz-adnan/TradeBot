import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AddUser.css';

const AddUser = () => {
    // Initialize state variables and functions
    const navigate = useNavigate();
    const [formError, setFormError] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repassword, setRepassword] = useState('');
    const [publicApiKey, setPublicApiKey] = useState('');
    const [privateApiKey, setPrivateApiKey] = useState('');
    const [baseUrl, setBaseUrl] = useState('');

    // Functions
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!name || !email || !password || !repassword || !publicApiKey || !privateApiKey || !baseUrl) {
            setFormError('Please provide all fields');
            return;
        }
        if (password !== repassword) {
            setFormError('Passwords do not match');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: name,
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

    return (
        <div className="add-user-container">
            <h1 className="text-center my-3">Add User</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)} />
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} />
                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} />
                <label htmlFor="repassword">Re-enter Password</label>
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
                <button type="submit">Add User</button>
            </form>

            {formError && <p className="error">{formError}</p>}
        </div>
    );
}

export default AddUser;