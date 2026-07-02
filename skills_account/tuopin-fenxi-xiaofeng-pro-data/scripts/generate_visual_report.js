#!/usr/bin/env node
/**
 * 拓品分析报告（小蜂学掌）v3.0.0 — 报告生成器
 * 优化点：
 *   1. 封面 + 项目背景合并至第 1 页（移除中间 PageBreak）
 *   2. 所有页面注入小蜂学掌页眉页脚（文字 Logo + 版权声明）
 *   3. 项目背景扩写（行业分析 + 战略定位段落）
 *   4. 落地建议扩展至 12 条（A/B/C/D 象限各 3 条）
 *   5. 新增"07 数据来源"章节
 *   6. 数据来源在报告内显式列出
 */

const {
    Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
    AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
    VerticalAlign, PageBreak, PageOrientation, TableLayoutType,
    Header, Footer, ImageRun
} = require('docx');
const fs = require('fs');
const path = require('path');

const COLORS = {
    PRIMARY:     "2E75B6",
    HEADER_BG:   "2E75B6",
    HEADER_TEXT: "FFFFFF",
    RECOMMEND:   "C00000",
    BORDER:      "D9D9D9",
    ZEBRA:       "F9F9F9",
    GOLD:        "D4A017",
    DARK_GRAY:   "555555"
};

const BRAND = {
    name:    "小蜂学掌",
    name_en: "BEE-EDUCATION",
    slogan:  "专注外贸增长 · 工业级选品方法论",
    footer:  "© 小蜂学掌  内部资料 · 请勿外传",
    website: "www.xfxz123.com"
};

// 横向 A4: 16838 DXA；左右 margin=400*2；可用=16038 DXA
// 序号 800 + 后 4 列等宽 2500*4 = 10800 DXA
const COL_WIDTHS = [800, 2500, 2500, 2500, 2500];
const TABLE_WIDTH = COL_WIDTHS.reduce((a, b) => a + b, 0);

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: COLORS.BORDER };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

// ─── 工具函数 ───────────────────────────────────────────────────────────────

function t(text, opts = {}) {
    return new TextRun({ text: text || "", font: "Microsoft YaHei", ...opts });
}

function para(children, opts = {}) {
    return new Paragraph({ children: Array.isArray(children) ? children : [children], ...opts });
}

function headingPara(text, level, color = COLORS.PRIMARY) {
    return new Paragraph({
        heading: level,
        spacing: { before: 300, after: 120 },
        children: [new TextRun({ text, bold: true, color, font: "Microsoft YaHei", size: level === HeadingLevel.HEADING_1 ? 30 : 24 })]
    });
}

function createCell(text, width, options = {}) {
    const { isHeader = false, isRecommended = false, isZebra = false, align = AlignmentType.LEFT } = options;
    return new TableCell({
        borders: cellBorders,
        width: { size: width, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 80, right: 80 },
        shading: {
            fill: isHeader ? COLORS.HEADER_BG : (isZebra ? COLORS.ZEBRA : "FFFFFF"),
            type: ShadingType.CLEAR
        },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
            alignment: align,
            spacing: { before: 40, after: 40 },
            children: [new TextRun({
                text: text || "",
                bold: isHeader || isRecommended,
                size: isHeader ? 20 : 18,
                color: isHeader ? COLORS.HEADER_TEXT : (isRecommended ? COLORS.RECOMMEND : "333333"),
                font: "Microsoft YaHei"
            })]
        })]
    });
}

function createStyledTable(data) {
    const headerRow = new TableRow({
        tableHeader: true,
        children: [
            createCell("序号",            COL_WIDTHS[0], { isHeader: true, align: AlignmentType.CENTER }),
            createCell("产品名称",        COL_WIDTHS[1], { isHeader: true }),
            createCell("英文关键词",      COL_WIDTHS[2], { isHeader: true }),
            createCell("核心逻辑",        COL_WIDTHS[3], { isHeader: true }),
            createCell("适配场景/痛点",   COL_WIDTHS[4], { isHeader: true })
        ]
    });
    const rows = [headerRow];
    data.forEach((item, index) => {
        const isZebra = index % 2 === 1;
        const isRec = !!item.recommend;
        rows.push(new TableRow({
            children: [
                createCell(String(item.id),                     COL_WIDTHS[0], { isZebra, align: AlignmentType.CENTER, isRecommended: isRec }),
                createCell(isRec ? `⭐ ${item.name}` : item.name, COL_WIDTHS[1], { isZebra, isRecommended: isRec }),
                createCell(item.keyword,                        COL_WIDTHS[2], { isZebra, isRecommended: isRec }),
                createCell(item.logic,                          COL_WIDTHS[3], { isZebra, isRecommended: isRec }),
                createCell(item.scenario,                       COL_WIDTHS[4], { isZebra, isRecommended: isRec })
            ]
        }));
    });
    return new Table({
        columnWidths: COL_WIDTHS,
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        layout: TableLayoutType.FIXED,
        rows
    });
}

