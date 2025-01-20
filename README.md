# Gone Phishin' - UofT Hacks 2025

We are proud to present **Gone Phishin'**, created by **Kartik Budihal**, **Darun Kanesalingam**, and **Evan Liu** for **UofT Hacks 2025**. This project addresses the growing issue of cybercrime perpetrated through scam calls and phishing attempts over the phone.

---

## What It Does
**Gone Phishin'** utilizes the **Gemini API** to listen to live calls and analyze the audio in real-time to determine if the caller's activity appears suspicious. The application is designed to:
- Detect potential scams during phone calls.
- Provide a user-friendly interface to monitor conversations.

### How It Works
1. When a call starts, the user clicks the **Start** button to begin monitoring.
2. During the call, buttons corresponding to **\"User Talking\"** and **\"Caller Talking\"** are clicked based on who is speaking.
3. The app uses the collected data and Gemini API to analyze the conversation for suspicious patterns.

---

## Getting Started

### Prerequisites
To run **Gone Phishin'**, ensure you have the following installed:
- **Python 3.x**: Download it from [python.org](https://www.python.org/downloads/)

### Installation

Follow these steps to set up the project on your local machine:

1. Clone the repository by running the following command in your terminal:
   ```bash
   git clone https://github.com/Kartikbud/GonePhishin-UofTHacks.git
   cd GonePhishin-UofTHacks
