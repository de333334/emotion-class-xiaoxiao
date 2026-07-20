# -*- coding: utf-8 -*-
"""
情绪管理课 builder（2026-07-20 · 第七天）
- 单一内容源 -> 生成 晓晓老师(XiaoxiaoNeural) 每句语音(base64 内联)
- 输出「独立」单文件自包含 emotion-class-20260720.html (宋体/可调播放位置/上一句下一句/不挡字幕/费曼提问)
  ※ 每天一个新文件，绝不覆盖旧课页面（满足"每个网页对应一课不要更新网页"）
- 同时输出 情绪管理-晓晓老师课堂笔记.md 与 带日期副本 供存入 ima 知识库 imao
本日结构：复习前10招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10)
  -> 新案例(2026 今日头条热帖：陈峰会议室拍桌摔门被裁 vs 林薇喝茶水间10分钟冷静补救)
  -> 原理(身体是情绪开关 + 表达分层金字塔)
  -> 新招1 身体急停法 -> 新招2 我信息表达法(非暴力沟通) -> 费曼自测
"""
import os, json, base64, asyncio, sys, shutil

WS = "C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-8%"
PITCH = "+0Hz"

# ---------------------------------------------------------------- 案例插画（内联 SVG，保证离线可开）
SVG_MAP = '''<svg viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg">
  <text x="340" y="22" font-size="16" fill="#5b8def" text-anchor="middle" font-family="sans-serif">🗺️ 情绪技能地图 · 前10招复习</text>
  <g font-family="sans-serif" font-size="11.5">
   <rect x="12" y="40" width="123" height="88" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="73" y="66" fill="#2b6fb0" text-anchor="middle" font-weight="bold">①五步刹车</text>
   <text x="73" y="88" fill="#243447" text-anchor="middle">停·数·命名·转·说</text>
   <text x="73" y="110" fill="#6b7c8f" text-anchor="middle">🔥快炸时灭火</text>
   <rect x="145" y="40" width="123" height="88" rx="12" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="206" y="66" fill="#1c7a4d" text-anchor="middle" font-weight="bold">②静音模式</text>
   <text x="206" y="88" fill="#243447" text-anchor="middle">心是一杯水</text>
   <text x="206" y="110" fill="#6b7c8f" text-anchor="middle">💧有火不泼人</text>
   <rect x="278" y="40" width="123" height="88" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="339" y="66" fill="#c98a14" text-anchor="middle" font-weight="bold">③五感着陆</text>
   <text x="339" y="88" fill="#243447" text-anchor="middle">看5摸4听3</text>
   <text x="339" y="110" fill="#6b7c8f" text-anchor="middle">🌀走神时着陆</text>
   <rect x="411" y="40" width="123" height="88" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="472" y="66" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④番茄专注</text>
   <text x="472" y="88" fill="#243447" text-anchor="middle">25分只做一事</text>
   <text x="472" y="110" fill="#6b7c8f" text-anchor="middle">🍅练定力</text>
   <rect x="544" y="40" width="123" height="88" rx="12" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="605" y="66" fill="#d6455f" text-anchor="middle" font-weight="bold">⑤认知重评</text>
   <text x="605" y="88" fill="#243447" text-anchor="middle">停·揪·换想法</text>
   <text x="605" y="110" fill="#6b7c8f" text-anchor="middle">🧠换念换情绪</text>
   <rect x="12" y="140" width="123" height="88" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="73" y="166" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑥方箱呼吸</text>
   <text x="73" y="188" fill="#243447" text-anchor="middle">吸4憋7呼8憋4</text>
   <text x="73" y="210" fill="#6b7c8f" text-anchor="middle">🌬️手抖时降温</text>
   <rect x="145" y="140" width="123" height="88" rx="12" fill="#eef7f2" stroke="#2bb673" stroke-width="2"/>
   <text x="206" y="166" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑦第三人称抽离</text>
   <text x="206" y="188" fill="#243447" text-anchor="middle">退后·换角·劝友</text>
   <text x="206" y="210" fill="#6b7c8f" text-anchor="middle">👁旁观一眼冷</text>
   <rect x="278" y="140" width="123" height="88" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="339" y="166" fill="#5b3fd6" text-anchor="middle" font-weight="bold">⑧冲动冲浪</text>
   <text x="339" y="188" fill="#243447" text-anchor="middle">认浪·看浪·等浪退</text>
   <text x="339" y="210" fill="#6b7c8f" text-anchor="middle">🌊浪过你还在</text>
   <rect x="411" y="140" width="123" height="88" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="472" y="166" fill="#c98a14" text-anchor="middle" font-weight="bold">⑨情绪命名</text>
   <text x="472" y="188" fill="#243447" text-anchor="middle">起名·打分·说写</text>
   <text x="472" y="210" fill="#6b7c8f" text-anchor="middle">🏷️乱时先起名</text>
   <rect x="544" y="140" width="123" height="88" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="605" y="166" fill="#2b6fb0" text-anchor="middle" font-weight="bold">⑩10-10-10</text>
   <text x="605" y="188" fill="#243447" text-anchor="middle">10分·10月·10年</text>
   <text x="605" y="210" fill="#6b7c8f" text-anchor="middle">🔭拉远看开</text>
  </g>
</svg>'''

