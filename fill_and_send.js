(async () => {
  const to = document.querySelector('input[name="to"], textarea[name="to"], [aria-label="收件人"], [aria-label="To"]');
  const subject = document.querySelector('input[name="subjectbox"], [aria-label="主题"], [aria-label="Subject"]');
  const body = document.querySelector('[role="textbox"][aria-label="邮件正文"], [role="textbox"][aria-label="Message Body"]');
  
  if (!to || !subject || !body) {
    return { error: 'Fields not found', to: !!to, subject: !!subject, body: !!body };
  }

  to.value = 'tahlie.hodson@kmart.com.au';
  to.dispatchEvent(new Event('input', { bubbles: true }));
  to.dispatchEvent(new Event('change', { bubbles: true }));

  subject.value = '[Innovation] 4500V Solar Mosquito Technology for Kmart Australia';
  subject.dispatchEvent(new Event('input', { bubbles: true }));
  subject.dispatchEvent(new Event('change', { bubbles: true }));

  body.innerHTML = `Hi Tahlie Hodson,<br><br>I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light.<br><br>I am writing to you regarding Kmart Australia's leadership in General Merchandise and your commitment to outdoor living solutions.<br><br>We are a pioneer factory in Solar Mosquito Killer Lamps since 2020. I want to share our 2026 4500V Industrial-Grade Solar Model. It provides the same killing power as traditional AC grid units with Zero Electricity Cost.<br><br>Performance Highlights:<br>- 4500V High-Voltage Grid: Consistent industrial-grade kill power.<br>- 3-Day Battery Backup: Optimized for cloudy weather performance.<br>- IP65 Waterproofing: Perfect for extreme outdoor durability.<br><br>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.<br><br>Best regards,<br><br>Miguel Yang<br>Business Development Manager<br>Guangdong Xingpu Energy Saving Light`;
  body.dispatchEvent(new Event('input', { bubbles: true }));

  // Wait a bit for UI to catch up
  await new Promise(r => setTimeout(r, 1000));

  const sendBtn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText.includes('发送') || b.innerText.includes('Send'));
  if (sendBtn) {
    sendBtn.click();
    return { success: true };
  }
  return { error: 'Send button not found' };
})()