// ─── 页眉：小蜂学掌品牌 ────────────────────────────────────────────────────

function buildHeader(productName) {
    return new Header({
        children: [
            new Paragraph({
                alignment: AlignmentType.RIGHT,
                border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.PRIMARY } },
                spacing: { after: 100 },
                children: [
                    t(`${BRAND.name_en}  |  ${BRAND.name}`, { bold: true, size: 18, color: COLORS.PRIMARY }),
                    t("    ", { size: 18 }),
                    t(`${productName}拓品分析报告`, { size: 16, color: COLORS.DARK_GRAY })
                ]
            })
        ]
    });
}

// ─── 页脚：版权声明 ────────────────────────────────────────────────────────

function buildFooter(date) {
    return new Footer({
        children: [
            new Paragraph({
                alignment: AlignmentType.CENTER,
                border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLORS.PRIMARY } },
                spacing: { before: 80 },
                children: [
                    t(BRAND.footer, { size: 16, color: COLORS.DARK_GRAY }),
                    t(`    报告日期：${date}    ${BRAND.website}`, { size: 15, color: "AAAAAA" })
                ]
            })
        ]
    });
}

// ─── 封面 + 背景（合并为同一页）────────────────────────────────────────────

function buildCoverAndBackground(payload) {
    const productName = payload.input.product.name;
    const date        = (payload.meta.timestamp || new Date().toISOString()).slice(0, 10).replace(/-/g, '');
    const dateDisplay = `${date.slice(0,4)}-${date.slice(4,6)}-${date.slice(6,8)}`;
    const market      = payload.input.target_market || "全球";
    const company     = payload.input.company || {};

    // 封面
    const coverChildren = [
        para([], { spacing: { before: 800 } }),
        para([
            t(`${BRAND.name_en}`, { bold: true, size: 20, color: COLORS.GOLD }),
            t("  |  小蜂学掌 ABCD 四象限拓品方法论", { size: 18, color: "888888" })
        ], { alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 } }),
        para([
            t(`${productName}拓品分析报告`, { bold: true, size: 80, color: COLORS.PRIMARY })
        ], { alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 } }),
        para([
            t(`${market}市场  ·  ${dateDisplay}`, { size: 32, color: "666666" })
        ], { alignment: AlignmentType.CENTER, spacing: { before: 0, after: 600 } }),
        new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 400 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.PRIMARY } },
            children: [t(BRAND.slogan, { size: 22, color: COLORS.DARK_GRAY, italics: true })]
        }),
    ];

    // 项目背景（紧随封面，同一页）
    const who        = company.who || "";
    const products   = company.products || "";
    const advantages = company.advantages || "";

    // 从三要素提取简要信息用于扩写段落
    const bgChildren = [
        headingPara("01  项目背景", HeadingLevel.HEADING_1),

        // 三要素基础信息
        para([t("🪪 我是谁：", { bold: true, size: 22 }), t(who, { size: 22 })], { spacing: { after: 80 } }),
        para([t("📦 核心产品：", { bold: true, size: 22 }), t(products, { size: 22 })], { spacing: { after: 80 } }),
        para([t("💪 核心优势：", { bold: true, size: 22 }), t(advantages, { size: 22 })], { spacing: { after: 200 } }),

        // 战略背景扩写
        para([t("▌ 行业背景与战略定位", { bold: true, size: 22, color: COLORS.PRIMARY })], { spacing: { before: 120, after: 80 } }),
        para([
            t(`在全球外贸竞争持续加剧的背景下，${market}市场对高质量、差异化 B2B 产品的需求持续攀升。` +
              `本次拓品分析基于小蜂学掌 ABCD 四象限战略框架，结合企业自身供应链能力与目标客群需求，` +
              `系统梳理从本行产品迭代（A象限）到跨行业蓝海布局（D象限）的完整拓品路径，` +
              `旨在帮助企业在保持现有客户粘性的同时，开辟第二、第三增长曲线。`, { size: 20, color: "444444" })
        ], { spacing: { before: 0, after: 120 } }),
        para([
            t(`基于「${who}」的核心定位，结合「${advantages}」的差异化优势，` +
              `本报告围绕 ${market}市场 2026 年度消费趋势与搜索数据，` +
              `精选 80 个高潜力 SKU，覆盖四大象限，每象限标记前 5 位强推产品（⭐），` +
              `并提供英文精准关键词、核心选品逻辑及落地场景分析，` +
              `助力企业高效完成从选品决策到市场切入的全链路布局。`, { size: 20, color: "444444" })
        ], { spacing: { before: 0, after: 120 } }),
        para([
            t("▌ 分析维度说明", { bold: true, size: 22, color: COLORS.PRIMARY })
        ], { spacing: { before: 120, after: 80 } }),
        para([
            t("本报告所有 SKU 均经过四维评分体系筛选：", { size: 20, color: "444444" })
        ], { spacing: { after: 60 } }),
        para([
            t("① 搜索量  — 月均搜索量 ≥ 1 万为基础门槛；", { size: 20, color: "555555" })
        ], { spacing: { after: 40 } }),
        para([
            t("② 趋势    — 近 12 个月 Google Trends 上升态势；", { size: 20, color: "555555" })
        ], { spacing: { after: 40 } }),
        para([
            t("③ 利润空间 — 品类毛利率与客单价综合评估；", { size: 20, color: "555555" })
        ], { spacing: { after: 40 } }),
        para([
            t("④ 工艺匹配 — 与企业现有供应链能力的重合程度。", { size: 20, color: "555555" })
        ], { spacing: { after: 80 } }),
        para([
            t("四维总分 ≥ 14 分的产品标记 ⭐ 优先推荐，建议优先启动资源投入。", { size: 20, bold: true, color: COLORS.DARK_GRAY })
        ], { spacing: { after: 300 } }),
    ];

    return [...coverChildren, ...bgChildren, new Paragraph({ children: [new PageBreak()] })];
}

