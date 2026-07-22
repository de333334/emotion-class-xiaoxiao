# -*- coding: utf-8 -*-
"""
情绪管理课 builder（2026-07-22 · 第九天）
- 单一内容源 -> 生成 晓晓老师(XiaoxiaoNeural) 每句语音(base64 内联)
- 输出「独立」单文件自包含 emotion-class-20260722.html (宋体/可调播放位置/上一句下一句/不挡字幕/费曼提问)
  ※ 每天一个新文件，绝不覆盖旧课页面（满足"每个网页对应一课不要更新网页"）
- 同时输出 情绪管理-晓晓老师课堂笔记.md 与 带日期副本 供存入 ima 知识库 imao
本日结构：复习前14招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本)
  -> 新案例(2026-07-16 腾讯新闻：小敏 被领导当众摔周报骂"吃干饭的"、为这话内耗整晚还去讨好、日均2.1h无效情绪消耗/78%内耗接别人课题)
  -> 原理(阿德勒课题分离：谁担后果谁负责 + 启动效应：动起来就不浮)
  -> 新招15 课题分离法(分清/归还/专注) -> 新招16 两分钟启动法(拆/动/稳) -> 费曼自测
"""
import os, json, base64, asyncio, sys, shutil

WS = "C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-8%"
PITCH = "+0Hz"

# ---------------------------------------------------------------- 案例插画（内联 SVG，保证离线可开）
SVG_MAP = '''<svg viewBox="0 0 680 232" xmlns="http://www.w3.org/2000/svg">
  <text x="340" y="20" font-size="16" fill="#5b8def" text-anchor="middle" font-family="sans-serif">🗺️ 情绪技能地图 · 前14招复习</text>
  <g font-family="sans-serif" font-size="11">
   <rect x="10" y="34" width="90" height="84" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="55" y="58" fill="#2b6fb0" text-anchor="middle" font-weight="bold">①五步刹车</text>
   <text x="55" y="80" fill="#243447" text-anchor="middle">停·数·命名</text>
   <text x="55" y="102" fill="#6b7c8f" text-anchor="middle">🔥快炸灭火</text>
   <rect x="104" y="34" width="90" height="84" rx="12" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="149" y="58" fill="#1c7a4d" text-anchor="middle" font-weight="bold">②静音模式</text>
   <text x="149" y="80" fill="#243447" text-anchor="middle">心是一杯水</text>
   <text x="149" y="102" fill="#6b7c8f" text-anchor="middle">💧有火不泼人</text>
   <rect x="198" y="34" width="90" height="84" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="243" y="58" fill="#c98a14" text-anchor="middle" font-weight="bold">③五感着陆</text>
   <text x="243" y="80" fill="#243447" text-anchor="middle">看5摸4听3</text>
   <text x="243" y="102" fill="#6b7c8f" text-anchor="middle">🌀走神着陆</text>
   <rect x="292" y="34" width="90" height="84" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="337" y="58" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④番茄专注</text>
   <text x="337" y="80" fill="#243447" text-anchor="middle">25分只做一事</text>
   <text x="337" y="102" fill="#6b7c8f" text-anchor="middle">🍅练定力</text>
   <rect x="386" y="34" width="90" height="84" rx="12" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="431" y="58" fill="#d6455f" text-anchor="middle" font-weight="bold">⑤认知重评</text>
   <text x="431" y="80" fill="#243447" text-anchor="middle">停·揪·换想法</text>
   <text x="431" y="102" fill="#6b7c8f" text-anchor="middle">🧠换念换情绪</text>
   <rect x="480" y="34" width="90" height="84" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="525" y="58" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑥方箱呼吸</text>
   <text x="525" y="80" fill="#243447" text-anchor="middle">吸4憋7呼8</text>
   <text x="525" y="102" fill="#6b7c8f" text-anchor="middle">🌬️手抖降温</text>
   <rect x="574" y="34" width="90" height="84" rx="12" fill="#eef7f2" stroke="#2bb673" stroke-width="2"/>
   <text x="619" y="58" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑦第三人称</text>
   <text x="619" y="80" fill="#243447" text-anchor="middle">退后·换角·劝友</text>
   <text x="619" y="102" fill="#6b7c8f" text-anchor="middle">👁旁观一眼冷</text>
   <rect x="10" y="134" width="90" height="84" rx="12" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="55" y="158" fill="#5b3fd6" text-anchor="middle" font-weight="bold">⑧冲动冲浪</text>
   <text x="55" y="180" fill="#243447" text-anchor="middle">认浪·看浪·退</text>
   <text x="55" y="202" fill="#6b7c8f" text-anchor="middle">🌊浪过你还在</text>
   <rect x="104" y="134" width="90" height="84" rx="12" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="149" y="158" fill="#c98a14" text-anchor="middle" font-weight="bold">⑨情绪命名</text>
   <text x="149" y="180" fill="#243447" text-anchor="middle">起名·打分·说写</text>
   <text x="149" y="202" fill="#6b7c8f" text-anchor="middle">🏷️乱时先起名</text>
   <rect x="198" y="134" width="90" height="84" rx="12" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="243" y="158" fill="#2b6fb0" text-anchor="middle" font-weight="bold">⑩10-10-10</text>
   <text x="243" y="180" fill="#243447" text-anchor="middle">10分·10月·10年</text>
   <text x="243" y="202" fill="#6b7c8f" text-anchor="middle">🔭拉远看开</text>
   <rect x="292" y="134" width="90" height="84" rx="12" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="337" y="158" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑪身体急停</text>
   <text x="337" y="180" fill="#243447" text-anchor="middle">离开·冷温·握踩</text>
   <text x="337" y="202" fill="#6b7c8f" text-anchor="middle">🧊先退烧</text>
   <rect x="386" y="134" width="90" height="84" rx="12" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="431" y="158" fill="#d6455f" text-anchor="middle" font-weight="bold">⑫我信息</text>
   <text x="431" y="180" fill="#243447" text-anchor="middle">事实·感受·需·请</text>
   <text x="431" y="202" fill="#6b7c8f" text-anchor="middle">💬只说观点</text>
   <rect x="480" y="134" width="90" height="84" rx="12" fill="#e9f9ef" stroke="#2bb673" stroke-width="2"/>
   <text x="525" y="158" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑬六秒法则</text>
   <text x="525" y="180" fill="#243447" text-anchor="middle">慢半拍·闭嘴数</text>
   <text x="525" y="202" fill="#6b7c8f" text-anchor="middle">⏳嘴快先停</text>
   <rect x="574" y="134" width="90" height="84" rx="12" fill="#fff3e6" stroke="#ff9a3c" stroke-width="2"/>
   <text x="619" y="158" fill="#c98a14" text-anchor="middle" font-weight="bold">⑭记账本</text>
   <text x="619" y="180" fill="#243447" text-anchor="middle">触发·念头·新招</text>
   <text x="619" y="202" fill="#6b7c8f" text-anchor="middle">📒天天记天天安</text>
  </g>
</svg>'''

