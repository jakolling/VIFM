import streamlit as st  
import pandas as pd  
import io  
  
def main():  
    st.title('Football Data Merger')  
      
    # File uploaders  
    physical_file = st.file_uploader('Physical Output Data (CSV)', type='csv')  
    pressure_file = st.file_uploader('Pressure Data (CSV)', type='csv')  
    wyscout_file = st.file_uploader('WyScout Data (XLSX)', type='xlsx')  
      
    if all([physical_file, pressure_file, wyscout_file]):  
        try:  
            # Load data  
            df_physical = pd.read_csv(physical_file, sep=';', encoding='utf-8')  
            df_pressure = pd.read_csv(pressure_file, sep=';', encoding='utf-8')  
            df_wyscout = pd.read_excel(wyscout_file)  
              
            # Clean column names  
            df_physical.columns = df_physical.columns.str.replace('\"', '').str.strip()  
            df_pressure.columns = df_pressure.columns.str.replace('\"', '').str.strip()  
              
            # Merge data  
            df_skillcorner = pd.merge(df_physical, df_pressure, on='Player', how='outer')  
            final_df = pd.merge(df_skillcorner, df_wyscout,   
                              left_on='Player',   
                              right_on=df_wyscout.columns[0],   
                              how='outer')  
              
            # Show preview  
            st.write('Data Preview:')  
            st.dataframe(final_df.head())  
              
            # Export button  
            output = io.BytesIO()  
            with pd.ExcelWriter(output, engine='openpyxl') as writer:  
                final_df.to_excel(writer, index=False)  
            output.seek(0)  
              
            st.download_button(  
                label='Download Merged Data',  
                data=output,  
                file_name='merged_football_data.xlsx',  
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  
            )  
              
        except Exception as e:  
            st.error(f'Error: {str(e)}')  
    else:  
        st.info('Please upload all required files.')  
  
if __name__ == '__main__':  
    main()  
