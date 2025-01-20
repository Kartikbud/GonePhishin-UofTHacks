Gone Phishin' - UofT Hacks 2025



We are proud to present Gone Phishin', created by Kartik Budihal, Darun Kanesalingam, and Evan Liu for UofT Hacks 2025. This project addresses the growing issue of cybercrime perpetrated through scam calls and phishing attempts over the phone.

What It Does

Gone Phishin' utilizes the Gemini API to listen to live calls and analyze the audio in real-time to determine if the caller's activity appears suspicious. The application is designed to:

Detect potential scams during phone calls.

Provide a user-friendly interface to monitor conversations.

How It Works

When a call starts, the user clicks the Start button to begin monitoring.

During the call, buttons corresponding to "User Talking" and "Caller Talking" are clicked based on who is speaking.

The app uses the collected data and Gemini API to analyze the conversation for suspicious patterns.

Getting Started

Prerequisites

Python installed

Required dependencies listed in requirements.txt

Installation

Clone the repository:

git clone https://github.com/Kartikbud/GonePhishin-UofTHacks.git
cd GonePhishin-UofTHacks

Install the required dependencies:

pip install -r requirements.txt

Run the program:

python manage.py runserver

Open the application in your web browser by navigating to the URL displayed in your terminal (typically http://127.0.0.1:8000).

Features

Real-Time Audio Analysis: Scans calls live to detect potential phishing attempts.

Interactive UI: Buttons for tracking conversation flow ensure accurate detection.

Gemini API Integration: Leverages advanced machine learning for scam detection.

Contribution

We welcome contributions to enhance Gone Phishin'. To contribute:

Fork the repository.

Create a new branch for your feature or bug fix.

Submit a pull request with detailed changes.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements

UofT Hacks 2025 for hosting an incredible hackathon.

Mentors, organizers, and participants for their guidance and support.

Screenshots
