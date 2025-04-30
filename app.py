
import streamlit as st
import pandas as pd
import io

def add_source_columns(df, source):
    return df.add_suffix(f' ({source})')

def main():
    st.title('WyScout + SkillCorner Data Merger')
    
    wyscout_file = st.file_uploader('WyScout Data (XLSX)', type='xlsx')
    physical_file = st.file_uploader('SkillCorner Physical Output (CSV)', type='csv')
    pressure_file = st.file_uploader('SkillCorner Overcoming Pressure (CSV)', type='csv')
    
    if wyscout_file:
        try:
            df_wyscout = pd.read_excel(wyscout_file)
            player_col = df_wyscout.columns[0]
            df_wyscout = df_wyscout.rename(columns={player_col: 'Player'})
            
            if physical_file:
                df_physical = pd.read_csv(physical_file, sep=';')
                df_physical.columns = df_physical.columns.str.replace('"', '').str.strip()
                physical_cols = df_physical.columns.difference(['Player'])
                df_physical_tagged = df_physical[physical_cols].add_suffix(' (Physical Output)')
                df_physical = pd.concat([df_physical['Player'], df_physical_tagged], axis=1)
                
            if pressure_file:
                df_pressure = pd.read_csv(pressure_file, sep=';')
                df_pressure.columns = df_pressure.columns.str.replace('"', '').str.strip()
                pressure_cols = df_pressure.columns.difference(['Player'])
                df_pressure_tagged = df_pressure[pressure_cols].add_suffix(' (Overcoming Pressure)')
                df_pressure = pd.concat([df_pressure['Player'], df_pressure_tagged], axis=1)
            
            final_df = df_wyscout.copy()
            
            if physical_file:
                final_df = final_df.merge(df_physical, on='Player', how='left')
            if pressure_file:
                final_df = final_df.merge(df_pressure, on='Player', how='left')
            
            st.write('Data Preview:')
            st.dataframe(final_df.head())
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False)
            output.seek(0)
            
            st.download_button(
                label='Download Merged Data',
                data=output,
                file_name='wyscout_skillcorner_merged.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            st.error(f'Error: {str(e)}')
    else:
        st.info('Please upload WyScout file to begin')

if __name__ == '__main__':
    main()
