## Relevant libraries

import re
from collections import defaultdict
import emoji
from statistics import mode
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

## Data Loading and Preprocessing

def extract_date_and_time(line):
    # Define a regex pattern to match date and time at the beginning of the line
    pattern = r'^(\d{1,2}\.\d{1,2}\.\d{4}), (\d{1,2}:\d{2}) -'
    
    match = re.match(pattern, line)
    if match:
        date_str, time_str = match.groups()
        year = int(date_str.split('.')[2])
        hour = int(time_str.split(':')[0])
        return year, hour
    else:
        return None, None
    

def process_lines(file_path):
    user_lines = defaultdict(list)  # Dictionary to store user lines
    year_count = defaultdict(int)   # Dictionary to count occurrences by year
    hour_count = defaultdict(int)   # Dictionary to count occurrences by hour
    user_message_count = defaultdict(int)  # Dictionary to count messages per user
    user_media_count = defaultdict(int)  # Dictionary to count media per user
    user_emoji_count = defaultdict(int)  # Dictionary to count emojis per user
    user_emoji_use = defaultdict(list)  # Dictionary to count emojis per user
    general_emoji_count = defaultdict(int)  # Dictionary to count emojis in general
    
    with open(file_path, encoding="utf8") as file:
        last_user = None  # Initialize variable to track the last detected user
        for line in file:
            year, hour = extract_date_and_time(line)
            if year is not None and hour is not None:
                # Extract user name (between "-" and ":")
                user_match = re.search(r'-(.*?):', line)
                if user_match:
                    user = user_match.group(1).strip()
                    user_message_count[user] += 1   # Update message count
                    year_count[year] += 1           # Update year count
                    hour_count[hour] += 1           # Update hour count
                    rest_of_line = line[user_match.end():].split()
                    if "<המדיה לא נכללה>" not in line:
                        for token in rest_of_line:
                        # Count words and emojis
                            if token in emoji.EMOJI_DATA:   # problem: ignore emoji that attached to a word (not recogized as an emoji) 
                                user_emoji_count[user] += 1
                                user_emoji_use[user].append(token)
                                general_emoji_count[token] += 1
                            else:
                                user_lines[user].append(token)  # Its not emoji but a regular word
                    elif "<המדיה לא נכללה>" in line:
                        user_media_count[user] += 1
                    last_user = user  # Update the last detected user
                    
            elif last_user:
                # Line doesn't start with date and time; add it to the last user's lines
                if "<המדיה לא נכללה>" not in line:
                    for word in line.split():
                        user_lines[last_user].append(word)
                    

    return dict(user_lines), dict(year_count), dict(hour_count),dict(user_message_count), dict(user_media_count), dict(user_emoji_count), dict(user_emoji_use), dict(general_emoji_count)


def create_chart_int(data):
    data_dict, x_label, y_label, Title = data
    df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label])
    
    if data_dict.items():
        # finding the max number and its user (value)
        target_number = df[y_label].max()
        target_value = df.loc[df[y_label] == target_number, x_label].values[0]
        
        #seting the colors for the max bar 
        clrs = ['lawngreen' if (x != target_number) else 'olivedrab' for x in df[y_label]]
        
        # Create a bar plot, and set the title
        sns.barplot(x=x_label, y=y_label, hue=x_label, legend=False, data=df, palette=clrs).set(title=Title)
        
        plt.show()
        
        print(f'the most busy {x_label} is {target_value} with {target_number} messages.')


def reverse_if_hebrew(text):    
    # Helper function to reverse the Hebrew text
    if re.search(r'[\u0590-\u05FF]', text) is not None:  # Check if text is Hebrew
        return text[::-1]  # Reverse the Hebrew text
    return text


def create_chart_name(data):
    data_dict, x_label, y_label, Title = data
    df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label]).sort_values(by=[y_label], ascending=False)
    
    if data_dict.items():
        # finding the max number and its user (value)
        target_number = df[y_label].max()
        target_value = df.loc[df[y_label] == target_number, x_label].values[0]
        
        #seting the colors
        clrs = ['lawngreen' if (x != target_number) else 'olivedrab' for x in df[y_label]]
        
        # Reverse Hebrew text in the Y-labels if necessary
        df[x_label] = df[x_label].apply(reverse_if_hebrew)
        
        # Create a horizontal bar plot by switching x and y
        ax = sns.barplot(y=x_label, x=y_label, hue=x_label, legend=False, data=df, palette=clrs)
        
        # Set title
        ax.set_title(Title)

        # Automatically adjust layout to fit all labels
        #plt.tight_layout()
        plt.show()

        print(f'The most busy {x_label} is {target_value} with {target_number} appearances.')


def create_emoji_chart(emoji_count):
    if emoji_count.items():
        emoji_dict = sorted(general_emoji_count.items(), key=lambda x: x[1], reverse=True)
        emoji_df = pd.DataFrame(emoji_dict, columns=['Emoji', 'Frequency'])
        if len(emoji_count.items()) > 20:
            print(emoji_df[:20])
        else:
            print(emoji_df)


YOUR_FILE = 'test.txt' # put the file path

# Enter the values
user_lines_dict, year_count_dict, hour_count_dict, message_count_dict, media_count_dict, emoji_count_dict, emoji_use_dict, general_emoji_count = process_lines(YOUR_FILE)


## Run and print results

"""
# Print the user lines dictionary (print the text per user)
print("User lines:")
for user, lines in user_lines_dict.items():
    print(f"{user}: {lines}")
"""

# Print the year count dictionary
print("\nYear count:")
for year, count in sorted(year_count_dict.items()):
    print(f"Year {year}: {count} occurrences")

create_chart_int((year_count_dict, "Year", "message_count","Message Count Per Year")) 

# Print the hour count dictionary
print("\nHour count:")
for hour, count in sorted(hour_count_dict.items()):
    print(f"Hour {hour}: {count} occurrences")

create_chart_int((hour_count_dict, "Hour", "message_count","Message Count Per Hour"))

# Print the massage count dictionary
print("\nMassage count:")
for user, message_count in sorted(message_count_dict.items()):
    print(f"{user}: {message_count} messages")

create_chart_name((message_count_dict, "User", "message_count", "Message usage"))

# Print word count and most used word for each user
print("\nWord count and most used word:")
for user, lines in user_lines_dict.items():
    print(f"{user}: {len(lines)} words")
    average = round((len(lines))/message_count_dict[user], 2)
    print(f"Average Words per Message: {average}")
    most_used_word = mode(lines)
    print(f"Most used word: {most_used_word}")

# Print the massage count dictionary
print("\nMedia count:")
for user, media_count in sorted(media_count_dict.items()):
    print(f"{user}: {media_count} media items")

create_chart_name((media_count_dict, "User", "media_count", "Media usage"))

# Print emoji count and most used emoji for each user
print("\nEmoji count and most used emoji:")
for user, emoji_count in emoji_count_dict.items():
    print(f"{user}: {emoji_count} emojis")
    most_used_emoji = mode(emoji_use_dict[user])
    print(f"Most used emoji: {most_used_emoji}")

create_chart_name((emoji_count_dict, "User", "emoji_count", 'Emoji Usage'))


print(f"\ngeneraly used emoji: ")
create_emoji_chart(general_emoji_count)

