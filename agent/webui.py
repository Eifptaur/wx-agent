# -*- coding: utf-8 -*-
"""Web 控制台：在浏览器里改设置、看状态、看日志、测试 API（移植自 qq-agent 的控制台思路）。

零第三方依赖，纯标准库 http.server，单文件 HTML（内联 CSS/JS，无框架）。
只监听本机回环地址，含可选访问口令。
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .config import deep_merge, get_config, save_config, set_config
from .console_html import HTML  # 界面模板（蓝白设计，设置项全量，独立文件便于改版）
from .util import mask_secret, redact_secrets

# 给挂件脚本（whale-widget/client/widget.js）注入访问口令：把脚本里的 /dsh-whale/*
# 绝对路径都补上 ?token=xxx，保证前端轮询/音频请求都带上口令
_WHALE_URL_RE = re.compile(r"(/dsh-whale/[^'\"\s?]+)(\?[^'\"\s]*)?")

_MASKED_MARK = "••••"


def _is_masked(v) -> bool:
    return isinstance(v, str) and (_MASKED_MARK in v or v.startswith("sk-***"))


def _protect_secrets(new_cfg: dict):
    """保存配置时：若密钥字段还是打码值，则不覆盖真实密钥。"""
    old = get_config()
    api_new = new_cfg.get("api")
    if isinstance(api_new, dict):
        api_old = old.get("api") or {}
        if _is_masked(api_new.get("api_key")):
            api_new["api_key"] = api_old.get("api_key") or ""
        pk_new = api_new.get("provider_keys")
        if isinstance(pk_new, dict):
            pk_old = (api_old.get("provider_keys") or {}) if isinstance(api_old, dict) else {}
            for k, v in pk_new.items():
                if _is_masked(v):
                    pk_new[k] = pk_old.get(k) or ""


class WebUI:
    """启动一个仅监听本机的 HTTP 服务，提供设置/状态/日志/测试 API 接口。"""

    def _data_path(self, name: str) -> str:
        """data 目录文件（尊重 WX_AGENT_DATA_DIR 环境，兼容测试隔离）。"""
        base = os.environ.get("WX_AGENT_DATA_DIR") or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data")
        return os.path.join(base, name)

    def _apply_whale(self, html: str) -> str:
        """鲸语文案服务端注入（保存后刷新必然正确；与前端 JS 时序无关）。"""
        try:
            cfg = get_config().get("ui", {}) or {}
            if str(cfg.get("text_style") or "") != "whale":
                return html
        except Exception:
            return html
        T = {
            "wx-agent 控制台": "wx-agent 控制台 · 想到再答",
            "概览": "🐋 概览 · 算力是省的，感情是真的",
            "配置与启动": "⚙️ 配置 · 你先别急，让我想想",
            "模型 API": "🧊 模型 API · deepseek，等我翻下资料",
            "微信": "💬 微信 · 收到，正在思考",
            "拍一拍": "👋 拍一拍 · 我轻轻出个手，就一下",
            "记忆": "🧠 记忆 · 我好像有点想起来了",
            "记忆共享": "🤝 记忆共享 · 想起来的都算数",
            "人设与响应": "🎭 人设 · 今天扮演谁，先想牌",
            "社区与学习": "📚 社区 · 好东西先存着，回头再想",
            "发送限制": "🚦 发送限制 · 说太多怕烧算力",
            "联网搜索": "🔎 联网搜索 · 我去外面翻翻",
            "服务器": "🖥️ 服务器 · 后台有人守着，不用想",
            "界面适配": "🎨 界面 · 脸面不能省",
            "运行日志": "📜 运行日志 · 思考过程全在这",
            "检测中心": "检测中心 · 出门前先自检一遍",
            "测试 API 连通": "测试 API 连通（先让我推理一下再说）",
            "保存": "保存（存好了，算力已省下）",
            "停止": "停止（下班了，别唤醒我）",
            "重启": "重启（睡饱了，重新思考）",
            "一键体检": "鼠标操作检测（动手前先想好）",
            "代码检测": "代码检测（先检查，再思考）",
            "功能自检清单": "功能自检清单（按重要性，一个一个过）",
            "程序鼠标检验": "🖱️ 程序鼠标检验（我说到做到）",
            "调试 · 高级功能": "调试 · 高级功能（内行才来的地方）",
            "停止检测": "停止检测（这次不推理了）",
            "发送消息": "发送消息（话给你带到了）",
        }
        for a, b in T.items():
            html = html.replace(a, b, 1)
        return html

    def _build_tag(self):
        """构建号（方便辨别新旧实例：console_html.py 修改时间 + 启动概率）。"""
        try:
            mt = os.path.getmtime(_HTML_SRC if "_HTML_SRC" in globals() else os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "console_html.py"))
            import datetime
            return "b." + datetime.datetime.fromtimestamp(mt).strftime("%m%d-%H%M")
        except Exception:
            return "b?"

    def __init__(self, status_provider, log_buffer, test_api_fn=None, on_save=None,
                 pause_fn=None, resume_fn=None, balance_fn=None, shutdown_fn=None,
                 whale=None, poke_test_fn=None, selfcheck_fn=None, restart_fn=None,
                 groups_fn=None, memory_fn=None, sessions_fn=None, emojis_fn=None,
                 recalibrate_fn=None, open_path_fn=None, ui_test_fn=None,
                 selfcheck_stop_fn=None, ui_stop_fn=None,
                 persona_scores_fn=None, persona_rate_fn=None,
                 persona_score_custom_fn=None, persona_ai_enrich_fn=None,
                 community_export_fn=None, community_upload_fn=None, scoring_import_fn=None):
        self.status_provider = status_provider      # () -> dict
        self.log_buffer = log_buffer                # collections.deque[str]
        self.test_api_fn = test_api_fn              # () -> dict
        self.on_save = on_save                      # (new_cfg) -> None（可选，用于通知运行中组件）
        self.pause_fn = pause_fn or (lambda: None)  # () -> None
        self.resume_fn = resume_fn or (lambda: None)  # () -> None
        self.balance_fn = balance_fn or (lambda: {"error": "未提供 balance_fn"})  # () -> dict
        self.shutdown_fn = shutdown_fn or (lambda: None)  # () -> None
        self.restart_fn = restart_fn or (lambda: None)    # () -> None（后台无窗口重启）
        self.whale = whale                          # agent.whale.WhaleWidget（小鲸鱼挂件，可选）
        self.poke_test_fn = poke_test_fn or (lambda: {"error": "未提供 poke_test_fn"})  # () -> dict
        self.selfcheck_fn = selfcheck_fn or (lambda: {"ok": False, "error": "未提供 selfcheck_fn"})  # () -> dict
        self.groups_fn = groups_fn or (lambda: {"ok": True, "groups": []})  # () -> dict（群列表）
        self.memory_fn = memory_fn or (lambda action, chat_key="", user_id="": {"ok": True,
                                                                               "chats": [], "members": []})  # (action, chat_key, user_id) -> dict
        self.sessions_fn = sessions_fn or (lambda limit: [])  # (limit) -> list（运行明细）
        self.emojis_fn = emojis_fn or (lambda: [])            # () -> list（表情包收藏夹）
        self.recalibrate_fn = recalibrate_fn or (lambda: {"ok": False, "error": "未提供"})
        self.open_path_fn = open_path_fn or (lambda path: {"ok": False, "error": "未提供"})
        self.ui_test_fn = ui_test_fn or (lambda kind: {"ok": False, "error": "未提供"})
        self.selfcheck_stop_fn = selfcheck_stop_fn or (lambda: None)
        self.ui_stop_fn = ui_stop_fn or (lambda: {"ok": False, "error": "未提供"})
        self.persona_scores_fn = persona_scores_fn or (lambda: {"ok": False, "error": "未提供"})
        self.persona_rate_fn = persona_rate_fn or (lambda k, s, n: {"ok": False, "error": "未提供"})
        self.persona_score_custom_fn = persona_score_custom_fn or (lambda t, l: {"ok": False, "error": "未提供"})
        self.persona_ai_enrich_fn = persona_ai_enrich_fn or (lambda n, t: {"ok": False, "error": "未提供"})
        self.community_export_fn = community_export_fn    # (kind) -> dict 金句/意见/聊天记录导出
        self.community_upload_fn = community_upload_fn    # (data) -> dict 上传到可配 URL
        self.scoring_import_fn = scoring_import_fn        # (text) -> dict 导入种子库
        self._server = None
        self._thread = None
        self.port = 0
        self._whale_js_cache = {}  # token -> bytes（注入口令后的挂件脚本缓存）
        # 静态素材根目录（assets\，含 logo-bg / icon-whale / cursor / custom-cursor）
        self._asset_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        # 加载图标（assets/icon.png），用于 favicon
        self._icon_bytes = b""
        try:
            icon_path = os.path.join(self._asset_root, "icon.png")
            with open(icon_path, "rb") as f:
                self._icon_bytes = f.read()
        except Exception:
            self._icon_bytes = b""

    # ── 小鲸鱼挂件路由（/dsh-whale/*，实现与原版插件一致的接口）───────────

    def _whale_get(self, handler, path: str, query: str):
        """GET /dsh-whale/* 分发。handler 是当前 HTTP Handler（带 _json/_bytes）。"""
        whale = self.whale
        if whale is None:
            return handler._json({"error": "not found"}, 404)
        if path == "/dsh-whale/balance.json":
            try:
                handler._json(whale.balance_payload())
            except Exception as e:
                handler._json({"ok": False, "error": str(e)[:200]})
        elif path == "/dsh-whale/size.json":
            handler._json(whale.size_payload())
        elif path == "/dsh-whale/last-turn.json":
            handler._json(whale.last_turn_payload())
        elif path == "/dsh-whale/image.png":
            handler._bytes(whale.asset_bytes("DSniang1.png") or b"", "image/png")
        elif path == "/dsh-whale/rua.gif":
            handler._bytes(whale.asset_bytes("rua.gif") or b"", "image/gif")
        elif path in ("/dsh-whale/sound/press.mp3", "/dsh-whale/sound/release.mp3"):
            kind = "press" if path.endswith("press.mp3") else "release"
            sound_set = (parse_qs(query).get("set") or [""])[0]
            data = whale.sound_bytes(kind, sound_set)
            handler._bytes(data or b"", "audio/mpeg")
        elif path == "/dsh-whale/widget.js":
            handler._bytes(self._whale_js_injected(), "application/javascript; charset=utf-8")
        else:
            handler._json({"error": "not found"}, 404)

    def _whale_js_injected(self) -> bytes:
        """返回注入口令后的挂件脚本字节（带缓存）。"""
        token = str(get_config().get("server", {}).get("token") or "").strip()
        if token in self._whale_js_cache:
            return self._whale_js_cache[token]
        try:
            js_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   "whale-widget", "client", "widget.js")
            with open(js_path, "r", encoding="utf-8") as f:
                js = f.read()
        except Exception:
            return b""
        if token:
            def _inj(m):
                base, q = m.group(1), (m.group(2) or "")[1:]
                return base + "?token=" + token + ("&" + q if q else "")
            js = _WHALE_URL_RE.sub(_inj, js)
        body = js.encode("utf-8")
        if len(self._whale_js_cache) > 4:
            self._whale_js_cache.clear()
        self._whale_js_cache[token] = body
        return body

    # ── 配置脱敏 ──────────────────────────────────────────────────────────

    def masked_config(self) -> dict:
        """返回配置副本：所有 API Key 打码（真实值只存服务器 config.json）。"""
        cfg = dict(get_config())
        api = dict(cfg.get("api") or {})
        if api.get("api_key"):
            api["api_key"] = mask_secret(api["api_key"])
        pk = api.get("provider_keys")
        if isinstance(pk, dict):
            api["provider_keys"] = {k: mask_secret(v) for k, v in pk.items() if v}
        cfg["api"] = api
        return cfg

    def _serve_wallpaper(self, path: str, handler, query):
        """视频壁纸（免认证，支持 Range 分段）：assets/wallpaper/<file>，供 <video> 背景流式播放。"""
        try:
            import urllib.parse as _up
            name = _up.unquote(os.path.basename(path))
            wdir = os.path.join(self._asset_root, "wallpaper")
            fp = os.path.join(wdir, name)
            if not os.path.exists(fp):
                handler._bytes(b"", "video/mp4", 404)
                return
            size = os.path.getsize(fp)
            ftype = "video/mp4"
            rng = handler.headers.get("Range")
            start, end = 0, size - 1
            if rng and rng.startswith("bytes="):
                try:
                    part = rng[6:].split(",", 1)[0]
                    s, _, e = part.partition("-")
                    start = int(s) if s else 0
                    end = int(e) if e else size - 1
                except Exception:
                    start, end = 0, size - 1
            end = min(end, size - 1)
            length = max(0, end - start + 1)
            handler.send_response(206 if rng else 200)
            handler.send_header("Content-Type", ftype)
            handler.send_header("Accept-Ranges", "bytes")
            handler.send_header("Content-Length", str(length))
            if rng:
                handler.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
            handler.end_headers()
            with open(fp, "rb") as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(64 * 1024, remaining))
                    if not chunk:
                        break
                    handler.wfile.write(chunk)
                    remaining -= len(chunk)
        except Exception:
            try:
                handler._bytes(b"", "video/mp4", 404)
            except Exception:
                pass

    def _serve_asset(self, path: str, handler):
        """静态素材服务（免认证）：favicon / 图标背景 / 鲸鱼主体 / 光标 / 表情收藏夹。"""
        name = os.path.basename(path)
        try:
            if name == "ui-bg.jpg":
                # 自定义背景图（用户上传）
                fp = self._data_path("ui_bg.jpg")
                if os.path.exists(fp):
                    with open(fp, "rb") as f:
                        handler._bytes(f.read(), "image/jpeg")
                    return
                handler._bytes(b"", "image/jpeg", 404)
                return
            if path.startswith("/assets/emoji/"):
                import urllib.parse as _up
                name = _up.unquote(name)
                emoji_dir = self._data_path("emojis")
                with open(os.path.join(emoji_dir, name), "rb") as f:
                    body = f.read()
            elif name == "icon.png":
                body = self._icon_bytes
            elif name == "DSniang1.png":
                body = (self.whale.asset_bytes(name) if self.whale else None) or b""
            else:
                # 默认资源：assets/ 根，其次 assets/wallpaper/（ocean1.jpg 等）
                for base in (self._asset_root, os.path.join(self._asset_root, "wallpaper")):
                    fp = os.path.join(base, name)
                    if os.path.exists(fp):
                        with open(fp, "rb") as f:
                            body = f.read()
                        break
                else:
                    raise FileNotFoundError(name)
        except Exception:
            body = b""
        handler._bytes(body, "image/png")

    def start(self) -> int:
        cfg = get_config().get("server", {})
        if cfg.get("enabled") is False:
            return 0
        host = str(cfg.get("host") or "127.0.0.1")
        port = int(cfg.get("port") or 3210)

        parent = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "wx-agent/1.0"

            def log_message(self, fmt, *args):
                pass  # 静默，避免刷屏

            def _json(self, obj, code=200):
                body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _bytes(self, body, ctype="application/octet-stream", code=200):
                if not body:
                    body = b""
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def _auth_ok(self):
                token = str(get_config().get("server", {}).get("token") or "").strip()
                if not token:
                    return True
                # 支持 ?token= 或 Authorization: Bearer
                q = urlparse(self.path).query
                from urllib.parse import parse_qs
                if token in parse_qs(q).get("token", []):
                    return True
                auth = self.headers.get("Authorization", "")
                return auth == "Bearer " + token

            def do_GET(self):
                parsed = urlparse(self.path)
                path = parsed.path
                # 静态素材（图标/光标图）免认证：<img> 不带 token，但素材不含隐私
                if path.startswith("/assets/"):
                    return parent._serve_asset(path, self)
                if path.startswith("/wallpaper/"):
                    return parent._serve_wallpaper(path, self, parsed.query)
                if not self._auth_ok():
                    return self._json({"error": "unauthorized"}, 401)
                if path in ("/", "/index.html"):
                    token = str(get_config().get("server", {}).get("token") or "").strip()
                    body = HTML.replace("__TKN__", token)
                    body = body.replace("__VER__", parent._build_tag())
                    body = parent._apply_whale(body)
                    body = body.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                    self.end_headers()
                    self.wfile.write(body)
                elif path.startswith("/dsh-whale/"):
                    parent._whale_get(self, path, parsed.query)
                elif path == "/api/config":
                    self._json(parent.masked_config())
                elif path == "/api/memory":
                    # 记忆页面：?chat_key= 传群则返回该群成员印象列表
                    q = parse_qs(parsed.query)
                    chat_key = (q.get("chat_key") or [""])[0]
                    try:
                        self._json(parent.memory_fn("list", chat_key))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/sessions":
                    # 运行明细（思考/token/工具）：?limit=30
                    q = parse_qs(parsed.query)
                    try:
                        self._json({"ok": True, "sessions": parent.sessions_fn(
                            int((q.get("limit") or ["30"])[0]))})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/status":
                    self._json(parent.status_provider())
                elif path == "/api/balance":
                    try:
                        self._json(parent.balance_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/logs":
                    self._json({"lines": list(parent.log_buffer)})
                elif path == "/api/wechat-groups":
                    # 检测到的群聊列表（白名单勾选用，GET）
                    try:
                        self._json(parent.groups_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e), "groups": []})
                elif path == "/api/emojis":
                    # 表情包收藏夹列表（GET）
                    try:
                        self._json({"ok": True, "emojis": parent.emojis_fn()})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e), "emojis": []})
                elif path == "/api/ui-test/stop":
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/scores":
                    # 角色评分表：系统自动贴合分 + 用户分（GET）
                    try:
                        self._json(parent.persona_scores_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas":
                    # 热门人设选单（GET，带分区 cat）
                    try:
                        from agent.persona import PERSONAS, PERSONA_CATS
                        self._json({"ok": True, "personas": [
                            {"key": k, "name": v.get("name") or k, "text": v.get("text") or "",
                             "cat": PERSONA_CATS.get(k, "🔥 网络热门")}
                            for k, v in PERSONAS.items()]})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/persona/cats":
                    # 分区列表（GET）：内置 + 用户新建分区
                    try:
                        import json as _json
                        _p = os.path.join(parent._asset_root, "..", "data", "persona_cats.json")
                        try:
                            with open(_p, "r", encoding="utf-8") as f:
                                user_cats = _json.load(f)
                        except Exception:
                            user_cats = {}
                        from agent.persona import PERSONA_CATS
                        built = sorted(set(PERSONA_CATS.values()))
                        self._json({"ok": True, "built": built,
                                    "user": [{"name": k, "desc": (v or {}).get("desc", "")} for k, v in user_cats.items()]})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/custom":
                    # 自定义角色卡列表（GET）
                    try:
                        import json as _json
                        _p = os.path.join(parent._asset_root, "..", "data", "custom_personas.json")
                        try:
                            with open(_p, "r", encoding="utf-8") as f:
                                items = _json.load(f)
                        except Exception:
                            items = {}
                        self._json({"ok": True, "custom": [
                            {"key": k, "name": (v or {}).get("name", k), "text": (v or {}).get("text", ""),
                             "cat": (v or {}).get("cat") or "📝 自定义"}
                            for k, v in items.items()]})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui-layout":
                    # 微信 UI 图标库标定状态（GET）
                    try:
                        from agent.wechat_ui import _load_layout
                        self._json({"ok": True, "layout": _load_layout()})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui/recalibrate":
                    # 重新标定微信 UI 图标库（POST；接管鼠标瞬间，需微信在前台）
                    try:
                        self._json(parent.recalibrate_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/open-path":
                    # 打开导出文件所在位置（POST {path}）
                    try:
                        self._json(parent.open_path_fn(str(data.get("path") or "")))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui-test":
                    # 程序鼠标检验（POST {kind}：程序直接操控鼠标执行对应操作；data 透传给检验函数）
                    try:
                        self._json(parent.ui_test_fn(str(data.get("kind") or ""), data))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/selfcheck-stop":
                    # 停止当前一键体检（POST；设置取消标志，体检循环下一步即退出）
                    try:
                        parent.selfcheck_stop_fn()
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                else:
                    self._json({"error": "not found"}, 404)

            def do_POST(self):
                if not self._auth_ok():
                    return self._json({"error": "unauthorized"}, 401)
                self._handle_body_request()

            def do_PUT(self):
                # 小鲸鱼挂件前端用 PUT 保存配置（fetch SIZE_URL, {method:'PUT'}）
                if not self._auth_ok():
                    return self._json({"error": "unauthorized"}, 401)
                self._handle_body_request()

            def _handle_body_request(self):
                path = urlparse(self.path).path
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b"{}"
                try:
                    data = json.loads(raw.decode("utf-8")) if raw else {}
                except Exception:
                    data = {}
                if path == "/api/config":
                    try:
                        new_cfg = data if isinstance(data, dict) and data else get_config()
                        # 部分字段保存不丢段：与当前配置深合并（新值优先，缺失键保留旧值）
                        # 注意：deep_merge 返回全新深拷贝，绝不能原地改 _current_config，
                        # 否则 _protect_secrets 拿到的"旧值"已被掩码写脏，真实 key 会丢失。
                        new_cfg = deep_merge(get_config(), new_cfg)
                        _protect_secrets(new_cfg)  # 掩码值不覆盖真实密钥
                        set_config(new_cfg)
                        save_config(new_cfg)
                        if parent.on_save:
                            parent.on_save(new_cfg)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/cursor/upload":
                    # 自定义光标：base64 PNG/JPEG → assets/custom-cursor.png
                    try:
                        import base64
                        b64 = str(data.get("image") or "")
                        if len(b64) > 12 * 1024 * 1024:
                            return self._json({"ok": False, "error": "图片过大（≤8MB 源图）"}, 400)
                        if b64.startswith("data:"):
                            b64 = b64.split(",", 1)[1]
                        img = base64.b64decode(b64)
                        if not img.startswith(b"\x89PNG") and not img.startswith(b"\xff\xd8"):
                            return self._json({"ok": False, "error": "仅支持 PNG/JPEG 图片"}, 400)
                        with open(os.path.join(parent._asset_root, "custom-cursor.png"), "wb") as f:
                            f.write(img)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/cursor/reset":
                    # 重置为默认鲸鱼：删除自定义光标残留文件（否则页面刷新后预览仍探测到旧文件——030538）
                    try:
                        _p = os.path.join(parent._asset_root, "custom-cursor.png")
                        if os.path.exists(_p):
                            os.remove(_p)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/memory":
                    # 记忆页：delete（删某成员印象） / update（编辑成员印象）
                    try:
                        action = str(data.get("action") or "delete")
                        if action == "update":
                            r = parent.memory_fn("update", str(data.get("chat_key") or ""),
                                                 str(data.get("user_id") or ""),
                                                 str(data.get("name") or ""),
                                                 data.get("contents") or [])
                        else:
                            r = parent.memory_fn(action, str(data.get("chat_key") or ""),
                                                 str(data.get("user_id") or ""))
                        self._json(r)
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/sessions":
                    # 运行明细：思考过程 / token / 工具调用
                    try:
                        self._json({"ok": True, "sessions": parent.sessions_fn(
                            int(data.get("limit") or 30))})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/dsh-whale/size.json":
                    # 小鲸鱼挂件配置保存（前端 PUT）
                    if parent.whale is None:
                        self._json({"error": "not found"}, 404)
                    else:
                        try:
                            self._json(parent.whale.save_size(data))
                        except Exception as e:
                            self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/test-api":
                    try:
                        if parent.test_api_fn:
                            self._json(parent.test_api_fn())
                        else:
                            self._json({"ok": False, "error": "未提供 test_api_fn"})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/poke-test":
                    # 拍一拍诊断：完整跑一遍并返回分步结果
                    # body: {group_wxid?, verify_only?}
                    try:
                        self._json(parent.poke_test_fn(str(data.get("group_wxid") or ""),
                                                       bool(data.get("verify_only"))))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/selfcheck":
                    # 一键体检：配置/微信/数据/界面适配/命中测试 全套
                    try:
                        self._json(parent.selfcheck_fn())
                    except Exception as e:
                        self._json({"ok": False, "checks": [], "summary": str(e)})
                elif path == "/api/wechat-groups":
                    # 检测到的群聊列表（白名单勾选用）
                    try:
                        self._json(parent.groups_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e), "groups": []})
                elif path == "/api/community/export":
                    # 导出：金句/意见/聊天记录/角色评分 → 本地文件
                    try:
                        if not parent.community_export_fn:
                            self._json({"ok": False, "error": "未提供导出功能"})
                        else:
                            self._json(parent.community_export_fn(str(data.get("kind") or "holyshits")))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/community/upload":
                    # 提交到可配置上传 URL（holyshits/feedback，默认关）——社区分享
                    try:
                        if not parent.community_upload_fn:
                            self._json({"ok": False, "error": "未提供上传功能"})
                        else:
                            self._json(parent.community_upload_fn(data))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/scoring/import":
                    # 从金句墙导出数据导入评分种子库
                    try:
                        if not parent.scoring_import_fn:
                            self._json({"ok": False, "error": "未提供评分导入"})
                        else:
                            self._json(parent.scoring_import_fn(str(data.get("text") or "")))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/scoring/stats":
                    try:
                        from agent.scoring import stats as _s
                        self._json({"ok": True, "data": _s()})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)}, 500)
                elif path == "/api/pause":
                    parent.pause_fn()
                    self._json({"ok": True})
                elif path == "/api/resume":
                    parent.resume_fn()
                    self._json({"ok": True})
                elif path == "/api/shutdown":
                    self._json({"ok": True, "note": "正在停止机器人…"})
                    # 稍等响应返回后再触发停止，避免连接被切断
                    threading.Timer(0.5, parent.shutdown_fn).start()
                elif path == "/api/restart":
                    # 重启：后台无窗口拉起新实例（释放端口后接替），当前实例退出
                    self._json({"ok": True, "note": "正在后台重启机器人…"})
                    threading.Timer(0.5, parent.restart_fn).start()
                elif path == "/api/ui-test":
                    # 程序鼠标检验（POST {kind}：程序直接操控鼠标执行对应操作；data 透传给检验函数）
                    try:
                        self._json(parent.ui_test_fn(str(data.get("kind") or ""), data))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui-test/stop":
                    # 单项鼠标检验「停止」（POST）
                    try:
                        self._json(parent.ui_stop_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/stats/cal":
                    # 日历：读取某日会话明细（data/sessions/YYYY-MM-DD.jsonl 汇总）
                    try:
                        import json as _j
                        d = str(data.get("d") or "")
                        _sf = os.path.join(parent._data_path("sessions"), (d + ".jsonl"))
                        agg = {"date": d, "sessions": 0, "tokens": 0, "cost": 0.0, "calls": 0, "sent": 0}
                        if d and os.path.exists(_sf):
                            with open(_sf, encoding="utf-8") as fh:
                                for line in fh:
                                    line = line.strip()
                                    if not line:
                                        continue
                                    try:
                                        o = _j.loads(line)
                                        agg["sessions"] += 1
                                        agg["tokens"] += int(o.get("tokens") or 0)
                                        agg["cost"] += float(o.get("cost") or 0)
                                        agg["calls"] += int(o.get("calls") or 0)
                                        if o.get("reply"):
                                            agg["sent"] += 1
                                    except Exception:
                                        pass
                        self._json({"ok": True, **agg})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/emojis/delete":
                    # 删除一个收藏的表情文件（POST {name}）
                    try:
                        import urllib.parse as _up
                        name = _up.unquote(str(data.get("name") or ""))
                        emoji_dir = parent._data_path("emojis")
                        fp = os.path.join(emoji_dir, os.path.basename(name))
                        if os.path.exists(fp):
                            os.remove(fp)
                            self._json({"ok": True})
                        else:
                            self._json({"ok": False, "error": "文件不存在：" + name})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/code-check":
                    # 代码检测（POST；纯代码层检查，不接管鼠标）。改为后台线程跑，前端轮询进度。
                    try:
                        import threading
                        from agent.code_check import run as _code_run
                        def _bg():
                            try:
                                _code_run._res = _code_run(bool(data.get("deps")))
                            except Exception as e:
                                _code_run._res = {"ok": False, "checks": [], "summary": "代码检测失败：%s" % e}
                            _code_run._done = True
                        # 若上一次已彻底完成，则清掉旧结果以便重跑
                        if getattr(_code_run, "_done", False) or getattr(_code_run, "_res", None):
                            _code_run._done = False
                            _code_run._res = None
                        threading.Thread(target=_bg, daemon=True).start()
                        self._json({"ok": True, "started": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/code-check/progress":
                    # 代码检测进度（GET/POST）：{done, progress:{done,total,current}, result?}
                    try:
                        from agent.code_check import run as _code_run
                        done = bool(getattr(_code_run, "_done", False))
                        self._json({"ok": True, "done": done,
                                    "progress": getattr(_code_run, "_prog", None),
                                    "result": getattr(_code_run, "_res", None) if done else None})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/persona/cats/save":
                    # 新建/更新分区（POST {name, desc?}）
                    try:
                        import json as _json
                        _p = os.path.join(parent._asset_root, "..", "data", "persona_cats.json")
                        try:
                            with open(_p, "r", encoding="utf-8") as f:
                                user_cats = _json.load(f)
                        except Exception:
                            user_cats = {}
                        name = str(data.get("name") or "").strip()
                        if not name:
                            self._json({"ok": False, "error": "分区名不能为空"})
                        else:
                            cur = user_cats.get(name, {}) or {}
                            cur["desc"] = str(data.get("desc") or cur.get("desc") or "")
                            user_cats[name] = cur
                            with open(_p, "w", encoding="utf-8") as f:
                                _json.dump(user_cats, f, ensure_ascii=False, indent=1)
                            self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/persona/cats/del":
                    # 删除用户分区（POST {name}）：分区下自定义卡"移回 📝 自定义"，分区移除
                    try:
                        import json as _json
                        cats_p = os.path.join(parent._asset_root, "..", "data", "persona_cats.json")
                        pers_p = os.path.join(parent._asset_root, "..", "data", "custom_personas.json")
                        name = str(data.get("name") or "").strip()
                        try:
                            with open(cats_p, "r", encoding="utf-8") as f:
                                user_cats = _json.load(f)
                        except Exception:
                            user_cats = {}
                        user_cats.pop(name, None)
                        with open(cats_p, "w", encoding="utf-8") as f:
                            _json.dump(user_cats, f, ensure_ascii=False, indent=1)
                        # 该分区下的卡移到默认
                        try:
                            with open(pers_p, "r", encoding="utf-8") as f:
                                items = _json.load(f)
                        except Exception:
                            items = {}
                        for k, v in items.items():
                            if (v or {}).get("cat") == name:
                                v["cat"] = "📝 自定义"
                        with open(pers_p, "w", encoding="utf-8") as f:
                            _json.dump(items, f, ensure_ascii=False, indent=1)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/persona/score":
                    # 自定义角色卡评分（POST {text, llm?}）：默认本地；llm=true 时交模型
                    try:
                        self._json(parent.persona_score_custom_fn(str(data.get("text") or ""),
                                                                  bool(data.get("llm"))))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/custom":
                    # 自定义角色卡保存（POST {name, text, key?, cat?}；无 key=新建；cat=分区名）
                    try:
                        import json as _json
                        _p = os.path.join(parent._asset_root, "..", "data", "custom_personas.json")
                        items = {}
                        try:
                            with open(_p, "r", encoding="utf-8") as f:
                                items = _json.load(f)
                        except Exception:
                            pass
                        key = str(data.get("key") or "")
                        name = str(data.get("name") or "").strip()
                        text = str(data.get("text") or "").strip()
                        cat = str(data.get("cat") or "").strip() or "📝 自定义"
                        if not text:
                            self._json({"ok": False, "error": "角色文本不能为空"})
                        else:
                            if not key:
                                key = "custom_" + str(int(time.time()))
                            cur = items.get(key, {}) or {}
                            cur["name"] = name or cur.get("name") or "自定义"
                            if text:
                                cur["text"] = text
                            cur["cat"] = cat
                            items[key] = cur
                            with open(_p, "w", encoding="utf-8") as f:
                                _json.dump(items, f, ensure_ascii=False, indent=1)
                            self._json({"ok": True, "key": key})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/custom/del":
                    # 删除自定义角色卡（POST {key}）
                    try:
                        import json as _json
                        _p = os.path.join(parent._asset_root, "..", "data", "custom_personas.json")
                        try:
                            with open(_p, "r", encoding="utf-8") as f:
                                items = _json.load(f)
                        except Exception:
                            items = {}
                        items.pop(str(data.get("key") or ""), None)
                        with open(_p, "w", encoding="utf-8") as f:
                            _json.dump(items, f, ensure_ascii=False, indent=1)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/persona/ai-enrich":
                    # 模型补足（POST {name, text?, rounds?}；rounds=补足轮数，人设导向+分升停止）
                    try:
                        self._json(parent.persona_ai_enrich_fn(str(data.get("name") or ""),
                                                               str(data.get("text") or ""),
                                                               int(data.get("rounds") or 1)))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui/background":
                    # 自定义背景图（POST {data: base64(dataURL)}, 或 {clear:true}）
                    try:
                        import base64 as _b64
                        _p = parent._data_path("ui_bg.jpg")
                        if data.get("clear"):
                            if os.path.exists(_p):
                                os.remove(_p)
                            try:
                                from agent.config import get_config as _gc, save_config as _sc
                                _c = _gc(); _c.setdefault("ui", {})["background"] = ""; _sc(_c)
                            except Exception:
                                pass
                            self._json({"ok": True, "note": "已恢复默认背景"})
                        else:
                            raw = str(data.get("data") or "")
                            if "base64," in raw[:60]:
                                raw = raw.split("base64,", 1)[1]
                            raw = re.sub(r"[\s\r\n]", "", raw)       # 清洗空白
                            raw += "=" * (-len(raw) % 4)             # padding 补全
                            try:
                                img_bytes = _b64.b64decode(raw, validate=False)
                            except Exception:
                                raise ValueError("base64 解码失败（图片数据损坏？请重试或换一张图）")
                            from PIL import Image
                            import io as _io
                            try:
                                im = Image.open(_io.BytesIO(img_bytes)).convert("RGB")
                            except Exception:
                                raise ValueError("图片格式无法识别（仅支持 PNG/JPEG/WEBP/GIF）")
                            im.thumbnail((1920, 1080))
                            im.save(_p, "JPEG", quality=82)
                            try:
                                from agent.config import get_config as _gc, save_config as _sc
                                _c = _gc(); _c.setdefault("ui", {})["background"] = "custom"; _sc(_c)
                            except Exception:
                                pass
                            self._json({"ok": True, "note": "背景已保存并应用"})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e).split("\n")[0][:140] or "图片处理失败"})
                elif path == "/api/personas/favs":
                    # 人设星标集合（GET）
                    try:
                        import json as _json
                        try:
                            with open(parent._data_path("persona_favs.json"), "r", encoding="utf-8") as f:
                                favs = _json.load(f)
                        except Exception:
                            favs = {}
                        self._json({"ok": True, "favs": favs})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/fav":
                    # 设/取消星标（POST {key, fav}）
                    try:
                        import json as _json
                        try:
                            with open(parent._data_path("persona_favs.json"), "r", encoding="utf-8") as f:
                                favs = _json.load(f)
                        except Exception:
                            favs = {}
                        k = str(data.get("key") or "")
                        if data.get("fav"):
                            favs[k] = 1
                        else:
                            favs.pop(k, None)
                        with open(parent._data_path("persona_favs.json"), "w", encoding="utf-8") as f:
                            _json.dump(favs, f, ensure_ascii=False, indent=1)
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/personas/rate":
                    # 用户为角色打分（POST {key, score, note?}，落盘）
                    try:
                        self._json(parent.persona_rate_fn(str(data.get("key") or ""),
                                                          data.get("score"),
                                                          str(data.get("note") or "")))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/selfcheck-stop":
                    # 停止当前一键体检（POST；设置取消标志，体检循环下一步即退出）
                    try:
                        parent.selfcheck_stop_fn()
                        self._json({"ok": True})
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/ui/recalibrate":
                    # 重新标定微信 UI 图标库（POST；接管鼠标瞬间，需微信在前台）
                    try:
                        self._json(parent.recalibrate_fn())
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                elif path == "/api/open-path":
                    # 打开导出文件所在位置（POST {path}）
                    try:
                        self._json(parent.open_path_fn(str(data.get("path") or "")))
                    except Exception as e:
                        self._json({"ok": False, "error": str(e)})
                else:
                    self._json({"error": "not found"}, 404)

        # 端口自适应：被占用则顺延
        for offset in range(20):
            try:
                self._server = ThreadingHTTPServer((host, port + offset), Handler)
                self.port = port + offset
                break
            except OSError:
                continue
        if self._server is None:
            raise RuntimeError("无法启动 Web 控制台：端口 %d-%d 均被占用" % (port, port + 19))

        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self.port

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
