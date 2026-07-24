# -*- coding: utf-8 -*-
"""
情绪管理课 builder（2026-07-24 · 第十一天）
- 单一内容源 -> 生成 晓晓老师(XiaoxiaoNeural) 每句语音(base64 内联)
- 输出「独立」单文件自包含 emotion-class-20260724.html (宋体/可调播放位置/上一句下一句/不挡字幕/费曼提问)
  ※ 每天一个新文件，绝不覆盖旧课页面（满足"每个网页对应一课不要更新网页"）
- 同时输出 情绪管理-晓晓老师课堂笔记.md 与 带日期副本 供存入 ima 知识库 imao
本日结构：复习前18招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪
  +情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本+课题分离+两分钟启动+预设护栏+自我慈悲)
  -> 新案例(2026 今日头条/腾讯新闻：小李谈涨薪被拒、气头上甩"不涨薪我就不干了"、被法院认定口头辞职有效丢掉工作)
  -> 原理(正念觉察+认知解离 ACT)
  -> 新招19 三分钟呼吸空间(觉察/集中呼吸/扩展) -> 新招20 认知解离法(加标签/看云/选动作) -> 费曼自测
"""
import os, json, base64, asyncio, sys, shutil

WS = "C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-8%"
PITCH = "+0Hz"

# ---------------------------------------------------------------- 案例插画（内联 SVG，保证离线可开）
# 十八招技能地图：3 行 × 6 列，用列表动态生成，避免手写 18 个框出错
SKILLS18 = [
    ("①五步刹车", "火起先停", "🔥", "#eaf1ff", "#5b8def"),
    ("②静音模式", "心如止水", "💧", "#eafaf2", "#2bb673"),
    ("③五感着陆", "看5摸4听3", "🌀", "#fff7e6", "#ffb84d"),
    ("④番茄专注", "25分只做一事", "🍅", "#f3ecff", "#7c5cff"),
    ("⑤认知重评", "停·揪·换想法", "🧠", "#fdeef4", "#ff8fab"),
    ("⑥方箱呼吸", "吸4憋7呼8", "🌬️", "#eaf6ff", "#3aa0e0"),
    ("⑦第三人称", "退后·换角·劝友", "👁", "#eef7f2", "#2bb673"),
    ("⑧冲动冲浪", "认浪·看浪·退", "🌊", "#f3ecff", "#7c5cff"),
    ("⑨情绪命名", "起名·打分·说写", "🏷️", "#fff7e6", "#ffb84d"),
    ("⑩10-10-10", "10分·10月·10年", "🔭", "#eaf1ff", "#5b8def"),
    ("⑪身体急停", "离开·冷温·握踩", "🧊", "#eaf6ff", "#3aa0e0"),
    ("⑫我信息", "事实·感受·需·请", "💬", "#fdeef4", "#ff8fab"),
    ("⑬六秒法则", "闭嘴·数六", "⏳", "#fff3e6", "#ff9a3c"),
    ("⑭记账本", "触发·念头·新招", "📒", "#e9f9ef", "#2bb673"),
    ("⑮课题分离", "别人的题不扛", "🚧", "#eaf1ff", "#5b8def"),
    ("⑯两分钟启动", "拆小步·只做2分", "🚀", "#fff7e6", "#ffb84d"),
    ("⑰预设护栏", "如果火起就退", "🛡️", "#f3ecff", "#7c5cff"),
    ("⑱自我慈悲", "对自己温柔", "💗", "#fdeef4", "#ff8fab"),
]

