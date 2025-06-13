import streamlit as st
import pandas as pd
import os

FILE_NAME = "visa_data.csv"

# Load existing data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["Name", "Passport No", "Visa Type", "Status", "Submission Date", "Appointment Date", "Notes"])

st.title("🛂 Visa Case Tracker - Wadan Air Travels")

# Input fields
name = st.text_input("Client Name")
passport_no = st.text_input("Passport Number")
visa_type = st.selectbox("Visa Type", ["Visit", "Work", "Student", "Other"])
status = st.selectbox("Visa Status", ["Applied", "Under Process", "Approved", "Rejected"])
submission_date = st.date_input("File Submission Date")
appointment_date = st.date_input("Embassy Appointment Date")
notes = st.text_area("Notes")

if st.button("Add Record"):
    new_row = {
        "Name": name,
        "Passport No": passport_no,
        "Visa Type": visa_type,
        "Status": status,
        "Submission Date": submission_date,
        "Appointment Date": appointment_date,
        "Notes": notes
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.success("Record added!")

# Filter section
st.subheader("Filter Records")
filter_status = st.selectbox("Filter by Visa Status", ["All"] + df["Status"].unique().tolist())
filter_visa = st.selectbox("Filter by Visa Type", ["All"] + df["Visa Type"].unique().tolist())

filtered_df = df
if filter_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == filter_status]
if filter_visa != "All":
    filtered_df = filtered_df[filtered_df["Visa Type"] == filter_visa]

st.table(filtered_df)

# Download button
st.download_button("Download Data as CSV", df.to_csv(index=False), file_name='visa_data_download.csv')

st.subheader("Search by Passport Number")
search_passport = st.text_input("Enter Passport Number to Search")
if search_passport:
    result_df = df[df["Passport No"] == search_passport]
    if not result_df.empty:
        st.table(result_df)
    else:
        st.warning("No record found with this passport number.")

# Delete record (by passport no)
st.subheader("Delete Record")
del_passport = st.text_input("Enter Passport Number to Delete")
if st.button("Delete"):
    df = df[df["Passport No"] != del_passport]
    df.to_csv(FILE_NAME, index=False)
    st.success("Record deleted (if passport matched).")
