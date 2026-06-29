$USER_EMAIL = "miguelyang42@gmail.com"
$IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"
$CLI_PATH = "C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
$CSV_PATH = "C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_overseas\leads_50.csv"

$leads = Import-Csv $CSV_PATH

$count = 0
foreach ($lead in $leads) {
    $to = $lead.Email
    $name = $lead.Name
    $company = $lead.Company
    $business = $lead.Category
    $country = $lead.Country
    
    if (-not $to) { continue }

    # Subject with specific focus on 2026 Innovation
    $subject = "[Innovation] 4500V Solar Mosquito Technology for $company ($country)"
    
    # Gold Standard Body
    $body = @"
<html>
<body style="font-family: Arial; font-size: 14px;">
<p>Hi $name,</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>I am writing to you regarding $company's leadership in $business within the $country market.</p>
<p>As a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>, we have just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It matches the killing power of traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
<p><b>Key Innovations:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Engineered for extreme outdoor environments.</li>
</ul>
<p><img src="$IMAGE_URL" width="300" alt="Product Image"></p>
<p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>
"@

    # Flatten body to single line
    $flatBody = $body -replace "`r`n", " " -replace "`n", " "

    Write-Host "Sending to $to ($name)..."
    
    # Invoke command
    & $CLI_PATH call send_gmail_message `
        --to "$to" `
        --subject "$subject" `
        --body "$flatBody" `
        --body_format "html" `
        --user_google_email "$USER_EMAIL"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: $to"
        $count++
    } else {
        Write-Host "FAILED: $to"
    }
    
    # 3s delay for 50 emails to maintain account health
    Start-Sleep -Seconds 3
}

Write-Host "--- OVERSEAS ROUND COMPLETE: $count SENT ---"
