---
name: "[Harvest-SubAgent] Gmail 浏览器截图验证"
description: 通过浏览器自动化对 Gmail 已发送邮件进行视觉验证并精准截图。适用于跨境业务中需要提供邮件收发凭证、展示完整信头（含收件人、签名档、正文图片）但程序化 API 无法满足合规格式要求的场景。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: browser
---
## Workflow
1. **浏览器状态恢复与直链导航**：检查浏览器活跃标签页，若目标页签已关闭或断开，先确认状态后直接导航至 URL：`https://mail.google.com/mail/u/0/#search/in:sent%20subject%3A%22{url_encoded_subject}%22`。此直链方式可绕过 Gmail SPA 搜索框的焦点丢失和输入超时问题。
2. **动态 DOM 快照与邮件展开**：等待 2000ms 确保单页应用路由渲染完成后，调用 `browser_snapshot` 获取最新交互引用。点击匹配邮件进入详情页。若信头处于折叠状态，定位并点击“显示详细信息”箭头，强制展开完整收件人列表与签名档。
3. **元素渲染控制台校验**：调用 `browser_console` 执行轻量级 JS 验证（如查询 `.gmail_signature` 或 `.gD` 容器的 `innerText`）。若返回空值，说明页面懒加载未完成，执行一次 `browser_scroll` 并等待 2000ms 后重试。
4. **视觉截图与异常重试**：调用 `browser_screenshot` 将当前视口保存至 `{save_path}`。若捕获到“Target page closed”或上下文丢失错误，立即重开标签页并重新导航，最多重试 2 次。

## Suggestions
- 若只需验证文本内容而非视觉排版，优先使用 `browser_console` 提取数据，比截图更稳定。
- 在导航 URL 中显式加入 `in:sent` 前缀可严格限定搜索范围，排除草稿箱或垃圾邮件干扰。
- 截图前确保浏览器窗口处于最大化状态，避免关键信头元素被视口边缘裁剪。

## Fallback / Edge Cases
- Step 2: 若目标邮件位于非主视图区域导致直链展开失败，可在搜索词后追加 `label:all` 参数扩大检索域。
- Step 3: 图片附件若持续显示为占位符，通常是网络延迟或登录态过期。需检查页面是否弹出重新登录提示，并手动完成验证。

## Pitfalls
- Step 1: 严禁使用 `browser_type` 向 Gmail 搜索框输入长标题，极易因覆盖层导致 `locator.fill timeout`。必须使用参数直链。
- Step 2: Gmail 的交互引用 (`ref`) 在路由跳转后会瞬间失效，每次点击前必须重新生成快照。
- Step 4: 截图报错“Target page closed”通常由内存溢出引起，重试前需关闭闲置标签页释放资源。
