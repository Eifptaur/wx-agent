<p align="center">
  <img src="assets/icon.png" width="132" height="132" alt="wx-agent 小鲸鱼">
</p>

<h1 align="center">wx-agent —— 微信智能机器人</h1>

<p align="center">
  <b>v2.0.0·Ⅱ</b> · Windows 10/11 · Python 3.10+（无需安装，一键启动自动配置）· UIA 无注入 · 仅供学习交流
</p>

<p align="center">
  <a href="#-快速安装三步"><b>快速安装</b></a> ·
  <a href="#-功能一览"><b>功能一览</b></a> ·
  <a href="#-web-控制台"><b>Web 控制台</b></a> ·
  <a href="#-常用配置"><b>常用配置</b></a> ·
  <a href="#-风险提示"><b>风险提示</b></a>
</p>

<p align="center">
  在微信群里 <b>@机器人</b> 即可对话：<br>
  多模型大脑（DeepSeek / Kimi / 智谱 / 通义 / MiniMax / 小米 MiMo / 腾讯混元 / 百度文心 / 豆包 /
  ChatGPT / Claude / Gemini / Grok / NVIDIA / OpenRouter 聚合 / 自定义）<br>
  + <b>无注入</b>微信接入（不 Hook、不改文件、不碰协议，纯模拟真人键鼠）。
</p>

---

<table align="center">
<tr>
  <td align="center" width="33%">🧠 <b>多模型</b><br><span style="font-size:12px;color:#666">15 家厂商 160+ 型号<br>内置 171 条单价表</span></td>
  <td align="center" width="33%">🎚️ <b>响应档位</b><br><span style="font-size:12px;color:#666">1~4 档 + 按群单独设档<br>没命中 = 零 token</span></td>
  <td align="center" width="33%">🗣️ <b>人设体系</b><br><span style="font-size:12px;color:#666">小鲸鱼 / 傲娇 / 毒舌<br>可自定义角色卡</span></td>
</tr>
<tr>
  <td align="center">📸 <b>识图 + 发图</b><br><span style="font-size:12px;color:#666">引用图片说「分析这张」<br>也能转发图片</span></td>
  <td align="center">🌐 <b>联网搜索</b><br><span style="font-size:12px;color:#666">Bing/DeepSeek/智谱/博查/<br>百度/秘塔 + SSRF 防护</span></td>
  <td align="center">🧠 <b>群友记忆</b><br><span style="font-size:12px;color:#666">每成员长期印象<br>默认每群独立池</span></td>
</tr>
<tr>
  <td align="center">🏓 <b>拍一拍</b><br><span style="font-size:12px;color:#666">自动回拍 90% + 冷却<br>主动皮一下低频</span></td>
  <td align="center">💸 <b>用量成本</b><br><span style="font-size:12px;color:#666">今日/本周/累计 + 余额<br>每轮消耗泡泡</span></td>
  <td align="center">🖥️ <b>Web 控制台</b><br><span style="font-size:12px;color:#666">浏览器改设置/看日志<br>一键体检 53 项</span></td>
</tr>
<tr>
  <td align="center">🚀 <b>主动开话题</b><br><span style="font-size:12px;color:#666">冷场超时按概率抛梗<br>（默认关）</span></td>
  <td align="center">⭐ <b>反应评分引擎</b><br><span style="font-size:12px;color:#666">本地正反馈 + 趣味种子库<br>越聊越有趣（零 token）</span></td>
  <td align="center">📤 <b>社区分享</b><br><span style="font-size:12px;color:#666">金句/意见本地导出<br>可选直发社区</span></td>
</tr>
</table>

---

## 🚀 装好就能用（零基础 2 步）

1. **启动**：登录电脑微信 4.x（**建议小号**）→ 双击「**一键启动.vbs**」——自动完成：依赖检查 →（缺则自动装完）→ 自检 → 启动机器人 → 打开浏览器控制台；首次向导 3 步：选厂商 → 选模型 → 填 Key → 勾选要回的群 → 完成。
2. **开玩**：群里 @机器人 说句话就行。

> **日常**：想改什么都在控制台点（浏览器），不用碰文件；停止 = 双击「停止机器人.vbs」。
> 📖 详细教程见 **《使用说明.md》**；💴 用量估价见 **《价目表.md》**；📊 版本记录见 **《更新日志.md》**。
> ⚠️ 微信窗口可缩小但别最小化；机器人发话时别抢键鼠；风险提示见文末。
> 🔀 备用开关：`启动机器人.vbs`（仅启动）· `停止机器人.vbs`（停止，详细弹窗说明）。

---

## ✨ 功能一览

