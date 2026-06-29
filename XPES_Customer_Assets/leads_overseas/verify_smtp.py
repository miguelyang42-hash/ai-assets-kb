import smtplib
import dns.resolver
import sys

def verify_email(email):
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = sorted(records, key=lambda r: r.preference)[0].exchange.to_text()
        
        server = smtplib.SMTP(timeout=5)
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True, "Success"
        else:
            return False, f"SMTP Error {code}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    emails = [
        "angela.adams@homedepot.com", "melissa.major@homedepot.com", "Arely.Guzman0@walmart.com",
        "Carrie.Mack@walmart.com", "Samantha.Raguso@walmart.com", "sutke@thermacell.net",
        "rillsley@thermacell.net", "kyle.robinson@pelsis.com", "billy_bastek@homedepot.com",
        "cristan.humeston@lowes.com", "todd.griebe@target-specialty.com", "jim.hodge@target-specialty.com",
        "mike.ross@target-specialty.com", "paola.montgomery@target-specialty.com", "jeremy.ray@lowes.com",
        "john.thajer@canadiantire.ca", "kristen.coenen@canadiantire.ca", "karen.fuoco@canadiantire.ca",
        "rashi_gupta@homedepot.com", "chris.jacques@wickes.co.uk", "lewis.janes@wickes.co.uk",
        "mike.alcock@diy.com", "paul.fogg@kingfisher.com", "dan.aumann@pelsis.com",
        "lee.smith@pelsis.com", "fleur.lloan@leroymerlin.fr", "elena.shatalova@leroymerlin.fr",
        "francois.noel@castorama.fr", "thomas.pasquesoone@castorama.fr", "vadim.chernov@obi.de",
        "katrin.beyer@obi.de", "frank.feiertag@obi.de", "timm.trautz@bauhaus.info",
        "melanie.stier@bauhaus.info", "monika.baesel@hornbach.com", "chantal.mohr@hornbach.com"
    ]
    for email in emails:
        ok, msg = verify_email(email)
        print(f"{email},{ok},{msg}")
