# 情绪管理自动化 · 执行记录

## 2026-07-14 执行
- 任务：围绕"办公室不是展示真性情的地方，只是表达观点的地方"，做情绪管理课（初中生能懂、分步讲解、编口诀、带晓晓老师语音的互动网页、存 ima 知识库）。
- 检索素材：用 WebSearch 找到真实案例——"资深秘书摔门而去"（今日头条）、李筱懿金句"没有收拾残局的能力，就不要放纵自己的情绪"，改编为初中生版"小组作业摔本子"故事。
- 产出1：`emotion-class.html` —— 单文件互动课。晓晓老师神经网络语音（优先 zh-CN-XiaoxiaoNeural，回退系统中文语音）、底部不挡字幕、五步刹车法讲解、4 道费曼式定时提问（模拟同学抢答+老师点评+记忆卡）、心如止水水杯比喻、两份口诀、结尾星星积分与费曼自测。
- 产出2：`情绪管理-晓晓老师课堂笔记.md` —— 完整课程答案，供存入 ima 知识库。
- ima 推送：本环境 ima-mcp 连接器 disconnected，且无 ima_api CLI/凭证，无法自动写入 ima 知识库（含用户说的 imao）。已生成 markdown 笔记并告知用户手动导入方式；待用户在 WorkBuddy 中连接并信任 ima 连接器后可再自动推送。
- 备注：语音依赖浏览器 Web Speech API，需在支持中文神经语音的浏览器（如 Windows 版 Edge/Chrome）打开并点击播放才会发声。

## 2026-07-15 执行
- 用户同题再跑，但明确补了硬指标：宋体小四号(放大)、可调播放位置 + 上一句/下一句按钮、真正的晓晓老师神经网络语音、字幕不挡讲解、不定时费曼提问模拟师生互动、测试能正常打开、答案存 ima 的 imao 知识库。
- 本轮相比 07-14 的关键升级（已覆盖用户全部硬指标）：
  1. 语音：用 edge-tts(zh-CN-XiaoxiaoNeural) 逐句生成 37 句真实神经网络语音，base64 内联进单文件 HTML（不再依赖浏览器 Web Speech API；个别句失败才回退合成）。
  2. 播放器：底部固定播放条含「⏮上一句 / ▶播放 / 下一句⏭」+ 可拖动进度条(seek)，可逐句回看、任意调位置；整页宋体(SimSun) 15pt（小四基础上放大），字幕固定底部不遮挡讲解区。
  3. 素材刷新：WebSearch 取 2026 热点文《那个把"真性情"当耿直的同事，正在被所有人屏蔽》——大K"情绪泄洪" vs 林姐"情绪拆弹"对比，更贴合"办公室不是秀真性情、只是表达观点"。
  4. 教学：分步五步刹车法(一停二数三命名四转五说)+ 静音模式+水杯比喻+李筱懿金句+两份口诀；4 道课间提问(含同学抢答+晓晓点评角色扮演)+结尾费曼自测。
- 测试：node --check 语法通过；jsdom 无头加载并点击走完全部 11 段->到达"下课"卡片，runtime errors=0；数据对齐 PLAYLIST(37)==AUDIO(37) 全为合法 base64 音频。
- ima 推送：本环境 ima 凭证(~/.config/ima/client_id|api_key)现已就绪。定位到知识库 imao(kb_id=pm8-1404_EPGkcfBKDri-wPiUpjUHUjqokpiC7NvFo8=)，走 preflight→check_repeated_names(未重名)→create_media→cos-upload(HTTP200)→add_knowledge(code0)，已验证搜索命中《情绪管理-晓晓老师课堂笔记.md》。本次成功自动入库。
- 产物：`emotion-class.html`(2.9MB 自包含)、`情绪管理-晓晓老师课堂笔记.md`、`build_lesson.py`(生成器，保留可复现)。