def build_map_svg():
    W = 720; cols = 6; rows = 3; mx = 8; gx = 8; gy = 10; y0 = 30; bh = 78
    bw = (W - 2*mx - (cols-1)*gx) / cols
    out = [f'<svg viewBox="0 0 {W} {y0+rows*bh+(rows-1)*gy+14}" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'  <text x="{W/2}" y="20" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">🗺️ 情绪技能地图 · 前18招复习</text>')
    for i,(name,sub,emo,fill,stroke) in enumerate(SKILLS18):
        r = i // cols; c = i % cols
        x = mx + c*(bw+gx); y = y0 + r*(bh+gy)
        out.append(f'  <rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out.append(f'  <text x="{x+bw/2:.1f}" y="{y+24}" fill="{stroke}" text-anchor="middle" font-weight="bold" font-size="11.5" font-family="sans-serif">{name}</text>')
        out.append(f'  <text x="{x+bw/2:.1f}" y="{y+45}" fill="#243447" text-anchor="middle" font-size="10" font-family="sans-serif">{sub}</text>')
        out.append(f'  <text x="{x+bw/2:.1f}" y="{y+66}" text-anchor="middle" font-size="15" font-family="sans-serif">{emo}</text>')
    out.append('</svg>')
    return "".join(out)

SVG_MAP = build_map_svg()

SVG_CASE = '''<svg viewBox="0 0 640 252" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="13.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">案例：小李谈涨薪被拒、气头上甩"不干了" → 没澄清 → 法院判口头辞职有效、丢工作无赔偿</text>
  <rect x="18" y="38" width="280" height="156" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="1.6"/>
  <circle cx="72" cy="82" r="23" fill="#ffd9b8"/>
  <path d="M57 76 l9 5 M87 76 l-9 5" stroke="#c0392b" stroke-width="3"/>
  <circle cx="65" cy="88" r="2.4" fill="#3a3a3a"/><circle cx="79" cy="88" r="2.4" fill="#3a3a3a"/>
  <path d="M62 98 q10 6 20 0" stroke="#c0392b" stroke-width="3" fill="none"/>
  <rect x="104" y="60" width="180" height="40" rx="10" fill="#fff" stroke="#ffb84d" stroke-width="1.6"/>
  <text x="194" y="78" font-size="12" fill="#c98a14" text-anchor="middle" font-family="sans-serif">"不涨薪我就不干了！"</text>
  <text x="158" y="116" font-size="11" fill="#c98a14" text-anchor="middle" font-family="sans-serif">😤 嘴比脑子快·气话出口</text>
  <text x="158" y="170" font-size="12" fill="#c0492a" text-anchor="middle" font-family="sans-serif">导火索：领导一句"今年不调"</text>
  <text x="158" y="190" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">他以为只是说说，没澄清收回</text>
  <text x="320" y="120" font-size="26" fill="#c0492a" text-anchor="middle">VS</text>
  <rect x="342" y="38" width="280" height="156" rx="14" fill="#fdf3f1" stroke="#ff8a8a" stroke-width="1.6"/>
  <rect x="372" y="58" width="60" height="44" rx="6" fill="#fff" stroke="#d9d9d9" stroke-width="1.4"/>
  <text x="402" y="84" font-size="9" fill="#888" text-anchor="middle" font-family="sans-serif">确认单</text>
  <text x="470" y="76" font-size="20" text-anchor="middle">🔨</text>
  <text x="470" y="98" font-size="10" fill="#c0492a" text-anchor="middle" font-family="sans-serif">法院:辞职有效</text>
  <text x="482" y="150" font-size="11.5" fill="#c0492a" text-anchor="middle" font-family="sans-serif">💥 工作丢了·一分没赔</text>
  <text x="482" y="178" font-size="12" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">✅ 本可:三分钟呼吸静心+</text>
  <text x="482" y="196" font-size="12" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">认知解离把"不干了"当广播</text>
  <text x="320" y="216" font-size="11.5" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">职场不是发泄情绪的地方：话一出口责任就来，气话被当真就成了辞职报告</text>
</svg>'''

SVG_PRINCIPLE = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="20" font-size="15" fill="#5b8def" text-anchor="middle" font-family="sans-serif">两个道理：正念觉察(不评判看当下,呼吸作锚) · 认知解离(念头≠事实,只观察不认同)</text>
  <g font-family="sans-serif">
   <rect x="20" y="38" width="290" height="196" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="165" y="64" font-size="13" fill="#2b6fb0" text-anchor="middle" font-weight="bold">道理一 · 正念觉察(卡巴金)</text>
   <circle cx="110" cy="110" r="22" fill="#cfe3ff"/>
   <text x="110" y="117" text-anchor="middle" font-size="20">🧘</text>
   <text x="220" y="100" font-size="11" fill="#243447" text-anchor="middle">"对当下不加评判的觉察"</text>
   <text x="220" y="120" font-size="11" fill="#243447" text-anchor="middle">像看湖面起风，风会自停</text>
   <text x="165" y="158" font-size="11" fill="#243447" text-anchor="middle">呼吸是"锚"：把飘走的心拉回当下</text>
   <text x="165" y="180" font-size="11" fill="#1c7a4d" text-anchor="middle">练几分钟，管平静的脑区会变厚</text>
   <text x="165" y="208" font-size="10.5" fill="#6b7c8f" text-anchor="middle">硬压像按皮球，松手更弹；正念温柔接住</text>
   <rect x="340" y="38" width="290" height="196" rx="14" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="485" y="64" font-size="13" fill="#d6455f" text-anchor="middle" font-weight="bold">道理二 · 认知解离(ACT)</text>
   <text x="400" y="104" font-size="20" text-anchor="middle">💭</text>
   <text x="400" y="128" font-size="10.5" fill="#c0492a" text-anchor="middle">念头"我不行"冒出</text>
   <text x="400" y="146" font-size="10.5" fill="#c0492a" text-anchor="middle">你当真→被牵着跑</text>
   <path d="M424 116 h30" stroke="#d99" stroke-width="2"/>
   <text x="570" y="104" font-size="20" text-anchor="middle">☁️</text>
   <text x="570" y="128" font-size="10.5" fill="#1c7a4d" text-anchor="middle">加前缀"我注意到想…"</text>
   <text x="570" y="146" font-size="10.5" fill="#1c7a4d" text-anchor="middle">当云看→不追不赶</text>
   <text x="485" y="184" font-size="11" fill="#243447" text-anchor="middle">你不是你的念头；念头≠事实≠命令</text>
   <text x="485" y="210" font-size="10.5" fill="#6b7c8f" text-anchor="middle">解离时,管"把念头当真"的脑区安静了</text>
  </g>
</svg>'''

SVG_BREATH = '''<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#1c7a4d" text-anchor="middle" font-family="sans-serif">三分钟呼吸空间（正念 MBSR）：心浮火冒时，觉察→集中呼吸→扩展觉知，风过湖面心自静</text>
  <g font-family="sans-serif">
   <rect x="14" y="44" width="190" height="140" rx="14" fill="#eafaf2" stroke="#2bb673" stroke-width="2"/>
   <text x="109" y="74" font-size="14" fill="#1c7a4d" text-anchor="middle" font-weight="bold">① 觉察(约1分)</text>
   <text x="109" y="100" font-size="11" fill="#243447" text-anchor="middle">问自己"我现在怎么了"</text>
   <text x="109" y="120" font-size="11" fill="#243447" text-anchor="middle">浮躁?生气?走神?</text>
   <text x="109" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">给情绪起名"我在浮躁"</text>
   <text x="109" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">不评判,看见就好</text>
   <path d="M204 114 l16 0 M220 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="222" y="44" width="190" height="140" rx="14" fill="#eaf6ff" stroke="#3aa0e0" stroke-width="2"/>
   <text x="317" y="74" font-size="14" fill="#1c7a9c" text-anchor="middle" font-weight="bold">② 集中呼吸(约1分)</text>
   <text x="317" y="100" font-size="11" fill="#243447" text-anchor="middle">注意放呼吸上</text>
   <text x="317" y="120" font-size="11" fill="#243447" text-anchor="middle">吸数一呼数一,跑偏拉回</text>
   <text x="317" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">呼吸是"锚"拴回当下</text>
   <text x="317" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">只跟呼吸走</text>
   <path d="M412 114 l16 0 M428 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="430" y="44" width="190" height="140" rx="14" fill="#f3ecff" stroke="#7c5cff" stroke-width="2"/>
   <text x="525" y="74" font-size="14" fill="#5b3fd6" text-anchor="middle" font-weight="bold">③ 扩展(回到事)</text>
   <text x="525" y="100" font-size="11" fill="#243447" text-anchor="middle">带静一点的觉知</text>
   <text x="525" y="120" font-size="11" fill="#243447" text-anchor="middle">睁眼回手头的事</text>
   <text x="525" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">心像湖面风过自平</text>
   <text x="525" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">只三分钟</text>
   <text x="320" y="216" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">一觉浮躁二回呼吸，三带觉知做手里事；心像湖面风过自静，正念三分钟就平息</text>
  </g>
</svg>'''

SVG_DEFUSE = '''<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg">
  <text x="320" y="22" font-size="15" fill="#c98a14" text-anchor="middle" font-family="sans-serif">认知解离法（念头≠事实）：给念头加前缀、当云看不追不赶、照样干活，不被念头牵着走</text>
  <g font-family="sans-serif">
   <rect x="14" y="44" width="190" height="140" rx="14" fill="#fff7e6" stroke="#ffb84d" stroke-width="2"/>
   <text x="109" y="74" font-size="14" fill="#c98a14" text-anchor="middle" font-weight="bold">① 加标签</text>
   <text x="109" y="100" font-size="11" fill="#243447" text-anchor="middle">念头"我不行"冒出</text>
   <text x="109" y="120" font-size="11" fill="#243447" text-anchor="middle">前面加"我注意到我</text>
   <text x="109" y="140" font-size="11" fill="#243447" text-anchor="middle">正在想…"</text>
   <text x="109" y="164" font-size="10.5" fill="#6b7c8f" text-anchor="middle">你≠念头,只是广播</text>
   <path d="M204 114 l16 0 M220 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="222" y="44" width="190" height="140" rx="14" fill="#eaf1ff" stroke="#5b8def" stroke-width="2"/>
   <text x="317" y="74" font-size="14" fill="#2b6fb0" text-anchor="middle" font-weight="bold">② 看云</text>
   <text x="317" y="100" font-size="11" fill="#243447" text-anchor="middle">念头当天上的云</text>
   <text x="317" y="120" font-size="11" fill="#243447" text-anchor="middle">看见,不追不赶</text>
   <text x="317" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">不和它吵架</text>
   <text x="317" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">它飘走,你站地上看</text>
   <path d="M412 114 l16 0 M428 106 l8 8 -8 8" stroke="#9aa7bd" stroke-width="3" fill="none"/>
   <rect x="430" y="44" width="190" height="140" rx="14" fill="#fdeef4" stroke="#ff8fab" stroke-width="2"/>
   <text x="525" y="74" font-size="14" fill="#d6455f" text-anchor="middle" font-weight="bold">③ 选动作</text>
   <text x="525" y="100" font-size="11" fill="#243447" text-anchor="middle">念头只是广播</text>
   <text x="525" y="120" font-size="11" fill="#243447" text-anchor="middle">问"带它我下一步干啥"</text>
   <text x="525" y="144" font-size="10.5" fill="#6b7c8f" text-anchor="middle">照样写报告回消息</text>
   <text x="525" y="166" font-size="10.5" fill="#6b7c8f" text-anchor="middle">你听广播还能走路</text>
   <text x="320" y="216" font-size="12" fill="#6b7c8f" text-anchor="middle" font-family="sans-serif">念头不是我，加个前缀看云飘；它说它说由它说，我干我的不逃跑</text>
  </g>
</svg>'''

# ---------------------------------------------------------------- 课程内容（第十一天）
SECTIONS = [
  {"type":"speak","title":"开场 · 第十一天，先串起前18招","rhyme":None,"img":None,"sentences":[
    "同学你好，我是晓晓老师！咱们的情绪管理课到第十一天啦。前面十天你攒了十八招本领：第一天五步刹车加静音模式，第二天五感着陆加番茄专注，第三天认知重评加方箱呼吸，第四天第三人称抽离加冲动冲浪，第五天情绪命名法加10-10-10透视法，第六天身体急停法加我信息表达法，第七天六秒法则加情绪记账本，第八天课题分离法加两分钟启动法，第九天预设护栏法加自我慈悲法。今天先把这十八招串成一张情绪技能地图，再教你两招新本领，专治你最头疼的——心不够静、浮躁不安，还有脑子里念头乱跑、老觉得自己不行、被念头牵着走。",
    "先复习老口号：任何场合——办公室、工作群、会议室——都不是展示真性情的地方，它只是表达观点的地方。你是去把事说清楚的，不是去把脾气和念头秀出来的。",
    "今天要补的两块：第一块，你心不够静、浮躁不安，坐下来心就飘、像有只猴子在脑子里蹦，越想静越乱。第二块，你不会管念头——委屈、生气时，脑子里冒出我不行了、我不干了、我真没用这些念头，你把它们当真，越想越炸、越想越丧，甚至真说出狠话、做出后悔的事。今天两招，一招让你心静下来，一招让你和念头拉开距离。"
  ]},

  {"type":"speak","title":"复习 · 十八招技能地图","rhyme":None,"img":SVG_MAP,"sentences":[
    "先复习十八招，编成一张地图。第一招五步刹车——一停二数三命名，四转五说；火气冒头先喊停。第二招静音模式——心是一杯水，有火不泼别人。第三招五感着陆——看五摸四听三声，走神用它。第四招番茄专注——二十五分只做一事，手机扔远练定力。",
    "第五招认知重评——停、揪念头、换想法。第六招方箱呼吸——吸四憋七呼八憋四，画方箱降温。第七招第三人称抽离——退后换角劝友。第八招冲动冲浪——认浪看浪等浪退。第九招情绪命名法——起名打分说写，你不是情绪你是起名的人。",
    "第十招10-10-10透视——10分10月10年后拉远看。第十一招身体急停——离开冷水握拳脚踩地，身体是开关。第十二招我信息——事实感受需要请求，只说观点。第十三招六秒法则——火冒三丈先闭嘴数六。第十四招记账本——睡前三栏触发念头新招。",
    "第十五招课题分离——别人的题不扛。第十六招两分钟启动——大活先拆只做两分，手指一动心就静。第十七招预设护栏——如果火起就退后，现场自动执行。第十八招自我慈悲——对自己温柔，不自我攻击。今天两招，专管心不够静浮躁和被念头带跑自我攻击。"
  ]},

  {"type":"quiz","title":"复习小测 · 浮躁/一点就炸/自我攻击用哪招","quiz":{
    "q":"你一坐到工位心就飘、老想摸手机，偏偏领导皱眉说方案不行，你火一下上来，同时脑子里冒出我真没用。前18招里，管浮躁坐不住、管一点就炸、管自我攻击（骂自己）分别该先动哪招？",
    "opts":[
      {"t":"浮躁坐不住→五感着陆(拉回当下)+番茄专注(开25分手机扔远)+两分钟启动(先拆小步)；一点就炸→五步刹车(停数)或六秒法则(数六)；自我攻击→自我慈悲(手放胸口说慢慢来)。今天再加心静用呼吸空间、念头带跑用认知解离","ok":True},
      {"t":"浮躁坐不住→冲动冲浪(那是管已起大浪想发作，不是走神)","ok":False},
      {"t":"自我攻击→继续骂自己骂醒(自责只会皮质醇↑更炸)","ok":False}
    ],
    "stu":"小浩抢答：老师，心静不下来是不是硬压住不想就静了？",
    "teacher":"晓晓老师笑：越硬压越反弹，像把皮球按水里，松手更弹。心浮躁时，别和它较劲——用第十九招三分钟呼吸空间，把注意力轻轻放到呼吸上，风过湖面自然静。再配两分钟启动，手指一动就踏实了。",
    "card":["浮躁坐不住=五感着陆+番茄专注+两分钟启动；一点就炸=五步刹车或六秒法则；自我攻击=自我慈悲。","心静不下来别硬压(越压越弹)，用呼吸空间把注意放呼吸，风过湖面自静。"]
  }},

  {"type":"speak","title":"第一幕 · 新案例：一句气话，丢了工作","rhyme":None,"img":SVG_CASE,"sentences":[
    "讲个 2026 年刚刷屏的真实事（来源今日头条、腾讯新闻：小李谈涨薪）。小李是个普通打工人，平时干活勤快，就是有个毛病——脾气一点就着，心也常浮。那天他和领导谈涨薪，领导说今年预算紧，先不调。小李一听，脑子里的火噌地上来，嘴比脑子快，当众甩出一句：不涨薪我就不干了！",
    "领导没吵，只平静地说：这是你说的，公司按制度来。当场让他把这句话写进确认单。小李当时还在气头上，没澄清、没收回，甚至回头跟同事抱怨本来就不想干了。他以为只是句气话，谁上班没说过？",
    "结果惊掉下巴：公司把他的口头辞职坐实，走合法流程和他解除了劳动合同。小李慌了，跑去仲裁、又打官司，说自己只是发泄情绪、不是真想辞职。可法院判了：口头表达有法律效力，他亲口说的、又没当场否认，辞职有效！一审二审都输，工作丢了，一分赔偿没拿到。",
    "全网炸锅，无数人替他冤：谁没说过气话，难道都当真？可冷静看——职场不是菜市场，不是发泄情绪的地方。小李的亏，亏在情绪上头时把气话当成了可以随便说的念头，没管住嘴，也没及时澄清。那句不干了，只是他气头上一个念头，不是事实、不是他真想做的。",
    "换成咱们的视角：小李和你是一样的——心不够静、浮躁、一上头念头乱飞，还把念头当真。如果他当时会两招就好了：先让心静下来（三分钟呼吸空间），再把我不干了看成我有个想不干的念头（认知解离），就不会说出那句毁工作的气话。下面两招，一招让心静，一招让念头和你拉开距离。"
  ]},

  {"type":"quiz","title":"课间提问① · 小李最亏在哪","quiz":{
    "q":"小李最亏在哪？一句气话，怎么就真成了丢工作的辞职报告？",
    "opts":[
      {"t":"他情绪上头把气话当随便说的念头，没当场澄清收回，法律上口头表达算数→被认定主动辞职。教训：职场不是发泄情绪的地方，话一出口责任就跟来；上头时先静心、别把念头当真话甩出去","ok":True},
      {"t":"他天生嘴贱、性格差","ok":False},
      {"t":"全怪领导心狠","ok":False}
    ],
    "stu":"小雪：可领导也太不近人情了吧！",
    "teacher":"晓晓老师点头：公司依规办事、不违法，这另说。但咱们能管的只有自己。小李的坑是情绪化表达加事后不作为——气话出口不澄清，就成证据。这正好引出今天两招：先让心静（呼吸空间），再把念头和真话分开（认知解离）。场合是表达观点的地方，不是秀脾气、更不是把气话当真扔出去的地方。",
    "card":["小李亏在：情绪上头把气话当随便说的念头，没澄清→法律认口头表达→算主动辞职。","职场不是发泄情绪的地方；话一出口责任就来；上头时先静心、别把念头当真话甩出。"]
  }},

  {"type":"speak","title":"第二幕 · 原理：正念 + 认知解离","rhyme":None,"img":SVG_PRINCIPLE,"sentences":[
    "为什么让心静和和念头拉开距离这么管用？先讲两个科学道理。道理一：正念。心理学家卡巴金说，正念就是对当下不加评判的觉察。你浮躁、心不静时，越想快静下来越乱；正念教你不评判地看着它——像看湖面起风，风会自己停。研究证明，每天几分钟正念练习，大脑负责平静的区域会变厚。这引出第十九招：三分钟呼吸空间。",
    "道理二：认知解离（接纳承诺疗法 ACT 的核心）。你的大脑会自动蹦出很多念头——我不行、我不干了、我太差了。但这些念头只是念头，不是事实，更不是命令。你不是你的念头。神经科学发现，当你和念头解离（只观察不认同），大脑里管把念头当真的区域就安静了，你不再被它牵着跑。",
    "一句话：心不静，靠把注意轻轻放到呼吸上（正念呼吸空间）；被念头带跑，靠把念头看成天上的云、不追不赶（认知解离）。道理一→三分钟呼吸空间；道理二→认知解离法。这两招，正好把你最愁的两件事接住。"
  ]},

  {"type":"quiz","title":"课间提问② · 为什么呼吸空间比硬压管用","quiz":{
    "q":"为什么三分钟呼吸空间（把注意放呼吸）比硬命令自己别浮躁、快静下来管用？",
    "opts":[
      {"t":"硬压像把皮球按水里，松手更弹；正念是不评判地觉察，呼吸是锚把飘走的心拉回当下，像风过湖面自然静。这是大脑可训练的机制，练几次就灵","ok":True},
      {"t":"因为呼吸能多吸氧气","ok":False},
      {"t":"因为硬压太累","ok":False}
    ],
    "stu":"小杰：那我烦的时候只想刷手机，哪静得下来？",
    "teacher":"晓晓老师笑：所以才要短——只三分钟，比刷手机省事。你越烦越刷，心越飘；反过来，把手机扔远，闭眼数三次呼吸，心就落回身体里了。呼吸空间不是让你变神仙，是给浮躁一个歇脚处。练上几天，一浮躁你身体会自动想呼吸，比硬压温柔多了。",
    "card":["正念不评判地觉察，呼吸是锚把飘走的心拉回当下；硬压像按皮球，松手更弹。","只三分钟：越烦越刷心越飘，闭眼数呼吸，心落回身体；练几天身体会自动想呼吸。"]
  }},

  {"type":"speak","title":"第三幕 · 新招19：三分钟呼吸空间（正念 MBSR）","rhyme":{
    "title":"🎵 呼吸空间口诀",
    "lines":["<b>一觉浮躁二回呼吸</b>，<b>三带觉知做手里事</b>；","<b>心像湖面风过自静</b>，<b>正念三分钟就平息</b>。"]
  },"img":SVG_BREATH,"sentences":[
    "新本领第十九招：三分钟呼吸空间（正念 MBSR）。一句话——心浮躁、坐不住、火往上冒时，用三分钟，把飘走的注意轻轻拉回呼吸，心就静了。三步：",
    "第一步觉察：先问自己我现在怎么了？是浮躁？是生气？是走神？把注意力转向内在，给情绪起个名——我在浮躁。别评判它好坏，看见就好。这步约一分钟。",
    "第二步集中：把全部注意放到呼吸上。吸气，数一；呼气，数一；吸气，数二……只跟呼吸走，脑子跑偏了就轻轻拉回来。呼吸是锚，把乱飘的心拴回当下。这步约一分多钟。",
    "第三步扩展：带着这份看见了、静了一点的觉知，慢慢睁开眼，回到手头的事——写字、回消息、听会。心像湖面，风过了自然平。整个过程就三分钟，比发呆刷手机值。",
    "记住：不是硬压浮躁，是温柔地看见它、用呼吸把它接住。这招和静音模式是搭档——水杯爱晃，就用呼吸把水稳一稳。场合里心一浮，先三步呼吸，再说观点。",
    "记口诀：一觉浮躁二回呼吸，三带觉知做手里事；心像湖面风过自静，正念三分钟就平息。"
  ]},

  {"type":"quiz","title":"课间提问③ · 呼吸空间怎么用","quiz":{
    "q":"晨会被当众说这方案不行，你脸一热、心浮、手伸向手机。按三分钟呼吸空间，你该怎么做？",
    "opts":[
      {"t":"先觉察我在浮躁、在被说难受→把手机扔远、闭眼把注意放呼吸(吸数呼数,跑偏就拉回)约一分多钟→带着静一点的觉知睁开眼,用我信息只说观点问清标准。先静心再说,不甩气话","ok":True},
      {"t":"立刻回怼你行你上","ok":False},
      {"t":"马上刷手机压惊(越刷心越飘)","ok":False}
    ],
    "stu":"小琳：开会没地方闭眼啊，同事看见多尬。",
    "teacher":"晓晓老师笑：不一定要闭眼——盯着手里笔、感受笔的凉，或者看窗外一片叶子，把注意放一个具体的东西加呼吸上，一样是锚。哪怕只三十秒的深呼吸，也能把火降半截。关键是先觉知、再回呼吸、后开口，不是非得盘腿打坐。",
    "card":["三分钟呼吸空间：①觉察(我在浮躁)②集中(注意放呼吸,跑偏拉回)③扩展(带觉知回做事)。","不一定要闭眼：盯笔/看叶+呼吸一样是锚；先觉知再呼吸后开口，不甩气话。"]
  }},

  {"type":"speak","title":"第四幕 · 新招20：认知解离法（念头不是事实）","rhyme":{
    "title":"🎵 认知解离口诀",
    "lines":["<b>念头不是我</b>，<b>加个前缀看云飘</b>；","<b>它说它说由它说</b>，<b>我干我的不逃跑</b>。"]
  },"img":SVG_DEFUSE,"sentences":[
    "新本领第二十招：认知解离法（念头不是事实）。一句话——脑子里冒出我不行、我不干了、我真没用时，别把它当真、别被它牵着走，给念头加个前缀，把它看成天上的云。三步：",
    "第一步加标签：当那个念头冒出来，在前面轻轻加一句——我注意到，我正在想：我不行了，或者有个念头飘过来说：我不干了。就这么加个前缀，你和念头之间就多了一道缝，它不再是你，只是你脑子里的广播。",
    "第二步看云：把念头当成天上飘的云、路上过的车——你看见它，但不追它、不赶它、不和它吵架。它爱飘就飘，你站在地上看。念头会自己变淡、飘走，你不用使劲甩。",
    "第三步选动作：念头只是念头，不是命令。问自己一句：带着这个念头，我下一步做什么有用的事？然后该写报告写报告、该回消息回消息——念头在旁边嘟囔，你照样干活。你不是被念头绑架的人，你是听得到广播、还能自己走路的人。",
    "记住：你不是你的念头。小李那句不干了要是加了前缀变成我注意到我正在想：不干了，他就知道那只是气头上的广播，不会当真甩出去。这招和认知重评是搭档——重评是换掉念头，解离是先退后看清楚念头不是你。",
    "记口诀：念头不是我，加个前缀看云飘；它说它说由它说，我干我的不逃跑。"
  ]},

  {"type":"quiz","title":"课间提问④ · 认知解离怎么用","quiz":{
    "q":"周报写岔被点名，你脑子里蹦出我真没用，完了。按认知解离法，你该怎么做才不被它带跑？",
    "opts":[
      {"t":"先加标签我注意到我正在想：我真没用→把念头当云看,不追不赶→问带着这念头我下一步干啥有用,照样改周报。念头是广播不是命令,不甩狠话不内耗","ok":True},
      {"t":"相信它我真没用,当场崩溃","ok":False},
      {"t":"骂自己别想了,硬塞回去(越塞越弹)","ok":False}
    ],
    "stu":"小强：可那念头太真了，我不信它是假的。",
    "teacher":"晓晓老师点头：你不用相信它是假的，也不用消灭它。解离不是念头是错的，是念头≠我、≠事实、≠必须照做。你只做一件事：加前缀、看它飘、照样干活。练几次你会发现，念头还在嘟囔，但你已经改完周报了——它没指挥了你。这正合场合是表达观点的地方：你说的是观点，不是念头的吼叫。",
    "card":["认知解离：①加标签(我注意到我正在想…)②看云(不追不赶)③选动作(带念头照样干活)。","解离不是消灭念头,是念头≠我≠事实≠命令；加前缀看它飘,照样干事。"]
  }},

  {"type":"speak","title":"结尾 · 今天你带走什么（前18招+两新招）","rhyme":None,"img":None,"sentences":[
    "今天的课到这儿，晓晓老师带你总复习。",
    "前18招（复习）：五步刹车——一停二数三命名四转五说；静音模式——心是一杯水；五感着陆——看五摸四听三声；番茄专注——二十五分只做一事；认知重评——停揪换、换想法就换情绪；方箱呼吸——吸4憋7呼8憋4；第三人称抽离——退后换角劝友；冲动冲浪——认浪看浪等浪退；情绪命名法——精准起名温度计打分说写下来；10-10-10透视法——10分10月10年后拉远看；身体急停法——离开冷水握拳脚踩地；我信息表达法——事实感受需要请求只说观点；六秒法则——火冒三丈先闭嘴数六等理智脑；记账本——睡前三栏触发念头新招；课题分离法——别人课题我不扛；两分钟启动法——大活先拆只做两分；预设护栏法——如果火起就退；自我慈悲法——对自己好。",
    "新本领①：三分钟呼吸空间——心浮火冒时，觉察→集中呼吸→扩展觉知，风过湖面心自静，专治心不够静浮躁不安。新本领②：认知解离法——念头冒出加前缀我注意到我正在想，当云看、不追不赶，照样干活，专治被念头带跑、自我攻击。",
    "一句话收尾：场合不是秀脾气、更不是把气话当真扔出去的地方，只是说观点的地方；心浮时先三分钟呼吸静一静，念头乱时加前缀看它飘，你会越来越稳。下课！"
  ]},

  {"type":"feynman","title":"费曼小测 · 讲给晓晓老师听","text":
    "费曼学习法说：你以为你懂了，不算懂；能用自己的话讲明白，才是真懂。\n\n现在轮到你啦——请用你自己的话，把下面这道题讲给晓晓老师听：\n\n如果下次我又被一句难听话点着、心浮坐不住、脑子里还冒出我不行了、我不干了的念头，我会怎么做，才能既不当场炸、又能管住浮躁、又不被念头带跑、把该干的活干好？\n\n提示：可以结合旧本领（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本、课题分离法、两分钟启动法、预设护栏法、自我慈悲法）和新本领（三分钟呼吸空间、认知解离法）一起说。\n\n在下面的框里写几句（或对着麦克风讲出来也行）。写完了，翻回上面的口诀卡对照一下，看看漏了哪一步。"
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
<title>晓晓老师的情绪管理课 · 第11天：让心静下来、和念头拉开距离——场合不是秀脾气，只是说观点</title>
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
  <h1>晓晓老师的情绪管理课 · 第11天</h1>
  <p>三分钟呼吸空间让心静、认知解离让念头不牵你走：场合不是秀脾气的地方，只是说观点的地方 🧘</p>
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
    '<textarea id="fm" placeholder="在这里用你自己的话写一写（比如：他一句难听话是触发，我先三分钟呼吸让心静，再给我不行了加前缀看成广播，照样改周报…）…"></textarea>'+
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
    '一觉浮躁二回呼吸，三带觉知做手里事；心像湖面风过自静，正念三分钟就平息。<br><br>'+
    '念头不是我，加个前缀看云飘；它说它说由它说，我干我的不逃跑。<br><br>'+
    '<b>前18招回顾：</b>见本页上方「复习 · 十八招技能地图」卡片（五步刹车/静音/五感着陆/番茄/认知重评/方箱呼吸/第三人称抽离/冲动冲浪/情绪命名/10-10-10/身体急停/我信息/六秒法则/记账本/课题分离/两分钟启动/预设护栏/自我慈悲）。'+
    '</div><p style="color:var(--soft)">记住：场合不是秀脾气、更不是把气话当真扔出去的地方，只是说观点的地方；心浮时先三分钟呼吸静一静，念头乱时加前缀看它飘，你会越来越稳。</p>'+
    '<div class="controls" style="justify-content:center"><button class="btn" onclick="location.reload()">🔁 再上一遍</button></div></div>';
  setSub('—— 今天的课结束啦，记得常回来练 ——');
}

(function(){
  const intro=document.createElement('div'); intro.className='card';
  intro.innerHTML='<h2>👋 准备好了吗？（第11天）</h2>'+
    '<div class="scene-text">这堂课大概 10 分钟。先带你复习前18招（五步刹车、静音模式、五感着陆、番茄专注、认知重评、方箱呼吸、第三人称抽离、冲动冲浪、情绪命名法、10-10-10 透视法、身体急停法、我信息表达法、六秒法则、情绪记账本、课题分离法、两分钟启动法、预设护栏法、自我慈悲法），再讲一个新案例（2026 真实热点：小李谈涨薪被拒、气头上甩"不干了"，被法院认定口头辞职有效、丢掉工作无赔偿）和两招新本领（三分钟呼吸空间、认知解离法）。\n\n'+
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
    L.append("# 情绪管理课 · 晓晓老师课堂笔记（第11天 · ima 知识库 imao）\n")
    L.append("> 主题：克服专注力差、浮躁易怒、情绪化。核心理念：**场合不是展示真性情的地方，只是表达观点的地方。**\n")
    L.append("> 配套互动网页：`emotion-class-20260724.html`（晓晓老师 XiaoxiaoNeural 神经网络语音 + 不挡字幕 + 上一句/下一句可调位置 + 费曼式定时提问）。\n")
    L.append("> 第11天结构：**复习**前18招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸+第三人称抽离+冲动冲浪+情绪命名+10-10-10+身体急停+我信息+六秒法则+记账本+课题分离+两分钟启动+预设护栏+自我慈悲) → **新案例**(2026 今日头条/腾讯新闻：小李谈涨薪被拒、气头上甩“不干了”、被法院认定口头辞职有效丢掉工作) → **原理**(正念觉察+认知解离 ACT) → **新招19**三分钟呼吸空间(觉察/集中呼吸/扩展) → **新招20**认知解离法(加标签/看云/选动作) → 费曼自测。\n")  # noqa
    L.append("\n## 一、复习：前18招（情绪技能地图）\n")
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
    L.append("- **⑰预设护栏法（执行意图 if-then）**：如果火起就退后、坐定就开番茄钟；提前写进脑子、现场自动执行不靠意志。\n")
    L.append("- **⑱自我慈悲法（对自己温柔）**：出错浮躁别骂自己，觉察、共通人性、手放胸口善待自己；自责→皮质醇↑更炸，慈悲→安抚系统。\n")
    L.append("- 这十八招管“快炸/走神/不专注/念头歪/手抖想怼/上头那一秒/心里乱/一点就炸/身体先炸/想回嘴/情绪过去就忘/替别人内耗/大活不动手/跟自己过不去”。今天两招管最前面的“心不够静浮躁”和“被念头带跑自我攻击”。\n")
    L.append("\n## 二、今日新案例（2026 真实热点，来源今日头条/腾讯新闻，人物化名）\n")
    L.append("素材：小李是个普通打工人，平时干活勤快，但脾气一点就着、心常浮。那天他和领导谈涨薪，领导说“今年预算紧、先不调”。小李脑子里的火“噌”地上来，嘴比脑子快，当众甩出一句：“不涨薪我就不干了！”领导没吵，只平静地说“这是你说的，公司按制度来”，当场让他把这句话写进确认单。小李还在气头上，没澄清、没收回，甚至回头跟同事抱怨“本来就不想干了”。\n")
    L.append("结果惊掉下巴：公司把他的“口头辞职”坐实，走合法流程解除劳动合同。小李跑去仲裁、打官司，说自己只是发泄情绪、不是真想辞职。可法院判了：口头表达有法律效力，他亲口说的、又没当场否认，辞职有效！一审二审都输，工作丢了，一分赔偿没拿到。全网炸锅，无数人替他冤：“谁没说过气话，难道都当真？”\n")
    L.append("- 关键解读：职场不是菜市场，不是发泄情绪的地方。小李的亏，亏在情绪上头时把“气话”当成了可以随便说的念头，没管住嘴、也没及时澄清。那句“不干了”，只是他气头上一个念头，不是事实、不是他真想做的。话一出口，责任就跟着来。\n")
    L.append("- 初中生版启示：小李和你是一样的——心不够静、浮躁、一上头念头乱飞，还把念头当真。如果他当时会两招：先让心静下来（三分钟呼吸空间），再把“我不干了”看成“我有个想不干的念头”（认知解离），就不会说出那句毁工作的气话。这正好对应你：心不够静、浮躁、被念头带跑。\n")
    L.append("\n## 三、原理：两个道理（正念觉察 + 认知解离 ACT）\n")
    L.append("- **道理一 正念觉察（卡巴金）**：正念就是“对当下不加评判的觉察”。你浮躁、心不静时，越想“快静下来”越乱；正念教你不评判地看着它——像看湖面起风，风会自己停。研究证明，每天几分钟正念练习，大脑负责平静的区域会变厚。硬压浮躁像把皮球按水里，松手更弹；正念是温柔地接住。这引出第十九招：三分钟呼吸空间。\n")
    L.append("- **道理二 认知解离（接纳承诺疗法 ACT 的核心）**：大脑会自动蹦出很多念头——“我不行”“我不干了”“我太差了”。但这些念头只是念头，不是事实，更不是命令。你不是你的念头。神经科学发现，当你和念头“解离”（只观察不认同），大脑里管“把念头当真”的区域就安静了，你不再被它牵着跑。这引出第二十招：认知解离法。\n")
    L.append("- 一句话：心不静，靠“把注意轻轻放到呼吸上”（正念呼吸空间）；被念头带跑，靠“把念头看成天上的云、不追不赶”（认知解离）。道理一→三分钟呼吸空间；道理二→认知解离法。\n")
    L.append("\n## 四、新招19：三分钟呼吸空间（正念 MBSR，让心静下来）\n")
    L.append("适用：心不够静、浮躁不安、坐不住、火往上冒、脑子像有猴子蹦。一句话——用三分钟，把飘走的注意轻轻拉回呼吸，心就静了。三步：\n")
    L.append("- **①觉察（约1分）**：先问自己“我现在怎么了？”浮躁？生气？走神？把注意力转向内在，给情绪起个名——“我在浮躁”。别评判好坏，看见就好。\n")
    L.append("- **②集中呼吸（约1分多）**：把全部注意放到呼吸上。吸气数一、呼气数一、吸气数二……只跟呼吸走，跑偏了就轻轻拉回来。呼吸是“锚”，把乱飘的心拴回当下。\n")
    L.append("- **③扩展（回到事）**：带着“看见了、静了一点”的觉知，慢慢睁眼，回到手头的事——写字、回消息、听会。心像湖面，风过了自然平。整个过程只三分钟，比发呆刷手机值。\n")
    L.append("- 要点：不是硬压浮躁，是温柔地看见它、用呼吸接住。和静音模式是搭档——水杯爱晃，就用呼吸把水稳一稳。场合里心一浮，先三步呼吸，再说观点。不一定要闭眼：盯笔/看叶+呼吸一样是锚；哪怕三十秒深呼吸也能降半截火。\n")
    L.append("\n**三分钟呼吸空间口诀**\n")
    L.append("> 一觉浮躁二回呼吸，三带觉知做手里事；心像湖面风过自静，正念三分钟就平息。\n")
    L.append("\n## 五、新招20：认知解离法（念头不是事实，不被念头带跑）\n")
    L.append("适用：委屈生气时脑子里冒出“我不行”“我不干了”“我真没用”，你把它们当真、越想越炸越丧、甚至说出狠话。一句话——给念头加前缀，把它看成天上的云，不追不赶、照样干活。三步：\n")
    L.append("- **①加标签**：当念头冒出，前面轻轻加一句——“我注意到，我正在想：我不行了”，或“有个念头飘过来说：我不干了”。加个前缀，你和念头间多一道缝，它不再是“你”，只是脑子里的广播。\n")
    L.append("- **②看云**：把念头当天上的云、路上的车——看见它，但不追不赶、不和它吵架。它爱飘就飘，你站地上看；念头自己变淡飘走，不用使劲甩。\n")
    L.append("- **③选动作**：念头只是念头，不是命令。问自己“带着这个念头，我下一步做什么有用的事？”然后照样写报告、回消息——念头嘟囔，你照样干活。你不是被念头绑架的人，是听得到广播还能自己走路的人。\n")
    L.append("- 要点：你不是你的念头。小李那句“不干了”若加前缀变成“我注意到我正在想：不干了”，就知道那只是气头上的广播，不会当真甩出去。和认知重评是搭档——重评是换掉念头，解离是先退后看清楚念头不是你。解离不是消灭念头，是“念头≠我≠事实≠命令”。\n")
    L.append("\n**认知解离口诀**\n")
    L.append("> 念头不是我，加个前缀看云飘；它说它说由它说，我干我的不逃跑。\n")
    L.append("\n## 六、费曼自测题（旧+新结合）\n")
    L.append("用自己的话回答：*如果下次我又被一句难听话点着、心浮坐不住、脑子里还冒出“我不行了”“我不干了”的念头，我会怎么做，才能既不当场炸、又能管住浮躁、又不被念头带跑、把该干的活干好？*\n")
    L.append("标准答案要点：\n")
    L.append("1. 先静心（三分钟呼吸空间）：觉察“我在浮躁/被说难受”→手机扔远、注意放呼吸（吸数呼数、跑偏拉回）→带静一点的觉知睁眼，用我信息只说观点。不是硬压，是温柔接住。\n")
    L.append("2. 身体被勾动时——身体急停法（离开/喝口水/握拳松拳）先降温；想回怼时——六秒法则（闭嘴数六）+我信息只说观点；上头时——第三人称抽离+冲动冲浪；小火苗先五步刹车。\n")
    L.append("3. 念头乱飞时——认知解离：加标签“我注意到我正在想…”→当云看不追不赶→问“带它我下一步干啥”照样改活（念头是广播不是命令）；也可配合情绪命名（先起名）和认知重评（换掉歪念头）。对自己温柔（自我慈悲）：觉察自责→共通人性→手放胸口，用安抚代替自责。\n")
    L.append("4. 面对大活/浮躁坐不住——两分钟启动法（拆小步→定两分钟只做一点→动起来）+番茄专注+五感着陆养专注；别人脸色→课题分离（别人的题不扛）。始终记：场合不是秀脾气、更不是把气话当真扔出去的地方，只是说观点的地方；心浮先三分钟呼吸静一静，念头乱加前缀看它飘。\n")
    L.append("\n## 七、今日带走的两句新口诀\n")
    L.append("1. 三分钟呼吸空间：一觉浮躁二回呼吸，三带觉知做手里事；心像湖面风过自静，正念三分钟就平息。\n")
    L.append("2. 认知解离法：念头不是我，加个前缀看云飘；它说它说由它说，我干我的不逃跑。\n")
    L.append("3. 一句话收尾：场合不是秀脾气、更不是把气话当真扔出去的地方，只是说观点的地方；心浮时先三分钟呼吸静一静，念头乱时加前缀看它飘，你会越来越稳。\n")
    return "\n".join(L)

# ---------------------------------------------------------------- 主流程
def main():
    audio = build_audio()
    sections_js = "window.SECTIONS = " + json.dumps(SECTIONS, ensure_ascii=False) + ";"
    audio_js = "window.AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";"
    html = HTML.replace("__LESSON_DATA__", sections_js).replace("__AUDIO_DATA__", audio_js)
    out_html = os.path.join(WS, "emotion-class-20260724.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html] 写出 {out_html} ({len(html)/1024:.0f} KB)")
    md = build_markdown()
    out_md = os.path.join(WS, "情绪管理-晓晓老师课堂笔记.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出 {out_md} ({len(md)/1024:.0f} KB)")
    dated = os.path.join(WS, "情绪管理-晓晓老师课堂笔记_20260724.md")
    with open(dated, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[md] 写出带日期副本 {dated} ({len(md)/1024:.0f} KB)")
if __name__ == "__main__":
    main()