SVG_CASE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <rect width="640" height="250" fill="#fdf3f1"/>
  <text x="320" y="24" font-size="15" fill="#c0492a" text-anchor="middle" font-family="sans-serif">案例：被一句话点着，陈峰拍桌摔门被裁 / 林薇喝十分钟咖啡稳住</text>
  <!-- 陈峰：拍桌摔门 -->
  <circle cx="118" cy="82" r="28" fill="#ffd9b8"/>
  <path d="M92 164 Q118 120 144 164 Z" fill="#6b8fd6"/>
  <path d="M104 76 l10 8 M132 76 l-10 8" stroke="#c0392b" stroke-width="3.2"/>
  <path d="M106 96 q12 12 24 0" stroke="#c0392b" stroke-width="3" fill="none"/>
  <rect x="56" y="114" width="124" height="40" rx="12" fill="#fff" stroke="#ff8a8a" stroke-width="1.6"/>
  <text x="118" y="131" font-size="10.5" fill="#c0392b" text-anchor="middle" font-family="sans-serif">“你懂个屁的技术！”</text>
  <text x="118" y="158" font-size="10.5" fill="#c0392b" text-anchor="middle" font-family="sans-serif">😡 拍桌·摔门而出</text>
  <text x="118" y="200" font-size="12.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">陈峰：秀脾气→半年后被裁</text>
  <text x="320" y="118" font-size="30" fill="#c0492a" text-anchor="middle">VS</text>
  <!-- 林薇：喝茶水间 -->
  <circle cx="500" cy="82" r="28" fill="#ffd9b8"/>
  <path d="M474 164 Q500 126 526 164 Z" fill="#9a9a9a"/>
  <circle cx="491" cy="80" r="3" fill="#3a3a3a"/><circle cx="509" cy="80" r="3" fill="#3a3a3a"/>
  <path d="M489 90 q11 7 22 0" stroke="#1c7a4d" stroke-width="2.4" fill="none"/>
  <rect x="452" y="112" width="96" height="44" rx="10" fill="#fff" stroke="#bfe3c9" stroke-width="1.6"/>
  <path d="M470 134 h60 v-14 h-44 v-6" fill="none" stroke="#9a6b3f" stroke-width="2.4"/>
  <text x="500" y="170" font-size="10.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">☕ 慢慢喝十分钟</text>
  <text x="500" y="200" font-size="12.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">林薇：先降温→冷静补救</text>
  <text x="320" y="238" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">同样被点燃，一冷一热，结局天差地别：场合只说观点，不秀脾气</text>
</svg>'''

SVG_PRINCIPLE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">两个道理：身体是情绪的开关 · 表达是分层的金字塔</text>
  <g font-family="sans-serif">
   <rect x="20" y="40" width="290" height="192" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="165" y="66" font-size="13.5" fill="#2b6fb0" text-anchor="middle" font-weight="bold">道理一 · 身体是开关</text>
   <circle cx="100" cy="120" r="22" fill="#ffd6cf"/><text x="100" y="125" font-size="14" text-anchor="middle">🔥</text>
   <text x="100" y="158" font-size="10.5" fill="#c0492a" text-anchor="middle">身体先炸</text>
   <path d="M128 120 h18 M146 112 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <circle cx="200" cy="120" r="22" fill="#cfe6ff"/><text x="200" y="125" font-size="14" text-anchor="middle">🧊</text>
   <text x="200" y="158" font-size="10.5" fill="#1c7a9c" text-anchor="middle">身体降温</text>
   <path d="M222 120 h16" stroke="#9aa7bd" stroke-width="3" stroke-dasharray="4 3"/>
   <circle cx="270" cy="120" r="22" fill="#d6f5e3"/><text x="270" y="125" font-size="14" text-anchor="middle">❄️</text>
   <text x="270" y="158" font-size="10.5" fill="#1c7a4d" text-anchor="middle">理智回来</text>
   <text x="165" y="196" font-size="10.5" fill="#243447" text-anchor="middle">脸红手抖呼吸短→</text>
   <text x="165" y="214" font-size="10.5" fill="#1c7a4d" text-anchor="middle">先给身体退烧，火才灭</text>
   <rect x="340" y="40" width="290" height="192" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="485" y="66" font-size="13.5" fill="#5b3fd6" text-anchor="middle" font-weight="bold">道理二 · 表达金字塔</text>
   <polygon points="485,200 415,200 485,162 555,200" fill="#ffd6cf" stroke="#c0492a" stroke-width="1.6"/>
   <text x="485" y="190" font-size="10" fill="#c0492a" text-anchor="middle">人身攻击✗</text>
   <polygon points="485,158 435,158 485,124 535,158" fill="#e6e0f2" stroke="#b9a9e6" stroke-width="1.4"/>
   <text x="485" y="151" font-size="9.5" fill="#5b3fd6" text-anchor="middle">请求</text>
   <polygon points="485,122 447,122 485,94 523,122" fill="#efeaf7" stroke="#b9a9e6" stroke-width="1.4"/>
   <text x="485" y="116" font-size="9.5" fill="#5b3fd6" text-anchor="middle">需要·观点</text>
   <polygon points="485,92 459,92 485,70 511,92" fill="#f5f0ff" stroke="#b9a9e6" stroke-width="1.4"/>
   <text x="485" y="87" font-size="9" fill="#5b3fd6" text-anchor="middle">事实</text>
   <text x="485" y="218" font-size="9.5" fill="#6b7c8f" text-anchor="middle">站在事实→观点→请求，别掉到人身攻击</text>
  </g>
</svg>'''