// ─── 落地建议 ───────────────────────────────────────────────────────────────

function buildSuggestions(payload) {
    const suggestions = payload.input.suggestions || {};
    const defaultSuggestions = {
        A: [
            "优先打造「A象限⭐推荐产品」的标准化数字营销素材（主图、视频、A+页面），以最小推广成本验证市场接受度；",
            "对已有询盘客户重点推荐A象限迭代升级款，通过产品对比说明差异化优势，提升客单价与复购意愿；",
            "建立A象限产品的快速打样通道，缩短从选品到样品寄出的周期至7天以内，抢占买家决策窗口期。"
        ],
        B: [
            "以配套方案切入现有客户，将B象限产品打包成「门窗一站式解决方案」，提升每单采购额；",
            "对B象限高利润配套产品（如智能锁、电动遮阳蓬）单独开设独立站产品页，面向DTC终端消费者测试市场热度；",
            "联合B象限供应商开展联合认证（如CE、UL），降低买家对新供应链的采购风险，加速导入期转化。"
        ],
        C: [
            "C象限产品优先服务工程渠道（建筑商、设计院、总包商），以项目制报价替代传统单品报价，抬升壁垒；",
            "将C象限产品以「铝材深加工能力输出」为品牌叙事，强化工厂直供与柔性定制的供应链背书；",
            "在Alibaba上为C象限顶层产品（如无框玻璃隔断、铝合金阳光房）开设独立展示专区，主动吸引高客单值的工程买家。"
        ],
        D: [
            "D象限产品属于高风险高回报布局，建议先以「小批量测款」策略（MOQ 10-20件）验证买家真实需求，再决定备货规模；",
            "利用D象限产品的跨界属性进行差异化定位，在营销内容中主打「铝材+智能化」或「铝材+环保」的新叙事；",
            "对D象限中与政策红利深度绑定的产品（如光伏停车棚、ADU模块化住宅），主动研究美国IRA法案补贴资格，以政策利好辅助销售转化。"
        ]
    };

    const A_sug = (suggestions.A && suggestions.A.length >= 3) ? suggestions.A : defaultSuggestions.A;
    const B_sug = (suggestions.B && suggestions.B.length >= 3) ? suggestions.B : defaultSuggestions.B;
    const C_sug = (suggestions.C && suggestions.C.length >= 3) ? suggestions.C : defaultSuggestions.C;
    const D_sug = (suggestions.D && suggestions.D.length >= 3) ? suggestions.D : defaultSuggestions.D;

    const items = [];

    const quadrants = [
        { label: "🅰 A象限  本行产品更新迭代", color: "1A5276", sug: A_sug },
        { label: "🅱 B象限  同心多元化",       color: "1E8449", sug: B_sug },
        { label: "🅲 C象限  上下游产业带延伸", color: "7D3C98", sug: C_sug },
        { label: "🅳 D象限  跨行业选品布局",   color: "B7770D", sug: D_sug }
    ];

    let globalIdx = 1;
    quadrants.forEach(q => {
        items.push(
            para([t(`${q.label}`, { bold: true, size: 22, color: q.color })], { spacing: { before: 200, after: 80 } })
        );
        q.sug.forEach(s => {
            items.push(
                para([
                    t(`${globalIdx++}.  `, { bold: true, size: 20, color: COLORS.PRIMARY }),
                    t(s, { size: 20, color: "333333" })
                ], { spacing: { before: 60, after: 60 } })
            );
        });
    });

    return [
        headingPara("06 🚀 落地建议", HeadingLevel.HEADING_1),
        para([
            t("以下 12 条建议基于 ABCD 四象限特性制定，优先启动各象限标 ⭐ 产品，快速验证市场反应。",
              { size: 20, color: "555555", italics: true })
        ], { spacing: { before: 80, after: 160 } }),
        ...items
    ];
}

