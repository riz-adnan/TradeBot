import React, { createContext, useContext, ReactNode, useState } from 'react';

interface AccountContextType {
  jwtToken: string | null;
  accountId: string | null;
  setJwtToken: (token: string | null) => void;
  setAccountId: (id: string | null) => void;
}

const AccountContext = createContext<AccountContextType | undefined>(undefined);

export const AccountProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [jwtToken, setJwtToken] = useState<string | null>(null);
  const [accountId, setAccountId] = useState<string | null>(null);

  return (
    <AccountContext.Provider value={{ jwtToken, accountId, setJwtToken, setAccountId }}>
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