SVG_BODY = '''<svg viewBox="0 0 640 210" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">身体急停法：气冲头顶，先给身体灭火再开口</text>
  <g font-family="sans-serif">
   <rect x="14" y="42" width="116" height="120" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="72" y="70" font-size="13.5" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 离开</text>
   <text x="72" y="94" font-size="11" fill="#243447" text-anchor="middle">转身离开</text>
   <text x="72" y="112" font-size="11" fill="#243447" text-anchor="middle">发火现场</text>
   <text x="72" y="134" font-size="11" fill="#243447" text-anchor="middle">眼不见火少</text>
   <path d="M134 102 l18 0 M150 94 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="156" y="42" width="116" height="120" rx="14" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="214" y="70" font-size="13.5" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 冷/温</text>
   <text x="214" y="94" font-size="11" fill="#243447" text-anchor="middle">冷水洗脸</text>
   <text x="214" y="112" font-size="11" fill="#243447" text-anchor="middle">或慢喝温水</text>
   <text x="214" y="134" font-size="11" fill="#243447" text-anchor="middle">心跳呼吸慢</text>
   <path d="M276 102 l18 0 M292 94 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="298" y="42" width="116" height="120" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="356" y="70" font-size="13.5" fill="#c98a14" text-anchor="middle" font-weight="bold">③ 握松</text>
   <text x="356" y="94" font-size="11" fill="#243447" text-anchor="middle">握拳五秒</text>
   <text x="356" y="112" font-size="11" fill="#243447" text-anchor="middle">猛地松开</text>
   <text x="356" y="134" font-size="11" fill="#243447" text-anchor="middle">重复三次</text>
   <path d="M418 102 l18 0 M434 94 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="440" y="42" width="116" height="120" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="498" y="70" font-size="13.5" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④ 踩地</text>
   <text x="498" y="94" font-size="11" fill="#243447" text-anchor="middle">双脚踩实</text>
   <text x="498" y="112" font-size="11" fill="#243447" text-anchor="middle">默数深呼吸</text>
   <text x="498" y="134" font-size="11" fill="#243447" text-anchor="middle">钉在当下</text>
   <path d="M560 102 l18 0 M576 94 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="582" y="42" width="48" height="120" rx="14" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="606" y="70" font-size="12.5" fill="#d6455f" text-anchor="middle" font-weight="bold">⑤</text>
   <text x="606" y="92" font-size="10" fill="#243447" text-anchor="middle">暂不</text>
   <text x="606" y="108" font-size="10" fill="#243447" text-anchor="middle">回消息</text>
   <text x="606" y="124" font-size="10" fill="#243447" text-anchor="middle">手机扣</text>
   <text x="606" y="140" font-size="10" fill="#243447" text-anchor="middle">过去</text>
   <text x="320" y="196" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">哪步方便用哪步；身体退烧，理智才回得来</text>
  </g>
</svg>'''

SVG_IMESSAGE = '''<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#5b3fd6" text-anchor="middle" font-family="sans-serif">我信息表达法（非暴力沟通）：事实→感受→需要→请求</text>
  <g font-family="sans-serif">
   <rect x="40" y="44" width="540" height="34" rx="12" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="310" y="66" font-size="13" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 事实：只说发生了什么，不带骂（"我那段被打断了三次"）</text>
   <rect x="80" y="86" width="500" height="34" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="330" y="108" font-size="13" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 感受：用"我"开头（"我有点着急"）不说"你讨厌"</text>
   <rect x="120" y="128" width="460" height="34" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="350" y="150" font-size="13" fill="#c98a14" text-anchor="middle" font-weight="bold">③ 需要：我想要什么（"因为我想把方案讲完"）</text>
   <rect x="160" y="170" width="420" height="34" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="370" y="192" font-size="13" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④ 请求：具体请对方做啥（"下次让我先讲完？"）</text>
   <text x="320" y="216" font-size="11.5" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">用"我"开头、只送观点不人身攻击 → 场合里人人服</text>
  </g>
</svg>'''