SVG_CASE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="13.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">案例：领导当众摔周报骂"吃干饭的" → 小敏为这话内耗整晚+还去讨好 → 胃炎+评优落空</text>
  <rect x="20" y="38" width="280" height="150" rx="14" fill="#fdf3f1" stroke="#ff8a8a" stroke-width="1.6"/>
  <circle cx="75" cy="86" r="24" fill="#ffd9b8"/>
  <path d="M53 146 Q75 112 97 146 Z" fill="#c0392b"/>
  <path d="M61 80 l8 6 M89 80 l-8 6" stroke="#c0392b" stroke-width="3"/>
  <path d="M59 96 q16 9 32 0" stroke="#c0392b" stroke-width="3" fill="none"/>
  <rect x="110" y="64" width="172" height="34" rx="10" fill="#fff" stroke="#ff8a8a" stroke-width="1.6"/>
  <text x="196" y="86" font-size="12" fill="#c0392b" text-anchor="middle" font-family="sans-serif">"连表都捋不明白，</text>
  <text x="196" y="100" font-size="12" fill="#c0392b" text-anchor="middle" font-family="sans-serif">吃干饭的？"</text>
  <text x="160" y="118" font-size="11" fill="#c0492a" text-anchor="middle" font-family="sans-serif">👔 领导当众摔周报、指鼻骂</text>
  <text x="160" y="170" font-size="12" fill="#c0492a" text-anchor="middle" font-family="sans-serif">小敏被当众羞辱</text>
  <text x="160" y="190" font-size="12.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">💥 当场憋泪改三版到深夜</text>
  <text x="320" y="118" font-size="26" fill="#c0492a" text-anchor="middle">VS</text>
  <rect x="340" y="38" width="280" height="150" rx="14" fill="#eef7f2" stroke="#2bb673" stroke-width="1.6"/>
  <circle cx="395" cy="86" r="24" fill="#ffd9b8"/>
  <path d="M373 146 Q395 120 417 146 Z" fill="#9a9a9a"/>
  <circle cx="386" cy="84" r="3" fill="#3a3a3a"/><circle cx="404" cy="84" r="3" fill="#3a3a3a"/>
  <path d="M388 96 q7 5 14 0" stroke="#1c7a4d" stroke-width="2.2" fill="none"/>
  <rect x="430" y="64" width="172" height="46" rx="10" fill="#fff" stroke="#bfe3c9" stroke-width="1.6"/>
  <text x="516" y="84" font-size="11.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">凌晨3点还在想那句话</text>
  <text x="516" y="100" font-size="11.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">第二天还帮领导订咖啡</text>
  <text x="480" y="118" font-size="11" fill="#c98a14" text-anchor="middle" font-family="sans-serif">😣 替别人背了课题</text>
  <text x="480" y="170" font-size="12" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">急性胃炎 + 评优给了别人</text>
  <text x="480" y="190" font-size="12.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">✅ 本可：只改好周报、不内耗</text>
  <text x="320" y="212" font-size="11.5" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">数据：职场人日均 2.1h 花在无效情绪消耗；78% 内耗 = 接别人的课题</text>
