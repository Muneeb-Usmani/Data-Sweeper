import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Layout of Data Sweeper
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background-color: #F8F9FA; }
    .title { text-align: center; font-size: 36px; font-weight: bold; color: #003366; }
    .subtitle { text-align: center; font-size: 18px; color: #666; }
    .block-container { padding-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 class='title'>📊 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Transform your files between CSV and Excel formats with built-in data cleaning and visualization!</p>", unsafe_allow_html=True)


# Sidebar for File Upload
st.sidebar.header("📂 Upload Your Files")
uploaded_files = st.sidebar.file_uploader("Upload CSV or Excel:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format: {file_ext}")
            continue


        # Display File Info
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: #fff;">
            <b>📄 File Name:</b> {file.name}<br>
            <b>📏 File Size:</b> {round(file.size / 1024, 2)} KB
        </div>
        """, unsafe_allow_html=True)


        # Show Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df, height=300)  


        #Data Cleaning
        st.subheader("🛠 Data Cleaning Options")

        if st.checkbox(f"🧹 Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates ({file.name})", use_container_width=True):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed Successfully!")

            with col2:
                if st.button(f"🛠 Fill Missing Values ({file.name})", use_container_width=True):
                    with st.spinner("Filling missing values..."):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled Successfully!")


        #Choose Specific Cloumns to Keep or Convert
        with st.expander(f"🎯 Select Columns to Convert ({file.name})", expanded=True):
            columns = st.multiselect("Choose Columns:", df.columns, default=df.columns)
            df = df[columns]


        #Visualization of Data
        st.subheader("📊 Data Visualization")

        if st.checkbox(f"📈 Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2], use_container_width=True)


        #Convert File from CSV to Excel
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            with st.spinner("Converting file..."):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)


            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
                use_container_width=True
            )

            st.success("✅ All Files Processed!")


# Footer Section
st.markdown(
    """
    <style>
    .footer {
        position: absolute;
        top: 100%;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: #666;
        background-color: #F8F9FA;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
        © 2025 Muneeb Usmani. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)