## 2026-07-16 执行（第3天）
- 用户同题第3天运行。本日结构：先复习昨天两招(五步刹车+静音模式)→新案例(今日头条2026-06《连续刷手机3小时，我差点被公司开除》小林)→原理(工作记忆切碎/注意力残留/心如湖面)→新招1 五感着陆法(54321)→新招2 番茄专注法→费曼自测。新增4张内联SVG案例图(案例/湖面/54321/番茄钟)。
- 语音：edge-tts(zh-CN-XiaoxiaoNeural) 逐句生成 40 句真实神经网络语音，base64 内联进 emotion-class.html（约 3.9MB 自包含）。正文放大到 16pt(宋体SimSun)，底部播放条含「上一句/下一句」+可拖动 seek，字幕固定底部不挡讲解。
- 测试：jsdom 无头点击全流程——13段→到达「下课」卡片、5道quiz全对(5⭐)、runtime errors=0；数据对齐 PLAYLIST(40)==AUDIO(40) 全为合法 base64 音频。
- ima 推送：上传 dated 副本到 imao(kb_id=pm8-1404_EPGkcfBKDri-wPiUpjUHUjqokpiC7NvFo8=)，走 check_repeated_names(未重名)→create_media→cos-upload(OK)→add_knowledge(code0)，已 search_knowledge 验证命中。
- 留存 harness：`test_open.cjs`(jsdom 自检)、`_ima_chain.cjs`(ima 上传链) 供每日复跑；`build_lesson.py` 为内容源生成器。

## 2026-07-17 执行（第4天）
- 用户同题第4天运行。本日结构：先复习前四招(五步刹车+静音模式+五感着陆54321+番茄专注)→新案例(2026-06-30 今日头条《那个在会议室摔杯子的人，后来把饭碗也摔没了》老金 vs 苏姐)→原理(情绪ABC理论)→新招1 认知重评三步法(停/揪/换)→新招2 方箱呼吸(4-7-8)→费曼自测。共 5 道课间提问(含同学抢答+晓晓点评)+结尾费曼自测。
- 新增 4 张内联 SVG 案例图：四招复习地图(map)、老金拍桌vs苏姐稳(案例)、情绪ABC流程、方箱呼吸。
- 语音：edge-tts(zh-CN-XiaoxiaoNeural, rate -8%) 逐句生成 33 句真实神经网络语音，base64 内联进 emotion-class.html（约 4.1MB 自包含）。正文 16pt 宋体(SimSun)，底部播放条含「上一句/下一句」+可拖动 seek，字幕固定底部不挡讲解。
- 测试：jsdom 无头点击全流程——15步→到达「下课」卡片、5道quiz全对(5⭐)、runtime errors=0；数据对齐 PLAYLIST(33)==AUDIO(33) 全为合法 base64 音频。
- ima 推送：上传 dated 副本到 imao(kb_id=pm8-1404_EPGkcfBKDri-wPiUpjUHUjqokpiC7NvFo8=)，走 create_media→cos-upload(OK)→add_knowledge(code0)；已用 search_knowledge("情绪管理")+get_knowledge_list 双重验证命中《情绪管理-晓晓老师课堂笔记_20260717.md》。
- 改动点：build_lesson.py 重写为第4天内容（SVGs/SECTIONS/markdown/带日期副本）；_ima_chain.cjs 的 FILE/FNAME 改为 _20260717.md。

## 2026-07-18 执行（第5天）
- 用户同题第5天运行。本日结构：先复习前六招(五步刹车+静音+五感着陆+番茄+认知重评+方箱呼吸)→新案例(2026-07 真实案例：翟某工作群辱骂同事被辞退、索赔9万被法院驳回，来源申工社)→原理(旁观者清/自我抽离 + 冲动像海浪)→新招1 第三人称抽离法(退后/换角/劝友)→新招2 冲动冲浪法(认浪/看浪/等浪退,配4-7-8)→费曼自测。共 5 道课间提问(含同学抢答+晓晓点评)+结尾费曼自测。
- 新增 5 张内联 SVG 案例图：六招技能地图(map)、翟某群聊开喷vs冷静(案例)、两个真相(旁观者清+冲动海浪)、第三人称抽离(我→旁观者)、冲动冲浪(浪起→顶→退)。
- 语音：edge-tts(zh-CN-XiaoxiaoNeural, rate -8%) 逐句生成 33 句真实神经网络语音，base64 内联进 emotion-class.html（约 4.1MB 自包含）。正文 16pt 宋体(SimSun)，底部播放条含「上一句/下一句」+可拖动 seek，字幕固定底部不挡讲解。
- 测试：jsdom 无头点击全流程——15步→到达「下课」卡片、5道quiz全对(5⭐)、runtime errors=0；数据对齐 PLAYLIST(33)==AUDIO(33) 全为合法 base64 音频。
- ima 推送：上传 dated 副本到 imao(kb_id=pm8-1404_EPGkcfBKDri-wPiUpjUHUjqokpiC7NvFo8=)，走 create_media→cos-upload(OK)→add_knowledge(code0)；已用 search_knowledge("情绪管理") 验证命中《情绪管理-晓晓老师课堂笔记_20260718.md》。
- 改动点：build_lesson.py 重写为第5天内容；_ima_chain.cjs 的 FILE/FNAME 改为 _20260718.md。
