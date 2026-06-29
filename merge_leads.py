import pandas as pd
import glob
import os

base_dir = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets"
output_path = os.path.join(base_dir, "XPES_Master_Leads_Database.csv")

# Standard headers required by user
STANDARD_COLS = ["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"]

# Map various formats to standard
def get_standardized_df(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except:
        df = pd.read_csv(file_path, encoding='latin1')
    
    # Simple mapping logic
    rename_map = {
        'Company': 'Company Name',
        'Name': 'Responsible Person',
        'Category': 'Main Business',
        'Country': 'Relevance' # Storing country in relevance for now
    }
    df = df.rename(columns=rename_map)
    
    # Ensure all columns exist
    for col in STANDARD_COLS:
        if col not in df.columns:
            df[col] = ""
            
    return df[STANDARD_COLS]

all_dfs = []

# List all csv files in Assets and subdirectories
csv_files = glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True)

for f in csv_files:
    if "Master" in f: continue
    print(f"Merging {f}...")
    all_dfs.append(get_standardized_df(f))

if all_dfs:
    master_df = pd.concat(all_dfs, ignore_index=True)
    # Deduplicate by email
    master_df = master_df.drop_duplicates(subset=['Email'], keep='last')
    master_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Successfully created Master Database with {len(master_df)} unique leads.")
else:
    print("No leads found to merge.")
