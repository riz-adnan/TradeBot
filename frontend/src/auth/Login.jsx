import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Login = ({ setAccount }) => {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleNameChange = (e) => {
        setName(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: name,
                    password: password
                })
            })
            const data = await response.json();
            if (data.access_token) {
                const account = {
                    username: data.username,
                    email: data.email,
                    token: data.access_token
                }
                setAccount(account);
                localStorage.setItem('account', JSON.stringify(account));
                navigate('/trade');
            }
        } catch (error) {
            console.error('Error:', error);
            console.log('The error message is: ', error.message);
        }
    };

    return (
        <div className='add-user-container'>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Name:
                    <input type="text" value={name} onChange={handleNameChange} />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" value={password} onChange={handlePasswordChange} />
                </label>
                <br />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;