import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar = ({ account, setAccount }) => {
    const handleLogout = () => {
        setAccount({ username: null, email: null, token: null});
        localStorage.removeItem('account');
    }

    return (
        <nav className="navbar-container">
            <ul>
                <li><Link to='/'>Home</Link></li>
                <li><Link to='/addUser'>Add User</Link></li>
                <li><Link to='/about'>About Us</Link></li>
                {account.token === null ? (
                    <li><Link to='/login'>Login</Link></li>
                ) : (
                    <>
                        <li><Link to='/trade'>Trade</Link></li>
                        <li><Link to='/login' onClick={handleLogout}>Logout</Link></li>
                    </>
                )}
            </ul>
        </nav>
    );
}

export default Navbar;