// ─── 数据来源章节 ────────────────────────────────────────────────────────────

function buildDataSources(payload) {
    const date        = (payload.meta.timestamp || new Date().toISOString()).slice(0, 10).replace(/-/g, '');
    const dateDisplay = `${date.slice(0,4)}-${date.slice(4,6)}-${date.slice(6,8)}`;
    const dataSources = payload.input.data_sources || [
        { platform: "Google Trends",            usage: "关键词近 12 个月搜索趋势验证（上升/平稳/下降）",                                    url: "https://trends.google.com" },
        { platform: "Amazon Best Sellers (US)", usage: "核心品类畅销榜单排名与评论量验证，用于判断品类成熟度与竞争烈度",                    url: "https://www.amazon.com/Best-Sellers/zgbs" },
        { platform: "Alibaba.com 数据参谋",     usage: "关键词搜索热度、买家国家分布、询盘量趋势（B2B视角）",                              url: "https://www.alibaba.com" },
        { platform: "Statista",                 usage: "宏观行业市场规模、CAGR 增长率数据支撑",                                            url: "https://www.statista.com" },
        { platform: "小蜂学掌 ABCD 知识库",     usage: "ABCD 四象限方法论、行业经验库、历史选品案例",                                      url: "https://www.xfxz123.com" }
    ];

    const rows = [
        new TableRow({
            tableHeader: true,
            children: [
                createCell("数据来源",  2000, { isHeader: true }),
                createCell("用途说明",  4000, { isHeader: true }),
                createCell("核查地址",  4000, { isHeader: true }),
            ]
        }),
        ...dataSources.map((ds, i) => new TableRow({
            children: [
                createCell(ds.platform,  2000, { isZebra: i % 2 === 1 }),
                createCell(ds.usage,     4000, { isZebra: i % 2 === 1 }),
                createCell(ds.url,       4000, { isZebra: i % 2 === 1 })
            ]
        }))
    ];

    const sourceTable = new Table({
        columnWidths: [2000, 4000, 4000],
        width: { size: 10000, type: WidthType.DXA },
        layout: TableLayoutType.FIXED,
        rows
    });

    return [
        headingPara("07 📊 数据来源", HeadingLevel.HEADING_1),
        para([
            t(`本报告所有选品数据采集截止日期：${dateDisplay}。以下为本次分析引用的核心数据源：`,
              { size: 20, color: "555555", italics: true })
        ], { spacing: { before: 80, after: 160 } }),
        sourceTable,
        para([
            t("免责声明：市场搜索量与趋势数据存在实时波动，建议结合实际市场调研综合判断，本报告数据仅供参考。",
              { size: 16, color: "AAAAAA", italics: true })
        ], { spacing: { before: 200, after: 100 } })
    ];
}