</svg>'''

SVG_PRINCIPLE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">两个道理：阿德勒课题分离(谁担后果谁负责) · 启动效应(动起来就不浮)</text>
  <g font-family="sans-serif">
   <rect x="20" y="38" width="290" height="196" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="165" y="64" font-size="13" fill="#2b6fb0" text-anchor="middle" font-weight="bold">道理一 · 课题分离</text>
   <circle cx="95" cy="116" r="22" fill="#ffd6cf"/><text x="95" y="121" font-size="13" text-anchor="middle">👔</text>
   <text x="95" y="156" font-size="10" fill="#c0492a" text-anchor="middle">领导情绪·他的</text>
   <path d="M123 116 h16 M139 108 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <circle cx="235" cy="116" r="22" fill="#cfe6ff"/><text x="235" y="121" font-size="13" text-anchor="middle">📝</text>
   <text x="235" y="156" font-size="10" fill="#1c7a9c" text-anchor="middle">我的活·我的</text>
   <text x="165" y="190" font-size="10" fill="#243447" text-anchor="middle">谁担后果谁负责</text>
   <text x="165" y="208" font-size="10" fill="#1c7a4d" text-anchor="middle">分清·归还·专注，不替人背</text>
   <rect x="340" y="38" width="290" height="196" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="485" y="64" font-size="13" fill="#c98a14" text-anchor="middle" font-weight="bold">道理二 · 启动效应</text>
   <text x="400" y="100" font-size="22" text-anchor="middle">🚗</text>
   <text x="400" y="124" font-size="10" fill="#c0492a" text-anchor="middle">停着：最难推</text>
   <path d="M424 104 h28" stroke="#d99" stroke-width="2"/>
   <text x="560" y="100" font-size="22" text-anchor="middle">🚗💨</text>
   <text x="560" y="124" font-size="10" fill="#1c7a4d" text-anchor="middle">动起来：惯性带飞</text>
   <rect x="420" y="146" width="130" height="26" rx="8" fill="#fff" stroke="#ffb84d" stroke-width="1.4"/>
   <text x="485" y="164" font-size="11" fill="#c98a14" text-anchor="middle">手指一动心就静</text>
   <text x="485" y="210" font-size="10" fill="#6b7c8f" text-anchor="middle">大活不动手＝浮躁；先动2分钟就顺</text>
  </g>
</svg>'''

SVG_SEP = '''<svg viewBox="0 0 640 210" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">课题分离法（阿德勒）：别人的情绪是别人的事，谁担后果谁负责</text>
  <g font-family="sans-serif">
   <rect x="14" y="44" width="170" height="120" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="99" y="74" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 分清</text>
   <text x="99" y="100" font-size="11" fill="#243447" text-anchor="middle">这是谁的事？</text>
   <text x="99" y="120" font-size="11" fill="#243447" text-anchor="middle">评价/情绪→他</text>
   <text x="99" y="142" font-size="11" fill="#243447" text-anchor="middle">活/观点→我</text>
   <path d="M184 104 l18 0 M200 96 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="202" y="44" width="170" height="120" rx="14" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="287" y="74" font-size="14" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 归还</text>
   <text x="287" y="100" font-size="11" fill="#243447" text-anchor="middle">别人的课题</text>
   <text x="287" y="120" font-size="11" fill="#243447" text-anchor="middle">还给别人</text>
   <text x="287" y="142" font-size="11" fill="#243447" text-anchor="middle">不解释不讨好</text>
   <path d="M372 104 l18 0 M388 96 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="390" y="44" width="170" height="120" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="475" y="74" font-size="14" fill="#c98a14" text-anchor="middle" font-weight="bold">③ 专注</text>
   <text x="475" y="100" font-size="11" fill="#243447" text-anchor="middle">省下的力气</text>
   <text x="475" y="120" font-size="11" fill="#243447" text-anchor="middle">花在自己活上</text>
   <text x="475" y="142" font-size="11" fill="#243447" text-anchor="middle">写好活·说清观点</text>
   <text x="320" y="196" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">同事甩脸领导火，那是他的小账簿；我的活儿我写好，别人的题我不扛</text>
  </g>
</svg>'''

SVG_TWO = '''<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#c98a14" text-anchor="middle" font-family="sans-serif">两分钟启动法（专治大活不动手、浮躁坐不住）：先动两分钟，启动效应让浮躁散</text>
  <g font-family="sans-serif">
   <rect x="20" y="44" width="180" height="140" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="110" y="74" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 拆</text>
   <text x="110" y="100" font-size="11" fill="#243447" text-anchor="middle">大活拆小步</text>
   <text x="110" y="120" font-size="11" fill="#243447" text-anchor="middle">别想"写完周报"</text>
   <text x="110" y="140" font-size="11" fill="#243447" text-anchor="middle">先想"只写标题"</text>
   <text x="110" y="166" font-size="10" fill="#6b7c8f" text-anchor="middle">小到不用鼓勇气</text>
   <path d="M200 114 l18 0 M216 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="218" y="44" width="180" height="140" rx="14" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="308" y="74" font-size="14" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 动</text>
   <text x="308" y="100" font-size="11" fill="#243447" text-anchor="middle">定两分钟闹钟</text>
   <text x="308" y="120" font-size="11" fill="#243447" text-anchor="middle">只做这一点</text>
   <text x="308" y="140" font-size="11" fill="#243447" text-anchor="middle">一动多半接着做</text>
   <text x="308" y="166" font-size="10" fill="#6b7c8f" text-anchor="middle">推车最难是推那下</text>
   <path d="M398 114 l18 0 M414 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="416" y="44" width="180" height="140" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="506" y="74" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">③ 稳</text>
   <text x="506" y="100" font-size="11" fill="#243447" text-anchor="middle">番茄专注养定</text>
   <text x="506" y="120" font-size="11" fill="#243447" text-anchor="middle">五感着陆拉回</text>
   <text x="506" y="140" font-size="11" fill="#243447" text-anchor="middle">大活不吓人了</text>
   <text x="506" y="166" font-size="10" fill="#6b7c8f" text-anchor="middle">专注慢慢长成棵</text>
   <text x="320" y="208" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵</text>
  </g>
</svg>'''

