# -*- coding: utf-8 -*-
"""
情绪管理课 builder（2026-07-23 · 第十天）
- 单一内容源 -> 生成 晓晓老师(XiaoxiaoNeural) 每句语音(base64 内联)
- 输出「独立」单文件自包含 emotion-class-20260723.html (宋体/可调播放位置/上一句下一句/不挡字幕/费曼提问)
  ※ 每天一个新文件，绝不覆盖旧课页面（满足"每个网页对应一课不要更新网页"）
- 同时输出 情绪管理-晓晓老师课堂笔记.md 与 带日期副本 供存入 ima 知识库 imao
本日结构：复习前16招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪
  +情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本+课题分离+两分钟启动)
  -> 新案例(2026-05-21 网易：药房男医生被一句小抱怨点着、当众扯白大褂要冲、同事死死拽住)
  -> 原理(执行意图 if-then + 自我慈悲安抚系统)
  -> 新招17 预设护栏法(列触发/写护栏/练自动) -> 新招18 自我慈悲法(觉察/共通人性/善待自己) -> 费曼自测
"""
import os, json, base64, asyncio, sys, shutil

WS = "C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-8%"
PITCH = "+0Hz"

# ---------------------------------------------------------------- 案例插画（内联 SVG，保证离线可开）
SVG_MAP = '''<svg viewBox="0 0 700 252" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="20" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">🗺️ 情绪技能地图 · 前16招复习</text>
  <g font-family="sans-serif" font-size="10.5">
   <rect x="8" y="34" width="78" height="86" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="47" y="58" fill="#2b6fb0" text-anchor="middle" font-weight="bold">①五步刹车</text>
   <text x="47" y="80" fill="#243447" text-anchor="middle">停·数·命名</text>
   <text x="47" y="100" fill="#6b7c8f" text-anchor="middle">🔥快炸灭火</text>
   <rect x="92" y="34" width="78" height="86" rx="12" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="131" y="58" fill="#1c7a4d" text-anchor="middle" font-weight="bold">②静音模式</text>
   <text x="131" y="80" fill="#243447" text-anchor="middle">心是一杯水</text>
   <text x="131" y="100" fill="#6b7c8f" text-anchor="middle">💧有火不泼人</text>
   <rect x="176" y="34" width="78" height="86" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="215" y="58" fill="#c98a14" text-anchor="middle" font-weight="bold">③五感着陆</text>
   <text x="215" y="80" fill="#243447" text-anchor="middle">看5摸4听3</text>
   <text x="215" y="100" fill="#6b7c8f" text-anchor="middle">🌀走神着陆</text>
   <rect x="260" y="34" width="78" height="86" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="299" y="58" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④番茄专注</text>
   <text x="299" y="80" fill="#243447" text-anchor="middle">25分只做一事</text>
   <text x="299" y="100" fill="#6b7c8f" text-anchor="middle">🍅练定力</text>
   <rect x="344" y="34" width="78" height="86" rx="12" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="383" y="58" fill="#d6455f" text-anchor="middle" font-weight="bold">⑤认知重评</text>
   <text x="383" y="80" fill="#243447" text-anchor="middle">停·揪·换想法</text>
   <text x="383" y="100" fill="#6b7c8f" text-anchor="middle">🧠换念换情绪</text>
   <rect x="428" y="34" width="78" height="86" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="467" y="58" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑥方箱呼吸</text>
   <text x="467" y="80" fill="#243447" text-anchor="middle">吸4憋7呼8</text>
   <text x="467" y="100" fill="#6b7c8f" text-anchor="middle">🌬️手抖降温</text>
   <rect x="512" y="34" width="78" height="86" rx="12" fill="#eef7f2" stroke="#2bb673" stroke-width="2"/>
   <text x="551" y="58" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑦第三人称</text>
   <text x="551" y="80" fill="#243447" text-anchor="middle">退后·换角·劝友</text>
   <text x="551" y="100" fill="#6b7c8f" text-anchor="middle">👁旁观一眼冷</text>
   <rect x="596" y="34" width="78" height="86" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="635" y="58" fill="#5b3fd6" text-anchor="middle" font-weight="bold">⑧冲动冲浪</text>
   <text x="635" y="80" fill="#243447" text-anchor="middle">认浪·看浪·退</text>
   <text x="635" y="100" fill="#6b7c8f" text-anchor="middle">🌊浪过你还在</text>
   <rect x="8" y="134" width="78" height="86" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="47" y="158" fill="#c98a14" text-anchor="middle" font-weight="bold">⑨情绪命名</text>
   <text x="47" y="180" fill="#243447" text-anchor="middle">起名·打分·说写</text>
   <text x="47" y="200" fill="#6b7c8f" text-anchor="middle">🏷️乱时先起名</text>
   <rect x="92" y="134" width="78" height="86" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="131" y="158" fill="#2b6fb0" text-anchor="middle" font-weight="bold">⑩10-10-10</text>
   <text x="131" y="180" fill="#243447" text-anchor="middle">10分·10月·10年</text>
   <text x="131" y="200" fill="#6b7c8f" text-anchor="middle">🔭拉远看开</text>
   <rect x="176" y="134" width="78" height="86" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="215" y="158" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑪身体急停</text>
   <text x="215" y="180" fill="#243447" text-anchor="middle">离开·冷温·握踩</text>
   <text x="215" y="200" fill="#6b7c8f" text-anchor="middle">🧊先退烧</text>
   <rect x="260" y="134" width="78" height="86" rx="12" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="299" y="158" fill="#d6455f" text-anchor="middle" font-weight="bold">⑫我信息</text>
   <text x="299" y="180" fill="#243447" text-anchor="middle">事实·感受·需·请</text>
   <text x="299" y="200" fill="#6b7c8f" text-anchor="middle">💬只说观点</text>
   <rect x="344" y="134" width="78" height="86" rx="12" fill="#fff3e6" stroke="#ff9a3c" stroke-width="2"/>
   <text x="383" y="158" fill="#c98a14" text-anchor="middle" font-weight="bold">⑬六秒法则</text>
   <text x="383" y="180" fill="#243447" text-anchor="middle">闭嘴·数六</text>
   <text x="383" y="200" fill="#6b7c8f" text-anchor="middle">⏳嘴快先停</text>
   <rect x="428" y="134" width="78" height="86" rx="12" fill="#e9f9ef" stroke="#2bb673" stroke-width="2"/>
   <text x="467" y="158" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑭记账本</text>
   <text x="467" y="180" fill="#243447" text-anchor="middle">触发·念头·新招</text>
   <text x="467" y="200" fill="#6b7c8f" text-anchor="middle">📒天天记天天安</text>
   <rect x="512" y="134" width="78" height="86" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="551" y="158" fill="#2b6fb0" text-anchor="middle" font-weight="bold">⑮课题分离</text>
   <text x="551" y="180" fill="#243447" text-anchor="middle">别人的题不扛</text>
   <text x="551" y="200" fill="#6b7c8f" text-anchor="middle">🚧不还别人账</text>
   <rect x="596" y="134" width="78" height="86" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="635" y="158" fill="#c98a14" text-anchor="middle" font-weight="bold">⑯两分钟启动</text>
   <text x="635" y="180" fill="#243447" text-anchor="middle">拆小步·只做2分</text>
   <text x="635" y="200" fill="#6b7c8f" text-anchor="middle">🚀手指一动静</text>
  </g>
</svg>'''

SVG_CASE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="13.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">案例：药房窗口一句小抱怨 → 男医生当众扯白大褂、红眼要冲 → 同事死死拽住</text>
  <rect x="20" y="38" width="280" height="150" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="1.6"/>
  <circle cx="74" cy="84" r="23" fill="#ffd9b8"/>
  <path d="M59 78 l9 5 M89 78 l-9 5" stroke="#c0392b" stroke-width="3"/>
  <circle cx="67" cy="90" r="2.4" fill="#3a3a3a"/><circle cx="81" cy="90" r="2.4" fill="#3a3a3a"/>
  <path d="M64 100 q10 6 20 0" stroke="#c0392b" stroke-width="3" fill="none"/>
  <rect x="106" y="62" width="176" height="40" rx="10" fill="#fff" stroke="#ffb84d" stroke-width="1.6"/>
  <text x="194" y="80" font-size="12" fill="#c98a14" text-anchor="middle" font-family="sans-serif">“白吃饭、不办事！”</text>
  <text x="160" y="118" font-size="11" fill="#c98a14" text-anchor="middle" font-family="sans-serif">😠 患者得理不饶人</text>
  <text x="160" y="170" font-size="12" fill="#c0492a" text-anchor="middle" font-family="sans-serif">导火索：一句小抱怨</text>
  <text x="160" y="190" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">本可翻篇，他却记进了“情绪账户”</text>
  <text x="320" y="118" font-size="26" fill="#c0492a" text-anchor="middle">VS</text>
  <rect x="340" y="38" width="280" height="150" rx="14" fill="#fdf3f1" stroke="#ff8a8a" stroke-width="1.6"/>
  <circle cx="396" cy="80" r="20" fill="#ffd9b8"/>
  <circle cx="389" cy="80" r="2.4" fill="#3a3a3a"/><circle cx="403" cy="80" r="2.4" fill="#3a3a3a"/>
  <path d="M388 90 q8 7 16 0" stroke="#c0392b" stroke-width="2.6" fill="none"/>
  <rect x="378" y="100" width="36" height="44" rx="8" fill="#fff" stroke="#d9d9d9" stroke-width="1.4"/>
  <path d="M430 104 q26 -8 40 22" stroke="#bbb" stroke-width="3" fill="none" stroke-dasharray="4 4"/>
  <rect x="430" y="118" width="34" height="40" rx="8" fill="#fff" stroke="#ddd" stroke-width="1.2" transform="rotate(18 447 138)"/>
  <text x="480" y="118" font-size="11" fill="#c0492a" text-anchor="middle" font-family="sans-serif">💥 当众扯白大褂甩地</text>
  <text x="480" y="170" font-size="12" fill="#c0492a" text-anchor="middle" font-family="sans-serif">情绪账户早透支，一句引爆</text>
  <text x="480" y="190" font-size="12" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">✅ 本可：退后一步、用护栏</text>
  <text x="320" y="212" font-size="11.5" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">情绪账户长期透支：平时委屈只忍不理，一句小抱怨成导火索 → 一点就炸、事后又后悔</text>
