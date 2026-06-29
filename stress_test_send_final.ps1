$CSV_PATH = "XPES_Customer_Assets/stress_test/max_leads.csv"
$USER_EMAIL = "miguelyang42@gmail.com"
$IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"
$CLI_PATH = "C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

$leads = Import-Csv $CSV_PATH

$count = 0
foreach ($lead in $leads) {
    if ($count -ge 50) { break }
    
    $name = $lead.Name
    $company = $lead.Company
    $business = $lead.Category
    $to = $lead.Email
    
    if (-not $to) { continue }

    $subject = "[Direct Factory] 4500V Solar Mosquito Technology for $company 2026 Lineup"
    
    $body = @"
<html>
<body>
<p>Hi $name,</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>I am writing to you regarding $company's leadership in $business.</p>
<p>We are a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>. I want to share our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for outdoor durability.</li>
</ul>
<p><img src="$IMAGE_URL" width="200" alt="Solar Mosquito Lamp"></p>
<p>Would you be open to a quick look at our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>
"@

    # Flatten body to single line to avoid batch file argument issues on Windows
    $body = $body -replace "`r`n", " " -replace "`n", " "
    
    Write-Host "Sending to $to ($name)..."
    
    # Ensure all arguments are quoted correctly
    & $CLI_PATH call send_gmail_message `
        --to "$to" `
        --subject "$subject" `
        --body "$body" `
        --body_format "html" `
        --user_google_email "$USER_EMAIL"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: $to"
        $count++
    } else {
        Write-Host "FAILED: $to"
    }
    
    Start-Sleep -Seconds 2
}

Write-Host "--- TEST COMPLETE ---"
Write-Host "Total Sent: $count"
