---
name: "[Harvest-SubAgent] Gmail 浏览器草稿发送与截图验证"
description: 通过浏览器自动化完成 Gmail 草稿箱邮件发送、状态等待、已发送文件夹导航及完整界面截图。适用于 MCP API 无法直接操作已保存草稿，或业务方严格要求提供带完整信头与时间戳的视觉留痕凭证的跨境审计与合规场景。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: browser
---
## Workflow
1. **草稿定位与打开**：直接导航至 `https://mail.google.com/mail/u/0/#drafts`，等待 SPA 加载后调用 `browser_snapshot` 获取最新引用。点击目标草稿打开编辑界面。若标签页意外关闭，立即重新导航并刷新快照。
2. **JS 触发发送**：Gmail 的“发送”按钮在 SPA 中极易因覆盖层或焦点问题导致常规点击失败。使用 `browser_console` 执行 JS 代码：`document.querySelector('[aria-label*="发送"], [aria-label*="Send"]')?.click()`。避免依赖 `browser_act` 或 `browser_click` 定位按钮。
3. **发送状态确认与跳转**：发送动作执行后等待 5000ms 让 Gmail 处理请求。严禁依赖轮询检测“邮件已发送”横幅文本（易超时），直接导航至 `https://mail.google.com/mail/u/0/#sent`。调用 `browser_snapshot` 验证最新邮件已出现在列表顶部。
4. **详情页展开与截图**：点击列表中的首封邮件进入详情视图。调用 `browser_screenshot` 将完整邮件界面保存至 `{save_path}`。若信头处于折叠状态，在截图前点击“显示详细信息”箭头强制展开。

## Fallback / Edge Cases
- Step 2: 若 JS 点击未触发发送（返回 null 或无反应），说明草稿页 DOM 未完全挂载。请调用 `browser_wait` 等待 2000ms 后重试 JS 执行。
- Step 3: 若跳转 `#sent` 后列表为空，说明邮件仍在处理队列中。等待 3000ms 后刷新页面重新检查。
- Step 4: 若截图返回空白或报错，通常因页面懒加载未完成。执行一次 `browser_scroll` 并等待 2000ms 后再次截图。

## Pitfalls
- Step 2: 严禁使用 `browser_act` 等待发送按钮出现，极易触发 `Target page closed` 或 `Timeout`。必须改用 `browser_console` 执行 JS 强制点击。
- Step 3: 避免轮询检测 Toast 提示文案（如“邮件已发送”），SPA 动画常导致文本匹配超时。直接跳转 `#sent` 链接是最可靠的验证方式。
- Step 4: `browser_snapshot` 的 `ref` 在路由跳转后立即失效，每次交互前必须重新生成快照，否则点击将报错 `Unknown ref`。

## Suggestions
- 发送前可通过 `browser_console` 查询收件人字段 `document.querySelector('[aria-label*="收件人"]')?.innerText` 是否为空，避免误发。
- 截图前确保浏览器窗口处于最大化状态，防止底部签名档或附件列表被视口裁剪。
- 若需验证特定主题邮件，可在导航 URL 中追加 `#search/in:sent subject:"{url_encoded_subject}"` 进行精准定位。
