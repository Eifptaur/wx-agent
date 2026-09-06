# wx-agent —— 微信智能机器人（当前版本 v2.0.0 · 2026-09-06）

微信群里 @机器人 即可对话：多模型大脑（DeepSeek / Kimi / 智谱 / 通义 / MiniMax / 豆包 / ChatGPT / Claude / Gemini / Grok / 自定义）+ 无注入微信接入（仅 Windows）。

## 致谢

本作品整合自以下开源项目（经二次开发整合，仅供学习交流；上游版权归原作者，许可证随包附送）：

- QQ Agent（智能大脑）：由 B 站网友 Kondius 基于 qq-bridge（https://github.com/Derpyu520/qq-bridge）修改而来。相关 B 站视频 BV1ss8R6zERG；修改版下载地址 https://t.bilibili.com/1244553403559837713
- wechat-deepseek-bot（微信接入层，底层 wechatauto UIA 无注入）：B 站视频 BV1Mz4267EHQ，GitHub https://github.com/bdydgz114514/wechat-deepseek-bot
- DeepSeek-Balance-Whale-Widget（小鲸鱼余额挂件）

不过尽管有这几个项目珠玉在前，但是做兼容和编写新的功能仍然十分困难，最终消耗的精力几乎相当于重构。

## ⚠️ 风险提示（基于公开案例与社区实测数据查证，2026-09）

微信官方协议禁止非官方客户端/自动化程序。公开调查（腾讯云开发者社区 2025-04，微信机器人框架作者对 200+ 用户的统计）显示：Hook/进程注入类机器人是封号重灾区（接近"用了必中"），官方打击清单还包括自动加好友、批量点赞/转发、抢红包插件；同一调查约 15% 机器人用户从未被处理；后果分档为 功能限制 → 短期封禁 → 永久封禁。

本项目是 UIA 无注入模式（不 Hook、不改文件、不碰协议，纯模拟真人键鼠），**不在上述清单内**——但仍是"非官方行为"，风险无法归零。务必：用有使用时长的小号、控制频率（默认 ≤20 条/分钟）、不群发不刷数据、机器人发话时别抢键鼠。是否使用、用哪个号请自行评估。

## 快速安装（三步）

1. 装环境：Windows 10/11（64 位）+ Python 3.10+，双击 `安装依赖.bat`（自动识别：已装好且版本正确直接跳过，缺什么装什么；检测到 offline\ 自动离线安装）。
2. 跑起来：登录电脑微信 4.x（小号，勾选自动登录）→ 双击「启动机器人.vbs」→ 浏览器自动打开控制台 → 首次向导：填大模型 Key → 勾选要回复的群 → 一键体检 → 完成。
3. 测试：群里 @机器人 说句话即可（全程不用改任何文件，之后都在控制台改）。

> 详细教程（含离线安装、Web 控制台、识图/拍一拍/引用）见《使用说明.md》；界面不适/想调参都在控制台，保存即生效。
> 实测用量与各厂商单价/充值能用多久，见《价目表.md》。
> 运行时微信窗口可缩小，但别最小化到任务栏；机器人在群里发言时别抢鼠标键盘。

## 功能一览

- 多模型（12 家厂商 80+ 型号，含 2026-09 榜单新模型）：DeepSeek / Kimi（含 K3）/ 智谱 / 通义 / MiniMax / 豆包 / ChatGPT·OpenAI（含 GPT-5）/ Claude / Gemini / Grok·xAI / 自定义 BaseURL，控制台一键切换、按厂商存 Key（api.provider_keys）
- 无状态会话：每次唤醒独立会话，提示词 = 静态人设 + 存档摘要 + 最新消息，成本不随历史膨胀
- 响应档位：4 档（仅艾特 / +关键词 / +随机 / 全响应），没命中不调模型（零 token）
- 工具集：发消息（分条 / @ / 引用）、看图、发图、翻历史、查活跃成员、记忆增删查、联网搜索/抓网页、拍一拍（别人拍自动回拍 90% + 30 分钟冷却，主动皮一下低频）
- 联网搜索：Bing/DeepSeek/智谱/博查/百度/秘塔/自定义，web_fetch 带 SSRF 防护
- 群友长期记忆：每成员一条 JSON，后台自动整理
- 人设模板：小鲸鱼（默认）/ 傲娇 / 毒舌，可自定义
- 发送保护：限频、真人化间隔、Markdown→纯文本、超长切分；新对话开始 70% 自动引用对方最近一句
- 用量统计：今日 / 本周 / 累计 token 与成本估算、账户余额、每轮消耗；运行明细（思考过程/token/工具调用）
- 多模态识图：引用图片后说「分析这张」，机器人解密看图作答
- Web 控制台：浏览器里改设置 / 看状态 / 看日志 / 一键体检 / 拍一拍诊断 / 测试 API / 查余额；三步首次向导（Key→选群→体检，只弹一次）；群选择带搜索+滚动；停止后自动关控制台标签
- 小鲸鱼余额挂件：右下角常驻（余额刷新、今日已用、每轮消耗泡泡、拖拽吸附、Q 弹、音效台词）
- 界面适配：DPI 缩放自动检测 + 手动覆盖、点击前自动清理遮挡、点击归属校验、自检按钮——换电脑无需逐个适配

