import re
from collections import defaultdict
import emoji
from statistics import mode
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import zipfile


st.set_page_config(
        page_title="Whatsapp Analysis", page_icon="random"
)


# Title:
st.markdown("<h1 style='text-align: center; color: green;'>Whatsapp Analysis</h1>", unsafe_allow_html=True)

st.header('Detailed analysis of your group WhatsApp conversations, with rich details and clear graphs')

st.write("") # for space


heb_text = """\n
1- כרגע, הקוד רץ רק על שיחות שחולצו **מאנדרואיד**\n
2- פתחו את אפליקציית הוואטסאפ וכנסו לשיחה המעניינת אתכם\n
3- לחצו על שלוש הנקודות שמצד שמאל למעלה\n
4- בחרו עוד -> יצוא הצאט -> ללא מדיה\n
5- שלחו לעצמכם את הקובץ בצורה הנוחה לכם, והעלו אותו למיקום המתאים כאן\n
6- זכרו להוריד את הניתוח המלא ולשתף עם החבורה או המשפחה, רק אם בא לכם כמובן\n
7- להורדה: שלוש נקודת בצד ימין למעלה -> הדפסה"""

eng_text = """\n
1- Currently the code only runs on conversations extracted from **Android**\n
2- Open the WhatsApp application and enter the conversation that interests you\n
3- Click on the three dots on the top left\n
4- Choose More -> Export Chat -> No Media\n
5- Send yourself the file in the convenient way for you, and upload it to the intended location here\n
6- Remember to download the full analysis and share with the group or family, only if you feel like it of course\n
7- To download: three dots on the upper right -> print """

col1, col2 = st.columns(2, gap="large", vertical_alignment="top")

with col1:
    st.subheader("operating instructions")
    st.write(eng_text)

with col2:
    st.subheader("הוראות הפעלה")
    st.write(heb_text)
    

st.write("") # for space


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


def process_lines(file):
    user_lines = defaultdict(list)  # Dictionary to store user lines
    year_count = defaultdict(int)   # Dictionary to count occurrences by year
    hour_count = defaultdict(int)   # Dictionary to count occurrences by hour
    user_message_count = defaultdict(int)  # Dictionary to count messages per user
    user_media_count = defaultdict(int)  # Dictionary to count media per user
    user_emoji_count = defaultdict(int)  # Dictionary to count emojis per user
    user_emoji_use = defaultdict(list)  # Dictionary to count emojis per user
    general_emoji_count = defaultdict(int)  # Dictionary to count emojis in general
    
    
    last_user = None  # Initialize variable to track the last detected user
    for line in file.split('\n'):
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


def create_chart_int_years(data):
    data_dict, x_label, y_label, Title = data
    df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label])

    if data_dict.items():
    # finding the max number and its user (value)
        target_number = df[y_label].max()
        target_value = df.loc[df[y_label] == target_number, x_label].values[0]
        
        #seting the colors for the max bar 
        clrs = ['lawngreen' if (x != target_number) else 'olivedrab' for x in df[y_label]]
        
        # Create a bar plot, and set the title
        fig, ax = plt.subplots()
        sns.barplot(x=x_label, y=y_label, hue=x_label, legend=False, data=df, palette=clrs, ax=ax).set(title=Title)
    
        # Display the plot in Streamlit
        st.pyplot(fig, use_container_width=True)
        
        st.subheader(f'The most busy {x_label} was {target_value} with {target_number} messages.')


def create_chart_int_hours(data):
    data_dict, x_label, y_label, Title = data
    df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label])

    if data_dict.items():
    # finding the max number and its user (value)
        target_number = df[y_label].max()
        target_value = df.loc[df[y_label] == target_number, x_label].values[0]
        
        #seting the colors for the bars
        clrs = ['lawngreen' for x in df[y_label]]
        
        # Create a bar plot, and set the title
        fig, ax = plt.subplots()
        sns.barplot(x=x_label, y=y_label, hue=x_label, legend=False, data=df, palette=clrs, ax=ax).set(title=Title)
    
        # Display the plot in Streamlit
        st.pyplot(fig, use_container_width=True)
        
        st.subheader(f'The most busy {x_label} was {target_value}:00-{target_value+1}:00 with {target_number} messages.')


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
        
        # Create a bar plot(horizontal, by switching x and y), and set the title
        fig, ax = plt.subplots()
        sns.barplot(y=x_label, x=y_label, hue=x_label, legend=False, data=df, palette=clrs, ax=ax).set(title=Title)
        
        # Display the plot in Streamlit
        st.pyplot(fig, use_container_width=True)

        st.subheader(f'The most busy user was {target_value} with {target_number} appearances.')


def create_emoji_chart(emoji_count):
    if emoji_count.items():
        emoji_dict = sorted(general_emoji_count.items(), key=lambda x: x[1], reverse=True)
        emoji_df = pd.DataFrame(emoji_dict, columns=['Emoji', 'Frequency'])
        if len(emoji_count.items()) > 20:
            st.write(emoji_df[:20])
        else:
            st.write(emoji_df)