</svg>'''

SVG_PRINCIPLE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">两个道理：执行意图 if-then(提前写剧本,现场不费意志) · 自我慈悲(对自己温柔,激活安抚系统)</text>
  <g font-family="sans-serif">
   <rect x="20" y="38" width="290" height="196" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="165" y="64" font-size="13" fill="#2b6fb0" text-anchor="middle" font-weight="bold">道理一 · 执行意图(if-then)</text>
   <rect x="55" y="84" width="100" height="34" rx="10" fill="#fff" stroke="#5b8def" stroke-width="1.4"/>
   <text x="105" y="106" font-size="13" fill="#c0492a" text-anchor="middle">如果 火起</text>
   <path d="M160 101 h26 M182 93 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="150" y="84" width="110" height="34" rx="10" fill="#eafaf2" stroke="#2bb673" stroke-width="1.4"/>
   <text x="205" y="106" font-size="13" fill="#1c7a4d" text-anchor="middle">就 退后喝水</text>
   <text x="165" y="148" font-size="11" fill="#243447" text-anchor="middle">提前写进脑子 → 现场触发自动执行</text>
   <text x="165" y="170" font-size="11" fill="#1c7a4d" text-anchor="middle">不靠快烧完的意志力</text>
   <text x="165" y="200" font-size="10.5" fill="#6b7c8f" text-anchor="middle">实验：用 if-then 的人，目标达成率高 2-3 倍</text>
   <rect x="340" y="38" width="290" height="196" rx="14" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="485" y="64" font-size="13" fill="#d6455f" text-anchor="middle" font-weight="bold">道理二 · 自我慈悲(安抚)</text>
   <text x="400" y="100" font-size="20" text-anchor="middle">😠</text>
   <text x="400" y="124" font-size="10.5" fill="#c0492a" text-anchor="middle">自责→威胁系统</text>
   <text x="400" y="142" font-size="10.5" fill="#c0492a" text-anchor="middle">皮质醇↑ 更焦虑更炸</text>
   <path d="M424 106 h30" stroke="#d99" stroke-width="2"/>
   <text x="570" y="100" font-size="20" text-anchor="middle">🌊</text>
   <text x="570" y="124" font-size="10.5" fill="#1c7a4d" text-anchor="middle">慈悲→安抚系统</text>
   <text x="570" y="142" font-size="10.5" fill="#1c7a4d" text-anchor="middle">平静 心如止水</text>
   <text x="485" y="186" font-size="11" fill="#243447" text-anchor="middle">对自己狠=心翻江倒海；对自己好=心静</text>
   <text x="485" y="210" font-size="10.5" fill="#6b7c8f" text-anchor="middle">心如止水，是先对自己止争</text>
  </g>
</svg>'''

SVG_GUARD = '''<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">预设护栏法（执行意图 if-then）：把"遇到刺激怎么办"写成"如果…就…"剧本，提前存脑子，现场自动执行</text>
  <g font-family="sans-serif">
   <rect x="14" y="44" width="190" height="140" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="109" y="74" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 列触发</text>
   <text x="109" y="100" font-size="11" fill="#243447" text-anchor="middle">想清楚最容易炸、</text>
   <text x="109" y="120" font-size="11" fill="#243447" text-anchor="middle">最容易摸机的场景</text>
   <text x="109" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">同事甩脸 / 坐工位想摸机</text>
   <text x="109" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">写下来存手机置顶</text>
   <path d="M204 114 l16 0 M220 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="222" y="44" width="190" height="140" rx="14" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="317" y="74" font-size="14" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 写护栏</text>
   <text x="317" y="100" font-size="11" fill="#243447" text-anchor="middle">每条触发配一个</text>
   <text x="317" y="120" font-size="11" fill="#243447" text-anchor="middle">"就"动作（要具体）</text>
   <text x="317" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">火起→退后喝水</text>
   <text x="317" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">坐定→开番茄手机扔远</text>
   <path d="M412 114 l16 0 M428 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="430" y="44" width="190" height="140" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="525" y="74" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">③ 练成自动</text>
   <text x="525" y="100" font-size="11" fill="#243447" text-anchor="middle">每天上班前扫一遍</text>
   <text x="525" y="120" font-size="11" fill="#243447" text-anchor="middle">像过安检、成肌肉记忆</text>
   <text x="525" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">现场一遇，身体自动做</text>
   <text x="525" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">不用想、不靠意志</text>
   <text x="320" y="216" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">如果火起我就退，如果坐定就开钟；提前写进脑子里，现场不靠意志力</text>
  </g>
</svg>'''

SVG_SELF = '''<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#c98a14" text-anchor="middle" font-family="sans-serif">自我慈悲法（对自己温柔）：出错浮躁别骂自己，像安慰好朋友一样安慰自己</text>
  <g font-family="sans-serif">
   <rect x="14" y="44" width="190" height="140" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="109" y="74" font-size="14" fill="#c98a14" text-anchor="middle" font-weight="bold">① 觉察</text>
   <text x="109" y="100" font-size="11" fill="#243447" text-anchor="middle">看见"我在骂自己"</text>
   <text x="109" y="120" font-size="11" fill="#243447" text-anchor="middle">喊停这个念头</text>
   <text x="109" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">你不是"没用的人"</text>
   <text x="109" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">你只是"此刻有点乱"</text>
   <path d="M204 114 l16 0 M220 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="222" y="44" width="190" height="140" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="317" y="74" font-size="14" fill="#2b6fb0" text-anchor="middle" font-weight="bold">② 共通人性</text>
   <text x="317" y="100" font-size="11" fill="#243447" text-anchor="middle">提醒自己</text>
   <text x="317" y="120" font-size="11" fill="#243447" text-anchor="middle">人人都会出错浮躁</text>
   <text x="317" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">这不只我一个</text>
   <text x="317" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">谁没崩过？不是怪胎</text>
   <path d="M412 114 l16 0 M428 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="430" y="44" width="190" height="140" rx="14" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="525" y="74" font-size="14" fill="#d6455f" text-anchor="middle" font-weight="bold">③ 善待自己</text>
   <text x="525" y="100" font-size="11" fill="#243447" text-anchor="middle">手放胸口说一句</text>
   <text x="525" y="120" font-size="11" fill="#243447" text-anchor="middle">"慢慢来，我可以的"</text>
   <text x="525" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">给心打镇静剂</text>
   <text x="525" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">先安抚，再改活</text>
   <text x="320" y="216" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">出错不是我一个，拍拍胸口对自己好；不骂自己不焦灼，心如止水静悄悄</text>
  </g>
</svg>'''