- **多模型（15 家厂商 160+ 型号，含 2026-09 榜单新模型）**：DeepSeek / Kimi（含 K3）/ 智谱 / 通义 / MiniMax / 小米 MiMo / 腾讯混元 / 百度文心 / 豆包 / ChatGPT·OpenAI（含 GPT-5）/ Claude / Gemini / Grok·xAI / NVIDIA / OpenRouter 聚合 / 自定义 BaseURL，控制台一键切换、按厂商存 Key（api.provider_keys）；内置 171 条官方/参考单价表（元/百万 token），未知型号按主流档位估算
- **无状态会话**：每次唤醒独立会话，提示词 = 静态人设 + 存档摘要 + 最新消息，成本不随历史膨胀
- **响应档位**：4 档（仅艾特 / +关键词 / +随机 / 全响应），没命中不调模型（零 token）；**默认 2 档**；可按群单独设档（store.unified_tier=false + store.group_tier）
- **群员黑名单**：store.group_blocklist 屏蔽指定群员（不存档、不触发、不进提示词）
- **记忆隔离**：默认每群独立记忆池（memory.share_across_groups=false），群间互不串味；一键共享开关
- **主动开话题**：proactive（可选，默认关）——群内冷场超时按概率主动抛话题（性价比抽一档人设）
- **反应评分引擎**：scoring（本地正反馈评分 + **官方精选种子库 91 条**（data/seed_library.json：知乎神回复/央视新闻神回复/群聊接梗，few-shot 参考，零 token 防饱和；可选导入金句墙种子/online 打分）；**不变人原则**：学习只调整语言风格——角色设定权重最高放提示词最前，参考素材只能"换衣服不能换魂"，越用越像角色卡，用户自定义角色卡同样适用（实测：毒舌角色+哲理种子→毒舌腔调说出机灵话））
- **社区分享**：community（金句/意见/聊天记录本地导出 exports\；可选填写上传 URL 直发社区，默认仅本地）
- **表情包积极度**：store.sticker_level 0~3（不鼓励 / 偶尔 / 较积极 / 爱好者，提示词引导）
- **工具集**：发消息（分条 / @ / 引用）、看图、发图、**收藏表情包（collect_emoji）→ 发表情包（send_emoji）**（**模型-程序协作表情库**：收藏时模型/程序生成极简概述入库 `data/emoji_index.json`，想发表情时程序把概述清单报给模型选第几个 → 程序换算行列→滚动→点选发送，采用鼠标真路径）、**收藏消息 / 撤回自己消息**、**点赞朋友圈 / 发朋友圈（实验性）**、**查看合并转发聊天记录（view_merge_forward）**、翻历史、查活跃成员、记忆增删查、联网搜索/抓网页、拍一拍（别人拍自动回拍 90% + 30 分钟冷却，主动皮一下低频）
- **人性化自主行为**（零 token 规则引擎）：收到表情自动收藏、群里发表情回敬、概率 @ 群友、点赞朋友圈——每类行为有概率/冷却/每日上限，**按角色卡自动调节频率**（角色卡管风格，引擎管频率：填角色卡后一键推荐行为档）
- **联网搜索**：Bing/DeepSeek/智谱/博查/百度/秘塔/自定义，web_fetch 带 SSRF 防护
- **群友长期记忆**：每成员一条 JSON，后台自动整理
- **人设模板**：小鲸鱼（默认）/ 傲娇 / 毒舌，可自定义
- **发送保护**：限频、真人化间隔、Markdown→纯文本、超长切分；新对话开始 70% 自动引用对方最近一句
- **用量统计**：今日 / 本周 / 累计 token 与成本估算、账户余额、每轮消耗；运行明细（思考过程/token/工具调用）
- **多模态识图**：引用图片后说「分析这张」，机器人解密看图作答
- **Web 控制台**：浏览器里改设置 / 看状态 / 看日志 / 一键体检 / 拍一拍诊断 / 测试 API / 查余额；三步首次向导（Key→选群→体检，只弹一次）；群选择带搜索+滚动；停止后自动关控制台标签
- **小鲸鱼余额挂件**：右下角常驻（余额刷新、今日已用、每轮消耗泡泡、拖拽吸附、Q 弹、音效台词）
- **界面适配**：DPI 缩放自动检测 + 手动覆盖、点击前自动清理遮挡、点击归属校验、自检按钮——换电脑无需逐个适配
- **控制台主题**：默认 🐋「鲸落」深海蓝渐变（出厂视觉）；可切换浅色 / 深色 / 跟随系统，保存设置即生效
- **🐋 鲸鱼图标果冻弹跳**：顶栏徽章 = 绿底背景 + 纯白鲸鱼主体（眼睛透绿底），悬停时原地果冻弹跳（下蹲-拉伸-压饼形变明显）；所有弹窗/向导图标均自动果冻弹跳
- **🐋 可拖拽小鲸鱼**：按住顶栏鲸鱼能拖出来（跟手+速度拉伸+被抓扭动挣扎），松开**随机三种方式返回徽章**（留在落点才触发，时长按拖拽距离计算，控制台「光标设置」可调速度系数）：① 蠕动着摆尾回去（波形+缩身钻入，最慢）② 平滑变形为白色纸飞机再滑翔飞回（抛物线，较快）③ 扎进 UI 消失 0.5 秒后从徽章里冒出来（气泡+回弹，距离自适应）
- **🐋 鲸鱼指针光标**：默认蓝色鲸鱼+白色微信气泡（保留原图颜色，仅背景透明；点击时向下果冻点头），控制台「光标设置」可选用户自己的图片（上传后立即生效）

