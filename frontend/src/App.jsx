import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

// pages
import Home from './pages/Home';
import AboutUs from './pages/AboutUs';
import AddUser from './pages/AddUser';
import UpdateUser from './pages/UpdateUser';
import FetchUser from './pages/FetchUser';
import Trade from './pages/Trade';

// components
import Navbar from './components/Navbar';

// authorization
import Login from './auth/Login';

function App() {
    const [account, setAccount] = useState(JSON.parse(localStorage.getItem('account')) || {
        username: null,
        email: null,
        token: null
    });

    return (
        <BrowserRouter>
            <Navbar
                account={account}
                setAccount={setAccount}
            />
            <Routes>
                <Route path="/" element={<Home account={account} />} />
                <Route path="/about" element={<AboutUs />} />
                <Route path="/addUser" element={<AddUser />} />
                <Route path="/updateUser/:id" element={<UpdateUser account={account} />} />
                <Route path="/fetchUser/:id" element={<FetchUser />} />
                <Route
                    path="/login"
                    element={<Login setAccount={setAccount} />}
                />
                <Route
                    path='/trade'
                    element={<Trade account={account} />}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;