# ---------------------------------------------------------------- 课程内容（第十天）
SECTIONS = [
  {"type":"speak","title":"开场 · 第十天，先串起前16招","rhyme":None,"img":None,"sentences":[
    "同学你好，我是晓晓老师！咱们的情绪管理课到第十天啦。前九天你攒了十六招本领：第一天五步刹车加静音模式，第二天五感着陆加番茄专注，第三天认知重评加方箱呼吸，第四天第三人称抽离加冲动冲浪，第五天情绪命名法加10-10-10透视法，第六天身体急停法加我信息表达法，第七天六秒法则加情绪记账本，第八天课题分离法加两分钟启动法。今天先把这十六招串成一张情绪技能地图，再教你两招新本领，专治你最头疼的两件事——一遇上刺激就火冒三丈、控制不住脾气；还有一坐到电脑前心就浮、老想摸手机、干正事像上刑。",
    "先复习老口号：任何场合——办公室、工作群、会议室、甚至医院药房窗口——都不是展示真性情的地方，它只是表达观点的地方。你是去把事说清楚的，不是去把脾气秀出来的。",
    "今天要补的第一块：你容易被一点小事点燃——别人一句难听话、一个甩脸，你火就上来了，话比脑子快，事后又后悔。第二块：你对自己特别狠——一出错就骂自己怎么这么没用，越骂越急躁越乱。今天两招，一招管现场不炸，一招管不跟自己过不去。"
  ]},

  {"type":"speak","title":"复习 · 十六招技能地图","rhyme":None,"img":SVG_MAP,"sentences":[
    "先复习十六招，编成一张地图。第一招五步刹车——一停二数三命名，四转五说；火气冒头先喊停，只说观点不秀脾气。第二招静音模式——心是一杯水，摇浑放自清，有火不泼别人。第三招五感着陆——看五摸四听三声，走神坐不住用它。第四招番茄专注——二十五分只做一事，手机扔远练定力。",
    "第五招认知重评——火起先喊停、揪出念头、换个想法，换想法就换情绪。第六招方箱呼吸——吸气四憋七呼八憋四，画方箱一分钟降温。第七招第三人称抽离——退后、换角、劝友，把我换成朋友视角火就小。第八招冲动冲浪——认浪、看浪、等浪退，约十分钟浪自己走。",
    "第九招情绪命名法——精准起名、温度计打分、说或写下来，你不是情绪你是起名的人。第十招10-10-10透视法——10分后10月后10年后还重要吗，拉远看浮躁就散。第十一招身体急停法——离开现场、冷水温水、握拳松拳、脚踩地、暂不回消息，身体是开关先退烧。第十二招我信息表达法——事实→感受→需要→请求，用我开头只说观点不人身攻击。",
    "第十三招六秒法则——火冒三丈先闭嘴、默数到六、等理智脑上线、再开口。第十四招情绪记账本——睡前三栏触发、念头、新招，天天记、天天安。第十五招课题分离法——同事甩脸是别人课题，我的活儿我写好，别人的题我不扛。第十六招两分钟启动法——大活先拆第一步、只做两分不贪多，手指一动心就静。今天两招管最前面的替别人内耗和大活不动手、还有一点就炸、跟自己过不去。"
  ]},

  {"type":"quiz","title":"复习小测 · 走神想摸机 + 一点就炸用哪招","quiz":{
    "q":"开会时你心飘了、老想摸手机，偏偏隔壁同事又甩你一句难听话，你火一下就上来了。前16招里该先动哪两招管走神想摸机，又该先动哪招管一点就炸？",
    "opts":[
      {"t":"走神摸机→五感着陆(拉回当下)+番茄专注(25分只做一事手机扔远)；一点就炸→五步刹车(一停二数)或六秒法则(闭嘴数六)先灭火","ok":True},
      {"t":"走神摸机→冲动冲浪(那是管已起冲动想发作，不是走神)","ok":False},
      {"t":"一点就炸→情绪记账本(那是睡前复盘，不是现场灭火)","ok":False}
    ],
    "stu":"小浩抢答：老师，一点就炸是不是用冲动冲浪压一压？",
    "teacher":"晓晓老师笑：冲动冲浪是给已经上头、想摔东西怼人那股浪用的，要等十分钟。可你这是刚被一句话点着、火苗还小——用第一招五步刹车(停、数、命名)或第十三招六秒法则(闭嘴数六)最快灭火；走神摸手机是另一码事，用第三招五感着陆加第四招番茄专注。分工记牢：走神→五感加番茄；小火苗→刹车加六秒；大浪→冲浪加方箱。",
    "card":["走神想摸机=五感着陆(拉回当下)+番茄专注(25分只做一事手机扔远)。","一点小火苗=五步刹车(停数命名)或六秒法则(闭嘴数六)；大浪才用冲浪加方箱。"]
  }},

  {"type":"speak","title":"第一幕 · 新案例：一句小抱怨，医生当众崩了","rhyme":None,"img":SVG_CASE,"sentences":[
    "讲个 2026 年刚发生的真实事（来源网易，2026-05-21，医院药房窗口）。主人公是位男医生，在药房窗口配药多年，平时话少、干活稳，最擅长一个字——忍。",
    "那天，一名男患者来取特慢病药，没带身份证，按规定必须核验身份。医生照规矩说：系统过不了，您回家取证件再来。这话没错吧？可患者当场当众高声骂他白吃饭、不办事，整个队伍都听见了。医生全程低头，头都没抬——这是一线窗口的日常，他忍了。",
    "患者拿完药，本该走了，却折回来对着工位低声嘀咕、言语讥讽。就这几句得理不饶人的抱怨，成了压垮他的最后一根稻草。他猛地起身，当众扯下白大褂狠狠甩在地上，红着眼眶要冲出去对峙。三四名同事死死拽住、劝了近十分钟，才把他拦下来。在场患者纷纷拍照。",
    "文章里说，这不是一次冲突，是无数次委屈积压后的彻底宣泄。穿上白大褂他是医者、忍辱负重；脱下白大褂他只是个普通人，也会委屈、也会愤怒。可那一扯一甩，他输了体面，也给了别人情绪失控的把柄。",
    "换成咱们的视角看：这位医生不是脾气差，是情绪账户早就透支了——平时一点一点往里存委屈，从不取出来管理，最后一句小抱怨就引爆。这正好对应你：心不够静、浮躁不安，一点就炸，事后又后悔。下面两招，一招教你提前装好护栏、小火苗别长大，一招教你对自己温柔点、别让自责把火越扇越旺。"
  ]},

  {"type":"quiz","title":"课间提问① · 医生最亏在哪","quiz":{
    "q":"医生最亏在哪？一句小抱怨，为什么能让他当众崩成那样？",
    "opts":[
      {"t":"他情绪账户长期透支——平时委屈只忍不理、从不管理；一句小抱怨只是导火索，真正炸的是积压的火。场面失控还给了别人把柄","ok":True},
      {"t":"他天生脾气爆、性格差","ok":False},
      {"t":"是患者太过分，全怪患者","ok":False}
    ],
    "stu":"小雪：可患者确实嘴欠啊！",
    "teacher":"晓晓老师点头：患者嘴欠不对，该批评。但咱们能管的只有自己。医生平时每受一次委屈就存进情绪账户不取，账户满了，一句小抱怨就爆。教训是——情绪要日常取出来管理(用前16招)，别等炸了才后悔。这引出今天第一招：提前装护栏，让小火苗刚冒头就被按住。",
    "card":["医生崩在：委屈长期积压、从不管理，一句小抱怨成导火索；情绪账户透支→一点就炸。","情绪要日常取出管理(前16招)，别等炸了才后悔；这引出提前装护栏。"]
  }},

  {"type":"speak","title":"第二幕 · 原理：执行意图 + 自我慈悲","rhyme":None,"img":SVG_PRINCIPLE,"sentences":[
    "为什么提前装护栏比现场硬扛管用？心理学家盖洛韦发现一个秘密：人脑喜欢如果…就…这条自动链路。你提前写好了如果A发生我就做B，现场真遇到A，脑子会自动跳到B，不费意志力。实验里用了如果…就…计划的人，目标达成率高出两三倍。反过来，靠临场喊我要冷静这种空口号，火一上来全忘光。",
    "所以一点就炸的治本办法，不是等火来了再压，而是提前把火来了怎么办写成剧本，存进脑子。这叫执行意图，英文 if-then 计划。现场一触发，自动执行，不靠你那点快烧完的意志力。",
    "第二个道理，专治跟自己过不去：神经科学发现，你一骂自己没用、笨，大脑就拉响警报——威胁系统启动，压力荷尔蒙皮质醇往上飙，你更焦虑、更易炸。反过来，对自己温柔一点，自我慈悲，会激活身体的安抚系统，让你平静下来。这跟咱们的心如止水一模一样——对自己狠，心就翻江倒海；对自己好，心才静得下来。",
    "一句话：现场不炸靠提前写剧本(执行意图)；不跟自己过不去靠对自己温柔(自我慈悲)。道理一→预设护栏法；道理二→自我慈悲法。"
  ]},

  {"type":"quiz","title":"课间提问② · 为什么预设护栏比喊冷静管用","quiz":{
    "q":"为什么如果火起我就退后这种提前写好的护栏，比火来了再喊我要冷静管用？",
    "opts":[
      {"t":"人脑认如果…就…自动链路：提前写好，现场触发自动执行、不费意志力；空喊要冷静火一上来就忘。这是执行意图","ok":True},
      {"t":"因为喊要冷静声音不够大","ok":False},
      {"t":"因为退后跑得快","ok":False}
    ],
    "stu":"小杰：那我火都上来了，退后不显得怂吗？",
    "teacher":"晓晓老师笑：退后是聪明，不是怂。你退一步，物理距离一拉，火就少一口氧气；等理智脑回来再开口，说的是观点不是脾气——这正合场合是表达观点的地方。而且这是你提前写好的剧本，执行起来毫不费力，比硬扛体面多了。",
    "card":["执行意图：提前写如果…就…，现场自动执行、不费意志力；空喊要冷静火来就忘。","退后是聪明不是怂：拉距离=给火断氧，回来只说观点。"]
  }},

  {"type":"speak","title":"第三幕 · 新招17：预设护栏法（执行意图 if-then）","rhyme":{
    "title":"🎵 预设护栏口诀",
    "lines":["<b>如果火起我就退</b>，<b>如果坐定就开钟</b>；","<b>提前写进脑子里</b>，<b>现场不靠意志力</b>。"]
  },"img":SVG_GUARD,"sentences":[
    "新本领第十七招：预设护栏法（执行意图 if-then）。一句话——把遇到刺激我怎么办提前写成如果…就…剧本，存进脑子，现场自动执行，不靠意志力。三步：",
    "第一步列触发：想清楚最容易让你炸、最容易让你摸手机的场景。比如：同事甩脸、被当众说、坐到工位想摸手机、收到难听话。把这几条写下来，存手机置顶。",
    "第二步写护栏：给每条触发配一个就动作——如果同事甩脸，我就先退后一步喝口水；如果坐到工位，我就先开25分钟番茄钟、手机扔抽屉；如果火冒三丈，我就闭嘴数六。动作要具体、能马上做。",
    "第三步练成自动：每天上班前扫一眼这条清单，像过安检。练几次，现场一遇到，身体自动就做了——你甚至不用想。这招对一点就炸和浮躁坐不住想摸机都管用。",
    "记住：别等火来了硬扛，提前把剧本写好。像给心装了一道护栏，小火苗刚冒头就被挡在门外。这招直接呼应核心理念——场合是表达观点的地方，你用护栏保住理智，说出来的才是观点不是脾气。",
    "记口诀：如果火起我就退，如果坐定就开钟；提前写进脑子里，现场不靠意志力。"
  ]},

  {"type":"quiz","title":"课间提问③ · 预设护栏怎么用","quiz":{
    "q":"周一晨会，领导当众皱眉说这方案不行，你脸一热、手就伸向手机想摸。按预设护栏法，你该提前写好哪条如果…就…？",
    "opts":[
      {"t":"如果领导皱眉说我，我就先退后一步、深呼吸、用我信息问清标准；如果坐到工位想摸机，我就先开番茄钟手机扔远——提前写进脑子，现场自动做","ok":True},
      {"t":"如果领导皱眉，我就当场怼回去","ok":False},
      {"t":"如果手伸向手机，就刷半小时放松","ok":False}
    ],
    "stu":"小琳：我怕写好了到时候还是摸。",
    "teacher":"晓晓老师点头：所以才要练成自动——每天上班前扫一遍清单，像肌肉记忆。刚开始可能还会摸，但护栏会一次次把你拦回来；练上十天半月，手伸出去自己就停了。关键是提前写、天天练，别指望火来了才现想。",
    "card":["预设护栏：①列触发(甩脸/坐工位想摸机)②写就动作(退后喝水/开番茄手机扔远)③练成自动。","提前写+天天练成肌肉记忆；别等火来现想。"]
  }},

  {"type":"speak","title":"第四幕 · 新招18：自我慈悲法（对自己温柔）","rhyme":{
    "title":"🎵 自我慈悲口诀",
    "lines":["<b>出错不是我一个</b>，<b>拍拍胸口对自己好</b>；","<b>不骂自己不焦灼</b>，<b>心如止水静悄悄</b>。"]
  },"img":SVG_SELF,"sentences":[
    "新本领第十八招：自我慈悲法（对自己温柔）。一句话——出错、浮躁、被说时，别骂自己，像安慰好朋友一样安慰自己。三步：",
    "第一步觉察：发现自己又在骂自己怎么这么没用、怎么又浮躁时，先喊停，看见这个念头。你不是没用的人，你只是此刻有点乱。",
    "第二步共通人性：提醒自己人人都会出错、人人都会浮躁，这不只我一个。你看那医生、看热搜上发飙的人，谁没崩过？你不是怪胎。",
    "第三步善待自己：把手放胸口，对自己说一句温柔的话——辛苦了，慢慢来，我可以的。这一句像给心打镇静剂，催你平静下来，而不是越骂越炸。所谓心如止水，是先对自己止争。",
    "记住：你对自己狠，心就翻江倒海，越急越乱；你对自己好，心才静得下来。浮躁不是你差，是心累了；拍拍它，继续走。这招和情绪命名是搭档——先给情绪起名，再对它慈悲。",
    "记口诀：出错不是我一个，拍拍胸口对自己好；不骂自己不焦灼，心如止水静悄悄。"
  ]},

  {"type":"quiz","title":"课间提问④ · 自我慈悲怎么用","quiz":{
    "q":"周报写岔了被领导点名，你当场在心里骂自己废物怎么又搞砸，越想越急躁、手抖。按自我慈悲法，你该做啥？",
    "opts":[
      {"t":"先觉察我在骂自己→共通人性人人都会出错不全是我→手放胸口对自己说慢慢来我可以，用安抚代替自责，心静下来再改","ok":True},
      {"t":"继续骂自己，骂醒了就能改好","ok":False},
      {"t":"假装没事，硬撑","ok":False}
    ],
    "stu":"小强：可我真的总出错，不骂记不住啊。",
    "teacher":"晓晓老师摇头：骂自己只会让皮质醇飙升、更焦虑更炸，反而改不好。研究说，自我慈悲的人犯错后恢复更快、更愿意改。你越温柔对待出错的自己，越有劲儿去改。先安抚，再改活——顺序别反。",
    "card":["自我慈悲三步：①觉察(我在骂自己)②共通人性(人人会错不全我)③善待(手放胸口说慢慢来)。","自责→皮质醇↑更炸；慈悲→安抚系统→更快改好。先安抚再改活。"]
  }},

  {"type":"speak","title":"结尾 · 今天你带走什么（前16招+两新招）","rhyme":None,"img":None,"sentences":[
    "今天的课到这儿，晓晓老师带你总复习。",
    "前16招（复习）：五步刹车——一停二数三命名四转五说；静音模式——心是一杯水；五感着陆——看五摸四听三声；番茄专注——二十五分只做一事；认知重评——停揪换、换想法就换情绪；方箱呼吸——吸4憋7呼8憋4；第三人称抽离——退后换角劝友；冲动冲浪——认浪看浪等浪退；情绪命名法——精准起名温度计打分说写下来；10-10-10透视法——10分10月10年后拉远看；身体急停法——离开冷水握拳脚踩地；我信息表达法——事实感受需要请求只说观点；六秒法则——火冒三丈先闭嘴数六等理智脑；记账本——睡前三栏触发念头新招；课题分离法——别人课题我不扛；两分钟启动法——大活先拆只做两分。",
    "新本领①：预设护栏法——把遇到刺激怎么办写成如果…就…剧本提前存脑子，现场自动执行不靠意志；遇火退后、坐定开钟不摸机。新本领②：自我慈悲法——出错浮躁别骂自己，觉察、共通人性、手放胸口善待自己，心如止水先对自己止争。",
    "一句话收尾：场合不是秀脾气的地方，只是说观点的地方；提前装好护栏、现场不炸，对自己温柔、心如止水，你会越来越稳。下课！"
  ]},

  {"type":"feynman","title":"费曼小测 · 讲给晓晓老师听","text":
    "费曼学习法说：你以为你懂了，不算懂；能用自己的话讲明白，才是真懂。\n\n现在轮到你啦——请用你自己的话，把下面这道题讲给晓晓老师听：\n\n如果下次我又被一句难听话点着、火一下窜上来，或者一坐到工位就忍不住摸手机、还因为写岔了活儿在心里骂自己没用，我会怎么做，才能既不当场炸、又能管住浮躁、还不对自已太狠、把该干的活干好？\n\n提示：可以结合旧本领（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本、课题分离法、两分钟启动法）和新本领（预设护栏法、自我慈悲法）一起说。\n\n在下面的框里写几句（或对着麦克风讲出来也行）。写完了，翻回上面的口诀卡对照一下，看看漏了哪一步。"
  }
]