鸣谢：本作品整合自开源项目 qq-agent（大脑）、wechat-deepseek-bot / wechatauto（微信接入）、DeepSeek-Balance-Whale-Widget（余额挂件），仅供学习交流；上游版权归原作者，许可证随包附送。具体下载地址与 B 站视频号见下文「致谢」一节。

## 🖥️ Web 控制台

启动后自动用浏览器打开（形如 `http://127.0.0.1:3210/?token=xxxx`）：概览（状态/今日/本周/累计用量/目标群）、体检与功能自检、运行明细（每轮思考/token/工具）、模型 API、微信、记忆、人设与响应、社区与学习、发送限制、联网搜索、服务器、界面适配（含主题/光标）、运行日志、原始 JSON。

## 📁 常用配置（平时在控制台改即可，保存即生效；下面只是 config.json 底层字段速查）

- api.base_url / api_key / model —— 大模型接口（必填）
- api.thinking —— 思考模式 auto/on/off（默认 off；推理文本是模型生成的链式输出而非真实思维，按输出价计费，off 省 50~90% token）
- api.use_official_price / model_prices —— 成本按内置价目/自定义单价（元/百万 token）估算
- wechat.bot_nickname —— 机器人微信昵称（群里 @ 这个触发）
- wechat.start_paused —— 启动后默认暂停（true=控制台点「恢复」才监听，防开机刷群/回应积压旧消息）
- wechat.group_name_white_list —— 允许回复的群名；空 = 所有群
- wechat.poll_interval —— 消息轮询秒数
- persona.bot_name / role_text / participation —— 人设名 / 人设文本 / 参与度
- persona.self_nickname —— 自我昵称（@识别时同时认它、微信实际昵称、人设名；留空用机器人昵称）
- store.context_tier / keywords —— 响应档位 1~4（默认 2） / 关键词（保存后真实生效：一档只回艾特，二档加关键词，三档再按概率随机，四档全响应）
- store.unified_tier / group_tier —— 全局档位 / 按群单独档位（false 时 {群名: 1~4}）
- store.group_blocklist —— 群员黑名单 {群名: [昵称, wxid...]}（不存档、不触发、不进提示词）
- store.sticker_level —— 表情包积极度 0~3
- memory.share_across_groups —— 所有群共享一个记忆池（默认 false=每群独立）
- proactive.* —— 主动开话题（enabled/间隔/冷场阈值/概率，默认全关）
- scoring.* —— 反应评分（enabled/seed_library/online_scoring/heat_decay/import_seed_file）
- community.export_dir / holyshits_upload_url / feedback_upload_url / upload_enabled —— 社区分享（本地导出/可选上传）
- store.random_percent —— 3 档随机回复概率（默认 60%）
- store.past_window_min —— 历史上下文时间窗（只把最近 N 分钟消息给模型，默认 30；0=不限，防回应很久前的艾特/旧话题）
- send.max_per_minute / max_per_hour —— 发送限频
- send.quote_on_new_talk / quote_reply_probability / quote_new_talk_gap_s —— 新对话自动引用规则
- poke.reply_probability / cooldown_seconds / active_probability / active_daily_limit —— 拍一拍概率
- stats.period —— 用量统计周期（daily/weekly/monthly，默认 weekly）
- server.port / token —— 控制台端口 / 访问口令（留空自动生成）
- ui.coord_scale / ui.clean_overlays / ui.theme / ui.whale_cursor —— 显示缩放 / 点击前清遮挡 / 主题（system|light|dark|whale）/ 鲸鱼光标

## 🛠️ 运维（全程无窗口，无需安装 Python）

