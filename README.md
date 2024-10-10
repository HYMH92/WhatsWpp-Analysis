# WhatsWpp-Analysis
Short code to break down a few features and characteristics of your WhatsApp correspondence
#### for immediate use of the WebApp enter: https://whatswpp-analysis.streamlit.app/ 
###  

## Documentation for the WhatsApp Analysis Code
###  

## README for webapp.py
Project Title:
WhatsApp Conversation Analysis Web Application

### Description:
This is a Streamlit-based web application that allows users to upload WhatsApp chat exports and perform detailed analyses of their group conversations. The analysis includes visualizations and rich details about the interactions within the chat. The application processes chats extracted from Android devices and generates insights into the conversation patterns.

### Features:
Multi-language Support: The app provides operating instructions in both English and Hebrew.
File Upload: Users can upload a WhatsApp .txt file (without media) extracted from their device.
Detailed Analysis: The app generates various visual insights using matplotlib and seaborn.
WhatsApp Specific: Designed to work with WhatsApp chat formats, currently supporting Android.

### Usage Instructions:
1. Extract WhatsApp Chat:
Open WhatsApp and enter the conversation.
Tap the three dots on the top-right corner.
Select "More" → "Export Chat" → "Without Media".
Upload the chat .txt file to the app.
2. Features of the Web App:
Displays rich text instructions.
Upload functionality to process the conversation file.
Visual analysis (graphs, word frequency, chat activity) of group conversations.

### Libraries Used:
Streamlit: For building the web interface.
Pandas: For data handling and manipulation.
Matplotlib & Seaborn: For creating visualizations.
Regex: To extract date and time from chat lines.
Emoji: For analyzing emojis used in the chats.
Statistics: For mode calculation.

### How to Run (globally):
https://whatswpp-analysis.streamlit.app/

### How to Run (locally):
Install the required Python packages:
pip install streamlit pandas matplotlib seaborn emoji

Run the application:
streamlit run webapp.py

After installation, start the app by running the command mentioned above.
Upload a WhatsApp conversation .txt file.
Analyze the results, which will be displayed as graphs and statistics in the browser.

### License:
This project is open-source and available under the [MIT License].
###   


## README for whatsappanalysis.py
Project Title:
WhatsApp Chat Analysis Tool

### Description:
This script analyzes WhatsApp chat exports to extract meaningful insights such as message counts, media usage, emoji usage, and time-based patterns. It processes chat logs, categorizing data by user, time (year, hour), and message content (including emojis and media).

### Features:
Message Count: Track the number of messages sent by each user.
Yearly and Hourly Analysis: Count messages per year and hour to identify activity trends.
Emoji Usage: Track emoji usage per user, including the most frequently used emoji.
Media Tracking: Count the number of media files sent by each user.
Word Count: Measure word frequency and determine the most used words.
Visualization: Generate charts for message and media usage, as well as emoji statistics.

### Requirements:
Python 3.x
Libraries: re, emoji, collections, statistics, matplotlib, seaborn, pandas

### How to Run:
Place your WhatsApp chat export file in .txt format.
Modify the script to reference your chat file path.
Run the script in a Python environment.
The script will generate insights and charts based on your chat data.

### File Structure:
Data Loading & Preprocessing: Functions to extract dates, times, users, and content.
Analysis: Counts for messages, media, and emojis per user and time.
Visualization: Functions to generate charts for different data aspects.

### Charts Generated:
Message count by year and hour.
Message and media usage per user.
Emoji usage per user and general emoji trends.
### License:
Open for personal use and modification.
