# WhatsWpp-Analysis
Short code to break down a few features and characteristics of your WhatsApp correspondence
#### for immediate use of the WebApp enter: https://whatswpp-analysis.streamlit.app/ 


## Documentation for the WhatsApp Analysis Code
### README for whatsappanalysis.py
Description:
This script analyzes WhatsApp chat exports to extract meaningful insights such as message counts, media usage, emoji usage, and time-based patterns. It processes chat logs, categorizing data by user, time (year, hour), and message content (including emojis and media).

Features:
Message Count: Track the number of messages sent by each user.
Yearly and Hourly Analysis: Count messages per year and hour to identify activity trends.
Emoji Usage: Track emoji usage per user, including the most frequently used emoji.
Media Tracking: Count the number of media files sent by each user.
Word Count: Measure word frequency and determine the most used words.
Visualization: Generate charts for message and media usage, as well as emoji statistics.
Requirements:
Python 3.x
Libraries: re, emoji, collections, statistics, matplotlib, seaborn, pandas
How to Run:
Place your WhatsApp chat export file in .txt format.
Modify the script to reference your chat file path.
Run the script in a Python environment.
The script will generate insights and charts based on your chat data.
File Structure:
Data Loading & Preprocessing: Functions to extract dates, times, users, and content.
Analysis: Counts for messages, media, and emojis per user and time.
Visualization: Functions to generate charts for different data aspects.
Charts Generated:
Message count by year and hour.
Message and media usage per user.
Emoji usage per user and general emoji trends.
License:
Open for personal use and modification.

