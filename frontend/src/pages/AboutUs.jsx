import React from 'react';
import '../styles/AboutUs.css';

const AboutUs = () => {
    return (
        <div className='aboutus-container'>
            <h1>About Us</h1>
            <div className="oveview">
                <h2>Overview</h2>
                <p>
                    Our Trade Bot leverages cutting-edge algorithms to analyze market trends, identify potential trading opportunities, and execute trades in real time. The goal is to maximize profits while minimizing risks, making it an invaluable tool for both novice and experienced traders.
                </p>
            </div>

            <div className="features">
                <h2>Features</h2>
                <ul>
                    <li>Cutting Edge Strategies: The bot employs sophisticated strategies to analyze market data and make informed trading decisions.</li>
                    <li>Machine Learning Algorithms: The devised strategies leverage Machine Learning to yield optimal outcomes.</li>
                    <li>Real-Time Trading: Execute trades in real-time to capitalize on market fluctuations.</li>
                    <li>Risk Management: Implement robust risk management techniques to protect your investments.</li>
                </ul>
            </div>

            <div className="algorithmic-detail">
                <h2>Algorithm Details</h2>
                <p>
                    Our algorithms are designed using Machine Learning, historical market data, technical indicators, and other relevant factors to make perfect trading signals.
                </p>
            </div>

            <div className="risk-management">
                <h2>Risk Management</h2>
                <p>
                    The investments are protected by implementing effective risk management strategies. Risk thresholds, stop-loss parameters, and other useful settings are used to align with your risk tolerance.
                </p>
            </div>

            <div className="contribute">
                <h2>Contributing</h2>
                <p>
                    We welcome contributions from the community. Feel free to submit bug reports, feature requests, or even pull requests to help improve the Trade Bot.
                </p>
            </div>

            <div className="author">
                <h2>Author</h2>
                <ul>
                    <li>Adnan Abbas Rizvi (Team Leader)</li>
                    <li>Prakhar Moses</li>
                    <li>Nandhavardhan</li>
                </ul>
            </div>
        </div>
    );
};

export default AboutUs;