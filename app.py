# Load and test with actual files
import pandas as pd
import numpy as np

def normalize_data(value):
    if pd.isna(value):
        return value
    value = str(value).strip().replace('"', '')
    value = value.replace(',', '.').replace(' ', '')
    value = ''.join(c for c in value if c.isdigit() or c in '.-')
    try:
        return float(value)
    except:
        return np.nan

# Load files
df_wyscout = pd.read_excel('Search results (49) (1).xlsx')
df_physical = pd.read_csv('SkillCorner-2025-04-30.csv', sep=';', encoding='utf-8')
df_pressure = pd.read_csv('SkillCorner-2025-04-30 (1).csv', sep=';', encoding='utf-8')

# Clean WyScout data
df_wyscout['Player'] = df_wyscout['Player'].str.strip()

# Process SkillCorner files
for col in df_physical.columns:
    if col != 'Player':
        df_physical[col] = df_physical[col].apply(normalize_data)
        df_physical = df_physical.rename(columns={col: f"{col} (Physical Output)"})
df_physical['Player'] = df_physical['Player'].str.strip()

for col in df_pressure.columns:
    if col != 'Player':
        df_pressure[col] = df_pressure[col].apply(normalize_data)
        df_pressure = df_pressure.rename(columns={col: f"{col} (Overcoming Pressure)"})
df_pressure['Player'] = df_pressure['Player'].str.strip()

# Merge data
final_df = df_wyscout.copy()
final_df = final_df.merge(df_physical, on='Player', how='left')
final_df = final_df.merge(df_pressure, on='Player', how='left')

# Save merged data
final_df.to_excel('wyscout_skillcorner_merged.xlsx', index=False)

print("Preview of merged data:")
print(final_df.head())

print("\
Columns in final dataset:")
print(final_df.columns.tolist())

print("\
Statistics for SkillCorner metrics:")
skillcorner_cols = [col for col in final_df.columns if 'Physical Output' in col or 'Overcoming Pressure' in col]
print(final_df[skillcorner_cols].describe())