# ---------------------------------------------------------------- 语音生成
def collect_sentences():
    out = []
    for s in SECTIONS:
        if s.get("type") == "speak":
            for t in s["sentences"]:
                out.append(t)
    return out

async def gen_one(text, path):
    try:
        import edge_tts
        comm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await comm.save(path)
        return True
    except Exception as e:
        print("FAIL:", text[:24], "->", repr(e), file=sys.stderr)
        return False

async def gen_all(texts, out_dir):
    import edge_tts, asyncio as aio
    sem = aio.Semaphore(4)
    res = [None]*len(texts)
    async def worker(i, t):
        async with sem:
            p = os.path.join(out_dir, f"{i}.mp3")
            ok = await gen_one(t, p)
            if ok and os.path.exists(p) and os.path.getsize(p) > 200:
                with open(p, "rb") as f:
                    res[i] = "data:audio/mp3;base64," + base64.b64encode(f.read()).decode("ascii")
    await aio.gather(*(worker(i, t) for i, t in enumerate(texts)))
    return res

def build_audio():
    texts = collect_sentences()
    cache = os.path.join(WS, ".tts_cache")
    os.makedirs(cache, exist_ok=True)
    res = asyncio.run(gen_all(texts, cache))
    ok = sum(1 for x in res if x)
    print(f"[audio] 生成 {ok}/{len(texts)} 句成功")
    shutil.rmtree(cache, ignore_errors=True)
    return res

