# -*- coding: utf-8 -*-
"""
情绪管理课 builder（2026-07-19 · 第六天）
- 单一内容源 -> 生成 晓晓老师(XiaoxiaoNeural) 每句语音(base64 内联)
- 输出「独立」单文件自包含 emotion-class-20260719.html (宋体/可调播放位置/上一句下一句/不挡字幕/费曼提问)
  ※ 每天一个新文件，绝不覆盖旧课页面（满足"每个网页对应一课不要更新网页"）
- 同时输出 情绪管理-晓晓老师课堂笔记.md 与 带日期副本 供存入 ima 知识库 imao
本日结构：复习前八招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪)
  -> 新案例(2026-03 田某 工资被扣→大群爆粗辱骂主管, 主管仅回"下午来沟通")
  -> 原理(情绪命名的大脑跷跷板 + 10-10-10 长镜头)
  -> 新招1 情绪命名法 -> 新招2 10-10-10 透视法 -> 费曼自测
"""
import os, json, base64, asyncio, sys, shutil

WS = "C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-8%"
PITCH = "+0Hz"

# ---------------------------------------------------------------- 案例插画（内联 SVG，保证离线可开）
SVG_MAP = '''<svg viewBox="0 0 660 250" xmlns="http://www.w3.org/2000/svg">
  <text x="330" y="22" font-size="16" fill="#5b8def" text-anchor="middle" font-family="sans-serif">🗺️ 情绪技能地图 · 前八招复习</text>
  <g font-family="sans-serif">
   <rect x="14" y="40" width="150" height="90" rx="13" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="89" y="68" font-size="14" fill="#2b6fb0" text-anchor="middle" font-weight="bold">①五步刹车</text>
   <text x="89" y="90" font-size="11" fill="#243447" text-anchor="middle">停·数·命名·转·说</text>
   <text x="89" y="112" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🔥快炸时灭火</text>
   <rect x="170" y="40" width="150" height="90" rx="13" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="245" y="68" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">②静音模式</text>
   <text x="245" y="90" font-size="11" fill="#243447" text-anchor="middle">心是一杯水</text>
   <text x="245" y="112" font-size="10.5" fill="#6b7c8f" text-anchor="middle">💧有火不泼人</text>
   <rect x="326" y="40" width="150" height="90" rx="13" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="401" y="68" font-size="14" fill="#c98a14" text-anchor="middle" font-weight="bold">③五感着陆</text>
   <text x="401" y="90" font-size="11" fill="#243447" text-anchor="middle">看5摸4听3</text>
   <text x="401" y="112" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🌀走神时着陆</text>
   <rect x="482" y="40" width="150" height="90" rx="13" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="557" y="68" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">④番茄专注</text>
   <text x="557" y="90" font-size="11" fill="#243447" text-anchor="middle">25分只做一事</text>
   <text x="557" y="112" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🍅练定力</text>
   <rect x="14" y="150" width="150" height="90" rx="13" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="89" y="178" font-size="14" fill="#d6455f" text-anchor="middle" font-weight="bold">⑤认知重评</text>
   <text x="89" y="200" font-size="11" fill="#243447" text-anchor="middle">停·揪·换想法</text>
   <text x="89" y="222" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🧠换念换情绪</text>
   <rect x="170" y="150" width="150" height="90" rx="13" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="245" y="178" font-size="14" fill="#1c7a9c" text-anchor="middle" font-weight="bold">⑥方箱呼吸</text>
   <text x="245" y="200" font-size="11" fill="#243447" text-anchor="middle">吸4憋7呼8憋4</text>
   <text x="245" y="222" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🌬️手抖时降温</text>
   <rect x="326" y="150" width="150" height="90" rx="13" fill="#eef7f2" stroke="#2bb673" stroke-width="2"/>
   <text x="401" y="178" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">⑦第三人称抽离</text>
   <text x="401" y="200" font-size="11" fill="#243447" text-anchor="middle">退后·换角·劝友</text>
   <text x="401" y="222" font-size="10.5" fill="#6b7c8f" text-anchor="middle">👁旁观一眼冷</text>
   <rect x="482" y="150" width="150" height="90" rx="13" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="557" y="178" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">⑧冲动冲浪</text>
   <text x="557" y="200" font-size="11" fill="#243447" text-anchor="middle">认浪·看浪·等浪退</text>
   <text x="557" y="222" font-size="10.5" fill="#6b7c8f" text-anchor="middle">🌊浪过你还在</text>
  </g>
</svg>'''

