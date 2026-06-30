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
    $body = "Hi $($r.name),

I am **Miguel Yang**, Business Development Manager at **Guangdong Xingpu Energy Saving Light**.

As a pioneer in Solar Mosquito Killer Lamps since 2020, we've released our 2026 4500V model with Zero Electricity Cost.

Highlights: 4500V Grid, 3-Day Battery, IP65 Waterproof.

Would you be open to our 2026 Catalog? Just reply 'YES'.

Best regards,
**Miguel Yang**
Business Development Manager
**Guangdong Xingpu Energy Saving Light**"

    # Escape the body for JSON
    $body_json = $body -replace '"', '\"' -replace "`n", '\n' -replace "`r", ''
    $json = "{`"to`": `"$($r.email)`", `"subject`": `"$subject`", `"body`": `"$body_json`", `"user_google_email`": `"$user_email`", `"body_format`": `"plain`"}"

    Write-Host "Sending to $($r.email)..."
    accio-mcp-cli call send_gmail_message --json $json
    Write-Host "Done."
}
