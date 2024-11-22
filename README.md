# Trade Bot

## 📖 Introduction

Welcome to our Trade Bot, a powerful tool designed to perform real-time trades in the market using advanced algorithms powered by Machine Learning. This README will guide you through the setup, features, and usage of our Trade Bot.

## 📝 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Algorithm Details](#algorithm-details)
6. [Risk Management](#risk-management)
7. [Contributing](#contributing)
8. [Authors](#authors)
9. [License](#license)

## 📝 Overview

Our Trade Bot leverages cutting-edge algorithms to analyze market trends, identify potential trading opportunities, and execute trades in real time. The goal is to maximize profits while minimizing risks, making it an invaluable tool for both novice and experienced traders.

## ✨ Features

- **Cutting Edge Strategies:** The bot employs sophisticated strategies to analyze market data and make informed trading decisions.
- **Machine Learning Algorithms:** The devised strategies to leverage Machine Learning to yield optimal outcomes.
- **Real-Time Trading:** Execute trades in real-time to capitalize on market fluctuations.
- **Risk Management:** Implement robust risk management techniques to protect your investments.

## 📲 Installation

Follow these steps to set up the Trade Bot on your system:

1. Clone the repository:
    ```bash
    git clone https://github.com/codeclubiittp/Trading_bot.git
    ```

2. Install dependencies:
    ```bash
    cd Trading_bot
    pip install -r requirements.txt
    ```

3. Set up API keys:
    - Obtain API keys from your preferred stock exchange. We recommend Alpaca.

##  🧑🏽‍💻 Usage
Run the bot with the following command:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port:8080
    ```

Monitor the bot's output for real-time updates, trade executions, and performance metrics.

## Using the Trading Bot Web Service

This document outlines how to interact with the trading bot web service, which is built using Python, FastAPI, and SwaggerUI.

### 🚀 Live Link:

[Live link to our web service.](https://trading-bot-8nld.onrender.com/docs)

### 📜 Accessing the API Documentation:

Visit the live link provided above.
You'll be presented with the SwaggerUI interface, which provides interactive documentation for the API endpoints. The window may look like below:
![image](https://github.com/codeclubiittp/Trading_bot/assets/113628188/81884732-4512-4480-8f45-62e76c01d951)


### Authentication (if applicable):

🎬 If you are a new user then register using the POST request as shown in the video below.

https://github.com/codeclubiittp/Trading_bot/assets/113628188/39490e83-2369-4714-a4b1-8aee49f01974

🎬 If already registered then authenticate as shown.

https://github.com/codeclubiittp/Trading_bot/assets/113628188/ed7c9f10-6def-4396-8591-c7afc6fc3178

### 📎 Available Endpoints:

1. **GET /strategies:**
<ul>
<li>Description: Get a list of all available trading strategies supported by the bot.</li>
<li>Status code: 200 (OK)</li>
<li>Response model: List[Strategy] (an array containing information about each strategy, including strategy name, description, and key parameters)</li>
</ul>

2. **POST /orders:**
<ul>
<li>Description: Place a new trade order for the bot to execute.</li>
<li>Body: Order (containing details like symbol, order type, amount, price)</li>
<li>Status code: 201 (Created)</li>
<li>Response model: Order (confirmation of the submitted order, including order ID and estimated execution time)</li>
</ul>

3. **GET /status:**
<ul>
<li>Description: Check the current status and performance of the trading bot.</li>
<li>Status code: 200 (OK)</li>
<li>Response model: BotStatus (providing information like current positions, open orders, account balance, total profit/loss, and key performance indicators)</li>
</ul>

### Additional Information:

Please use it at your own risk.

### Contact Information:

For any related queries contact: <a href = 'mailto:codeclub@iittp.ac.in'>codeclub@iittp.ac.in</a>

## 📋 Algorithm Details
Our algorithms are designed using Machine Learning, historical market data, technical indicators, and other relevant factors to make perfect trading signals.

## 🦟 Risk Management
The investments are protected by implementing effective risk management strategies. Risk thresholds, stop-loss parameters, and other useful settings to align with your risk tolerance.

## 👷 Contributing
We welcome contributions from the community. Feel free to submit bug reports, feature requests, or even pull requests to help improve the Trade Bot.

## 🎓 Author

<p>  <a href="https://github.com/riz-adnan"><b>Adnan Abbas Rizvi</b><a/> (Team Leader)<p/>
<p> <a href="https://github.com/prakharmoses"><b>Prakhar Moses </b><a/></p>
<p> <a href="https://github.com/cs21b037iittp"><b>Nandhavardhan </b><a/></p>

## 📰 License
This Trade Bot is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.

Happy trading! 🚀