SVG_CASE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <rect width="640" height="250" fill="#fdf3f1"/>
  <text x="320" y="24" font-size="15" fill="#c0492a" text-anchor="middle" font-family="sans-serif">案例：工资被扣，他在几百人大群里爆粗，主管只回一句</text>
  <!-- 田某：群内开喷 -->
  <circle cx="118" cy="84" r="28" fill="#ffd9b8"/>
  <path d="M92 166 Q118 122 144 166 Z" fill="#6b8fd6"/>
  <path d="M104 78 l10 8 M132 78 l-10 8" stroke="#c0392b" stroke-width="3.2"/>
  <path d="M108 98 q10 11 20 0" stroke="#c0392b" stroke-width="3" fill="none"/>
  <rect x="58" y="116" width="120" height="44" rx="12" fill="#fff" stroke="#ff8a8a" stroke-width="1.6"/>
  <text x="118" y="135" font-size="10.5" fill="#c0392b" text-anchor="middle" font-family="sans-serif">“扣我三四千，</text>
  <text x="118" y="150" font-size="10.5" fill="#c0392b" text-anchor="middle" font-family="sans-serif">什么鸡巴领导！”</text>
  <text x="320" y="60" font-size="11" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">😡 还晒出部门工资</text>
  <text x="118" y="206" font-size="12.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">田某：爆粗→泄密→辞退</text>
  <text x="320" y="120" font-size="30" fill="#c0492a" text-anchor="middle">VS</text>
  <!-- 主管：冷静 -->
  <circle cx="500" cy="84" r="28" fill="#ffd9b8"/>
  <path d="M474 166 Q500 126 526 166 Z" fill="#9a9a9a"/>
  <circle cx="491" cy="82" r="3" fill="#3a3a3a"/><circle cx="509" cy="82" r="3" fill="#3a3a3a"/>
  <path d="M489 92 q11 7 22 0" stroke="#1c7a4d" stroke-width="2.4" fill="none"/>
  <rect x="440" y="116" width="120" height="44" rx="12" fill="#fff" stroke="#bfe3c9" stroke-width="1.6"/>
  <text x="500" y="135" font-size="10.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">“有问题下午</text>
  <text x="500" y="150" font-size="10.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">来找我沟通”</text>
  <text x="500" y="206" font-size="12.5" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">主管：只说观点→稳住场面</text>
  <text x="320" y="238" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">委屈是真的，但把群当倒情绪的地方，诉求没解决还丢了工作</text>
</svg>'''

SVG_PRINCIPLE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">两个道理：命名踩刹车（大脑跷跷板）· 拉远看开（长镜头）</text>
  <g font-family="sans-serif">
   <rect x="20" y="40" width="290" height="192" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="165" y="66" font-size="13.5" fill="#2b6fb0" text-anchor="middle" font-weight="bold">道理一 · 命名踩刹车</text>
   <!-- 跷跷板 -->
   <line x1="60" y1="150" x2="270" y2="150" stroke="#9aa7bd" stroke-width="3"/>
   <polygon points="165,150 156,168 174,168" fill="#9aa7bd"/>
   <circle cx="80" cy="128" r="20" fill="#ffd6cf"/><text x="80" y="133" font-size="14" text-anchor="middle">🔥</text>
   <text x="80" y="166" font-size="10.5" fill="#c0492a" text-anchor="middle">杏仁核(火)</text>
   <circle cx="250" cy="128" r="20" fill="#cfe6ff"/><text x="250" y="133" font-size="14" text-anchor="middle">❄️</text>
   <text x="250" y="166" font-size="10.5" fill="#1c7a9c" text-anchor="middle">前额叶(理智)</text>
   <text x="165" y="196" font-size="11" fill="#243447" text-anchor="middle">一说"我很生气"→</text>
   <text x="165" y="214" font-size="11" fill="#1c7a4d" text-anchor="middle">理智那头压下火，火就熄</text>
   <rect x="340" y="40" width="290" height="192" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="485" y="66" font-size="13.5" fill="#5b3fd6" text-anchor="middle" font-weight="bold">道理二 · 长镜头看开</text>
   <circle cx="400" cy="120" r="26" fill="#ffd6cf" stroke="#c0492a" stroke-width="2"/>
   <text x="400" y="124" font-size="11" fill="#c0492a" text-anchor="middle">现在</text>
   <text x="400" y="162" font-size="10.5" fill="#c0492a" text-anchor="middle">天塌了？</text>
   <line x1="430" y1="120" x2="500" y2="120" stroke="#9aa7bd" stroke-width="2" stroke-dasharray="5 4"/>
   <circle cx="540" cy="120" r="16" fill="#e6e0f2" stroke="#7c5cff" stroke-width="2"/>
   <text x="540" y="124" font-size="9.5" fill="#5b3fd6" text-anchor="middle">10月</text>
   <line x1="558" y1="120" x2="598" y2="120" stroke="#9aa7bd" stroke-width="2" stroke-dasharray="5 4"/>
   <circle cx="612" cy="120" r="9" fill="#efeaf7" stroke="#b9a9e6" stroke-width="1.6"/>
   <text x="485" y="186" font-size="11" fill="#6b7c8f" text-anchor="middle">10年后→连水花都不是</text>
   <text x="485" y="210" font-size="11" fill="#5b3fd6" text-anchor="middle">拉远看，浮躁就泄了气</text>
  </g>
</svg>'''