# ---------------------------------------------------------------- 课程内容（第七天）
SECTIONS = [
  {"type":"speak","title":"开场 · 第七天，先串起前10招","rhyme":None,"img":None,"sentences":[
    "同学你好，我是晓晓老师。咱们的情绪管理课到第七天啦！前六天你攒了十招本领：第一天五步刹车加静音模式，第三天五感着陆加番茄专注，第四天认知重评加方箱呼吸，第五天第三人称抽离加冲动冲浪，第六天情绪命名法加10-10-10透视法。今天先把这十招串成一张'情绪技能地图'，再教你两招新本领，专治'身体先炸、一开口就人身攻击、明明只想表达观点却变成了发火'。",
    "先复习老口号：任何场合——办公室、工作群、会议室——都不是展示真性情的地方，它只是表达观点的地方。你是去'把事说清楚'的，不是去'把脾气秀出来'的。",
    "今天要补的，是你最容易吃亏的一类时刻：气已经冲到头顶、脸红手抖，或者明明想提个意见，一张嘴却变成'你懂个屁'这种人身攻击。咱们先用一个 2026 年网上热传的真事开场。"
  ]},

  {"type":"speak","title":"复习 · 十招技能地图","rhyme":None,"img":SVG_MAP,"sentences":[
    "先复习十招，编成一张地图。第一招五步刹车——一停二数三命名，四转五说；火气冒头先喊停，只说观点不秀脾气。第二招静音模式——心是一杯水，摇浑放自清，收拾不了局别纵脾气。",
    "第三招五感着陆——看五摸四听三声，闻二尝一拉回神；走神坐不住用它。第四招番茄专注——二十五分专注钟，五分休息不硬撑，手机扔远练定力。第五招认知重评——火起先喊停、揪出念头、换个想法，换想法就换情绪。",
    "第六招方箱呼吸——吸气四憋七呼八憋四，画方箱一分钟降温。第七招第三人称抽离——退后、换角、劝友，把'我'换成'朋友视角'火就小。第八招冲动冲浪——认浪、看浪、等浪退，约十分钟浪自己走。",
    "第九招情绪命名法——精准起名、温度计打分、说或写下来，你不是情绪你是起名的人。第十招10-10-10透视法——10分后10月后10年后还重要吗，拉远看浮躁就散。今天两招管最前面的'身体开关'和'怎么开口只说观点'。"
  ]},

  {"type":"quiz","title":"复习小测 · 走神时用哪招","quiz":{
    "q":"你正想专注干活，手机一响就走神刷了半小时。前10招里你该用哪一招把心拉回来、练定力？",
    "opts":[
      {"t":"五感着陆（54321，把心拉回当下）+ 番茄专注（手机扔远，25分只做一事）","ok":True},
      {"t":"冲动冲浪（那是管'冲动已起想发作'，不是走神）","ok":False},
      {"t":"方箱呼吸（那是手抖想怼时降温，不是走神）","ok":False}
    ],
    "stu":"小宇抢答：老师，走神是不是用冲动冲浪压一压？",
    "teacher":"晓晓老师笑：冲动冲浪是给'已经上头、想怼人'那股浪用的。你这是走神、定力差，得用第三招五感着陆（看5摸4听3把心拉回当下）和第四招番茄专注（手机扔远、25分钟只做一件事）。各招分工不同：走神→五感+番茄；想怼→冲浪+方箱。",
    "card":["走神/不专注 = 五感着陆(54321) + 番茄专注(25分只做一事，手机扔远)。","冲浪管冲动、方箱管手抖，别乱用。"]
  }},

  {"type":"speak","title":"第一幕 · 新案例：会议室拍桌摔门的总监","rhyme":None,"img":SVG_CASE,"sentences":[
    "讲个 2026 年网上热传的职场真事（来源今日头条热帖，人物化名）。主人公陈峰，某公司前途无量的项目总监，能力顶尖，但脾气一点就着。",
    "半年前一次跨部门协调会，因为技术方案和产品部僵持不下。对方负责人说了句：'你这想法太理想化，不考虑现实成本。'——就这一句话，点燃了陈峰。他当场拍桌而起，指着对方鼻子吼：'你懂个屁的技术！除了会卡成本，你还会什么？！'然后在所有人错愕的目光里，摔门而出。",
    "他以为这是'据理力争'。可后果远超想象：合作部门寒了心、从此能拖就拖；'情绪不稳定、难合作'成了撕不掉的标签；大老板只说了一句：'连自己情绪都管理不好，我怎么敢把几百人的团队交给他？'半年后公司调整，他上了首批裁员名单——五年口碑，被那几分钟怒火烧光。",
    "反过来看同公司的另一位负责人林薇。她也遇到更棘手的局面：关键上线前夜，核心程序员突然撂挑子，团队熬了仨月的心血眼看要黄，有人急哭了。林薇当时脸也白了——但她做了一件事：转身走进茶水间，给自己冲了杯很烫的咖啡，盯着、一口一口慢慢喝，整整十分钟。",
    "十分钟后她走回办公室，脸上已看不到慌乱。她平静地布置了三步补救，核心功能准时上线。你看，同样是被点燃，陈峰用'拍桌摔门'把场合变成了秀脾气，林薇用'十分钟的咖啡'先把身体的火降下来，再只说观点——这一冷一热，结局天差地别。"
  ]},

  {"type":"quiz","title":"课间提问① · 陈峰最吃亏在哪","quiz":{
    "q":"陈峰最吃亏的地方在哪？",
    "opts":[
      {"t":"他技术真的太差，被产品部看不起","ok":False},
      {"t":"他能力不差，但把会议室当成了秀真性情、发泄脾气的地方，用'你懂个屁'的人身攻击代替了'对方案提意见'，最后丢了职业形象","ok":True},
      {"t":"产品部故意害他，所以他冤","ok":False}
    ],
    "stu":"小雅：可对方先说'理想化不考虑成本'，不也挑衅吗？",
    "teacher":"晓晓老师点头：对方的话刺耳，可以先记着（第三人称抽离+情绪命名）。但陈峰错在'表达'——场合是讲观点的地方，不是倒情绪的地方。你一拍桌、一人身攻击，别人就不听你方案了，还给你贴'难合作'标签。林薇示范了对的：先冷却身体，再只说观点。",
    "card":["陈峰崩在：能力不差，却把会议室当倒情绪/秀真性情的地方，用'你懂个屁'人身攻击代替提意见。","场合只说观点；情绪归情绪，诉求归诉求。"]
  }},

  {"type":"speak","title":"第二幕 · 原理：身体是开关 + 表达金字塔","rhyme":None,"img":SVG_PRINCIPLE,"sentences":[
    "为什么林薇'喝十分钟咖啡'就稳了？又为什么陈峰'一拍桌'就收不回？科学家讲了两个道理，初中生都懂。",
    "道理一：身体是情绪的开关（情绪具身化）。你生气时，身体先有反应——脸红、心跳快、手抖、呼吸变短。但反过来也成立：你一调身体，脑子就跟着冷静。就像你发烧先捂汗没用，得先退烧；情绪'烧'起来，先给身体降温，理智才回得来。林薇那十分钟，就是给身体'退了烧'。",
    "道理二：表达是分层的金字塔。最底下是'事实'（发生了什么），往上是'感受'（我怎么了），再往上是'观点'（我的看法），最顶上是'请求'（我要什么）。陈峰只站在'人身攻击'那一层乱敲；林薇站在'事实+安排'那两层，把观点稳稳说出来。记住：场合里你该站在'事实→观点→请求'这三层，别掉到'人身攻击'那一层。",
    "一句话：情绪从身体起，也从身体灭；观点要分层说，别把脾气混进去。道理一对应'身体急停法'，道理二对应'我信息表达法'。"
  ]},

  {"type":"quiz","title":"课间提问② · 为什么先调身体有用","quiz":{
    "q":"为什么'先去茶水间喝杯咖啡、等十分钟'能让你不发火？",
    "opts":[
      {"t":"因为拖十分钟，事情就没人管了","ok":False},
      {"t":"因为身体是情绪的开关：脸红手抖呼吸短是身体先炸，先给身体降温（离开现场、慢慢喝温水），理智才回得来，火才灭","ok":True},
      {"t":"因为喝咖啡提神，更能吵赢","ok":False}
    ],
    "stu":"小杰：那我强忍着不说话，不也行？",
    "teacher":"晓晓老师摇头：强忍是'把火压进瓶子'，迟早炸。林薇不是忍，是'先离开现场+用动作给身体降温'（慢慢喝热咖啡），让生理的火自己退下去，这叫主动降温，不是憋着。身体凉了，话才说得准。",
    "card":["身体是情绪开关：先降温（离开/喝温水/慢动作）理智才回；强忍是憋火，会炸。","情绪从身体起，也从身体灭。"]
  }},

  {"type":"speak","title":"第三幕 · 新招1：身体急停法（先给身体灭火）","rhyme":{
    "title":"🎵 急停口诀",
    "lines":["<b>气冲头顶脸发红</b>，先别开口别发疯；","转身<b>离开</b>喝口温，<b>握拳松拳脚踩地</b>。","<b>暂不回消息</b>手机扣，身体退烧理智回；","再开口只说事，<b>场合不秀脾气</b>。"]
  },"img":SVG_BODY,"sentences":[
    "新本领第一招：身体急停法。一句话——气冲到头顶、脸红手抖时，先别开口，用身体的动作把'火'降下来，再说话。五步任选，哪里方便用哪里：",
    "第一步'离开现场'：陈峰是当场拍桌，林薇是转身进茶水间。这一步最关键——物理上离开发火的地方，眼睛不见、火就少一半。",
    "第二步'冷水或温水'：用冷水洗把脸，或像林薇一样慢慢喝杯温水。冷/温的刺激能让心跳和呼吸慢下来，这是真有科学依据的降温。",
    "第三步'握拳松拳'：用力握拳五秒、再猛地松开，重复三次。把手上的'想打人、想砸'的劲，变成可控制的松紧，不伤人也发泄了。",
    "第四步'脚踩地'：双脚踩实地面，感受地板托住你，默数三次深呼吸。把自己'钉'在当下，不飘、不炸。",
    "第五步'暂不回消息'：气头上别在群里回、别发语音，把手机扣过去十分钟。等身体凉了再回，话就准了。",
    "记住：情绪从身体起，也从身体灭。你不是你的火，你是那个'先给身体退退烧，再开口'的人。",
    "记口诀：气冲头顶脸发红，先别开口别发疯；转身离开喝口温，握拳松拳脚踩地。暂不回消息手机扣，身体退烧理智回；再开口只说事，场合不秀脾气。"
  ]},

  {"type":"quiz","title":"课间提问③ · 身体急停法怎么用","quiz":{
    "q":"你在会上被当众怼了一句，脸一下红了、手发抖，想立刻回怼。按身体急停法，第一步该做啥？",
    "opts":[
      {"t":"当场拍桌回怼，不能怂","ok":False},
      {"t":"先离开现场（或低头喝口水、握拳松拳），给身体降温，等理智回来再开口","ok":True},
      {"t":"强忍着不说话但心里记仇","ok":False}
    ],
    "stu":"小琳：离开现场会不会显得我输了？",
    "teacher":"晓晓老师摇头：离开不是认输，是'先给身体退烧'。你脸红手抖时说的每句都是火上浇油，林薇离开茶水间十分钟，回来反而赢得尊重。身体凉了，你再开口说观点才稳。场合里，稳住的人才掌局。",
    "card":["身体急停法：①离开现场②冷水/温水③握拳松拳④脚踩地⑤暂不回消息。","先退烧再开口；离开不是认输是掌局。"]
  }},

  {"type":"speak","title":"第四幕 · 新招2：我信息表达法（只说观点不人身攻击）","rhyme":{
    "title":"🎵 我信息口诀",
    "lines":["想提意见<b>别开火</b>，<b>我信息法</b>四步走；","先说<b>事实</b>不带骂，再讲<b>感受</b>用我开头。","<b>需要</b>什么说清楚，具体<b>请求</b>送到手；","人身攻击最掉价，<b>只说观点人人服</b>。"]
  },"img":SVG_IMESSAGE,"sentences":[
    "新本领第二招：我信息表达法（也叫非暴力沟通）。一句话——在场合里提意见、说诉求时，按'事实→感受→需要→请求'四步说，只讲观点不人身攻击。",
    "第一步'说事实'：只说发生了什么，不带骂人。比如'刚才会上，我那段话被打断了三次'，而不是'你老是打断我'。",
    "第二步'说感受'：用'我'开头讲自己的情绪。比如'我有点着急'，而不是'你真讨厌'。",
    "第三步'说需要'：你想要什么。比如'因为我想把方案完整地讲完'。把'你针对我'换成'我需要被听完'。",
    "第四步'说请求'：具体、可操作地请对方怎么做。比如'下次能不能让我先讲完，再讨论？'——这就把观点清清楚楚送出去了，谁都挑不出你发火。",
    "你看林薇那三句话就是模板：先说事实（现在问题是补救）、再说安排（A去联系外援、B拆解功能、C安抚团队）。她没骂谁、没甩锅，纯观点，所以大家服。",
    "记口诀：想提意见别开火，我信息法四步走；先说事实不带骂，再讲感受用我开头。需要什么说清楚，具体请求送到手；人身攻击最掉价，只说观点人人服。"
  ]},

  {"type":"quiz","title":"课间提问④ · 我信息表达法怎么用","quiz":{
    "q":"同事又抢了你的功劳，你很气。用'我信息表达法'，你会怎么开口？",
    "opts":[
      {"t":"'你又抢我功劳，太不要脸了！'","ok":False},
      {"t":"'这次汇报里那部分是我做的（事实），我有点失落（感受），因为我希望付出被看见（需要），下次能不能在PPT里署我的名（请求）？'","ok":True},
      {"t":"'算了我不说了，反正没人听'","ok":False}
    ],
    "stu":"小强：直接骂不是更解气？",
    "teacher":"晓晓老师摆手：骂一句'不要脸'，同事立刻自我保护，反而更不承认，还给你贴'情绪化'标签。用我信息：先事实、再感受、再需要、再请求，对方听得进去，你的功劳也讨回来了。场合是讲观点的地方，我信息就是'把观点稳稳送出去'的快递盒。",
    "card":["我信息表达法：事实→感受→需要→请求，用'我'开头、不人身攻击。","场合只送观点；骂人=贴情绪化标签。"]
  }},

  {"type":"speak","title":"结尾 · 今天你带走什么（前10招+两新招）","rhyme":None,"img":None,"sentences":[
    "今天的课到这儿，晓晓老师带你总复习。",
    "前10招（复习）：五步刹车——一停二数三命名四转五说；静音模式——心是一杯水；五感着陆——看五摸四听三声；番茄专注——二十五分只做一事；认知重评——停揪换、换想法就换情绪；方箱呼吸——吸4憋7呼8憋4；第三人称抽离——退后换角劝友；冲动冲浪——认浪看浪等浪退；情绪命名法——精准起名温度计打分说写下来；10-10-10透视法——10分10月10年后拉远看。",
    "新本领①：身体急停法——气冲头顶先离开现场、冷水温水、握拳松拳、脚踩地、暂不回消息；身体是情绪开关，先退烧再开口。新本领②：我信息表达法——事实→感受→需要→请求，用'我'开头、只说观点不人身攻击；林薇就是模板。",
    "一句话收尾：场合不是秀脾气的地方，只是说观点的地方；身体先降温、开口只送观点，心会越练越静。下课！"
  ]},

  {"type":"feynman","title":"费曼小测 · 讲给晓晓老师听","text":
    "费曼学习法说：你以为你懂了，不算懂；能用自己的话讲明白，才是真懂。\n\n现在轮到你啦——请用你自己的话，把下面这道题讲给晓晓老师听：\n\n'如果下次我在会上又被怼、脸红手抖想回怼，或者像陈峰那样觉得委屈想拍桌发作，我会怎么做，才能既把意见/诉求说清、又不发火、还不丢人？'\n\n提示：可以结合旧本领（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法）和新本领（身体急停法、我信息表达法）一起说。\n\n在下面的框里写几句（或对着麦克风讲出来也行）。写完了，翻回上面的口诀卡对照一下，看看漏了哪一步。"
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
<title>晓晓老师的情绪管理课 · 第7天：先冷却身体，再冷静说</title>
<style>
  :root{
    --bg:#f4f7fb; --card:#ffffff; --ink:#243447; --soft:#6b7c8f;
    --brand:#5b8def; --brand2:#7c5cff; --good:#2bb673; --warn:#ff7a59;
    --pink:#ff8fab; --yellow:#ffd66b; --mint:#bdeed3; --shadow:0 10px 30px rgba(40,60,90,.12);
  }
  *{box-sizing:border-box;}
  /* 宋体 + 小四号(12pt)基础上放大，正文更大更清晰 */
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
  /* 底部播放控制条（可调位置 + 上一句/下一句） */
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
  /* 字幕条（不挡讲解） */
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
  <h1>晓晓老师的情绪管理课 · 第7天</h1>
  <p>先冷却身体，再冷静说：场合不是秀脾气的地方，只是说观点的地方 🧊</p>
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

// 全局句子播放列表（仅 speak 段落贡献句子）
let PLAYLIST = [];
SECTIONS.forEach((s, si)=>{
  if(s.type==='speak'){ s.sentences.forEach((t, ji)=>{ PLAYLIST.push({si, ji, gi:PLAYLIST.length, text:t}); }); }
});
let sectionIdx = -1;      // 当前 FLOW 段落
let cur = 0;              // 当前在 PLAYLIST 中的位置
let stars = 0;
let answered = new Set();
let textContainer = null; // 当前段落的句子容器
let allMode = false;

const audioEl = new Audio();
let synthOn = ('speechSynthesis' in window);
let curUtter = null;

function setSub(t){ subText.textContent = t; }
function sectionSentences(si){ return PLAYLIST.filter(p=>p.si===si); }

/* ---------- 播放控制 ---------- */
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

/* ---------- 渲染 ---------- */
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
    '<textarea id="fm" placeholder="在这里用你自己的话写一写（比如：我先离开现场用身体急停法退烧，再用我信息四步——事实+感受+需要+请求，只说观点不人身攻击…）…"></textarea>'+
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
    '气冲头顶脸发红，先别开口别发疯；转身离开喝口温，握拳松拳脚踩地。暂不回消息手机扣，身体退烧理智回；再开口只说事，场合不秀脾气。<br><br>'+
    '想提意见别开火，我信息法四步走；先说事实不带骂，再讲感受用我开头。需要什么说清楚，具体请求送到手；人身攻击最掉价，只说观点人人服。<br><br>'+
    '<b>前10招回顾：</b>见本页上方「复习 · 十招技能地图」卡片（五步刹车/静音/五感着陆/番茄/认知重评/方箱呼吸/第三人称抽离/冲动冲浪/情绪命名/10-10-10）。'+
    '</div><p style="color:var(--soft)">记住：场合不是秀脾气的地方，只是说观点的地方。身体先降温、开口只送观点，心会越练越静。</p>'+
    '<div class="controls" style="justify-content:center"><button class="btn" onclick="location.reload()">🔁 再上一遍</button></div></div>';
  setSub('—— 今天的课结束啦，记得常回来练 ——');
}

/* 开场卡片 */
(function(){
  const intro=document.createElement('div'); intro.className='card';
  intro.innerHTML='<h2>👋 准备好了吗？（第7天）</h2>'+
    '<div class="scene-text">这堂课大概 10 分钟。先带你复习前10招（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法），再讲一个新案例（陈峰会议室拍桌摔门被裁 vs 林薇喝茶水间十分钟冷静补救）和两招新本领（身体急停法、我信息表达法）。\n\n'+
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
    L.append("# 情绪管理课 · 晓晓老师课堂笔记（第7天 · ima 知识库 imao）\n")
    L.append("> 主题：克服专注力差、浮躁易怒、情绪化。核心理念：**场合不是展示真性情的地方，只是表达观点的地方。**\n")
    L.append("> 配套互动网页：`emotion-class-20260720.html`（晓晓老师 XiaoxiaoNeural 神经网络语音 + 不挡字幕 + 上一句/下一句可调位置 + 费曼式定时提问）。\n")
    L.append("> 第7天结构：**复习**前10招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10) → **新案例**(2026 今日头条热帖：陈峰会议室拍桌摔门被裁 vs 林薇喝茶水间10分钟冷静补救) → **原理**(身体是情绪开关 + 表达分层金字塔) → **新招1**身体急停法 → **新招2**我信息表达法(非暴力沟通) → 费曼自测。\n")
    L.append("\n## 一、复习：前10招（情绪技能地图）\n")
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
    L.append("- 这十招管“已经炸了/快炸了/走神了/不专注/念头歪了/手抖想怼/上头那一秒/心里乱糟糟/一点就炸”。今天两招管最前面的“身体开关”和“怎么开口只说观点”。\n")
    L.append("\n## 二、今日新案例（2026 今日头条热帖，人物化名）\n")
    L.append("素材：陈峰，某公司前途无量的项目总监，能力顶尖但脾气一点就着。半年前一次跨部门协调会，因技术方案与产品部僵持，对方说了句“你这想法太理想化，不考虑现实成本”，陈峰当场拍桌、指着对方鼻子吼“你懂个屁的技术！除了会卡成本你还会什么？！”，随后摔门而出。\n")
    L.append("- 后果：合作部门寒心能拖就拖；“情绪不稳定、难合作”成标签；大老板评“连自己情绪都管理不好，我怎么敢把几百人的团队交给他”；半年后公司调整，他上首批裁员名单——五年口碑被几分钟怒火烧光。\n")
    L.append("- 对照：同公司负责人林薇，关键上线前夜核心程序员撂挑子、团队急哭，她脸也白了，却转身进茶水间冲了杯很烫的咖啡，慢慢喝十分钟，回来平静布置三步补救，核心功能准时上线。\n")
    L.append("- 初中生版启示：同样被点燃，陈峰把会议室当“秀脾气、人身攻击”的地方，一句话把“提意见”变成“发火”，丢了职业形象；林薇先给身体降温、再只说观点（事实+安排），反而赢得尊重。场合是讲观点的地方，不是倒情绪的地方。\n")
    L.append("\n## 三、原理：两个道理（身体是开关 + 表达金字塔）\n")
    L.append("- **道理一 身体是情绪的开关（情绪具身化）**：生气时身体先有反应——脸红、心跳快、手抖、呼吸变短；反过来，一调身体脑子就冷静。像发烧先退烧，情绪“烧”起来先给身体降温，理智才回得来。林薇那十分钟就是给身体“退了烧”。\n")
    L.append("- **道理二 表达是分层的金字塔**：底层“事实”（发生什么）→ 上层“感受”（我怎么了）→ 再上“观点”（我的看法）→ 顶层“请求”（我要什么）。陈峰只站在“人身攻击”那层乱敲；林薇站“事实+安排”两层稳稳说出观点。场合里该站“事实→观点→请求”，别掉到“人身攻击”。\n")
    L.append("- 一句话：情绪从身体起，也从身体灭；观点要分层说，别把脾气混进去。道理一→身体急停法；道理二→我信息表达法。\n")
    L.append("\n## 四、新招1：身体急停法（先给身体灭火）\n")
    L.append("适用：气冲到头顶、脸红手抖、想立刻回怼/拍桌时。一句话——先别开口，用身体动作把“火”降下来，再说话。五步任选：\n")
    L.append("- **①离开现场**：物理离开发火的地方，眼睛不见火少一半（陈峰当场拍桌，林薇转身进茶水间）。\n")
    L.append("- **②冷水/温水**：冷水洗把脸，或慢慢喝杯温水；冷/温刺激让心跳呼吸慢下来（林薇的十分钟咖啡）。\n")
    L.append("- **③握拳松拳**：用力握拳五秒、猛地松开，重复三次；把手上“想打人”的劲变成可控松紧，不伤人也发泄。\n")
    L.append("- **④脚踩地**：双脚踩实地面，感受地板托住你，默数三次深呼吸；把自己“钉”在当下。\n")
    L.append("- **⑤暂不回消息**：气头上别在群里回、别发语音，手机扣过去十分钟；等身体凉了再回，话就准。\n")
    L.append("- 要点：情绪从身体起，也从身体灭。你不是你的火，你是“先给身体退退烧，再开口”的人。强忍是憋火会炸，离开+动作降温是主动退烧。\n")
    L.append("\n**急停口诀**\n")
    L.append("> 气冲头顶脸发红，先别开口别发疯；转身离开喝口温，握拳松拳脚踩地。暂不回消息手机扣，身体退烧理智回；再开口只说事，场合不秀脾气。\n")
    L.append("\n## 五、新招2：我信息表达法（非暴力沟通 / 只说观点不人身攻击）\n")
    L.append("适用：要提意见、说诉求、被抢功、被怼时，想表达又不想发火。按“事实→感受→需要→请求”四步说：\n")
    L.append("- **①说事实**：只说发生什么，不带骂人。如“刚才会上我那段话被打断了三次”，而非“你老是打断我”。\n")
    L.append("- **②说感受**：用“我”开头讲情绪。如“我有点着急”，而非“你真讨厌”。\n")
    L.append("- **③说需要**：我想要什么。如“因为我想把方案完整地讲完”；把“你针对我”换成“我需要被听完”。\n")
    L.append("- **④说请求**：具体、可操作地请对方怎么做。如“下次能不能让我先讲完，再讨论？”——观点清清楚楚送出去，谁都挑不出你发火。\n")
    L.append("- 林薇那三句话即模板：先说事实（现在问题是补救）、再说安排（A联系外援、B拆解功能、C安抚团队），没骂谁没甩锅，纯观点所以大家服。\n")
    L.append("- 要点：场合是讲观点的地方，我信息就是“把观点稳稳送出去”的快递盒；骂人=给人贴“情绪化”标签、还把诉求办砸。\n")
    L.append("\n**我信息口诀**\n")
    L.append("> 想提意见别开火，我信息法四步走；先说事实不带骂，再讲感受用我开头。需要什么说清楚，具体请求送到手；人身攻击最掉价，只说观点人人服。\n")
    L.append("\n## 六、费曼自测题（旧+新结合）\n")
    L.append("用自己的话回答：*如果下次我在会上又被怼、脸红手抖想回怼，或者像陈峰那样觉得委屈想拍桌发作，我会怎么做，才能既把意见/诉求说清、又不发火、还不丢人？*\n")
    L.append("标准答案要点：\n")
    L.append("1. 身体先炸时——身体急停法（离开现场→冷水/温水→握拳松拳→脚踩地→暂不回消息），先把身体的火降下来；同时静音模式（有火不泼别人）。\n")
    L.append("2. 上头/冲动时——第三人称抽离（退后换角劝友）+ 冲动冲浪（认浪看浪等浪退），绝不发出去。\n")
    L.append("3. 开口说观点时——我信息表达法（事实→感受→需要→请求，用“我”开头不人身攻击），像林薇那样只送观点。\n")
    L.append("4. 心里乱/一点就炸时——情绪命名法（精准起名+打分+说写）+ 10-10-10 透视法（拉远看）；快炸/念头歪用五步刹车+认知重评；手抖配方箱呼吸；走神/不专注用五感着陆+番茄专注。始终记：场合不是秀脾气的地方，只是说观点的地方。\n")
    L.append("\n## 七、今日带走的两句新口诀\n")
    L.append("1. 身体急停法：气冲头顶脸发红，先别开口别发疯；转身离开喝口温，握拳松拳脚踩地。暂不回消息手机扣，身体退烧理智回；再开口只说事，场合不秀脾气。\n")
    L.append("2. 我信息表达法：想提意见别开火，我信息法四步走；先说事实不带骂，再讲感受用我开头。需要什么说清楚，具体请求送到手；人身攻击最掉价，只说观点人人服。\n")
    L.append("3. 一句话收尾：场合不是秀脾气的地方，只是说观点的地方；身体先降温、开口只送观点，心会越练越静。\n")
    return "\n".join(L)

# ---------------------------------------------------------------- 主流程
def main():
    audio = build_audio()
    sections_js = "window.SECTIONS = " + json.dumps(SECTIONS, ensure_ascii=False) + ";"
    audio_js = "window.AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";"
    html = HTML.replace("__LESSON_DATA__", sections_js).replace("__AUDIO_DATA__", audio_js)
    out_html = os.path.join(WS, "emotion-class-20260720.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html] 写出 {out_html} ({len(html)/1024:.0f} KB)")
    md = build_markdown()
    out_md = os.path.join(WS, "情绪管理-晓晓老师课堂笔记.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出 {out_md} ({len(md)/1024:.0f} KB)")
    # 带日期副本，供 ima 知识库入库（避免重名覆盖）
    dated = os.path.join(WS, "情绪管理-晓晓老师课堂笔记_20260720.md")
    with open(dated, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出带日期副本 {dated} ({len(md)/1024:.0f} KB)")
if __name__ == "__main__":
    main()