# ---------------------------------------------------------------- 课程内容（第九天）
SECTIONS = [
  {"type":"speak","title":"开场 · 第九天，先串起前14招","rhyme":None,"img":None,"sentences":[
    "同学你好，我是晓晓老师！咱们的情绪管理课到第九天啦。前八天你攒了十四招本领：第一天五步刹车加静音模式，第二天五感着陆加番茄专注，第三天认知重评加方箱呼吸，第四天第三人称抽离加冲动冲浪，第五天情绪命名法加10-10-10透视法，第六天身体急停法加我信息表达法，第七天六秒法则加情绪记账本。今天先把这十四招串成一张情绪技能地图，再教你两招新本领，专治你最头疼的两件事——别人的脸色一变，你就跟着浮躁一整天；还有一坐到电脑前，心就浮、干正事像上刑，刷手机两小时才开始动。",
    "先复习老口号：任何场合——办公室、工作群、会议室——都不是展示真性情的地方，它只是表达观点的地方。你是去把事说清楚的，不是去把脾气秀出来的，更不是去替别人的情绪买单的。",
    "今天要补的第一块：你总为别人的态度内耗——同事甩脸、领导批评、群里一句阴阳怪气，你能琢磨一整天。这其实是把别人的课题背到了自己身上。第二块：你专注力差、浮躁坐不住，大活一摆就慌，迟迟不动。今天两招分别治这两块。"
  ]},

  {"type":"speak","title":"复习 · 十四招技能地图","rhyme":None,"img":SVG_MAP,"sentences":[
    "先复习十四招，编成一张地图。第一招五步刹车——一停二数三命名，四转五说；火气冒头先喊停，只说观点不秀脾气。第二招静音模式——心是一杯水，摇浑放自清，收拾不了局别纵脾气。",
    "第三招五感着陆——看五摸四听三声，闻二尝一拉回神；走神坐不住用它。第四招番茄专注——二十五分专注钟，五分休息不硬撑，手机扔远练定力。第五招认知重评——火起先喊停、揪出念头、换个想法，换想法就换情绪。",
    "第六招方箱呼吸——吸气四憋七呼八憋四，画方箱一分钟降温。第七招第三人称抽离——退后、换角、劝友，把我换成朋友视角火就小。第八招冲动冲浪——认浪、看浪、等浪退，约十分钟浪自己走。",
    "第九招情绪命名法——精准起名、温度计打分、说或写下来，你不是情绪你是起名的人。第十招10-10-10透视法——10分后10月后10年后还重要吗，拉远看浮躁就散。第十一招身体急停法——离开现场、冷水温水、握拳松拳、脚踩地、暂不回消息，身体是开关先退烧。第十二招我信息表达法——事实→感受→需要→请求，用我开头只说观点不人身攻击。第十三招六秒法则——火冒三丈先闭嘴、默数到六、等理智脑上线、再开口。第十四招情绪记账本——睡前三栏触发、念头、新招，天天记、天天安。今天两招管最前面的替别人内耗和大活不动手。"
  ]},

  {"type":"quiz","title":"复习小测 · 开会走神坐不住用哪两招","quiz":{
    "q":"开会时你心飘了、坐不住、老想摸手机。前14招里该先动哪两招，把走神浮躁拉回当下、又能练出定力？",
    "opts":[
      {"t":"五感着陆法（看5摸4听3声，把心拉回当下）+ 番茄专注法（25分钟只做一事，手机扔远练定力）","ok":True},
      {"t":"冲动冲浪（那是管冲动已起想发作，不是走神）","ok":False},
      {"t":"情绪记账本（那是睡前复盘，不是开会走神）","ok":False}
    ],
    "stu":"小浩抢答：老师，走神是不是用冲动冲浪压一压？",
    "teacher":"晓晓老师笑：冲动冲浪是给已经上头想摔东西怼人那股浪用的。你这是心飘、坐不住、想摸手机——用第三招五感着陆把注意力拉回眼前（看5样、摸4样、听3声），再用第四招番茄专注法（25分钟只干一件事、手机扔远）练定力。各招分工：走神→五感加番茄；发作→冲浪加方箱。",
    "card":["开会走神坐不住 = 五感着陆(拉回当下) + 番茄专注(25分只做一事练定力)。","冲浪管发作、五感管走神、番茄管不专注。"]
  }},

  {"type":"speak","title":"第一幕 · 新案例：一句骂，内耗一整晚","rhyme":None,"img":SVG_CASE,"sentences":[
    "讲个 2026 年刚发生的真实事（来源腾讯新闻，2026-07-16《上班只为碎银几两，别为烂人消耗自己》，人物化名）。主人公小敏，济南一家互联网公司做运营。",
    "一次周会，领导当众把她的周报摔在桌上，指着鼻子骂：连个基础表都捋不明白，招你进来是吃干饭的？小敏当场憋着泪，改了三版熬到晚上十点半才走。",
    "换作以前，这事翻篇就完了。可小敏回家后，翻来覆去想那句吃干饭的，凌晨三点还没睡。第二天到公司，她还主动帮那个领导订了客户要见的咖啡——明明被骂的是自己，还去讨好。",
    "结果月底评优，名额给了领导刚入职三个月的小舅子。小敏当晚急性胃炎，蹲在出租屋地上给闺蜜打电话，医药费加误工扣的钱，比那点绩效奖金还多两千。",
    "文章里还给出一组扎心数据：调研说职场人平均每天花 2.1 小时在无效情绪消耗上，一年相当于多上 27 个情绪班；更狠的是——78% 的内耗，都是花在接别人的课题上：领导一句吐槽琢磨半天、同事一个眼神复盘半小时。小敏就是把领导的课题，背了自己一整晚。"
  ]},

  {"type":"quiz","title":"课间提问① · 小敏最亏在哪","quiz":{
    "q":"小敏最亏的地方在哪？",
    "opts":[
      {"t":"她把领导的评价、领导的情绪当成了自己的事，内耗一整晚还去讨好，白白消耗了自己——那是领导的课题，不该她背","ok":True},
      {"t":"她能力真的差，活该被骂","ok":False},
      {"t":"她没当场回怼，太软弱","ok":False}
    ],
    "stu":"小雪：可领导当众骂人，确实气人啊！",
    "teacher":"晓晓老师点头：骂人当然不对，小敏也委屈。但咱们能管的只有自己。领导怎么评价你、领导心情好不好，那是领导的课题——他担后果。小敏为这话失眠、讨好、胃炎，等于替领导背了他的课题，自己亏大了。道理就一句：别人的情绪，不该你买单。这就引出今天第一招。",
    "card":["小敏崩在：把领导的评价/情绪当自己的事，内耗整晚还讨好，替别人背了课题。","别人的情绪是别人的课题，不该你买单（78%内耗都花在接别人课题）。"]
  }},

  {"type":"speak","title":"第二幕 · 原理：课题分离 + 启动效应","rhyme":None,"img":SVG_PRINCIPLE,"sentences":[
    "为什么别为别人情绪内耗？心理学家阿德勒一句话点破：课题分离——谁承担结果，就是谁的活。领导骂你，是他情绪管理差，后果他担；你活干没干完，是你自己的事，后果你担。两边别混。",
    "所以别人甩脸、同事阴阳、群里一句难听话——那是他们的课题，你接过来背身上，只会把自己压垮。你只负责把分内活写好、把观点说清，剩下的，还给他们。",
    "第二个道理，专治大活不动手、浮躁坐不住：心理学有个启动效应——人一旦动起来，焦虑就会往下掉。就像推一辆停住的车，最难是刚推那一下；推起来，惯性就帮你走。你越拖着不动，越浮躁；手指一动，心就静了。",
    "还有个蔡格尼克效应：没做完的事总在脑子里转，越想越烦；你先动手做一点点，那股悬着的浮躁就落了地。一句话：别人的事还别人（课题分离）；自己的大活，先拆一小步动起来（启动效应）。道理一→课题分离法；道理二→两分钟启动法。"
  ]},

  {"type":"quiz","title":"课间提问② · 为什么别为别人情绪内耗","quiz":{
    "q":"同事阴阳怪气甩你一句，你琢磨了一下午还睡不着。从今天的原理看，问题出在哪？",
    "opts":[
      {"t":"你把同事的情绪、评价这个他的课题，背到了自己身上；按课题分离，谁担后果谁负责，你该还给他","ok":True},
      {"t":"说明你心地善良、在乎别人","ok":False},
      {"t":"说明你能力不行","ok":False}
    ],
    "stu":"小杰：那我装听不见不就行了？",
    "teacher":"晓晓老师摇头：装听不见是硬压，心里还是堵。课题分离不是装，是想清楚——这是他的情绪，后果他担；我的活我写好就行。想通这一层，你自然就不接了。身体急停法（离开、喝口水）也能帮你把那股想琢磨的劲儿先降下来。",
    "card":["课题分离：谁承担结果谁负责；同事的情绪是他的课题，你别背。","装听不见是硬压；想通不归我管才真不接。"]
  }},

  {"type":"speak","title":"第三幕 · 新招15：课题分离法（阿德勒）","rhyme":{
    "title":"🎵 课题分离口诀",
    "lines":["<b>同事甩脸领导火</b>，<b>那是他的小账簿</b>；","<b>我的活儿我写好</b>，<b>别人的题我不扛</b>。"]
  },"img":SVG_SEP,"sentences":[
    "新本领第十五招：课题分离法（阿德勒）。一句话——别人的情绪、别人的评价，是别人的事；谁承担后果，谁负责。你只管把分内的活写好、把观点说清。三步：",
    "第一步分清：遇到事先问一句这是谁的事？领导批评我、同事甩脸——这是他们的情绪课题，后果他们担；我活干没干完、我说没说清——这是我的事。先把线画清楚。",
    "第二步归还：别人的课题，还给别人。同事阴阳怪气，你在心里说这是他的情绪，我不当接盘侠，然后把注意力拉回自己的活。不解释、不讨好、不替他背。",
    "第三步专注：把省下来的力气，花在自己的事上——把周报写好、把观点用我信息说清。你越专注自己的课题，别人的脸色就越掀不起你的浪。",
    "记住：同事甩脸、领导发火，那是他们的小账簿，你不用替他们记；你的活儿你写好，别人的课题你不扛。这招直接呼应咱们的核心理念——场合是表达观点的地方，不是替谁情绪买单的地方。",
    "记口诀：同事甩脸领导火，那是他的小账簿；我的活儿我写好，别人的题我不扛。"
  ]},

  {"type":"quiz","title":"课间提问③ · 课题分离怎么用","quiz":{
    "q":"周一晨会，领导当众皱眉说这方案不行，你脸一热、一上午都在想他是不是针对我。按课题分离法，你该做啥？",
    "opts":[
      {"t":"先分清——评价方案是他的课题(后果他担)；归还——不琢磨他针对我，把注意拉回；专注——把方案改好、用我信息问清标准","ok":True},
      {"t":"当场回怼你才不行，不能忍","ok":False},
      {"t":"一上午都在想他是不是针对我，越想越气","ok":False}
    ],
    "stu":"小琳：不琢磨，万一他真针对我呢？",
    "teacher":"晓晓老师笑：他针对不针对，是他的课题；你方案行不行、活交没交，是你的。就算他真针对，你把他情绪还给他、把自己活干漂亮，才是真稳。别拿他针对我当借口，把自己一上午搭进去——那叫替他背课题。",
    "card":["课题分离三步：①分清(谁的事)②归还(不背别人的)③专注(自己的活写好)。","别人脸色是别人的小账簿，你不用替他记。"]
  }},

  {"type":"speak","title":"第四幕 · 新招16：两分钟启动法","rhyme":{
    "title":"🎵 两分钟启动口诀",
    "lines":["<b>大活先拆第一步</b>，<b>只做两分不贪多</b>；","<b>手指一动心就静</b>，<b>专注慢慢长成棵</b>。"]
  },"img":SVG_TWO,"sentences":[
    "新本领第十六招：两分钟启动法（专治大活不动手、浮躁坐不住）。一句话——再大的活，先只做两分钟或第一步，动起来，浮躁就散了。三步：",
    "第一步拆：大活摆眼前心慌？把它拆成一口能吃的小块。别想写完整个报告，先想只写个标题；别想收拾整间屋，先想只叠两件衣服。拆到小到不用鼓勇气就能动。",
    "第二步动：给自己定个超短闹钟——只做两分钟。两分钟一到，你可以停。但神奇的是，一旦动了，你多半会接着做。像推车，最难是推那一下，推起来就顺了。",
    "第三步稳：动起来后，用番茄专注法（25分钟只做一事）把专注养出来；走神了用五感着陆拉回。你会发现，原来让你浮一上午的大活，动两分钟就不吓人了。",
    "记住：大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵。浮躁不是你懒，是没启动；启动那一下，最难也最值。",
    "记口诀：大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵。"
  ]},

  {"type":"quiz","title":"课间提问④ · 两分钟启动怎么用","quiz":{
    "q":"周报摆在眼前，你越看越烦、刷手机两小时还没动笔。按两分钟启动法，第一步该做啥？",
    "opts":[
      {"t":"先拆——把写完周报拆成只写个标题这种一口能吃的小步；再动——定个两分钟闹钟只做这一点，动起来浮躁就散","ok":True},
      {"t":"逼自己今天必须写完，写不完不许停","ok":False},
      {"t":"干脆刷手机放松一下再说","ok":False}
    ],
    "stu":"小强：我怕一拆就更不想写了。",
    "teacher":"晓晓老师摇头：你不想写恰恰是因为盯着整篇周报这个大山。拆成只写标题——小到不用勇气。而且一旦动了，启动效应会推着你走，两分钟常常变成二十分钟。反过来，你越逼必须写完，越浮躁越不动。先动两分钟，比想一下午强。",
    "card":["两分钟启动：①拆(大活拆小步)②动(只做2分闹钟)③稳(番茄+五感养专注)。","越逼必须写完越浮躁；先动2分钟，启动效应推着你走。"]
  }},

  {"type":"speak","title":"结尾 · 今天你带走什么（前14招+两新招）","rhyme":None,"img":None,"sentences":[
    "今天的课到这儿，晓晓老师带你总复习。",
    "前14招（复习）：五步刹车——一停二数三命名四转五说；静音模式——心是一杯水；五感着陆——看五摸四听三声；番茄专注——二十五分只做一事；认知重评——停揪换、换想法就换情绪；方箱呼吸——吸4憋7呼8憋4；第三人称抽离——退后换角劝友；冲动冲浪——认浪看浪等浪退；情绪命名法——精准起名温度计打分说写下来；10-10-10透视法——10分10月10年后拉远看；身体急停法——离开冷水握拳脚踩地暂不回消息；我信息表达法——事实感受需要请求只说观点；六秒法则——火冒三丈先闭嘴数六等理智脑；情绪记账本——睡前三栏触发念头新招天天记。",
    "新本领①：课题分离法——别人的情绪是别人的课题，谁担后果谁负责；分清、归还、专注三步，不替别人背。新本领②：两分钟启动法——大活先拆小步、只做两分钟动起来，启动效应让浮躁散、专注长。",
    "一句话收尾：场合不是秀脾气的地方，只是说观点的地方；别人的脸色还别人，自己的大活先动两分钟，心会越练越静。下课！"
  ]},

  {"type":"feynman","title":"费曼小测 · 讲给晓晓老师听","text":
    "费曼学习法说：你以为你懂了，不算懂；能用自己的话讲明白，才是真懂。\n\n现在轮到你啦——请用你自己的话，把下面这道题讲给晓晓老师听：\n\n如果下次同事又甩脸子、或者领导又当众批评我，让我一整天浮躁、还忍不住想讨好、想琢磨他是不是针对我，我会怎么做，才能既不替别人背情绪、又能管住浮躁、把该干的活干好？\n\n提示：可以结合旧本领（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本）和新本领（课题分离法、两分钟启动法）一起说。\n\n在下面的框里写几句（或对着麦克风讲出来也行）。写完了，翻回上面的口诀卡对照一下，看看漏了哪一步。"
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
<title>晓晓老师的情绪管理课 · 第9天：分清你我，动起来就不浮躁</title>
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
  <h1>晓晓老师的情绪管理课 · 第9天</h1>
  <p>分清谁的事、动起来就不浮躁：场合不是秀脾气的地方，只是说观点的地方 🧊</p>
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
    '<textarea id="fm" placeholder="在这里用你自己的话写一写（比如：他批评是领导自己的课题，我不背；我先只写个标题动两分钟，再用身体急停法降温、用我信息说清观点，剩下的还给他…）…"></textarea>'+
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
    '同事甩脸领导火，那是他的小账簿；我的活儿我写好，别人的题我不扛。<br><br>'+
    '大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵。<br><br>'+
    '<b>前14招回顾：</b>见本页上方「复习 · 十四招技能地图」卡片（五步刹车/静音/五感着陆/番茄/认知重评/方箱呼吸/第三人称抽离/冲动冲浪/情绪命名/10-10-10/身体急停/我信息/六秒法则/记账本）。'+
    '</div><p style="color:var(--soft)">记住：场合不是秀脾气的地方，只是说观点的地方；别人的脸色还别人，自己的大活先动两分钟，心会越练越静。</p>'+
    '<div class="controls" style="justify-content:center"><button class="btn" onclick="location.reload()">🔁 再上一遍</button></div></div>';
  setSub('—— 今天的课结束啦，记得常回来练 ——');
}

(function(){
  const intro=document.createElement('div'); intro.className='card';
  intro.innerHTML='<h2>👋 准备好了吗？（第9天）</h2>'+
    '<div class="scene-text">这堂课大概 10 分钟。先带你复习前14招（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本），再讲一个新案例（2026-07-16 腾讯新闻：小敏被领导当众摔周报骂“吃干饭的”，为这话内耗整晚还去讨好）和两招新本领（课题分离法、两分钟启动法）。\n\n'+
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
    L.append("# 情绪管理课 · 晓晓老师课堂笔记（第9天 · ima 知识库 imao）\n")
    L.append("> 主题：克服专注力差、浮躁易怒、情绪化。核心理念：**场合不是展示真性情的地方，只是表达观点的地方。**\n")
    L.append("> 配套互动网页：`emotion-class-20260722.html`（晓晓老师 XiaoxiaoNeural 神经网络语音 + 不挡字幕 + 上一句/下一句可调位置 + 费曼式定时提问）。\n")
    L.append("> 第9天结构：**复习**前14招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本) → **新案例**(2026-07-16 腾讯新闻：小敏被领导当众摔周报骂“吃干饭的”、为这话内耗整晚还去讨好) → **原理**(阿德勒课题分离 + 启动效应) → **新招15**课题分离法(分清/归还/专注) → **新招16**两分钟启动法(拆/动/稳) → 费曼自测。\n")
    L.append("\n## 一、复习：前14招（情绪技能地图）\n")
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
    L.append("- 这十四招管“快炸/走神/不专注/念头歪/手抖想怼/上头那一秒/心里乱/一点就炸/身体先炸/想回嘴/情绪过去就忘/大活不动手”。今天两招管最前面的“替别人内耗（别人脸色一变就跟着浮）”和“大活不动手、浮躁坐不住”。\n")
    L.append("\n## 二、今日新案例（2026-07-16 腾讯新闻《上班只为碎银几两，别为烂人消耗自己》，人物化名）\n")
    L.append("素材：小敏，济南一家互联网公司做运营。一次周会，领导当众把她的周报摔在桌上，指着鼻子骂“连个基础表都捋不明白，招你进来是吃干饭的？”。小敏当场憋泪，改了三版熬到深夜。回家后翻来覆去想那句话，凌晨三点没睡；第二天到公司还主动帮那个领导订咖啡（被骂的竟去讨好）。结果月底评优给了领导刚入职三个月的小舅子，小敏当晚急性胃炎，医药费加误工扣的钱比绩效奖金还多两千。\n")
    L.append("- 关键数据（文内调研）：职场人平均每天花 **2.1 小时**在“无效情绪消耗”上，一年相当于多上 27 个“情绪班”；更狠的是——**78% 的内耗，都是花在“接别人的课题”上**：领导一句吐槽琢磨半天、同事一个眼神复盘半小时。小敏就是把“领导的课题”背了自己一整晚。\n")
    L.append("- 初中生版启示：领导怎么评价你、同事甩不甩脸，那是**他们的课题、后果他们担**；你为这话失眠、讨好、胃炎，等于替别人背了课题，自己亏大了。场合是讲观点的地方；你管不住别人失不失态，只能还回别人的课题、写好自己的活。\n")
    L.append("\n## 三、原理：两个道理（阿德勒课题分离 + 启动效应）\n")
    L.append("- **道理一 阿德勒课题分离（谁承担结果，就是谁的活）**：心理学家阿德勒一句话点破——领导骂你，是他情绪管理差，后果他担；你活干没干完，是你自己的事，后果你担。两边别混。别人甩脸、同事阴阳、群里一句难听话，都是他们的课题，你接过来背身上只会压垮自己。你只负责把分内活写好、把观点说清，剩下的还给他们。\n")
    L.append("- **道理二 启动效应（动起来就不浮）**：心理学发现，人一旦动起来，焦虑会往下掉。像推一辆停住的车，最难是刚推那一下；推起来，惯性就帮你走。你越拖着不动越浮躁；手指一动，心就静。还有“蔡格尼克效应”：没做完的事总在脑子里转，越想越烦；先动手做一点点，那股“悬着”的浮躁就落地。所以：别人的事还别人（课题分离）；自己的大活，先拆一小步动起来（启动效应）。\n")
    L.append("- 一句话：嘴替别人背情绪是因为没分清课题；大活不动手是因为没启动。道理一→课题分离法；道理二→两分钟启动法。\n")
    L.append("\n## 四、新招15：课题分离法（阿德勒，别人的情绪是别人的事）\n")
    L.append("适用：别人脸色一变你就跟着浮躁一整天、忍不住琢磨“他是不是针对我”、还想去讨好。一句话——别人的情绪、别人的评价，是别人的事；谁承担后果谁负责。你只管把分内活写好、把观点说清。三步：\n")
    L.append("- **①分清**：遇到事先问“这是谁的事？”领导批评我、同事甩脸——这是他们的情绪课题，后果他们担；我活干没干完、我说没说清——这是我的事。先把线画清楚。\n")
    L.append("- **②归还**：别人的课题，还给别人。同事阴阳怪气，心里说“这是他的情绪，我不当接盘侠”，把注意力拉回自己的活；不解释、不讨好、不替他背。\n")
    L.append("- **③专注**：把省下的力气花在自己事上——把周报写好、用我信息把观点说清。你越专注自己的课题，别人的脸色越掀不起你的浪。\n")
    L.append("- 要点：同事甩脸、领导发火，那是他们的“小账簿”，你不用替他们记；你的活儿你写好，别人的课题你不扛。这招直接呼应核心理念——场合是表达观点的地方，不是替谁情绪买单的地方。（身体急停法也能帮你先把那股“想琢磨”的劲儿降下来。）\n")
    L.append("\n**课题分离口诀**\n")
    L.append("> 同事甩脸领导火，那是他的小账簿；我的活儿我写好，别人的题我不扛。\n")
    L.append("\n## 五、新招16：两分钟启动法（专治大活不动手、浮躁坐不住）\n")
    L.append("适用：大活一摆就慌、迟迟不动、刷手机两小时还没动笔。一句话——再大的活，先只做“两分钟”或“第一步”，动起来浮躁就散。三步：\n")
    L.append("- **①拆**：大活摆眼前心慌？拆成一口能吃的小块。别想“写完整个报告”，先想“只写个标题”；别想“收拾整间屋”，先想“只叠两件衣服”。拆到小到不用鼓勇气就能动。\n")
    L.append("- **②动**：给自己定个超短闹钟——只做两分钟。两分钟一到可以停。但神奇的是，一旦动了你多半会接着做。像推车，最难是推那一下，推起来就顺（启动效应）。\n")
    L.append("- **③稳**：动起来后用番茄专注法（25分钟只做一事）把专注养出来；走神了用五感着陆拉回。原来让你浮一上午的“大活”，动两分钟就不吓人了。\n")
    L.append("- 要点：浮躁不是你懒，是“没启动”；启动那一下最难也最值。越逼“必须写完”越浮躁越不动；先动两分钟，比想一下午强。（启动效应 + 蔡格尼克效应：做一点点，悬着的浮躁就落地。）\n")
    L.append("\n**两分钟启动口诀**\n")
    L.append("> 大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵。\n")
    L.append("\n## 六、费曼自测题（旧+新结合）\n")
    L.append("用自己的话回答：*如果下次同事又甩脸子、或者领导又当众批评我，让我一整天浮躁、还忍不住想讨好、想琢磨“他是不是针对我”，我会怎么做，才能既不替别人背情绪、又能管住浮躁、把该干的活干好？*\n")
    L.append("标准答案要点：\n")
    L.append("1. 先课题分离（分清/归还/专注）：领导批评、同事甩脸是**他们的课题**（后果他们担），我不背；只把注意力拉回自己的活、用我信息把观点说清。绝不替别人情绪买单，也绝不因为“他针对我”把自己一上午搭进去。\n")
    L.append("2. 身体被勾动时——身体急停法（离开/喝口水/握拳松拳）先降温；想回怼时——六秒法则（闭嘴数六）+ 我信息只说观点；上头时——第三人称抽离+冲动冲浪。\n")
    L.append("3. 面对大活/浮躁坐不住——两分钟启动法（拆成只写标题这种小步→定两分钟闹钟只做一点→动起来启动效应推着走），再用番茄专注+五感着陆养专注。不逼“必须写完”，先动两分钟。\n")
    L.append("4. 心里乱/一点就炸时——情绪命名法+10-10-10 透视法；快炸/念头歪用五步刹车+认知重评；手抖配方箱呼吸；睡前用情绪记账本三栏（触发/念头/新招）复盘。始终记：场合不是秀脾气的地方，只是说观点的地方；别人的脸色还别人，自己的大活先动两分钟。\n")
    L.append("\n## 七、今日带走的两句新口诀\n")
    L.append("1. 课题分离法：同事甩脸领导火，那是他的小账簿；我的活儿我写好，别人的题我不扛。\n")
    L.append("2. 两分钟启动法：大活先拆第一步，只做两分不贪多；手指一动心就静，专注慢慢长成棵。\n")
    L.append("3. 一句话收尾：场合不是秀脾气的地方，只是说观点的地方；别人的脸色还别人，自己的大活先动两分钟，心会越练越静。\n")
    return "\n".join(L)

# ---------------------------------------------------------------- 主流程
def main():
    audio = build_audio()
    sections_js = "window.SECTIONS = " + json.dumps(SECTIONS, ensure_ascii=False) + ";"
    audio_js = "window.AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";"
    html = HTML.replace("__LESSON_DATA__", sections_js).replace("__AUDIO_DATA__", audio_js)
    out_html = os.path.join(WS, "emotion-class-20260722.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html] 写出 {out_html} ({len(html)/1024:.0f} KB)")
    md = build_markdown()
    out_md = os.path.join(WS, "情绪管理-晓晓老师课堂笔记.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出 {out_md} ({len(md)/1024:.0f} KB)")
    dated = os.path.join(WS, "情绪管理-晓晓老师课堂笔记_20260722.md")
    with open(dated, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出带日期副本 {dated} ({len(md)/1024:.0f} KB)")
if __name__ == "__main__":
    main()
