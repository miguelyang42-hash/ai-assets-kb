# 🧭 ABCD 四象限关键词生成框架

> Step ② 前置任务：给定一个产品（如「瑜伽垫」），如何在 4 个象限内各生成 20 个**有效的英文搜索关键词**。

---

## 📐 通用方法论：每个象限的关键词三段式

每个英文关键词 = `[修饰词] + [核心品类词] + [应用场景/材质/特征词]`，长度 2-5 个单词最佳（Amazon 搜索匹配率最高）。

---

## 🅰 A 象限：本行产品更新迭代

**逻辑**：同供应链、同客户。在原产品上做 ① 升级 ② 细分 ③ 定制 ④ 高端化。

### 修饰词词库（任选组合）
```
smart, alignment, antimicrobial, biodegradable, extra wide, extra long,
suede, foldable, travel, high density, ar interactive, odorless, tpe,
outdoor, vegan leather, kids, men's thick, cork natural rubber, anti mold,
double sided, durable hiit, custom printed, professional black, eco friendly
```

### 关键词生成示例（产品 = yoga mat）
1. smart alignment yoga mat
2. antimicrobial yoga mat
3. biodegradable natural rubber yoga mat
4. extra wide long yoga mat
5. suede hot yoga mat
6. foldable travel yoga mat
7. high density ashtanga yoga mat
8. ar interactive yoga mat
9. odorless tpe yoga mat
10. alignment lines yoga mat
... (共 20 个)

---

## 🅱 B 象限：同心多元化

**逻辑**：不同供应链、同客户。客户买了 A，他还会买 X/Y/Z（周边、配套、消耗品、配件）。

### 关键词类别（每类 2-3 个）
```
配套件 (10个): towel, block, strap, carrier bag, foam roller, massage ball,
              socks, resistance bands, pilates ring, exercise ball
消耗品 (3个): mat cleaner spray, anti-microbial spray, refresher mist
储存收纳 (2个): wall mounted yoga mat rack, yoga mat hanger
仪式辅件 (3个): meditation cushion, eye pillow, half balance ball trainer
水/服 (2个): sport water bottle, seamless yoga set
```

### 关键词生成示例（用户 = yoga mat 买家）
1. microfiber yoga towel
2. cork yoga block
3. yoga stretching strap
4. yoga mat carrier bag
5. high density foam roller
6. massage ball set
7. non slip yoga socks
8. yoga resistance bands
9. pilates ring magic circle
10. anti burst exercise ball
... (共 20 个)

---

## 🅲 C 象限：上下游、产业带、原材料延伸

**逻辑**：同供应链、不同客户。"我的工厂能用同样的产线/原料/工艺，做出给完全不同行业卖的产品。"

### 关键词类别（每类 2-3 个，**核心是迁移工艺/材料**）
```
办公场景 (2个): standing desk anti fatigue mat, office comfort mat
家居场景 (3个): kitchen anti fatigue mat, bath shower mat, baby foam play mat
宠物场景 (1个): non slip pet training mat
户外场景 (2个): camping sleeping pad, boat decking eva foam sheet
工业场景 (3个): treadmill noise mat, anti vibration washing machine pad,
              esd antistatic table mat, weightlifting platform mat
特殊功能 (3个): medical anti fatigue mat, custom tool box foam insert,
              acoustic insulation foam panel
车/船/医 (3个): car dashboard anti slip mat, horse stall rubber mat,
              swimming kickboard
游戏 (1个): extended gaming mouse pad
保温 (2个): cooler bag liner, wall safety padding foam
```

### 关键词生成示例（产品 = yoga mat → 同样是「闭孔泡棉/橡胶垫」工艺）
1. standing desk anti fatigue mat
2. kitchen comfort mat anti fatigue
3. non slip pet training mat
4. baby foam play mat
5. insulated camping sleeping pad
6. car dashboard anti slip mat
7. esd antistatic table mat
8. treadmill mat noise reduction
9. boat decking eva foam sheet
10. elderly bath shower mat
... (共 20 个)

---

## 🅳 D 象限：跨行业选品

**逻辑**：不同供应链、不同客户。**完全跳出本行**，进入相邻或完全无关的高增长赛道（蓝海/第二曲线）。

### 关键词类别（按"健康+科技+智能化"主题，每类 4-5 个）
```
智能健身 (4个): smart fitness mirror, ems abs stimulator, pilates reformer machine, tonal home gym
红光/恢复 (3个): red light therapy panel, theragun massage gun, percussion massager
量化健康 (4个): smart body fat scale, fitbit charge, oura ring, polar heart rate sensor
环境健康 (3个): air purifier, hydrogen water generator, essential oil diffuser
冷热疗法 (2个): cold plunge tub, mission cooling shirt
神经科技 (2个): muse eeg meditation, vr fitness headset
追踪 (1个): apple airtag tracker
家庭种植 (1个): indoor smart garden hydroponic
```

### 关键词生成示例（跳出"瑜伽"进入「健康消费品」蓝海）
1. fiture smart fitness mirror
2. ems abs stimulator
3. red light therapy panel
4. smart body fat scale
5. fitbit charge fitness tracker
6. cold plunge tub
7. theragun prime
8. smart food nutrition scale
9. portable hydrogen water generator
10. oura ring health tracker
... (共 20 个)

---

## ⚠️ 关键词质量校验红线

> 生成完 80 个关键词后，必须自检：
> - 单个关键词长度 2-5 词（太短匹配过多 Sponsored，太长无结果）
> - 严禁出现品牌词组合（如 "Nike yoga mat"），否则只匹配单一品牌
> - 严禁出现 "best/top/cheap" 等比较词
> - C 象限必须真正"换客户"（不能还是健身爱好者）
> - D 象限必须真正"换供应链"（不能还是泡棉/橡胶工艺）
