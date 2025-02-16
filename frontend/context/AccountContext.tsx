import React, { createContext, useContext, ReactNode, useState, use } from 'react';
import { useRouter } from 'next/navigation';

interface AccountContextType {
  accountId: string | null;
  account: any;
  setAccountId: (id: string | null) => void;
  setAccount: (account: any) => void;
  signup: (username: string, email: string, password: string, api_key_private: string, api_key_public: string, base_url: string, confirmPassword: string) => void;
  login: (email: string, password: string) => void;
  logout: () => void;
}

const AccountContext = createContext<AccountContextType | undefined>(undefined);

export const AccountProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const router = useRouter();
  // const [jwtToken, setJwtToken] = useState<string | null>('fggjgjgd89');
  const [accountId, setAccountId] = useState<string | null>('hgfjdh3s');
  const [account, setAccount] = useState<any>({
    username: '',
    email: '',
    profilePicture: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNYLv3ILZTm1R35NsHkSwt4JSgral8pgRwDg&s',
    currentBalance: 0,
    profit: 0,
    api_key_private: '',
    api_key_public: '',
    base_url: ''
  });

  const signup = async (username: string, email: string, password: string, api_key_private: string, api_key_public: string, base_url: string, confirmPassword: string) => {
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    try {
      const response = await fetch('https://trading-bot-lmca.onrender.com/user/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, api_key_private, api_key_public, base_url }),
      });
      
      if (response.ok || response.status === 201) {
        const data = await response.json();
        setAccountId(data.id);
        localStorage.setItem('jwtToken', data.access_token);
        setAccount({
          username: data.username,
          email: email,
          currentBalance: data.current_balance,
          profit: data.profit,
          api_key_private: data.api_key_private,
          api_key_public: data.api_key_public,
          base_url: data.base_url
        })
        router.push('/');
      } else {
        console.error('Account creation');
        alert('Account creation failed');
      }

    } catch (error) {
      console.error('Error:', error);
    }
  }

  const login = async (email: string, password: string) => {
    try {
      console.log("The login request is: ", email, password);
      const response = await fetch('https://trading-bot-lmca.onrender.com/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password
        }),
      })

      if (response.ok || response.status === 200) {
        const data = await response.json();
        console.log("The login response recieved is: ", data);
        localStorage.setItem('jwtToken', data.access_token);
        setAccountId(data.id);
        setAccount({
          username: data.username,
          email: email,
          profilePicture: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNYLv3ILZTm1R35NsHkSwt4JSgral8pgRwDg&s',
          currentBalance: data.current_balance,
          profit: data.profit,
          api_key_private: data.api_key_private,
          api_key_public: data.api_key_public,
          base_url: data.base_url
        })
        localStorage.setItem('account', JSON.stringify({
          username: data.username,
          email: email,
          profilePicture: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNYLv3ILZTm1R35NsHkSwt4JSgral8pgRwDg&s',
          currentBalance: data.current_balance,
          profit: data.profit,
          api_key_private: data.api_key_private,
          api_key_public: data.api_key_public,
          base_url: data.base_url
        }));
        router.push('/');
      } else {
        console.error('Login failed');
        alert('Login failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  const logout = async () => {
    try {
      const response = await fetch('https://trading-bot-lmca.onrender.com/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: localStorage.getItem('jwtToken'),
      })

      if (response.ok || response.status === 200 || response.status === 204) {
        localStorage.removeItem('jwtToken');
        setAccountId(null);
        console.log("User logged out");
        router.push('/signin');
      } else {
        console.error('Logout failed');
        alert('Logout failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  return (
    <AccountContext.Provider value={{ accountId, account, setAccountId, setAccount, signup, login, logout }}>
      {children}
    </AccountContext.Provider>
  );
};

export const useAccount = (): AccountContextType => {
  const context = useContext(AccountContext);
  if (!context) {
    throw new Error('useAccount must be used within an AccountProvider');
  }
  return context;
};