SVG_NAME = '''<svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">情绪命名法：先给那团乱起个精准的名字</text>
  <g font-family="sans-serif">
   <rect x="20" y="44" width="170" height="110" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="105" y="72" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 命名</text>
   <text x="105" y="98" font-size="11.5" fill="#243447" text-anchor="middle">别只说"我好烦"</text>
   <text x="105" y="118" font-size="11.5" fill="#243447" text-anchor="middle">是委屈？丢脸？</text>
   <text x="105" y="138" font-size="11.5" fill="#243447" text-anchor="middle">被否定？</text>
   <path d="M194 99 l24 0 M210 91 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="235" y="44" width="170" height="110" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="320" y="72" font-size="14" fill="#c98a14" text-anchor="middle" font-weight="bold">② 打分</text>
   <text x="320" y="100" font-size="11.5" fill="#243447" text-anchor="middle">情绪温度计</text>
   <text x="320" y="122" font-size="20" fill="#c0492a" text-anchor="middle">0 ── 10 分</text>
   <text x="320" y="144" font-size="11.5" fill="#243447" text-anchor="middle">量化，它就变小</text>
   <path d="M409 99 l24 0 M425 91 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="450" y="44" width="170" height="110" rx="14" fill="#eef7f2" stroke="#2bb673" stroke-width="2"/>
   <text x="535" y="72" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">③ 说/写</text>
   <text x="535" y="98" font-size="11.5" fill="#243447" text-anchor="middle">小声说·写日记</text>
   <text x="535" y="118" font-size="11.5" fill="#243447" text-anchor="middle">录段语音也行</text>
   <text x="535" y="138" font-size="11.5" fill="#243447" text-anchor="middle">理智就回来</text>
   <text x="320" y="186" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">名字一起，理智上线，再只把观点说清</text>
  </g>
</svg>'''

SVG_101010 = '''<svg viewBox="0 0 640 210" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#7c5cff" text-anchor="middle" font-family="sans-serif">10-10-10 透视法：把眼前炸点拉到长镜头里看</text>
  <g font-family="sans-serif">
   <circle cx="110" cy="100" r="54" fill="#ffe0d6" stroke="#c0492a" stroke-width="2.5"/>
   <text x="110" y="96" font-size="16" fill="#c0492a" text-anchor="middle" font-weight="bold">10分钟后</text>
   <text x="110" y="118" font-size="12" fill="#c0492a" text-anchor="middle">还气吗？</text>
   <path d="M170 100 l40 0 M200 92 l9 8 -9 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <circle cx="330" cy="100" r="38" fill="#efe6ff" stroke="#7c5cff" stroke-width="2.5"/>
   <text x="330" y="96" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">10个月后</text>
   <text x="330" y="116" font-size="11.5" fill="#5b3fd6" text-anchor="middle">还重要？</text>
   <path d="M378 100 l40 0 M408 92 l9 8 -9 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <circle cx="520" cy="100" r="24" fill="#f5f0ff" stroke="#b9a9e6" stroke-width="2"/>
   <text x="520" y="98" font-size="12" fill="#7c5cff" text-anchor="middle">10年后</text>
   <text x="520" y="116" font-size="10" fill="#7c5cff" text-anchor="middle">谁记得</text>
   <text x="320" y="186" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">多数"炸点"只值10分钟——拉远看，浮躁就散了</text>
  </g>
</svg>'''

