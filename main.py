import streamlit as st
import preprocessor
import stats
import matplotlib.pyplot as plt
import seaborn as sns

# --- UI Configuration & Styling ---
# Set a consistent style for all plots for a cleaner look
sns.set_style("whitegrid")

# Set the main page title
st.title("WhatsApp Chat Analyzer")

# --- Sidebar ---
st.sidebar.title("Analyze Your Chat")

# Add a little instruction text in the sidebar
st.sidebar.markdown("1. Export your WhatsApp chat as a `.txt` file.")
st.sidebar.markdown("2. Upload the file below.")

uploaded_file = st.sidebar.file_uploader("Upload a chat file (txt format)", type=['txt'])

# --- Main Page ---
if uploaded_file is None:
    # Show a welcoming/instructional message if no file is uploaded
    st.info("💡 Please upload a WhatsApp chat export file using the sidebar to get started.")

else:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors="ignore")
    df = preprocessor.preprocess(data)

    # --- User Selection in Sidebar ---
    users = df['Sender'].dropna().astype(str).unique().tolist()
    if 'group_notification' in users:
        users.remove('group_notification')
    users.sort()
    users.insert(0, 'Group')

    selected_user = st.sidebar.selectbox("Show analysis for:", users)

    if st.sidebar.button('Show Analysis'):

        # --- Top Statistics Section ---
        st.header(f"Top Statistics for {selected_user}")
        num_messages, total_words, total_media, total_stickers = stats.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", total_words)
        with col3:
            st.metric("Media Shared", total_media)
        with col4:
            st.metric("Stickers Sent", total_stickers)

        # Add a visual separator
        st.markdown("---")

        # --- Timeline Analysis Section ---
        st.header("Timeline Analysis")

        # Monthly Timeline
        st.subheader("Monthly Timeline")
        timeline = stats.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'], color='green')
        ax.set_title(f"Monthly Message Count for {selected_user}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.subheader("Daily Timeline")
        daily_timeline = stats.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
        ax.set_title(f"Daily Message Count for {selected_user}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Add a visual separator
        st.markdown("---")

        # --- Activity Analysis Section ---
        st.header("Activity Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Busy Day")
            busy_day = stats.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            ax.set_title(f"Most Busy Days for {selected_user}")
            ax.set_xlabel("Day of the Week")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = stats.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_title(f"Most Busy Months for {selected_user}")
            ax.set_xlabel("Month")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Weekly Activity Heatmap
        st.subheader("Weekly Activity Heatmap")
        user_heatmap = stats.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax, cmap="viridis")
        ax.set_title(f"Weekly Activity for {selected_user}")
        ax.set_xlabel("Time Period")
        ax.set_ylabel("Day of the Week")
        st.pyplot(fig)

        # Add a visual separator
        st.markdown("---")

        # --- Group-Specific Analysis ---
        if selected_user == 'Group':
            st.header("Group-Level Analysis")

            # Most Busy Users
            st.subheader("Most Active Users")
            x, new_df = stats.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='skyblue')
                ax.set_title("User Activity (Bar Chart)")
                ax.set_xlabel("User")
                ax.set_ylabel("Number of Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                # Add a title to the dataframe for context
                st.subheader("User Activity (Table)")
                st.dataframe(new_df)

            st.markdown("---")

        # --- Message Content Analysis ---
        st.header("Message Content Analysis")

        # WordCloud
        st.subheader("Word Cloud")
        df_wc = stats.words(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        # Hide the axes for a cleaner look on the wordcloud
        plt.axis("off")
        st.pyplot(fig)

        # Most Common Words
        st.subheader("Most Common Words")
        most_common_df = stats.most_common_words(selected_user, df)
        st.dataframe(most_common_df, use_container_width=True)  # Fills the column width

        # Most Common Emojis
        st.subheader("Most Common Emojis")
        emoji_df = stats.common_emojis(selected_user, df)
        st.dataframe(emoji_df, use_container_width=True)