import subprocess
import json
import time

cli = r'C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd'
user_email = "miguelyang42@gmail.com"

leads = [
    {"to": "james.kearney@bcf.com.au", "name": "James Kearney", "company": "BCF (Super Retail Group)", "biz": "Camping/Outdoor Gear Brand", "country": "Australia"},
    {"to": "monique.holmes@bcf.com.au", "name": "Monique Holmes", "company": "BCF (Super Retail Group)", "biz": "Camping/Outdoor Gear Brand", "country": "Australia"},
    {"to": "naji.alsalem@sherwoodpst.com", "name": "Naji Alsalem", "company": "Sherwood Middle East", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "hassan.motawig@sherwoodpst.com", "name": "Hassan Motawig", "company": "Sherwood Middle East", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "ahmad.alnajem@sherwoodpst.com", "name": "Ahmad Alnajem", "company": "Sherwood Middle East", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "firos@ecovargroup.com", "name": "Firos Ambarath", "company": "Ecovar Group", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "sajith@ecovargroup.com", "name": "Sajith Narayanan", "company": "Ecovar Group", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "santosh.sonar@danubehome.com", "name": "Santosh Sonar", "company": "Danube Home", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "imthiyas.ali@luluuae.com", "name": "Imthiyas Ali", "company": "Lulu Group International", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "uday.rao@luluuae.com", "name": "Uday Raghavendra Rao", "company": "Lulu Group International", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "aneesh.ks@luluuae.com", "name": "Aneesh KS", "company": "Lulu Group International", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "ajay.othayoth@luluuae.com", "name": "Ajay Kumar Othayoth", "company": "Lulu Group International", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "hasil.hasil@luluuae.com", "name": "Hasil Hasil", "company": "Lulu Group International", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "sami.chiha@sherwoodpst.com", "name": "Sami Chiha", "company": "Sherwood Middle East", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "sakher@sherwoodpst.com", "name": "Sakher Abu Ghaze", "company": "Sherwood Middle East", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "m.junaid@ecovargroup.com", "name": "Mohammad Junaid", "company": "Ecovar Group", "biz": "Specialized Pest Control Distributor", "country": "UAE"},
    {"to": "arafayy@amazon.ae", "name": "Abdul Rafay", "company": "Amazon UAE", "biz": "Retailer Private Label", "country": "UAE"},
    {"to": "joshua.clouser@snowpeak.com", "name": "Josh Clouser", "company": "Snow Peak", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "sarah.peak@snowpeak.com", "name": "Sarah Peak", "company": "Snow Peak", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "kyle.wakayama@snowpeak.com", "name": "Kyle Wakayama", "company": "Snow Peak", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "m.andersen@snowpeak.com", "name": "Michael Andersen", "company": "Snow Peak", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "noah.reis@snowpeak.com", "name": "Noah Reis", "company": "Snow Peak", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "mai.mizuno@decathlon.com", "name": "Mai Mizuno", "company": "Decathlon Japan", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "s.yamamoto@ichijo.co.jp", "name": "Shinsuke Yamamoto", "company": "Ichijo", "biz": "Specialized Pest Control Distributor", "country": "Japan"},
    {"to": "m.ishiko@spp.co.jp", "name": "Masaaki Ishiko", "company": "Sumitomo Precision Products", "biz": "Specialized Pest Control Distributor", "country": "Japan"},
    {"to": "i.tatsuno@montbell.jp", "name": "Isamu Tatsuno", "company": "Mont-bell", "biz": "Camping/Outdoor Gear Brand", "country": "Japan"},
    {"to": "mogan@fumakilla.com.my", "name": "Mogan Sinniah", "company": "Fumakilla", "biz": "Specialized Pest Control Distributor", "country": "Japan"},
    {"to": "carl.lee@emart.com", "name": "Carl Lee", "company": "Emart Inc.", "biz": "Retailer Private Label", "country": "South Korea"},
    {"to": "joosang.park@emart.com", "name": "Joosang Park", "company": "Emart America", "biz": "Retailer Private Label", "country": "South Korea"},
    {"to": "juntak.do@emart.com", "name": "Juntak Do", "company": "Emart HQ (Strategic Leader)", "biz": "Retailer Private Label", "country": "South Korea"},
    {"to": "jisun.baek@emart.com", "name": "Baek Jisun", "company": "Emart (Global Procurement)", "biz": "Retailer Private Label", "country": "South Korea"},
    {"to": "rachel.lee@emart.com", "name": "Rachel Lee", "company": "Emart Inc.", "biz": "Retailer Private Label", "country": "South Korea"},
    {"to": "sae.moon@helinox.com", "name": "Sae Moon", "company": "Helinox", "biz": "Camping/Outdoor Gear Brand", "country": "South Korea"},
    {"to": "ted.ganio@helinox.com", "name": "Ted Ganio", "company": "Helinox", "biz": "Camping/Outdoor Gear Brand", "country": "South Korea"},
    {"to": "young.lah@helinox.com", "name": "Young Lah", "company": "Helinox", "biz": "Camping/Outdoor Gear Brand", "country": "South Korea"},
    {"to": "truong.huynh@helinox.com", "name": "Huynh Anh Truong", "company": "Helinox", "biz": "Camping/Outdoor Gear Brand", "country": "South Korea"},
    {"to": "suk.kim@helinox.com", "name": "Kim Suk", "company": "Helinox", "biz": "Camping/Outdoor Gear Brand", "country": "South Korea"}
]

template = """<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I noticed {company}'s leadership in {biz} within the {country} market, and I am reaching out with a breakthrough for your 2026 lineup.</p>

<p>As a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>, we have just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for extreme outdoor durability.</li>
</ul>

<p>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.</p>

<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

for lead in leads:
    body = template.format(name=lead['name'], company=lead['company'], biz=lead['biz'], country=lead['country'])
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {lead['company']} ({lead['country']})"
    
    payload = {
        "to": lead['to'],
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": user_email
    }
    
    print(f"Sending to {lead['to']}...")
    res = subprocess.run([cli, 'call', 'send_gmail_message', '--json', json.dumps(payload)], capture_output=True, text=True)
    print(f"Result: {res.stdout} {res.stderr}")
    time.sleep(1)
