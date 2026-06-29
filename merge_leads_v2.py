import csv
import glob
import os

base_dir = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets"
output_path = os.path.join(base_dir, "XPES_Master_Leads_Database.csv")

STANDARD_COLS = ["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"]

# Field mapping for common variations
MAPPING = {
    'Company': 'Company Name',
    'Name': 'Responsible Person',
    'Category': 'Main Business',
    'Country': 'Relevance'
}

master_records = {} # Use Email as key for deduplication

csv_files = glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True)

for f_path in csv_files:
    if "Master" in f_path: continue
    print(f"Reading {f_path}...")
    
    try:
        with open(f_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                standard_row = {col: "" for col in STANDARD_COLS}
                
                # Copy values with mapping
                for key, val in row.items():
                    target_key = MAPPING.get(key, key)
                    if target_key in STANDARD_COLS:
                        standard_row[target_key] = val
                
                email = standard_row.get("Email", "").strip().lower()
                if email:
                    master_records[email] = standard_row
    except Exception as e:
        print(f"Error reading {f_path}: {e}")

# Write to Master
with open(output_path, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=STANDARD_COLS)
    writer.writeheader()
    for email in sorted(master_records.keys()):
        writer.writerow(master_records[email])

print(f"Successfully created Master Database at {output_path} with {len(master_records)} unique records.")