# ---------------------------------------------------------------- 课程内容（第六天）
SECTIONS = [
  {"type":"speak","title":"开场 · 第六天，先串起前八招","rhyme":None,"img":None,"sentences":[
    "同学你好，我是晓晓老师。咱们的情绪管理课到第六天啦！前五天你攒了八招本领：第一天五步刹车加静音模式，第三天五感着陆加番茄专注，第四天认知重评加方箱呼吸，第五天第三人称抽离加冲动冲浪。今天先把这八招串成一张'情绪技能地图'，再教你两招新本领，专治'心里乱糟糟、说不清自己怎么了、一点小事就炸'。",
    "先复习老口号：任何场合——办公室、工作群、会议室——都不是展示真性情的地方，它只是表达观点的地方。你是去'把事说清楚'的，不是去'把脾气秀出来'的。",
    "今天要补的，是你最吃亏的一类时刻：心里一团火，但说不清自己到底是'委屈'还是'被忽视'，结果一开口就变怼人、变闹情绪。咱们先复习地图，再用一个 2026 年网上热传的真事开场。"
  ]},

  {"type":"speak","title":"复习 · 八招技能地图","rhyme":None,"img":SVG_MAP,"sentences":[
    "先复习八招，编成一张地图。第一招五步刹车——一停二数三命名，四转五说；火气冒头先喊停，只说观点不秀脾气。第二招静音模式——心是一杯水，摇浑放自清，收拾不了局别纵脾气。",
    "第三招五感着陆——看五摸四听三声，闻二尝一拉回神；走神坐不住用它。第四招番茄专注——二十五分专注钟，五分休息不硬撑，手机扔远练定力。第五招认知重评——火起先喊停、揪出念头、换个想法，换想法就换情绪。",
    "第六招方箱呼吸——吸气四憋七呼八憋四，画方箱一分钟降温。第七招第三人称抽离——退后、换角、劝友，把'我'换成'朋友视角'火就小。第八招冲动冲浪——认浪、看浪、等浪退，约十分钟浪自己走。这八招管的是'已经炸了、快炸了、走神了、不专注、念头歪了、手抖想怼、上头那一秒'。"
  ]},

  {"type":"quiz","title":"复习小测 · 上头想发狠话用哪两招","quiz":{
    "q":"你被一句话点着，手已经放在键盘上想打狠话发出去。前八招里，你该优先用哪两招先'刹住'？",
    "opts":[
      {"t":"五步刹车（一停二数…）+ 五感着陆（那是走神时用的）","ok":False},
      {"t":"第三人称抽离（退后换角劝友）+ 冲动冲浪（认浪看浪等浪退）","ok":True},
      {"t":"番茄专注 + 方箱呼吸（番茄是平时练定力，不是救火）","ok":False}
    ],
    "stu":"小豪抢答：老师，是不是先番茄钟定个心？",
    "teacher":"晓晓老师笑：番茄钟是平时练定力的，不是救火用的。你现在手放键盘、火已上头，得用第七招抽离（退一步当旁观者）和第八招冲浪（等那股火退下去）。各招分工不同：抽离管'上头那一秒'、冲浪管'冲动已起'，它们才是这一刻的灭火器。",
    "card":["上头想发狠话=第三人称抽离(退后换角劝友)+冲动冲浪(认浪看浪等浪退)。","八招各管一段：抽离管上头、冲浪管冲动，别乱用。"]
  }},

  {"type":"speak","title":"第一幕 · 新案例：工资被扣，他在大群里爆粗","rhyme":None,"img":SVG_CASE,"sentences":[
    "讲个 2026 年 3 月网上热传的职场真事（来源今日头条热帖，人物化名）。主人公田某，在一家公司生产中心干活，导火索是一张工资截图——他发现自己一个月一万二的工资，被扣了两三千。",
    "田某心里委屈又火大，没去找主管好好聊，而是直接在公司几百人的大群里，@主管连发带脏话的质问：'上个月全被你们扣了三四千，这个月又扣两三千，什么鸡巴领导'，甚至说了很过分、诅咒的话，还把整个部门的工资数据晒了出来。",
    "群里一下炸了。可你猜主管回啥？主管只在群里回了一句：'有问题下午来找我沟通处理。'——人家根本没在群里接他的火，更没对骂。",
    "结局：公司认定田某泄露经营数据、公然辱骂主管、还煽动同事，属于严重违纪，直接解除劳动合同。网友一边骂公司'扣钱太狠'，一边也承认：委屈是真的，但在几百人群里爆粗、晒工资，这表达方式把自己坑了。",
    "你看，田某的'委屈'一点不假——被扣钱谁不憋屈？但他把'场合'当成了'倒情绪、秀真性情'的地方，一句狠话把诉求和脾气搅成一团，最后诉求没解决，自己还丢了脸、丢了工作。今天两招，就教你怎么把'情绪'和'观点'分开。"
  ]},

  {"type":"quiz","title":"课间提问① · 田某最吃亏在哪","quiz":{
    "q":"田某最吃亏的地方在哪？",
    "opts":[
      {"t":"他工资被扣是假的，是编的","ok":False},
      {"t":"他的委屈是真的，但把场合当成了倒情绪、秀真性情的地方，用爆粗代替了'说观点、提诉求'","ok":True},
      {"t":"主管故意不理他，才把他逼急的","ok":False}
    ],
    "stu":"小丽：那公司扣他钱，难道就对了？",
    "teacher":"晓晓老师点头：公司扣钱合不合理，那是另一回事，可以走正规渠道去争。但田某错在'表达'——场合是讲观点的地方，不是倒情绪的地方。你越在群里秀真性情、爆粗，越没人听你诉求，还把自己坑了。分开两步：先认情绪，再提观点。",
    "card":["田某崩在：委屈是真的，却把场合当倒情绪/秀真性情的地方，用爆粗代替提诉求。","场合只说观点；情绪归情绪，诉求归诉求，两件事分开办。"]
  }},

  {"type":"speak","title":"第二幕 · 原理：命名踩刹车 + 长镜头看开","rhyme":None,"img":SVG_PRINCIPLE,"sentences":[
    "为什么'说不清自己怎么了'最容易炸？又为什么'看开一点'就不炸了？科学家讲了两个道理，初中生都懂。",
    "道理一：给情绪起个名字，大脑就踩刹车。美国 UCLA 用脑扫描发现：你看到生气害怕的脸，脑子里'杏仁核'（情绪警报器）会狂响；可一旦你说出'我现在很生气'这几个字，杏仁核的火就降下来，而'前额叶'（管理智的区域）亮起来。就像跷跷板：你一命名，理智那头压下情绪那头。",
    "道理二：眼前的大事，拉长时间看就变小。你此刻觉得'天塌了'的那点事，放到 10 个月后、10 年后看，多半连个小水洼都不算。所以'看不开'往往是因为你只盯着眼前的这一秒。",
    "记住一句话：你不是你的情绪，你是那个'给情绪起名、再把它放到时间长河里看'的人。道理一对应'情绪命名法'，道理二对应'10-10-10 透视法'。"
  ]},

  {"type":"quiz","title":"课间提问② · 为什么'说出来'能冷静","quiz":{
    "q":"为什么'把“我很生气”说出口或写下来'能让你冷静？",
    "opts":[
      {"t":"因为说出去就解气了，别人都听见了","ok":False},
      {"t":"因为给情绪起名，会让大脑的杏仁核(警报器)熄火、前额叶(理智)亮起，等于给情绪踩了刹车","ok":True},
      {"t":"因为写下来就不用管它了","ok":False}
    ],
    "stu":"小明：那我发个朋友圈骂一顿，不也算'说出来'？",
    "teacher":"晓晓老师摆手：发圈是把火往外倒，越倒越上头，还坑自己（看田某晒工资）。'命名'是把情绪说给'自己'听——小声嘀咕、写日记、录语音都行。这一命名，理智就上线、火就降温。场合里尤其别把群当树洞。",
    "card":["情绪命名：说出/写下'我很委屈+被忽视'，杏仁核熄火、前额叶亮起=踩刹车。","发泄是倒火(越倒越上头)；命名是给火起名(理智上线)。"]
  }},

  {"type":"speak","title":"第三幕 · 新招1：情绪命名法（给乱糟糟起个名）","rhyme":{
    "title":"🎵 命名口诀",
    "lines":["心里乱糟糟，先给<b>情绪起个名</b>；","<b>委屈</b>或<b>丢脸</b>，精准才管用。","<b>温度计打分</b>，零到十分量一量；","<b>说出口写下来</b>，理智回来再讲理。"]
  },"img":SVG_NAME,"sentences":[
    "新本领第一招：情绪命名法。一句话——心里一团乱时，先给那团情绪起个精准的名字，再开口说话。三步走：",
    "第一步'命名'：别只说'我好烦'，要精准。是'委屈'？'被忽视'？'丢脸'？'害怕被否定'？名字越准，降温越狠。研究说，精准命名比模糊说'我不好'效果好得多。",
    "第二步'打分'：在心里给这股情绪打 0 到 10 分（情绪温度计）。'我现在愤怒 8 分'——一量化，它就从'淹没你的洪流'变成'你能观察的对象'。",
    "第三步'说或写'：小声说出、写下来、或录段语音。光在脑子里想也行，但说出来/写下来，大脑刹车反应更强。写完这步，你通常已经没那么想怼人了，再只把观点说清。",
    "记住：你不是你的情绪，你是那个'给情绪起名'的人。名字一起，理智就回来了。先别问'为什么'，命名本身就是救命的那一下。",
    "记口诀：心里乱糟糟，先给情绪起个名；委屈或丢脸，精准才管用。温度计打分，零到十分量一量；说出口写下来，理智回来再讲理。"
  ]},

  {"type":"quiz","title":"课间提问③ · 命名法怎么用","quiz":{
    "q":"你被领导当众批评，脸通红想回怼'你才不懂'。按情绪命名法，第一步该做啥？",
    "opts":[
      {"t":"立刻回怼，不怼更丢人","ok":False},
      {"t":"先精准给情绪起名（如'我现在感到丢脸+被否定'），再打分、再说/写下来，等理智回来","ok":True},
      {"t":"假装没事但其实记仇","ok":False}
    ],
    "stu":"小美：被当众说，不怼回去不就怂了？",
    "teacher":"晓晓老师摇头：命名不是认怂，是'先稳住再开口'。你精准叫出'我是觉得丢脸、被否定'，杏仁核就熄火，前额叶亮起，这时你回的可能是'这点我接受，但我有个不同看法'——既保住体面，又把观点说清。场合里，怼回去才是真丢人。",
    "card":["情绪命名法：①精准起名(委屈/丢脸/被否定)②温度计打分0-10③说或写下来。","命名不是认怂，是给情绪踩刹车，再开口说观点。"]
  }},

  {"type":"speak","title":"第四幕 · 新招2：10-10-10 透视法（拉远看开）","rhyme":{
    "title":"🎵 透视口诀",
    "lines":["<b>火起别盯眼前</b>，三问拉远看一看；","<b>十分后</b>还气吗？<b>十月后</b>算个啥？","<b>十年后</b>谁记得？小事一朵浪花。","长镜头里看自己，<b>浮躁散了心安定</b>。"]
  },"img":SVG_101010,"sentences":[
    "新本领第二招：10-10-10 透视法。一句话——上头时，把眼前这件'天塌了'的事，放到三个时间镜头里看，火就散了。三问：",
    "第一问'10 分钟后，我还气吗？'——多半已经忘了，气个啥。第二问'10 个月后，这事还重要吗？'——大概率早翻篇了。第三问'10 年后，谁还记得？'——连影子都没了。",
    "你会发现：绝大多数的'炸点'，只值 10 分钟。你盯着眼前这一秒，才觉得天塌；拉远看，它只是长河里一个小水花。这一拉远，'浮躁'就泄了气。",
    "用法：火上来时，心里默念这三问，像把镜头从'特写'拉到'全景'。配合情绪命名一起用更稳：先命名稳住，再拉远看开，最后只把观点报。",
    "记口诀：火起别盯眼前，三问拉远看一看；十分后还气吗？十月后算个啥？十年后谁记得？小事一朵浪花。长镜头里看自己，浮躁散了心安定。"
  ]},

  {"type":"quiz","title":"课间提问④ · 10-10-10 怎么用","quiz":{
    "q":"同事又甩锅给你，你火大想当场掀桌。用 10-10-10 透视法，你会怎么想？",
    "opts":[
      {"t":"现在就掀桌，反正他欺负我","ok":False},
      {"t":"问自己：10分钟后还气吗、10个月后还重要吗、10年后谁记得？多半只值10分钟，于是拉远看、只提观点不掀桌","ok":True},
      {"t":"憋着但心里记一辈子","ok":False}
    ],
    "stu":"小刚：可是他老甩锅，不闹以后更被欺。",
    "teacher":"晓晓老师点头：甩锅是要解决，但'掀桌'解决不了，反而让你背锅。10-10-10 不是叫你忍，是叫你'别被眼前这一秒带跑'。拉远看后，你照样可以冷静提诉求：'这活儿口径不对，咱们对一下责任人。'既护住自己，又不秀脾气。场合是讲观点的地方。",
    "card":["10-10-10：10分后/10月后/10年后还重要吗？多数只值10分钟。","透视不是忍，是拉远看、不被眼前一秒带跑，再提观点。"]
  }},

  {"type":"speak","title":"结尾 · 今天你带走什么（前八招+两新招）","rhyme":None,"img":None,"sentences":[
    "今天的课到这儿，晓晓老师带你总复习。",
    "前八招（复习）：五步刹车——一停二数三命名，四转五说；静音模式——心是一杯水；五感着陆——看五摸四听三声；番茄专注——二十五分只做一事；认知重评——停揪换、换想法就换情绪；方箱呼吸——吸4憋7呼8憋4；第三人称抽离——退后换角劝友；冲动冲浪——认浪看浪等浪退。",
    "新本领①：情绪命名法——精准起名、温度计打分、说或写下来；你不是你的情绪，你是给情绪起名的人。新本领②：10-10-10 透视法——10分后、10月后、10年后还重要吗？拉远看，浮躁就散。",
    "一句话收尾：场合不是秀脾气的地方，只是说观点的地方；心里乱时，先给情绪起个名、再把镜头拉远看，最后只把观点说清。慢慢来，心会越练越静。下课！"
  ]},

  {"type":"feynman","title":"费曼小测 · 讲给晓晓老师听","text":
    "费曼学习法说：你以为你懂了，不算懂；能用自己的话讲明白，才是真懂。\n\n现在轮到你啦——请用你自己的话，把下面这道题讲给晓晓老师听：\n\n'如果下次我又被一句话点着，或者像田某那样觉得委屈想爆粗、想在工作群里发作，我会怎么做，才能既把委屈/诉求说清、又不发火、还不丢人？'\n\n提示：可以结合旧本领（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪）和新本领（情绪命名法、10-10-10 透视法）一起说。\n\n在下面的框里写几句（或对着麦克风讲出来也行）。写完了，翻回上面的口诀卡对照一下，看看漏了哪一步。"
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
<title>晓晓老师的情绪管理课 · 第6天：先起名，再看开</title>
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
  .scene-img{ width:100%; max-width:660px; margin:6px auto 16px; border-radius:14px; overflow:hidden;
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
  <h1>晓晓老师的情绪管理课 · 第6天</h1>
  <p>先起名，再看开：场合不是秀脾气的地方，只是说观点的地方 🧊</p>
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
    '<textarea id="fm" placeholder="在这里用你自己的话写一写（比如：我先给情绪起个名——我是觉得委屈+被否定；再用10-10-10拉远看，发现只值10分钟；最后只把观点说清…）…"></textarea>'+
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
    '<b>🎵 今日口诀（前八招 + 两新招）</b><br>'+
    '一停二数三命名，四转五说心如镜；场合只把观点讲，静音模式最清醒。<br>'+
    '心是一杯水，摇浑放自清；拍桌水会洒，残局难收平。<br><br>'+
    '看五摸四听三声，闻二尝一拉回神；二十五分专注钟，五分休息不硬撑。<br><br>'+
    '火起先喊停，揪出那念头；是不是针对？换个想法透。<br>'+
    '吸气四秒憋七秒，呼气八秒再四秒；画个方箱心就静，开口只把观点报。<br><br>'+
    '退后换角劝朋友，旁观一眼火就收；冲动像浪会退下，方箱呼吸等它走。<br><br>'+
    '心里乱糟糟，先给情绪起个名；委屈或丢脸，精准才管用。温度计打分，零到十分量一量；说出口写下来，理智回来再讲理。<br>'+
    '火起别盯眼前，三问拉远看一看；十分后还气吗？十月后算个啥？十年后谁记得？小事一朵浪花。长镜头里看自己，浮躁散了心安定。'+
    '</div><p style="color:var(--soft)">记住：场合不是秀脾气的地方，只是说观点的地方。先起名、再看开，心会越练越静。</p>'+
    '<div class="controls" style="justify-content:center"><button class="btn" onclick="location.reload()">🔁 再上一遍</button></div></div>';
  setSub('—— 今天的课结束啦，记得常回来练 ——');
}

/* 开场卡片 */
(function(){
  const intro=document.createElement('div'); intro.className='card';
  intro.innerHTML='<h2>👋 准备好了吗？（第6天）</h2>'+
    '<div class="scene-text">这堂课大概 10 分钟。先带你复习前八招（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪），再讲一个新案例（田某工资被扣→大群爆粗，主管只回一句）和两招新本领（情绪命名法、10-10-10 透视法）。\n\n'+
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
    L.append("# 情绪管理课 · 晓晓老师课堂笔记（第6天 · ima 知识库 imao）\n")
    L.append("> 主题：克服专注力差、浮躁易怒、情绪化。核心理念：**场合不是展示真性情的地方，只是表达观点的地方。**\n")
    L.append("> 配套互动网页：`emotion-class-20260719.html`（晓晓老师 XiaoxiaoNeural 神经网络语音 + 不挡字幕 + 上一句/下一句可调位置 + 费曼式定时提问）。\n")
    L.append("> 第6天结构：**复习**前八招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪) → **新案例**(2026-03 田某 工资被扣→大群爆粗辱骂主管,主管仅回\"下午来沟通\") → **原理**(命名踩刹车的大脑跷跷板 + 10-10-10 长镜头) → **新招1**情绪命名法 → **新招2**10-10-10 透视法 → 费曼自测。\n")
    L.append("\n## 一、复习：前八招（情绪技能地图）\n")
    L.append("- **①五步刹车法**：一停、二数、三命名、四转、五说——火气冒头先喊停，只说观点不秀脾气。\n")
    L.append("- **②静音模式（心如止水）**：心是一杯水，安静清、摇晃浑；场合里拍桌水洒难收，有火不泼别人。\n")
    L.append("- **③五感着陆法（54321）**：看五摸四听三声，闻二尝一拉回神；走神、坐不住时把心拉回当下。\n")
    L.append("- **④番茄专注法**：二十五分专注钟，五分休息不硬撑；手机扔远练定力。\n")
    L.append("- **⑤认知重评三步法**：停、揪出念头、换个想法；换想法就换情绪。\n")
    L.append("- **⑥方箱呼吸（4-7-8）**：吸气4憋7呼8憋4，画方箱一分钟降温；手抖想怼时用。\n")
    L.append("- **⑦第三人称抽离法**：退后、换角、劝友——把“我”换成“朋友视角”，火先降一半；上头那一秒用。\n")
    L.append("- **⑧冲动冲浪法**：认浪、看浪、等浪退，约十分钟浪自己走；冲动已起时用。\n")
    L.append("- 这八招管“已经炸了/快炸了/走神了/不专注/念头歪了/手抖想怼/上头那一秒”。今天两招管更前面的环节——心里乱糟糟、说不清自己怎么了、一点小事就炸。\n")
    L.append("\n## 二、今日新案例（2026-03 网上热传，来源今日头条热帖，人物化名）\n")
    L.append("素材：田某，某公司生产中心员工。导火索是一张工资截图——他发现自己一个月一万二的工资，被扣了两三千。\n")
    L.append("- 田某心里委屈又火大，没去找主管好好聊，而是直接在公司几百人的大群里，@主管连发带脏话的质问（“扣我三四千，什么鸡巴领导”），还说了很过分的话，并把整个部门工资数据晒出。\n")
    L.append("- 群里炸了；可主管只在群里回一句：“有问题下午来找我沟通处理。”——人家没在群里接火、更没对骂。\n")
    L.append("- 结局：公司认定其泄露经营数据、公然辱骂主管、煽动同事，属严重违纪，直接解除劳动合同。网友一边骂公司“扣钱太狠”，一边也承认：委屈是真的，但在几百人群里爆粗、晒工资，这表达方式把自己坑了。\n")
    L.append("- 初中生版启示：田某的“委屈”一点不假——被扣钱谁不憋屈？但他把“场合”当成了“倒情绪、秀真性情”的地方，一句狠话把诉求和脾气搅成一团，最后诉求没解决，还丢了脸、丢了工作。场合是讲观点的地方：“工资口径对一下”三句话能解决；秀脾气则把事办砸。\n")
    L.append("\n## 三、原理：两个道理（命名踩刹车 + 长镜头看开）\n")
    L.append("- **道理一 命名踩刹车（大脑跷跷板）**：美国 UCLA 脑扫描发现，看到生气/害怕的脸，脑子里“杏仁核”（情绪警报器）会狂响；可一旦说出“我现在很生气”，杏仁核的火就降下来，而“前额叶”（管理智的区域）亮起来。就像跷跷板：一命名，理智那头压下情绪那头。研究还说，名字越精准（如“我感到被否定”而非“我不好”），降温越狠。\n")
    L.append("- **道理二 长镜头看开（10-10-10）**：你此刻觉得“天塌了”的那点事，放到 10 个月后、10 年后看，多半连个小水洼都不算。“看不开”往往是因为你只盯着眼前的这一秒。\n")
    L.append("- 一句话：你不是你的情绪，你是那个“给情绪起名、再把它放到时间长河里看”的人。道理一→情绪命名法；道理二→10-10-10 透视法。\n")
    L.append("\n## 四、新招1：情绪命名法（给乱糟糟起个精准的名字）\n")
    L.append("适用：心里一团乱、说不清自己怎么了，结果一开口就变怼人、变闹情绪。三步走：\n")
    L.append("- **①命名**：别只说“我好烦”，要精准——是“委屈”？“被忽视”？“丢脸”？“害怕被否定”？名字越准，降温越狠。\n")
    L.append("- **②打分**：在心里给这股情绪打 0 到 10 分（情绪温度计），如“愤怒 8 分”。一量化，它就从“淹没你的洪流”变成“你能观察的对象”。\n")
    L.append("- **③说/写**：小声说出、写下来、或录段语音。光在脑子里想也行，但说出来/写下来，大脑刹车反应更强。写完这步通常已没那么想怼人，再只把观点说清。\n")
    L.append("- 要点：你不是你的情绪，你是“给情绪起名”的人。先别问“为什么”，命名本身就是救命的那一下。\n")
    L.append("\n**命名口诀**\n")
    L.append("> 心里乱糟糟，先给情绪起个名；委屈或丢脸，精准才管用。温度计打分，零到十分量一量；说出口写下来，理智回来再讲理。\n")
    L.append("\n## 五、新招2：10-10-10 透视法（拉远看开 / 长镜头）\n")
    L.append("适用：一点小事就炸、浮躁、只盯着眼前的委屈。一句话——上头时，把眼前这件“天塌了”的事，放到三个时间镜头里看，火就散了。\n")
    L.append("- **①10 分钟后，我还气吗？**——多半已经忘了，气个啥。\n")
    L.append("- **②10 个月后，这事还重要吗？**——大概率早翻篇了。\n")
    L.append("- **③10 年后，谁还记得？**——连影子都没了。\n")
    L.append("- 用法：火上来时心里默念这三问，像把镜头从“特写”拉到“全景”。配合情绪命名一起用更稳：先命名稳住，再拉远看开，最后只把观点报。绝大多数的“炸点”只值 10 分钟。\n")
    L.append("- 要点：透视不是叫你忍，是叫你“别被眼前这一秒带跑”。拉远看后照样可以冷静提诉求，既护住自己又不秀脾气。\n")
    L.append("\n**透视口诀**\n")
    L.append("> 火起别盯眼前，三问拉远看一看；十分后还气吗？十月后算个啥？十年后谁记得？小事一朵浪花。长镜头里看自己，浮躁散了心安定。\n")
    L.append("\n## 六、费曼自测题（旧+新结合）\n")
    L.append("用自己的话回答：*如果下次我又被一句话点着，或者像田某那样觉得委屈想爆粗、想在工作群里发作，我会怎么做，才能既把委屈/诉求说清、又不发火、还不丢人？*\n")
    L.append("标准答案要点：\n")
    L.append("1. 上头瞬间——第三人称抽离（退后→换角→劝友）+ 冲动冲浪（认浪→看浪→等浪退约10分钟），绝不发出去；同时静音模式（有火不泼别人）。\n")
    L.append("2. 心里乱时——情绪命名法（精准起名“委屈+被否定”→温度计打分→说/写下来），让理智上线、火降温。\n")
    L.append("3. 一点就炸时——10-10-10 透视法（10分/10月/10年后还重要吗？多数只值10分钟），拉远看、不秀脾气。\n")
    L.append("4. 快炸/念头歪时——五步刹车（停/数/命名/转/说）+ 认知重评（揪出“他针对我”→换善意解释）；手抖时配方箱呼吸；走神/不专注用五感着陆+番茄专注。始终记：场合不是秀脾气的地方，只是说观点的地方。\n")
    L.append("\n## 七、今日带走的四句口诀\n")
    L.append("1. 情绪命名法：心里乱糟糟，先给情绪起个名；委屈或丢脸，精准才管用。温度计打分，零到十分量一量；说出口写下来，理智回来再讲理。\n")
    L.append("2. 10-10-10 透视法：火起别盯眼前，三问拉远看一看；十分后还气吗？十月后算个啥？十年后谁记得？小事一朵浪花。长镜头里看自己，浮躁散了心安定。\n")
    L.append("3. 静音模式：心是一杯水，摇浑放自清；拍桌水会洒，残局难收平。\n")
    L.append("4. 一句话收尾：场合不是秀脾气的地方，只是说观点的地方；心里乱时先给情绪起个名、再把镜头拉远看，最后只把观点说清——慢慢练，心会越练越静。\n")
    return "\n".join(L)

# ---------------------------------------------------------------- 主流程
def main():
    audio = build_audio()
    sections_js = "window.SECTIONS = " + json.dumps(SECTIONS, ensure_ascii=False) + ";"
    audio_js = "window.AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";"
    html = HTML.replace("__LESSON_DATA__", sections_js).replace("__AUDIO_DATA__", audio_js)
    out_html = os.path.join(WS, "emotion-class-20260719.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html] 写出 {out_html} ({len(html)/1024:.0f} KB)")
    md = build_markdown()
    out_md = os.path.join(WS, "情绪管理-晓晓老师课堂笔记.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出 {out_md} ({len(md)/1024:.0f} KB)")
    # 带日期副本，供 ima 知识库入库（避免重名覆盖）
    dated = os.path.join(WS, "情绪管理-晓晓老师课堂笔记_20260719.md")
    with open(dated, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出带日期副本 {dated} ({len(md)/1024:.0f} KB)")
if __name__ == "__main__":
    main()
