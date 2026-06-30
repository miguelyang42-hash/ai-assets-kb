$recipients = @(
    @{ name = "Tahlie Hodson"; email = "tahlie.hodson@kmart.com.au"; company = "Kmart Australia" },
    @{ name = "Maihemuti Keremu"; email = "m-keremu@komeri.bit.or.jp"; company = "KOMERI Japan" },
    @{ name = "Tony Lee"; email = "tony.lee@emart.com"; company = "EMART South Korea" },
    @{ name = "Freddie Lim"; email = "freddie.lim@fairprice.com.sg"; company = "NTUC Fairprice" },
    @{ name = "Adam Baker"; email = "adam.baker@superretailgroup.com.au"; company = "BCF Australia" },
    @{ name = "Joshua Strickland"; email = "joshua.strickland@superretailgroup.com.au"; company = "BCF Australia" },
    @{ name = "Henry Murning"; email = "henry.murning@superretailgroup.com.au"; company = "BCF Australia" },
    @{ name = "Jonny Wears"; email = "jonny.wears@superretailgroup.com.au"; company = "BCF Australia" },
    @{ name = "Matt Behan"; email = "matt.behan@bcf.com.au"; company = "BCF Australia" }
)

$user_email = "miguelyang42@gmail.com"

foreach ($r in $recipients) {
    $subject = "[Innovation] 4500V Solar Mosquito Technology for $($r.company)"
    $body = @"
<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi $($r.name),</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've released our 2026 4500V model with Zero Electricity Cost.</p>
<p>Highlights: <b>4500V Grid</b>, <b>3-Day Battery</b>, <b>IP65 Waterproof</b>.</p>
<p>Would you be open to our 2026 Catalog? Just reply "YES".</p>
<br>
<p>Best regards,<br>
<b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body></html>
"@

    Write-Host "Sending to $($r.email)..."
    accio-mcp-cli call send_gmail_message --key to --val $r.email --key subject --val $subject --key body --val $body --key user_google_email --val $user_email --key body_format --val html
    Write-Host "Done."
}