# File uploader to accept both text and zip files
upl = st.file_uploader("**Upload your text or zip file**", type=["txt", "zip"])

# Process the file
if upl:
    if upl.name.endswith(".txt"):
        # If a text file is uploaded
        file = upl.read().decode("utf-8")
    elif upl.name.endswith(".zip"):
        # If a zip file is uploaded
        with zipfile.ZipFile(upl, 'r') as zip_ref:
            # Extract all files from the zip
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith(".txt"):
                    # Only process the .txt file
                    with zip_ref.open(file_info) as txt_file:
                        file = txt_file.read().decode("utf-8")
                    break

    
    # Enter the values
    user_lines_dict, year_count_dict, hour_count_dict, message_count_dict, media_count_dict, emoji_count_dict, emoji_use_dict, general_emoji_count = process_lines(file)


    ## Run and print results


    st.header("") # for space


    # Print the year count dictionary
    st.markdown("<h4 style='text-align: right; color: gray;'>:מספר ההודעות שנשלחו בכל שנה</h4>", unsafe_allow_html=True)
    create_chart_int_years((year_count_dict, "Year", "message_count","Message Count Per Year"))

    with st.expander('The number of messages each year'):
        st.write("\n ")
        for year, count in sorted(year_count_dict.items()):
            st.markdown(f"**{year}:** {count} messages")
    

    st.header("") # for space
    
     
    # Print the hour count dictionary
    st.markdown("<h4 style='text-align: right; color: gray;'>:מספר ההודעות שנשלחו בכל שעה</h4>", unsafe_allow_html=True)
    create_chart_int_hours((hour_count_dict, "Hour", "message_count","Message Count Per Hour"))
    
    with st.expander('The number of messages each hour'):
        st.write("\n ")
        for hour, count in sorted(hour_count_dict.items()):
            st.markdown(f"**{hour}:00 - {hour+1}:00** : {count} occurrences")


    st.header("") # for space
    

    # Print the massage count dictionary
    st.markdown("<h4 style='text-align: right; color: gray;'>:מספר ההודעות ששלח כל משתמש</h4>", unsafe_allow_html=True)
    create_chart_name((message_count_dict, "", "message_count", "Message usage"))

    with st.expander('The number of messages per user'):
        st.write("\n")
        for user, message_count in sorted(message_count_dict.items(), key=lambda x:x[1], reverse=True):
            st.markdown(f"**{user}**: {message_count} messages")


    st.header("") # for space


    # Print the media count dictionary
    st.markdown("<h4 style='text-align: right; color: gray;'>:מספר הודעות המדיה ששלח כל משתמש</h4>", unsafe_allow_html=True)
    create_chart_name((media_count_dict, "", "media_count", "Media usage"))

    with st.expander('The number of media messages per user'):
        st.write("\n")
        for user, media_count in sorted(media_count_dict.items(), key=lambda x:x[1], reverse=True):
            st.markdown(f"**{user}**: {media_count} media items")


    st.header("") # for space


    # Print emoji count and most used emoji for each user
    st.markdown("<h4 style='text-align: right; color: gray;'>:מספר האימוג'ים ששלח כל משתמש</h4>", unsafe_allow_html=True)
    create_chart_name((emoji_count_dict, "", "emoji_count", 'Emoji Usage'))

    with st.expander('Emoji count and most used emoji per user'):
        st.write("\n")
        for user, emoji_count in sorted(emoji_count_dict.items(), key=lambda x:x[1], reverse=True):
            st.markdown(f"**{user}**: {emoji_count} emojis")
            most_used_emoji = mode(emoji_use_dict[user])
            st.write(f"Most used emoji: {most_used_emoji}")
            st.write(" ") # for space


    st.header("") # for space


    st.subheader(f"\ngeneraly used emoji: ")
    create_emoji_chart(general_emoji_count)

    

    st.header("") # for space


    # Print word count and most used word for each user
    st.markdown("<h4 style='text-align: right; color: gray;'>:מידע כללי נוסף</h4>", unsafe_allow_html=True)
    st.subheader("\nWord Count, Most Used Word, and Average Words per Message:")
    with st.expander('More details'):
        st.write("\n")
        new_user_lines_dict= {key: len(value) for key, value in user_lines_dict.items()}
        for user, len_lines in sorted(new_user_lines_dict.items(), key=lambda x:x[1], reverse=True):
            st.markdown(f"**{user}**: {len_lines} words")
            average = round((len_lines)/message_count_dict[user], 2)
            st.write(f"Average Words per Message: {average}")
            most_used_word = mode(user_lines_dict[user])
            st.write(f"Most used word: {most_used_word}")
            st.divider()  # Draws a horizontal rule


    st.header("") # for space

    
    st.write('Consider Starring 🌟 The repository if you like it')    

    @st.cache_data
    # IMPORTANT: Cache the conversion to prevent computation on every rerun

    # this function is here only because I cant understand how to delet it
    def convert_df(df):    
        return df.to_csv().encode('utf-8')
    