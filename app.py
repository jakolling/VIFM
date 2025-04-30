
import streamlit as st
import pandas as pd
import io
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Merger App", layout="wide")

def load_and_process_data(physical_file, pressure_file, wyscout_file):
    # Load data
    df_physical = pd.read_csv(physical_file, sep=';', encoding='utf-8')
    df_pressure = pd.read_csv(pressure_file, sep=';', encoding='utf-8')
    df_wyscout = pd.read_excel(wyscout_file, engine='openpyxl')
    
    # Clean column names
    df_physical.columns = df_physical.columns.str.replace('"', '').str.strip()
    df_pressure.columns = df_pressure.columns.str.replace('"', '').str.strip()
    
    # Merge data
    df_skillcorner = pd.merge(df_physical, df_pressure, on='Player', how='outer')
    
    if 'Player' in df_wyscout.columns:
        final_df = pd.merge(df_skillcorner, df_wyscout, on='Player', how='outer')
    else:
        final_df = pd.merge(df_skillcorner, df_wyscout, 
                          left_on='Player', 
                          right_on=df_wyscout.columns[0], 
                          how='outer')
    
    return final_df

def main():
    st.title('Football Data Merger')
    st.sidebar.title('Upload Files')
    
    # File uploaders
    physical_file = st.sidebar.file_uploader('Physical Output Data (CSV)', type='csv')
    pressure_file = st.sidebar.file_uploader('Pressure Data (CSV)', type='csv')
    wyscout_file = st.sidebar.file_uploader('WyScout Data (XLSX)', type='xlsx')
    
    if all([physical_file, pressure_file, wyscout_file]):
        try:
            final_df = load_and_process_data(physical_file, pressure_file, wyscout_file)
            
            # Data Preview
            st.header('Data Preview')
            st.dataframe(final_df.head())
            
            # Basic Stats
            st.header('Basic Statistics')
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric('Total Players', len(final_df))
            with col2:
                st.metric('Total Features', len(final_df.columns))
            
            # Export Options
            st.header('Export Data')
            
            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name='Merged Data')
            
            output.seek(0)
            st.download_button(
                label='Download Excel File',
                data=output,
                file_name='merged_football_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            st.error(f'Error processing data: {str(e)}')
    else:
        st.info('Please upload all required files to begin.')

if __name__ == '__main__':
    main()
