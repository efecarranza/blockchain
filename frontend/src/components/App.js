import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../config';
import logo from '../assets/logo.png';

function App() {
    const [walletInfo, setWalletInfo] = useState({});
    useEffect(() => {
        fetch(`${API_BASE_URL}/wallet/info`)
        .then(response => response.json())
        .then(json => setWalletInfo(json));
    }, []);

    const { address, balance } = walletInfo;
    return (
        <div className="App">
            <img className="logo" src={logo} alt="beachcoin-logo" />
            <h3>Welcome to BeachCoin</h3>
            <br/>
            <Link to="/blockchain">Blockchain</Link>
            <Link to="/transaction">Transaction</Link>
            <Link to="/transaction_pool">Transaction Pool</Link>
            <div className="WalletInfo">
                <div>Address: {address}</div>
                <div>Balance: {balance}</div>
            </div>
        </div>
    );
}

export default App;
