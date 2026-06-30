import csv
import os

MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"
BOUNCED_EMAILS = [
    "mike.alcock@diy.com", "mliu@miloenterprises.com", "sourcing@scotts.com.au",
    "m.thibaut@mr-bricolage.com", "monika.baesel@hornbach.com", "frank.feiertag@obi.de",
    "vadim.chernov@obi.de", "anton.bezbokov@castorama.fr", "ignacio.villares@leroymerlin.fr",
    "catalin.lene@leroymerlin.fr", "alain.ryckeboer@leroymerlin.fr", "francois.noel@castorama.fr",
    "elena.shatalova@leroymerlin.fr", "sjassal@bunnings.com.au", "jweinstein@woodstream.com",
    "cfowler@target-specialty.com", "matthew.henriksen@stvuk.com", "ykim@homeplus.co.kr",
    "aeo@homeplus.co.kr", "mahmood.obaid@saco-ksa.com", "frederique.mussat-broussard@leroymerlin.fr",
    "olga.ponadtsova@obi.de", "montaser.abdullah@saco-ksa.com", "m.nabaa@saco-ksa.com",
    "anna.hosszu@procurementservices.co.uk", "karen.fillingham@procurementservices.co.uk",
    "contacto@pestweb.com", "info@kombatstore.com", "support@langy-energy.com"
]

def force_update():
    try:
        # Read everything into memory first
        data = []
        headers = []
        with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                email = row.get("Email", "").strip().lower()
                if email in [e.lower() for e in BOUNCED_EMAILS]:
                    row["Status"] = "Invalid (Bounced)"
                data.append(row)
        
        # Write to a NEW file to avoid locking issues during write
        NEW_CSV = MASTER_CSV.replace(".csv", "_Updated.csv")
        with open(NEW_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Created updated database at: {NEW_CSV}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

force_update()
