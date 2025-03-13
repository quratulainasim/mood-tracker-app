import streamlit as st  
import pandas as pd  
import datetime  
import csv 
import os  

MOOD_FILE = "mood_log.csv"

def ensure_csv_headers():
    file_exists = os.path.exists(MOOD_FILE)

    if file_exists and os.stat(MOOD_FILE).st_size == 0:
        file_exists = False 

    if not file_exists:
        with open(MOOD_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Mood"]) 
            print("✅ Headers added to CSV") 

def load_mood_data():
    ensure_csv_headers()

    try:
        data = pd.read_csv(MOOD_FILE)

        if list(data.columns) != ["Date", "Mood"]:
            st.error("⚠️ Error: CSV headers are incorrect! Expected ['Date', 'Mood']")
            return pd.DataFrame(columns=["Date", "Mood"])
        
        return data
    except Exception as e:
        st.error(f"⚠️ Error reading CSV file: {e}")
        return pd.DataFrame(columns=["Date", "Mood"])  

def save_mood_data(date, mood):
    ensure_csv_headers() 

    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, mood]) 

st.title("Mood Tracker 😊")

today = datetime.date.today()

st.subheader("How are you feeling today?")
mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

if st.button("Log Mood"):
    save_mood_data(today, mood)
    st.success("✅ Mood Logged Successfully!")
    st.balloons()  

data = load_mood_data()

if not data.empty:
    st.subheader("Mood Trends Over Time")

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce") 

        mood_counts = data["Mood"].value_counts()

        st.bar_chart(mood_counts)
    else:
        st.error("⚠️ Error: 'Date' column not found in dataset!")