# ---------------------------------------------------------------- HTML 模板
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>晓晓老师的情绪管理课 · 第10天：提前装护栏、对自己温柔——场合不是秀脾气，只是说观点</title>
<style>
  :root{
    --bg:#f4f7fb; --card:#ffffff; --ink:#243447; --soft:#6b7c8f;
    --brand:#5b8def; --brand2:#7c5cff; --good:#2bb673; --warn:#ff7a59;
    --pink:#ff8fab; --yellow:#ffd66b; --mint:#bdeed3; --shadow:0 10px 30px rgba(40,60,90,.12);
  }
  *{box-sizing:border-box;}
  body{
    margin:0; font-family:"SimSun","宋体","Songti SC","STSong",serif;
    font-size:16pt; line-height:2.0; color:var(--ink);
    background:linear-gradient(160deg,#eef3ff 0%,#f7f0ff 55%,#fff5f0 100%);
    padding-bottom:160px;
  }
  header{ text-align:center; padding:26px 16px 10px; }
  header h1{ font-size:28pt; margin:8px 0 4px; letter-spacing:1px; }
  header p{ color:var(--soft); margin:0; font-size:15pt; }
  .teacher{ width:96px; height:96px; margin:0 auto 6px; border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#fff,#ffe3ef 60%,#ffd0e2);
    box-shadow:var(--shadow); display:flex; align-items:center; justify-content:center; border:4px solid #fff; }
  .badge{ display:inline-block; background:var(--mint); color:#1c7a4d; font-size:13pt;
    padding:4px 12px; border-radius:999px; margin-top:6px; }
  .wrap{ display:flex; gap:18px; max-width:1040px; margin:14px auto; padding:0 16px; align-items:flex-start; }
  .progress{ flex:0 0 230px; background:var(--card); border-radius:18px; padding:14px;
    box-shadow:var(--shadow); position:sticky; top:14px; }
  .progress h3{ font-size:15pt; margin:2px 0 10px; color:var(--soft); }
  .step{ display:flex; align-items:center; gap:10px; padding:9px 10px; border-radius:12px;
    font-size:14pt; color:var(--soft); cursor:pointer; transition:.2s; margin-bottom:4px; }
  .step:hover{ background:#f0f4fb; }
  .step.active{ background:linear-gradient(90deg,#eaf1ff,#f3ecff); color:var(--ink); font-weight:700; }
  .step.done{ color:var(--good); }
  .dot{ width:22px; height:22px; border-radius:50%; background:#e3e9f2; color:#fff; flex:0 0 22px;
    display:flex; align-items:center; justify-content:center; font-size:12pt; }
  .step.active .dot{ background:var(--brand); }
  .step.done .dot{ background:var(--good); }
  .stage{ flex:1; min-width:0; }
  .card{ background:var(--card); border-radius:20px; padding:24px 26px; box-shadow:var(--shadow); margin-bottom:16px; }
  .card h2{ font-size:23pt; margin:0 0 14px; display:flex; align-items:center; gap:8px; }
  .scene-text{ font-size:16pt; white-space:pre-wrap; }
  .scene-text .cur{ background:#fff3c4; border-radius:5px; transition:.15s; padding:0 2px; }
  .scene-img{ width:100%; max-width:680px; margin:6px auto 16px; border-radius:14px; overflow:hidden;
    box-shadow:0 6px 16px rgba(40,60,90,.10); background:#fff; }
  .scene-img svg{ display:block; width:100%; height:auto; }
  .controls{ display:flex; gap:10px; flex-wrap:wrap; margin-top:16px; align-items:center; }
  button.btn{ border:none; cursor:pointer; font-family:inherit; font-size:15pt; padding:10px 18px;
    border-radius:12px; background:var(--brand); color:#fff; box-shadow:0 6px 14px rgba(91,141,239,.35); transition:.15s; }
  button.btn:hover{ transform:translateY(-1px); }
  button.btn.ghost{ background:#eef2f9; color:var(--ink); box-shadow:none; }
  button.btn.good{ background:var(--good); }
  button.btn:disabled{ opacity:.45; cursor:not-allowed; transform:none; }
  .pill{ font-size:13pt; color:var(--soft); }
  .rhyme{ background:linear-gradient(135deg,#fff7e6,#ffeef6); border-left:6px solid var(--yellow);
    border-radius:14px; padding:14px 18px; margin:14px 0; font-size:17pt; line-height:2.1; letter-spacing:.5px; }
  .rhyme b{ color:#d98324; }
  .quiz{ background:linear-gradient(160deg,#f1f6ff,#f6f0ff); border-radius:18px; padding:22px 24px;
    box-shadow:var(--shadow); border:2px dashed #c9d6f5; }
  .quiz .q{ font-size:18pt; font-weight:700; margin-bottom:12px; }
  .opt{ display:block; width:100%; text-align:left; border:2px solid #e1e8f4; background:#fff;
    border-radius:12px; padding:12px 14px; margin:8px 0; font-size:15pt; cursor:pointer; transition:.15s;
    color:var(--ink); font-family:inherit; }
  .opt:hover{ border-color:var(--brand); }
  .opt.correct{ border-color:var(--good); background:#eafaf2; }
  .opt.wrong{ border-color:var(--warn); background:#fff1ec; }
  .opt:disabled{ cursor:default; }
  .feedback{ margin-top:12px; padding:12px 14px; border-radius:12px; font-size:15pt; display:none; }
  .feedback.show{ display:block; }
  .feedback.ok{ background:#eafaf2; color:#1c7a4d; }
  .feedback.no{ background:#fff1ec; color:#c0492a; }
  .role{ display:flex; gap:10px; align-items:flex-start; margin:12px 0; font-size:15pt; }
  .role .who{ flex:0 0 70px; font-weight:700; color:var(--brand2); }
  .role .who.stu{ color:var(--brand); }
  .role .say{ background:#f5f7fb; border-radius:12px; padding:8px 12px; }
  .feynman{ background:#fffdf5; border:2px solid #ffe3a3; border-radius:14px; padding:14px 16px; margin-top:14px; }
  .feynman h4{ margin:0 0 8px; color:#c98a14; font-size:16pt; }
  .feynman ul{ margin:0; padding-left:22px; }
  textarea{ width:100%; border:2px solid #e1e8f4; border-radius:12px; padding:10px 12px; font-size:15pt;
    font-family:inherit; resize:vertical; min-height:90px; margin-top:10px; }
  .star{ color:var(--yellow); }
  .finish{ text-align:center; background:linear-gradient(135deg,#e9fff4,#eef3ff); border-radius:20px; padding:28px; box-shadow:var(--shadow); }
  .finish h2{ color:var(--good); font-size:23pt; }
  .playerbar{ position:fixed; left:0; right:0; bottom:54px; height:70px; z-index:60;
    background:rgba(28,40,58,.94); color:#fff; display:flex; align-items:center; gap:12px;
    padding:0 16px; box-shadow:0 -6px 20px rgba(0,0,0,.25); backdrop-filter:blur(6px); }
  .playerbar button{ border:none; cursor:pointer; font-family:inherit; font-size:15pt; padding:8px 14px;
    border-radius:10px; background:#3a5274; color:#fff; }
  .playerbar button:hover{ background:#47638c; }
  .playerbar button:disabled{ opacity:.4; cursor:not-allowed; }
  .playerbar .pseek{ flex:1; accent-color:var(--pink); height:6px; }
  .playerbar .pmeta{ font-size:13pt; min-width:96px; text-align:right; color:#cfe0ff; }
  .playerbar .pbtnplay{ background:var(--pink); color:#3a1020; font-weight:700; }
  .playerbar .pbtnplay:hover{ background:#ffa7c0; }
  .subtitle{ position:fixed; left:0; right:0; bottom:0; height:54px; z-index:50;
    background:rgba(20,28,40,.9); color:#fff; padding:0 18px; font-size:15pt; letter-spacing:.5px;
    display:flex; align-items:center; justify-content:center; text-align:center;
    box-shadow:0 -4px 16px rgba(0,0,0,.2); }
  .subtitle .spk{ display:inline-block; width:9px; height:9px; border-radius:50%; background:var(--pink);
    margin-right:9px; animation:pulse 1s infinite; }
  @keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
  .hint{ font-size:13pt; color:var(--soft); text-align:center; margin:0 0 26px; }
  @media(max-width:820px){ .wrap{flex-direction:column;} .progress{position:static; width:100%; flex:none;} }
</style>
</head>
<body>
<header>
  <div class="teacher" aria-hidden="true">
    <svg width="64" height="64" viewBox="0 0 64 64">
      <circle cx="32" cy="34" r="20" fill="#ffe0ec"/>
      <path d="M12 30 Q12 8 32 8 Q52 8 52 30 Q44 22 32 22 Q20 22 12 30Z" fill="#6b4a3a"/>
      <circle cx="25" cy="34" r="3.2" fill="#3a3a3a"/><circle cx="39" cy="34" r="3.2" fill="#3a3a3a"/>
      <path d="M26 43 Q32 48 38 43" stroke="#d36a86" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <circle cx="44" cy="30" r="3" fill="#ffb3c8" opacity=".7"/>
    </svg>
  </div>
  <h1>晓晓老师的情绪管理课 · 第10天</h1>
  <p>提前装护栏不炸、对自己温柔心静：场合不是秀脾气的地方，只是说观点的地方 🧊</p>
  <span class="badge">🌟 晓晓老师 · 神经网络语音讲解（XiaoxiaoNeural）</span>
</header>

<div class="wrap">
  <aside class="progress"><h3>📒 今天的课表</h3><div id="steps"></div></aside>
  <main class="stage"><div id="stage"></div>
    <p class="hint">💡 点「▶ 听这一段」会有晓晓老师语音+字幕；底部黑条可拖动调位置，用「上一句 / 下一句」逐句回看；中间会突然提问你、还有同学抢答。</p>
  </main>
</div>

<!-- 底部播放控制条 -->
<div class="playerbar" id="playerbar" style="display:none">
  <button id="pPrev">⏮ 上一句</button>
  <button class="pbtnplay" id="pPlay">▶ 播放</button>
  <button id="pNext">下一句 ⏭</button>
  <input type="range" class="pseek" id="pSeek" min="0" max="100" value="0" step="0.1" disabled />
  <span class="pmeta" id="pMeta">— / —</span>
</div>

<!-- 字幕条 -->
<div class="subtitle" id="subtitle"><span class="spk"></span><span id="subText">点上方「开始上课」听晓晓老师讲～</span></div>

<script>__LESSON_DATA__</script>
<script>__AUDIO_DATA__</script>
<script>
"use strict";
const SECTIONS = window.SECTIONS;
const AUDIO = window.AUDIO || [];
const stage = document.getElementById('stage');
const stepsEl = document.getElementById('steps');
const subText = document.getElementById('subText');
const bar = document.getElementById('playerbar');
const pPrev = document.getElementById('pPrev');
const pPlay = document.getElementById('pPlay');
const pNext = document.getElementById('pNext');
const pSeek = document.getElementById('pSeek');
const pMeta = document.getElementById('pMeta');

let PLAYLIST = [];
SECTIONS.forEach((s, si)=>{
  if(s.type==='speak'){ s.sentences.forEach((t, ji)=>{ PLAYLIST.push({si, ji, gi:PLAYLIST.length, text:t}); }); }
});
let sectionIdx = -1;
let cur = 0;
let stars = 0;
let answered = new Set();
let textContainer = null;
let allMode = false;

const audioEl = new Audio();
let synthOn = ('speechSynthesis' in window);
let curUtter = null;

function setSub(t){ subText.textContent = t; }
function sectionSentences(si){ return PLAYLIST.filter(p=>p.si===si); }

function highlightSentence(ji){
  if(!textContainer) return;
  const spans = textContainer.querySelectorAll('span[data-ji]');
  spans.forEach(sp=>{ sp.classList.toggle('cur', parseInt(sp.getAttribute('data-ji'),10)===ji); });
}
function setMeta(){
  const list = sectionSentences(sectionIdx);
  const pos = list.findIndex(p=>p.gi===PLAYLIST[cur].gi);
  pMeta.textContent = '第 '+(pos+1)+' / '+list.length+' 句';
}
function playCurrent(){
  const item = PLAYLIST[cur];
  highlightSentence(item.ji);
  setSub(item.text);
  setMeta();
  const data = AUDIO[item.gi];
  if(data){
    pSeek.disabled = false;
    audioEl.src = data; audioEl.currentTime = 0;
    audioEl.play().then(()=>{ pPlay.textContent='⏸ 暂停'; }).catch(()=>{ pPlay.textContent='▶ 播放'; });
  } else if(synthOn){
    pSeek.disabled = true; pSeek.value = 0;
    if(window.speechSynthesis) window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(item.text);
    u.lang='zh-CN'; u.rate=0.95; u.pitch=1.0;
    const v = window.speechSynthesis ? speechSynthesis.getVoices().find(x=>/xiaoxiao|晓晓/i.test(x.name)) : null;
    if(v) u.voice=v;
    u.onend = ()=>{ pPlay.textContent='▶ 播放'; onSentenceEnd(); };
    curUtter = u; window.speechSynthesis.speak(u); pPlay.textContent='⏸ 暂停';
  } else {
    pSeek.disabled = true;
  }
}
function onSentenceEnd(){
  const list = sectionSentences(sectionIdx);
  const idxInSec = list.findIndex(p=>p.gi===PLAYLIST[cur].gi);
  if(idxInSec < list.length-1){
    cur++; playCurrent();
  } else if(allMode){
    goNextSection();
    if(sectionIdx>=0 && SECTIONS[sectionIdx] && SECTIONS[sectionIdx].type==='speak'){ playCurrent(); }
  }
}
audioEl.addEventListener('ended', ()=>{ pPlay.textContent='▶ 播放'; onSentenceEnd(); });
audioEl.addEventListener('timeupdate', ()=>{
  if(audioEl.duration){ pSeek.value = (audioEl.currentTime/audioEl.duration*100).toFixed(1); }
});
pSeek.addEventListener('input', ()=>{
  if(audioEl.duration){ audioEl.currentTime = pSeek.value/100*audioEl.duration; }
});
pPlay.addEventListener('click', ()=>{
  if(audioEl.src){ if(audioEl.paused){ audioEl.play(); pPlay.textContent='⏸ 暂停'; } else { audioEl.pause(); pPlay.textContent='▶ 播放'; } }
  else if(synthOn){ if(window.speechSynthesis && window.speechSynthesis.speaking){ window.speechSynthesis.pause(); pPlay.textContent='▶ 播放'; } else { playCurrent(); } }
});
pPrev.addEventListener('click', ()=>{
  const list = sectionSentences(sectionIdx);
  const idxInSec = list.findIndex(p=>p.gi===PLAYLIST[cur].gi);
  if(idxInSec>0){ cur--; playCurrent(); }
});
pNext.addEventListener('click', ()=>{
  const list = sectionSentences(sectionIdx);
  const idxInSec = list.findIndex(p=>p.gi===PLAYLIST[cur].gi);
  if(idxInSec < list.length-1){ cur++; playCurrent(); }
  else { goNextSection(); }
});

function renderSteps(){
  stepsEl.innerHTML='';
  SECTIONS.forEach((s,i)=>{
    const d=document.createElement('div');
    d.className='step'+(i===sectionIdx?' active':'')+(i<sectionIdx?' done':'');
    d.innerHTML='<span class="dot">'+(i<sectionIdx?'✓':(i+1))+'</span><span>'+s.title+'</span>';
    d.onclick=()=>{ if(i<=sectionIdx) goSection(i); };
    stepsEl.appendChild(d);
  });
}
function goSection(i){
  if(window.speechSynthesis) window.speechSynthesis.cancel();
  audioEl.pause();
  sectionIdx=i; render();
}
function goNextSection(){ if(sectionIdx < SECTIONS.length-1) goSection(sectionIdx+1); else finish(); }
function render(){
  renderSteps();
  const s = SECTIONS[sectionIdx];
  stage.innerHTML='';
  if(s.type==='speak') renderSpeak(s);
  else if(s.type==='quiz') renderQuiz(s);
  else if(s.type==='feynman') renderFeynman(s);
  if(s.type==='speak'){
    const list = sectionSentences(sectionIdx);
    if(list.length){ cur = PLAYLIST.indexOf(list[0]); }
    bar.style.display='flex';
    pPrev.disabled = (sectionSentences(sectionIdx).findIndex(p=>p.gi===PLAYLIST[cur].gi)===0);
    setMeta();
  } else {
    bar.style.display='none';
  }
  window.scrollTo({top:0, behavior:'smooth'});
}
function renderSpeak(s){
  const card=document.createElement('div'); card.className='card';
  let html='<h2>📣 '+s.title+'</h2>';
  if(s.img) html += '<div class="scene-img">'+s.img+'</div>';
  html += '<div class="scene-text" id="stext"></div>';
  card.innerHTML=html;
  if(s.rhyme){
    card.innerHTML += '<div class="rhyme"><b>'+s.rhyme.title+'</b><br>'+s.rhyme.lines.join('<br>')+'</div>';
  }
  card.innerHTML += '<div class="controls"><button class="btn" id="playBtn">▶ 听这一段</button>'+
    '<button class="btn ghost" id="allBtn">🔊 一口气听完</button>'+
    '<button class="btn good" id="nextBtn">下一步 ⏭</button></div>';
  stage.appendChild(card);
  const stext=card.querySelector('#stext');
  stext.textContent='';
  s.sentences.forEach((t,ji)=>{
    const sp=document.createElement('span'); sp.setAttribute('data-ji',ji); sp.textContent=t; stext.appendChild(sp);
    if(ji<s.sentences.length-1) stext.appendChild(document.createTextNode(''));
  });
  textContainer=stext;
  card.querySelector('#playBtn').onclick=()=>{ allMode=false; const list=sectionSentences(sectionIdx); cur=PLAYLIST.indexOf(list[0]); playCurrent(); };
  card.querySelector('#allBtn').onclick=()=>{ allMode=true; const list=sectionSentences(sectionIdx); cur=PLAYLIST.indexOf(list[0]); playCurrent(); };
  card.querySelector('#nextBtn').onclick=()=>goNextSection();
}
function renderQuiz(s){
  const q=s.quiz;
  const card=document.createElement('div'); card.className='quiz';
  card.innerHTML='<h2 style="margin-top:0">✋ '+s.title+'</h2><div class="q">'+q.q+'</div>';
  const optBox=document.createElement('div');
  q.opts.forEach((o,j)=>{
    const b=document.createElement('button'); b.className='opt'; b.textContent=o.t;
    b.onclick=()=>{
      if(answered.has(sectionIdx)) return;
      answered.add(sectionIdx);
      q.opts.forEach((_,k)=> optBox.children[k].disabled=true);
      if(o.ok){ b.classList.add('correct'); stars++; }
      else { b.classList.add('wrong'); const right=q.opts.findIndex(x=>x.ok); optBox.children[right].classList.add('correct'); }
      showFeedback(card,o.ok,q,stars);
    };
    optBox.appendChild(b);
  });
  card.appendChild(optBox);
  const roleBox=document.createElement('div');
  roleBox.innerHTML='<div class="role"><div class="who stu">🙋 同学</div><div class="say">'+q.stu+'</div></div>'+
    '<div class="role"><div class="who">👩‍🏫 晓晓</div><div class="say">'+q.teacher+'</div></div>';
  card.appendChild(roleBox);
  const ctrl=document.createElement('div'); ctrl.className='controls';
  ctrl.innerHTML='<button class="btn good" id="nextBtn">下一步 ⏭</button>';
  card.appendChild(ctrl);
  card.querySelector('#nextBtn').onclick=()=>goNextSection();
  stage.appendChild(card);
}
function showFeedback(card,ok,q,starCount){
  const fb=document.createElement('div');
  fb.className='feedback show '+(ok?'ok':'no');
  fb.innerHTML=(ok?'✅ 答对啦！你拿到一颗星星 ⭐（共 '+starCount+' 颗）':'❌ 再想想～正确答案已用绿色标出。')+
    '<div class="feynman"><h4>🧠 费曼记忆卡 · 记住这两点</h4><ul>'+q.card.map(c=>'<li>'+c+'</li>').join('')+'</ul></div>';
  card.appendChild(fb);
  const sp=document.querySelector('.badge'); if(sp) sp.textContent='🌟 晓晓老师课堂 · 已得 '+starCount+' ⭐';
}
function renderFeynman(s){
  const card=document.createElement('div'); card.className='card';
  card.innerHTML='<h2>'+s.title+'</h2><div class="scene-text">'+s.text+'</div>'+
    '<textarea id="fm" placeholder="在这里用你自己的话写一写（比如：他一句难听话是触发，我提前写好如果火起就退后、坐定就开番茄钟；出错时我觉察自责、手放胸口说慢慢来，先安抚再改活…）…"></textarea>'+
    '<div class="controls"><button class="btn" id="speakBtn">🎤 朗读我的回答</button>'+
    '<button class="btn good" id="finishBtn">完成本节课 ✅</button></div>';
  stage.appendChild(card);
  card.querySelector('#speakBtn').onclick=()=>{
    const txt=card.querySelector('#fm').value.trim();
    if(!txt){ setSub('先写几句再读哦～'); return; }
    if(synthOn){ window.speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance('你说：'+txt); u.lang='zh-CN'; u.rate=0.95; window.speechSynthesis.speak(u); }
    setSub('你说：'+txt);
  };
  card.querySelector('#finishBtn').onclick=()=>finish();
}
function finish(){
  if(window.speechSynthesis) window.speechSynthesis.cancel();
  audioEl.pause(); bar.style.display='none';
  stage.innerHTML='<div class="finish"><h2>🎉 下课啦，你真棒！</h2>'+
    '<p style="font-size:18pt">今天你拿到了 <b style="color:#d98324">'+stars+'</b> 颗星星 ⭐</p>'+
    '<div class="rhyme" style="text-align:left; display:inline-block; margin:10px auto;">'+
    '<b>🎵 今日新口诀（两新招）</b><br>'+
    '如果火起我就退，如果坐定就开钟；提前写进脑子里，现场不靠意志力。<br><br>'+
    '出错不是我一个，拍拍胸口对自己好；不骂自己不焦灼，心如止水静悄悄。<br><br>'+
    '<b>前16招回顾：</b>见本页上方「复习 · 十六招技能地图」卡片（五步刹车/静音/五感着陆/番茄/认知重评/方箱呼吸/第三人称抽离/冲动冲浪/情绪命名/10-10-10/身体急停/我信息/六秒法则/记账本/课题分离/两分钟启动）。'+
    '</div><p style="color:var(--soft)">记住：场合不是秀脾气的地方，只是说观点的地方；提前装好护栏、现场不炸，对自己温柔、心如止水，你会越来越稳。</p>'+
    '<div class="controls" style="justify-content:center"><button class="btn" onclick="location.reload()">🔁 再上一遍</button></div></div>';
  setSub('—— 今天的课结束啦，记得常回来练 ——');
}

(function(){
  const intro=document.createElement('div'); intro.className='card';
  intro.innerHTML='<h2>👋 准备好了吗？（第10天）</h2>'+
    '<div class="scene-text">这堂课大概 10 分钟。先带你复习前16招（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本、课题分离法、两分钟启动法），再讲一个新案例（2026-05-21 网易：药房男医生被一句小抱怨点着、当众扯白大褂要冲、同事死死拽住）和两招新本领（预设护栏法、自我慈悲法）。\n\n'+
    '晓晓老师会用神经网络语音一段一段讲，字幕在底部（不挡讲解）；讲到中间会突然提问你、还会模拟同学抢答，最后让你用自己的话讲一遍（费曼记忆法）。\n\n'+
    '建议戴上耳机，点下面「开始上课」就出发吧～</div>'+
    '<div class="controls"><button class="btn" id="startBtn">▶ 开始上课</button>'+
    '<button class="btn ghost" id="allBtn2">🔊 一口气听完讲解</button></div>';
  stage.appendChild(intro);
  document.getElementById('startBtn').onclick=()=>{ sectionIdx=0; render(); };
  document.getElementById('allBtn2').onclick=()=>{
    if(!PLAYLIST.length) return;
    sectionIdx=0; render();
    allMode=true; cur=0; playCurrent();
  };
  renderSteps();
})();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------- markdown 笔记
def build_markdown():
    L = []
    L.append("# 情绪管理课 · 晓晓老师课堂笔记（第10天 · ima 知识库 imao）\n")
    L.append("> 主题：克服专注力差、浮躁易怒、情绪化。核心理念：**场合不是展示真性情的地方，只是表达观点的地方。**\n")
    L.append("> 配套互动网页：`emotion-class-20260723.html`（晓晓老师 XiaoxiaoNeural 神经网络语音 + 不挡字幕 + 上一句/下一句可调位置 + 费曼式定时提问）。\n")
    L.append("> 第10天结构：**复习**前16招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本+课题分离+两分钟启动) → **新案例**(2026-05-21 网易：药房男医生被一句小抱怨点着、当众扯白大褂要冲、同事死死拽住) → **原理**(执行意图 if-then + 自我慈悲安抚系统) → **新招17**预设护栏法(列触发/写护栏/练自动) → **新招18**自我慈悲法(觉察/共通人性/善待自己) → 费曼自测。\n")
    L.append("\n## 一、复习：前16招（情绪技能地图）\n")
    L.append("- **①五步刹车法**：一停、二数、三命名、四转、五说——火气冒头先喊停，只说观点不秀脾气。\n")
    L.append("- **②静音模式（心如止水）**：心是一杯水，安静清、摇晃浑；场合里拍桌水洒难收，有火不泼别人。\n")
    L.append("- **③五感着陆法（54321）**：看五摸四听三声，闻二尝一拉回神；走神、坐不住时把心拉回当下。\n")
    L.append("- **④番茄专注法**：二十五分专注钟，五分休息不硬撑；手机扔远练定力。\n")
    L.append("- **⑤认知重评三步法**：停、揪出念头、换个想法；换想法就换情绪。\n")
    L.append("- **⑥方箱呼吸（4-7-8）**：吸气4憋7呼8憋4，画方箱一分钟降温；手抖想怼时用。\n")
    L.append("- **⑦第三人称抽离法**：退后、换角、劝友——把“我”换成“朋友视角”，火先降一半；上头那一秒用。\n")
    L.append("- **⑧冲动冲浪法**：认浪、看浪、等浪退，约十分钟浪自己走；冲动已起时用。\n")
    L.append("- **⑨情绪命名法**：精准起名、温度计打分、说或写下来；你不是情绪，你是给情绪起名的人。\n")
    L.append("- **⑩10-10-10 透视法**：10分后/10月后/10年后还重要吗？拉远看浮躁就散。\n")
    L.append("- **⑪身体急停法**：离开现场、冷水/温水、握拳松拳、脚踩地、暂不回消息；身体是情绪开关，先退烧再开口。\n")
    L.append("- **⑫我信息表达法**：事实→感受→需要→请求，用“我”开头、只说观点不人身攻击；场合里把观点稳稳送出去。\n")
    L.append("- **⑬六秒法则（慢半拍）**：火冒三丈先闭嘴、默数到六、等理智脑上线、再开口；嘴比脑子快时闭嘴就是赢。\n")
    L.append("- **⑭情绪记账本**：睡前三栏触发/念头/新招，天天记、天天安；情绪过去就复盘不重犯。\n")
    L.append("- **⑮课题分离法（阿德勒）**：同事甩脸是别人的课题、后果他们担；我的活儿我写好，别人的题我不扛。\n")
    L.append("- **⑯两分钟启动法**：大活先拆小步、只做两分不贪多，手指一动心就静；启动效应让浮躁散。\n")
    L.append("- 这十六招管“快炸/走神/不专注/念头歪/手抖想怼/上头那一秒/心里乱/一点就炸/身体先炸/想回嘴/情绪过去就忘/替别人内耗/大活不动手”。今天两招管最前面的“一点就炸（现场不炸）”和“跟自己过不去（不自我攻击）”。\n")
    L.append("\n## 二、今日新案例（2026-05-21 网易，医院药房窗口，人物化名）\n")
    L.append("素材：一位男医生，在药房窗口配药多年，平时话少、干活稳，最擅长“忍”。一名男患者来取特慢病药、没带身份证，按规定必须核验身份；医生照规矩说“系统过不了，您回家取证件再来”——这话没错。可患者当场当众高声骂他“白吃饭、不办事”，整个队伍都听见，医生低头忍了。患者拿完药折回来，对着工位低声嘀咕、言语讥讽。就这几句得理不饶人的抱怨，成了压垮他的最后一根稻草：他猛地起身，当众扯下白大褂狠狠甩在地上，红着眼眶要冲出去对峙，三四名同事死死拽住、劝了近十分钟才拦下，在场患者纷纷拍照。\n")
    L.append("- 关键解读（文内视角）：这不是一次冲突，是无数次委屈积压后的彻底宣泄。穿上白大褂他是医者、忍辱负重；脱下白大褂他只是个普通人，也会委屈、也会愤怒。可那一扯一甩，他输了体面，也给了别人“情绪失控”的把柄。\n")
    L.append("- 初中生版启示：这位医生不是脾气差，是“情绪账户”长期透支——平时一点一点往里存委屈、从不取出来管理，最后一句小抱怨就引爆（一点就炸、事后又后悔）。教训：情绪要日常“取出来”管理（用前16招），别等炸了才后悔。这正好对应你：心不够静、浮躁不安，一点就炸。\n")
    L.append("\n## 三、原理：两个道理（执行意图 if-then + 自我慈悲安抚系统）\n")
    L.append("- **道理一 执行意图（if-then 计划，心理学家盖洛韦）**：人脑喜欢“如果…就…”这条自动链路。你提前写好了“如果A发生，我就做B”，现场真遇到A，脑子会自动跳到B，不费意志力。实验里用了 if-then 计划的人，目标达成率高出两三倍。反过来，靠临场喊“我要冷静”这种空口号，火一上来全忘光。所以“一点就炸”的治本办法，不是等火来了再压，而是提前把“火来了怎么办”写成剧本存进脑子——现场触发自动执行，不靠快烧完的意志力。\n")
    L.append("- **道理二 自我慈悲（对自己温柔，神经科学）**：你一骂自己“没用、笨”，大脑就拉响警报——威胁系统启动，压力荷尔蒙皮质醇往上飙，你更焦虑、更易炸。反过来，对自己温柔一点（自我慈悲），会激活身体的“安抚系统”，让你平静下来。这跟“心如止水”一模一样——对自己狠，心就翻江倒海；对自己好，心才静得下来。所谓心如止水，是先对自己止争。\n")
    L.append("- 一句话：现场不炸靠“提前写剧本”（执行意图）；不跟自己过不去靠“对自己温柔”（自我慈悲）。道理一→预设护栏法；道理二→自我慈悲法。\n")
    L.append("\n## 四、新招17：预设护栏法（执行意图 if-then，提前装护栏、现场不炸）\n")
    L.append("适用：一遇上刺激就火冒三丈、控制不住脾气；或一坐到工位就忍不住摸手机、浮躁坐不住。一句话——把“遇到刺激我怎么办”提前写成“如果…就…”剧本，存进脑子，现场自动执行，不靠意志力。三步：\n")
    L.append("- **①列触发**：想清楚最容易让你炸、最容易让你摸手机的场景（同事甩脸、被当众说、坐到工位想摸手机、收到难听话），写下来存手机置顶。\n")
    L.append("- **②写护栏**：给每条触发配一个“就”动作（要具体、能马上做）——如果同事甩脸，我就先退后一步喝口水；如果坐到工位，我就先开25分钟番茄钟、手机扔抽屉；如果火冒三丈，我就闭嘴数六。\n")
    L.append("- **③练成自动**：每天上班前扫一眼这条清单，像过安检。练几次，现场一遇到，身体自动就做了——你甚至不用想。对“一点就炸”和“浮躁坐不住想摸机”都管用。\n")
    L.append("- 要点：别等火来了硬扛，提前把剧本写好，像给心装一道护栏，小火苗刚冒头就被挡在门外。这招直接呼应核心理念——场合是表达观点的地方，你用护栏保住理智，说出来的才是观点不是脾气。退后是聪明不是怂：拉距离=给火断氧，回来只说观点。\n")
    L.append("\n**预设护栏口诀**\n")
    L.append("> 如果火起我就退，如果坐定就开钟；提前写进脑子里，现场不靠意志力。\n")
    L.append("\n## 五、新招18：自我慈悲法（对自己温柔，不自我攻击）\n")
    L.append("适用：一出错/浮躁/被说就骂自己“没用、怎么又搞砸”，越骂越急躁越乱。一句话——出错、浮躁、被说时，别骂自己，像安慰好朋友一样安慰自己。三步：\n")
    L.append("- **①觉察**：发现自己又在骂自己时，先喊停、看见这个念头。你不是“没用的人”，你只是“此刻有点乱”。\n")
    L.append("- **②共通人性**：提醒自己“人人都会出错、人人都会浮躁，这不只我一个”。谁没崩过？你不是怪胎。\n")
    L.append("- **③善待自己**：把手放胸口，对自己说一句温柔的话——“辛苦了，慢慢来，我可以的”。这一句像给心打镇静剂，催你平静，而不是越骂越炸。先安抚，再改活（顺序别反）。\n")
    L.append("- 要点：你对自己狠，心就翻江倒海、越急越乱；你对自己好，心才静得下来。浮躁不是你差，是心累了；拍拍它，继续走。这招和情绪命名是搭档——先给情绪起名，再对它慈悲。研究说，自我慈悲的人犯错后恢复更快、更愿意改。\n")
    L.append("\n**自我慈悲口诀**\n")
    L.append("> 出错不是我一个，拍拍胸口对自己好；不骂自己不焦灼，心如止水静悄悄。\n")
    L.append("\n## 六、费曼自测题（旧+新结合）\n")
    L.append("用自己的话回答：*如果下次我又被一句难听话点着、火一下窜上来，或者一坐到工位就忍不住摸手机、还因为写岔了活儿在心里骂自己没用，我会怎么做，才能既不当场炸、又能管住浮躁、还不对自已太狠、把该干的活干好？*\n")
    L.append("标准答案要点：\n")
    L.append("1. 先预设护栏（列触发/写护栏/练自动）：把“遇到刺激怎么办”写成“如果…就…”剧本——火起→退后喝口水、闭嘴数六；坐定→开番茄钟手机扔远；提前写进脑子、天天练成肌肉记忆，现场自动执行不靠意志。\n")
    L.append("2. 身体被勾动时——身体急停法（离开/喝口水/握拳松拳）先降温；想回怼时——六秒法则（闭嘴数六）+我信息只说观点；上头时——第三人称抽离+冲动冲浪；一点小火苗先五步刹车。\n")
    L.append("3. 对自己温柔（自我慈悲）：觉察“我在骂自己”→共通人性“人人会错不全我”→手放胸口说“慢慢来我可以”，用安抚代替自责（自责→皮质醇↑更炸；慈悲→安抚系统→更快改好）。先安抚再改活。\n")
    L.append("4. 面对大活/浮躁坐不住——两分钟启动法（拆成只写标题这种小步→定两分钟闹钟只做一点→动起来启动效应推着走），再用番茄专注+五感着陆养专注；别人脸色→课题分离（别人的题不扛）。始终记：场合不是秀脾气的地方，只是说观点的地方；提前装好护栏、现场不炸，对自己温柔、心如止水。\n")
    L.append("\n## 七、今日带走的两句新口诀\n")
    L.append("1. 预设护栏法：如果火起我就退，如果坐定就开钟；提前写进脑子里，现场不靠意志力。\n")
    L.append("2. 自我慈悲法：出错不是我一个，拍拍胸口对自己好；不骂自己不焦灼，心如止水静悄悄。\n")
    L.append("3. 一句话收尾：场合不是秀脾气的地方，只是说观点的地方；提前装好护栏、现场不炸，对自己温柔、心如止水，你会越来越稳。\n")
    return "\n".join(L)

# ---------------------------------------------------------------- 主流程
def main():
    audio = build_audio()
    sections_js = "window.SECTIONS = " + json.dumps(SECTIONS, ensure_ascii=False) + ";"
    audio_js = "window.AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";"
    html = HTML.replace("__LESSON_DATA__", sections_js).replace("__AUDIO_DATA__", audio_js)
    out_html = os.path.join(WS, "emotion-class-20260723.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html] 写出 {out_html} ({len(html)/1024:.0f} KB)")
    md = build_markdown()
    out_md = os.path.join(WS, "情绪管理-晓晓老师课堂笔记.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出 {out_md} ({len(md)/1024:.0f} KB)")
    dated = os.path.join(WS, "情绪管理-晓晓老师课堂笔记_20260723.md")
    with open(dated, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出带日期副本 {dated} ({len(md)/1024:.0f} KB)")
if __name__ == "__main__":
    main()
