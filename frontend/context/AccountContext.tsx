"use client";

import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";

import { BACKEND_URL } from "@/lib/api";

type Account = {
  id?: string;
  username: string;
  email: string;
  profilePicture: string;
  currentBalance: number;
  profit: number;
  api_key_private: string;
  api_key_public: string;
  base_url: string;
};

interface AccountContextType {
  accountId: string | null;
  account: Account;
  setAccountId: (id: string | null) => void;
  setAccount: (account: Account) => void;
  signup: (
    username: string,
    email: string,
    password: string,
    api_key_private: string,
    api_key_public: string,
    base_url: string,
    confirmPassword: string,
  ) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const storageKeys = {
  account: "account",
  tradingUser: "trading_user",
  token: "auth_token",
  legacyToken: "jwtToken",
  apiKey: "alpaca_api_key",
  apiSecret: "alpaca_api_secret",
};

const emptyAccount: Account = {
  username: "",
  email: "",
  profilePicture:
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNYLv3ILZTm1R35NsHkSwt4JSgral8pgRwDg&s",
  currentBalance: 0,
  profit: 0,
  api_key_private: "",
  api_key_public: "",
  base_url: "",
};

const AccountContext = createContext<AccountContextType | undefined>(undefined);

async function parseResponse(response: Response) {
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "string"
        ? payload
        : payload?.detail
          ? JSON.stringify(payload.detail)
          : "Request failed";
    throw new Error(message);
  }

  return payload;
}

function persistAccount(account: Account) {
  localStorage.setItem(storageKeys.account, JSON.stringify(account));
  localStorage.setItem(
    storageKeys.tradingUser,
    JSON.stringify({
      name: account.username,
      email: account.email,
    }),
  );

  if (account.api_key_public) {
    localStorage.setItem(storageKeys.apiKey, account.api_key_public);
  }
  if (account.api_key_private) {
    localStorage.setItem(storageKeys.apiSecret, account.api_key_private);
  }
}

export const AccountProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const router = useRouter();
  const [accountId, setAccountId] = useState<string | null>(null);
  const [account, setAccount] = useState<Account>(emptyAccount);

  useEffect(() => {
    const storedAccount = localStorage.getItem(storageKeys.account);
    if (!storedAccount) return;

    try {
      const parsedAccount = JSON.parse(storedAccount) as Account;
      setAccount({ ...emptyAccount, ...parsedAccount });
      setAccountId(parsedAccount.id || parsedAccount.email || null);
    } catch {
      localStorage.removeItem(storageKeys.account);
    }
  }, []);

  const signup = async (
    username: string,
    email: string,
    password: string,
    api_key_private: string,
    api_key_public: string,
    base_url: string,
    confirmPassword: string,
  ) => {
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/user/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
          api_key_private,
          api_key_public,
          base_url,
        }),
      });

      const data = await parseResponse(response);
      const nextAccount: Account = {
        ...emptyAccount,
        id: data.id || email,
        username: data.user_name || username,
        email: data.email || email,
        api_key_private,
        api_key_public,
        base_url,
      };

      setAccountId(nextAccount.id || nextAccount.email);
      setAccount(nextAccount);
      persistAccount(nextAccount);
      router.push("/");
    } catch (error) {
      console.error("Signup error:", error);
      alert(error instanceof Error ? error.message : "Account creation failed");
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const body = new URLSearchParams();
      body.set("username", email);
      body.set("password", password);

      const response = await fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
      });

      const data = await parseResponse(response);
      const storedAccount = localStorage.getItem(storageKeys.account);
      const previousAccount = storedAccount
        ? (JSON.parse(storedAccount) as Account)
        : emptyAccount;
      const nextAccount: Account = {
        ...emptyAccount,
        ...previousAccount,
        id: previousAccount.id || email,
        username: previousAccount.username || email.split("@")[0],
        email,
      };

      localStorage.setItem(storageKeys.token, data.access_token);
      localStorage.setItem(storageKeys.legacyToken, data.access_token);
      setAccountId(nextAccount.id || nextAccount.email);
      setAccount(nextAccount);
      persistAccount(nextAccount);
      router.push("/");
    } catch (error) {
      console.error("Login error:", error);
      alert(error instanceof Error ? error.message : "Login failed");
    }
  };

  const logout = () => {
    localStorage.removeItem(storageKeys.token);
    localStorage.removeItem(storageKeys.legacyToken);
    localStorage.removeItem(storageKeys.account);
    localStorage.removeItem(storageKeys.tradingUser);
    localStorage.removeItem(storageKeys.apiKey);
    localStorage.removeItem(storageKeys.apiSecret);
    setAccountId(null);
    setAccount(emptyAccount);
    router.push("/signin");
  };

  return (
    <AccountContext.Provider
      value={{
        accountId,
        account,
        setAccountId,
        setAccount,
        signup,
        login,
        logout,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
};

export const useAccount = (): AccountContextType => {
  const context = useContext(AccountContext);
  if (!context) {
    throw new Error("useAccount must be used within an AccountProvider");
  }
  return context;
};