- 一键启动.vbs —— **一键启动（自动：检测/下载绿色 Python → 装依赖 → 自检 → 启动，零弹窗后台；无需去官网装 Python）**
- 启动机器人.vbs —— 启动（同样自动保障 Python；隐藏跑 watchdog.py → pythonw 跑主程序，崩溃自动重启）
- 停止机器人.vbs —— 停止（按 PID 文件静默结束机器人+看门狗）
- scripts\watchdog.py / stop_bot.py —— 看门狗 / 停止器本体
- 安装依赖.bat / 自检.bat / scripts\onestart.py / scripts\设置开机自启.bat —— 装依赖（已装自动跳过）/ 环境自检 / 一键启动主体 / 开机自启
- scripts\开机自启.bat / 取消开机自启.bat —— 注册/取消登录自启（登录即自动一键启动）

**零 Python 启动**：电脑没装 Python 也能跑——一键启动会先找系统 Python 3.10+，找不到就用内置 `offline\python` 里的绿色版（自动解压到 `runtime\`），离线包已带 pip 依赖 wheels，装完依赖自动进入自检并拉起。

**离线部署**：仓库已含 `offline\`（依赖 wheels + 绿色版 Python 3.10 + 微信 4.1.13 安装包，微信版权归腾讯），目标电脑没网时：解压主体包 → 把 `offline\` 放进去 → 双击 `一键启动.vbs`（或 `安装依赖.bat`）→ 没装微信就装 `offline\wechat` 里的微信 4.1.13 → 完事。

## 📂 目录结构与文件用途

- wx_agent.py —— 主程序（消息轮询 + 大脑编排 + 用量统计 + 启动控制台）
- 安装依赖.bat —— 一键安装依赖（先体检：已装好且版本正确自动跳过，缺什么装什么；识别 offline\ 自动离线安装）
- config.json / config.example.json —— 你的配置（含 Key，勿上传）/ 配置模板
- 启动机器人.vbs / 停止机器人.vbs —— 无窗口启动 / 停止
- requirements.txt —— Python 依赖清单
- agent\ —— 核心代码：llm 模型调用、wechat 微信操作（读/发/引用/拍一拍）、tools 工具集、sender 发送队列、prompt 提示词、store 存档、memory 记忆、scoring 反应评分、webui 控制台服务、whale 余额挂件、ui_adapt 界面适配、stats 用量统计、session_log 运行明细、config 配置、util 工具、safe_fetch 安全抓取
- scripts\ —— 辅助脚本：watchdog 看门狗、stop_bot 停止器、selftest 自检、gen_price_table 价目表生成、备份 / 开机自启（自检.bat 在根目录）
- whale-widget\ —— 小鲸鱼余额挂件的浏览器脚本与素材（client\widget.js + assets\）
- offline\ —— 离线部署包（依赖 wheels + 绿色版 Python 3.10 + 微信 4.1.13 安装包，目标电脑没网也能装）
- data\ logs\ media\ —— 运行时生成：记忆/聊天存档/运行明细/账单/日志/下载图片（含隐私，勿上传）

## ⚠️ 风险提示（基于公开案例与社区实测数据查证，2026-09）

微信官方协议禁止非官方客户端/自动化程序。公开调查（腾讯云开发者社区 2025-04，微信机器人框架作者对 200+ 用户的统计）显示：Hook/进程注入类机器人是封号重灾区（接近"用了必中"），官方打击清单还包括自动加好友、批量点赞/转发、抢红包插件；同一调查约 15% 机器人用户从未被处理；后果分档为 功能限制 → 短期封禁 → 永久封禁。

本项目是 UIA 无注入模式（不 Hook、不改文件、不碰协议，纯模拟真人键鼠），**不在上述清单内**——但仍是"非官方行为"，风险无法归零。务必：用有使用时长的小号、控制频率（默认 ≤20 条/分钟）、不群发不刷数据、机器人发话时别抢键鼠。是否使用、用哪个号请自行评估。

## 🙏 致谢

本作品整合自以下开源项目（经二次开发整合，仅供学习交流；上游版权归原作者，许可证随包附送）：

- QQ Agent（智能大脑）：由 B 站网友 Kondius 基于 qq-bridge（https://github.com/Derpyu520/qq-bridge）修改而来。相关 B 站视频 BV1ss8R6zERG；修改版下载地址 https://t.bilibili.com/1244553403559837713
- wechat-deepseek-bot（微信接入层，底层 wechatauto UIA 无注入）：B 站视频 BV1Mz4267EHQ，GitHub https://github.com/bdydgz114514/wechat-deepseek-bot
- DeepSeek-Balance-Whale-Widget（小鲸鱼余额挂件）

不过尽管有这几个项目珠玉在前，但是做兼容和编写新的功能仍然十分困难，最终消耗的精力几乎相当于重构。