// ─── 主文档构建 ──────────────────────────────────────────────────────────────

function buildDocument(payload) {
    const productName = payload.input.product.name;
    const date        = (payload.meta.timestamp || new Date().toISOString()).slice(0, 10).replace(/-/g, '');
    const dateDisplay = `${date.slice(0,4)}-${date.slice(4,6)}-${date.slice(6,8)}`;
    const { A, B, C, D } = payload.input.data;

    const header = buildHeader(productName);
    const footer = buildFooter(dateDisplay);

    const children = [
        // 封面 + 项目背景（同一页，末尾有 PageBreak）
        ...buildCoverAndBackground(payload),

        // A 象限
        headingPara("02 🅰 A 象限：本行产品更新迭代", HeadingLevel.HEADING_1),
        createStyledTable(A),
        new Paragraph({ children: [new PageBreak()] }),

        // B 象限
        headingPara("03 🅱 B 象限：同心多元化", HeadingLevel.HEADING_1),
        createStyledTable(B),
        new Paragraph({ children: [new PageBreak()] }),

        // C 象限
        headingPara("04 🅲 C 象限：上下游、产业带延伸", HeadingLevel.HEADING_1),
        createStyledTable(C),
        new Paragraph({ children: [new PageBreak()] }),

        // D 象限
        headingPara("05 🅳 D 象限：跨行业选品布局", HeadingLevel.HEADING_1),
        createStyledTable(D),
        new Paragraph({ children: [new PageBreak()] }),

        // 落地建议（12 条）
        ...buildSuggestions(payload),
        new Paragraph({ children: [new PageBreak()] }),

        // 数据来源
        ...buildDataSources(payload)
    ];

    return new Document({
        creator: `${BRAND.name} × Accio Work`,
        title:   `${productName}拓品报告`,
        styles: { default: { document: { run: { font: "Microsoft YaHei" } } } },
        sections: [{
            properties: {
                page: {
                    size: { orientation: PageOrientation.LANDSCAPE, width: 16838, height: 11906 },
                    margin: { top: 700, right: 400, bottom: 700, left: 400 }
                }
            },
            headers: { default: header },
            footers: { default: footer },
            children
        }]
    });
}

// ─── CLI 入口 ────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const opts = {};
for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) opts[args[i].slice(2)] = args[++i];
}

let payload;
if (opts.payload) {
    payload = JSON.parse(fs.readFileSync(opts.payload, 'utf8'));
} else {
    if (!opts.product) { console.error("❌ 缺少 --product 参数"); process.exit(1); }
    if (!opts.data)    { console.error("❌ 缺少 --data 参数");    process.exit(1); }
    const rawData = JSON.parse(fs.readFileSync(opts.data, 'utf8'));
    payload = {
        meta: { timestamp: new Date().toISOString() },
        input: {
            product: { name: opts.product },
            target_market: rawData.target_market || "全球",
            company: rawData.company,
            data: rawData.data || rawData,
            suggestions: rawData.suggestions || {},
            data_sources: rawData.data_sources || []
        }
    };
}

const doc = buildDocument(payload);
const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const filename = `${payload.input.product.name}拓品报告${dateStr}（小蜂学掌）.docx`;
const outPath = opts.output ? path.join(opts.output, filename) : filename;
const absPath = path.resolve(outPath);

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outPath, buffer);
    console.log('');
    console.log('╔══════════════════════════════════════════════════════════════╗');
    console.log('║  ✅ 报告生成成功                                              ║');
    console.log('╠══════════════════════════════════════════════════════════════╣');
    console.log(`║  📄 文件名：${filename}`);
    console.log(`║  📁 完整路径：`);
    console.log(`║     ${absPath}`);
    console.log('╠══════════════════════════════════════════════════════════════╣');
    console.log('║  💡 在 Windows 资源管理器地址栏粘贴上方路径可直接打开文件        ║');
    console.log('╚══════════════════════════════════════════════════════════════╝');
    console.log('');
}).catch(err => {
    console.error("❌ 生成失败：", err);
    process.exit(1);
});
