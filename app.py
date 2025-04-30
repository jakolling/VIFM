import streamlit as st  
import pandas as pd  
from io import BytesIO  
import time  
  
# Page config  
st.set_page_config(  
    page_title="CSV to Excel Converter",  
    page_icon="📊",  
    layout="wide"  
)  
  
# Custom CSS  
st.markdown('''  
<style>  
    .main {  
        padding: 2rem;  
    }  
    .stButton>button {  
        width: 100%;  
        height: 3em;  
        background-color: #4CAF50;  
        color: white;  
        border-radius: 10px;  
        border: none;  
        margin: 10px 0;  
    }  
    .stButton>button:hover {  
        background-color: #45a049;  
    }  
    .css-1d391kg {  
        padding: 2rem 1rem;  
    }  
    .upload-text {  
        text-align: center;  
        padding: 20px;  
    }  
    .stProgress > div > div > div > div {  
        background-color: #4CAF50;  
    }  
</style>  
''', unsafe_allow_html=True)  
  
def convert_df_to_excel(df):  
    output = BytesIO()  
    with pd.ExcelWriter(output, engine='openpyxl') as writer:  
        df.to_excel(writer, index=False)  
    processed_data = output.getvalue()  
    return processed_data  
  
def main():  
    st.title("📊 CSV to Excel Converter")  
    st.markdown("---")  
  
    # Sidebar  
    with st.sidebar:  
        st.header("Settings")  
        preview_rows = st.slider("Preview Rows", 5, 50, 10)  
        st.markdown("---")  
        st.markdown("### Instructions")  
        st.markdown("1. Upload your CSV file(s) (semicolon-separated).")  
        st.markdown("2. Preview the data")  
        st.markdown("3. Download as Excel")  
  
    # Main content  
    uploaded_files = st.file_uploader(  
        "Upload your CSV files",  
        type=['csv'],  
        accept_multiple_files=True  
    )  
  
    if uploaded_files:  
        for uploaded_file in uploaded_files:  
            st.markdown(f"### Processing: {uploaded_file.name}")  
              
            try:  
                # Progress bar  
                progress_bar = st.progress(0)  
                for i in range(100):  
                    time.sleep(0.01)  
                    progress_bar.progress(i + 1)  
  
                # Read CSV using semicolon as separator  
                df = pd.read_csv(uploaded_file, sep=';')  
                  
                col1, col2, col3 = st.columns(3)  
                with col1:  
                    st.metric("Total Rows", len(df))  
                with col2:  
                    st.metric("Total Columns", len(df.columns))  
                with col3:  
                    st.metric("File Size", f"{uploaded_file.size/1024:.2f} KB")  
  
                # Data preview  
                st.subheader("Data Preview")  
                st.dataframe(df.head(preview_rows))  
  
                # Column info  
                st.subheader("Column Information")  
                col_info = pd.DataFrame({  
                    'Column Name': df.columns,  
                    'Data Type': df.dtypes,  
                    'Non-Null Count': df.count(),  
                    'Null Count': df.isnull().sum()  
                })  
                st.dataframe(col_info)  
  
                # Convert and download  
                excel_data = convert_df_to_excel(df)  
                  
                st.download_button(  
                    label="📥 Download Excel File",  
                    data=excel_data,  
                    file_name=uploaded_file.name.replace('.csv', '.xlsx'),  
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  
                )  
                  
                st.success(f"✅ {uploaded_file.name} processed successfully!")  
                st.markdown("---")  
  
            except Exception as e:  
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")  
                continue  
  
    else:  
        st.info("👆 Please upload your CSV file(s) to begin conversion")  
  
if __name__ == "__main__":  
    main()  
