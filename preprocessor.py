import re
import pandas as pd

def preprocess(chat):
    # Clean and prepare chat lines
    lines = chat.splitlines()
    data = []

    # Regex pattern to match WhatsApp message lines
    pattern = r'^\[(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2}\s?[APMapm]{2})\]\s(.+)'

    for line in lines:
        # Remove non-visible characters
        line = line.strip().replace('\u202f', '').replace('\u200e', '')
        line = line.replace('\u202f', '').replace('\u200e', '')  # clean invisible unicode

        match = re.match(pattern, line)
        if match:
            date = match.group(1)
            message = match.group(2)
            data.append([date, message])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Date", "Sender_Message"])

    # Extract sender and actual message
    df[['Sender', 'Message']] = df['Sender_Message'].str.extract(r'^(.*?):\s(.*)', expand=True)

    # Replace group name with notification if applicable
    df['Sender'] = df['Sender'].str.replace(r'^Team Alfaaz.*', 'group_notification', regex=True)

    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'].str.replace('\u202f', ''), format="%d/%m/%y, %I:%M:%S%p", errors='coerce')

    # Add additional time-based features
    df['only_date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    # Drop combined column
    df.drop(columns=['Sender_Message'], inplace=True)

    return df
