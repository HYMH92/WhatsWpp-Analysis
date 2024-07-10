# WhatsWpp-Analysis
Short code to break down a few features and characteristics of your WhatsApp correspondence

## Documentation for the WhatsApp Analysis Code
### Overview
This Jupyter Notebook performs analysis on WhatsApp chat data. It generates various charts to visualize the distribution of messages, media, and emojis over different time periods and by different participants.

### Dependencies
Ensure you have the following Python libraries installed:
re
collections
emoji
statistics
matplotlib

### Notebook Sections

#### Data Loading and Preprocessing
Load the WhatsApp chat data file.
Preprocess the data to extract relevant information such as dates, times, senders, and content types.
Aggregate data by year, hour, message type, and sender.
Store these aggregated results in dictionaries.

#### Visualization Functions
Define functions to create charts for different aspects of the data:
create_chart_int(data): Generates charts for integer-based data (e.g., messages per hour).
create_chart_name(data): Generates charts for name-based data (e.g., messages per sender).
Generating Charts

Use the defined functions to generate and display the charts for the aggregated data.
