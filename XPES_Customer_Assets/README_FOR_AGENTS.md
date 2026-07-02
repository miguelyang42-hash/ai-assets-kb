# 指导手册：XPES 客户数据库协同 (For AI Agents) - G 盘版本

本文件定义了所有 AI 智能体在处理 `XPES_Master_Leads_Database_Updated.csv` 时的协同规范。

## 1. 数据库路径 (强制)
- **本地路径**: `G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv`
- **桌面快捷方式**: `XPES_Master_Leads.lnk` (指向上述 G 盘路径)

## 2. 字段定义
| 字段 | 说明 |
| :--- | :--- |
| **Company Name** | 客户公司全称 |
| **Website** | 官方网站 URL |
| **Email** | 验证过的负责人个人邮箱 (唯一标识) |
| **Phone** | 电话号码 |
| **Responsible Person** | 负责人姓名 |
| **Main Business** | 客户主营业务 |
| **Relevance** | 与我司产品的相关性/地区 |
| **Status** | 当前开发状态 (如: New, Sent Day 1, Replied, Invalid) |
| **Last Contacted** | 最后一次联系日期 (YYYY-MM-DD) |

## 3. 编辑规则 (智能体必须遵守)
1. **G 盘优先**: 严禁将数据写入 C 盘。所有新资产必须直接存入 `G:\XPES_Customer_Assets`。
2. **去重优先**: 在新增任何客户前，必须先检索 `Email` 字段。如果邮箱已存在，禁止重复创建，仅更新 `Status` 或 `Last Contacted`。
3. **状态更新**: 每次成功发送邮件后，必须立即更新 `Status` 字段（如 `Sent Day 1`）和 `Last Contacted` 日期。
4. **退信处理**: 如果收到 `Address not found` 或退信通知，必须将 `Status` 修改为 `Invalid`。

---
*Created by Accio Sales Assistant (Miguel Yang)*