鸣谢：本作品整合自开源项目 qq-agent（大脑）、wechat-deepseek-bot / wechatauto（微信接入）、DeepSeek-Balance-Whale-Widget（余额挂件），仅供学习交流；上游版权归原作者，许可证随包附送。具体下载地址与 B 站视频号见开头「致谢」一节。

## 常用配置（平时在控制台改即可，保存即生效；下面只是 config.json 底层字段速查）

- api.base_url / api_key / model —— 大模型接口（必填）
- api.thinking —— 思考模式 auto/on/off（默认 off；推理文本是模型生成的链式输出而非真实思维，按输出价计费，off 省 50~90% token）
- api.use_official_price / model_prices —— 成本按内置价目/自定义单价（元/百万 token）估算
- wechat.bot_nickname —— 机器人微信昵称（群里 @ 这个触发）
- wechat.start_paused —— 启动后默认暂停（true=控制台点「恢复」才监听，防开机刷群/回应积压旧消息）
- wechat.group_name_white_list —— 允许回复的群名；空 = 所有群
- wechat.poll_interval —— 消息轮询秒数
- persona.bot_name / role_text / participation —— 人设名 / 人设文本 / 参与度
- persona.self_nickname —— 自我昵称（@识别时同时认它、微信实际昵称、人设名；留空用机器人昵称）
- store.context_tier / keywords —— 响应档位 1~4 / 关键词（保存后真实生效：一档只回艾特，二档加关键词，三档再按概率随机，四档全响应）
- store.random_percent —— 3 档随机回复概率（默认 60%）
- store.past_window_min —— 历史上下文时间窗（只把最近 N 分钟消息给模型，默认 30；0=不限，防回应很久前的艾特/旧话题）
- send.max_per_minute / max_per_hour —— 发送限频
- send.quote_on_new_talk / quote_reply_probability / quote_new_talk_gap_s —— 新对话自动引用规则
- poke.reply_probability / cooldown_seconds / active_probability / active_daily_limit —— 拍一拍概率
- stats.period —— 用量统计周期（daily/weekly/monthly，默认 weekly）
- server.port / token —— 控制台端口 / 访问口令（留空自动生成）
- ui.coord_scale / ui.clean_overlays —— 显示缩放（auto 或 1.25~2.0）/ 点击前清遮挡

## Web 控制台

启动后自动用浏览器打开（形如 `http://127.0.0.1:3210/?token=xxxx`）：概览（状态/今日/本周/累计用量/目标群）、体检与功能自检、运行明细（每轮思考/token/工具）、模型 API、微信、记忆、人设与响应、发送限制、联网搜索、服务器、界面适配、运行日志、原始 JSON。

## 运维（无需 PowerShell，全程无窗口）

- 启动机器人.vbs —— 启动（pyw 隐藏跑 watchdog.py → pythonw 跑主程序，崩溃自动重启）
- 停止机器人.vbs —— 停止（按 PID 文件静默结束机器人+看门狗）
- scripts\watchdog.py / stop_bot.py —— 看门狗 / 停止器本体
- 安装依赖.bat / 自检.bat / scripts\备份配置.bat —— 装依赖（已装自动跳过）/ 环境自检 / 备份
- scripts\开机自启.bat / 取消开机自启.bat —— 注册/取消登录自启

离线部署：仓库已含 offline\（依赖 wheels + 绿色版 Python 3.10 + 微信 4.1.13 安装包，微信版权归腾讯），目标电脑没网时：解压主体包 → 把 offline\ 放进去 → 双击 安装依赖.bat（已装好自动跳过）→ 没装微信就装 offline\wechat 里的微信 4.1.13 → 运行 自检.bat 收尾。

## 目录结构与文件用途

- wx_agent.py —— 主程序（消息轮询 + 大脑编排 + 用量统计 + 启动控制台）
- 安装依赖.bat —— 一键安装依赖（先体检：已装好且版本正确自动跳过，缺什么装什么；识别 offline\ 自动离线安装）
- config.json / config.example.json —— 你的配置（含 Key，勿上传）/ 配置模板
- 启动机器人.vbs / 停止机器人.vbs —— 无窗口启动 / 停止
- requirements.txt —— Python 依赖清单
- agent\ —— 核心代码：llm 模型调用、wechat 微信操作（读/发/引用/拍一拍）、tools 工具集、sender 发送队列、prompt 提示词、store 存档、memory 记忆、webui 控制台服务、whale 余额挂件、ui_adapt 界面适配、stats 用量统计、session_log 运行明细、config 配置、util 工具、safe_fetch 安全抓取
- scripts\ —— 辅助脚本：watchdog 看门狗、stop_bot 停止器、selftest 自检、备份 / 开机自启（自检.bat 在根目录）
- whale-widget\ —— 小鲸鱼余额挂件的浏览器脚本与素材（client\widget.js + assets\）
- offline\ —— 离线部署包（依赖 wheels + 绿色版 Python 3.10 + 微信 4.1.13 安装包，目标电脑没网也能装）
- data\ logs\ media\ —— 运行时生成：记忆/聊天存档/运行明细/账单/日志/下载图片（含隐私，勿上传）
