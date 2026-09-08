# -*- coding: utf-8 -*-
"""⑤ 3轮补足+评分：遍历 PERSONAS，模型五维评分，<75 → persona_enrich 补足 → 再评（最多3轮），目标全≥75。
用法：py -3 -X utf8 scripts/persona_fix.py [test]"""
import sys, os, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
from agent.persona import PERSONAS
from agent.persona_enrich import enrich
from agent.persona_rating import WEIGHTS
from agent import llm

RULES = "你是角色卡五维评分器（唯一权威细则）。\n五维（0~100.00）：风格辨识25%/角色贴合30%/内在一致20%/表达自然15%/完整可用10%。\n扣分上限：无口头禅→风格≤45；通用词口头禅→风格≤70；AI套话→表达≤65；'客服/助手'口吻→贴合≤60；换角色都能用→贴合≤50；示例占位→完整≤75；沉默类无扩展→完整≤70；缺说话规则→完整≤70。满分100唯一条件：仅凭此卡+一次提醒即可逐句贴合本人。\n只输出严格JSON：{\"style\":0,\"fit\":0,\"coher\":0,\"natural\":0,\"usable\":0}"

def score(key, card):
    try:
        sys_msg = [{"role": "system", "content": RULES},
                   {"role": "user", "content": "角色卡「%s」：\n%s" % (key, str(card.get("text") or ""))}]
        r = llm.chat_completion(sys_msg, temperature=0.1)
        t = str((r.get("message") or {}).get("content", ""))
        m = re.search(r"\{[^}]+\}", t)
        if not m:
            return None
        d = json.loads(m.group(0))
        dims = {k: float(d.get(k, 0)) for k in WEIGHTS}
        return round(sum(max(0.0, dims[k]) * w / 100 for k, w in WEIGHTS.items()), 2), dims
    except Exception:
        return None

def score_median(key, card, n=3):
    """评分稳定化：评 n 次取中位（规避模型评分噪声波动）。返回 (中位总分, dims)。"""
    vals = []
    for _ in range(n):
        s = score(key, card)
        if s:
            vals.append(s[0])
    if not vals:
        return None
    vals.sort()
    return vals[len(vals) // 2], {}

def main(keys=None):
    todo = keys or list(PERSONAS.keys())
    for rnd in range(1, 4):
        low = []
        for key in todo:
            card = PERSONAS.get(key) or {}
            sc = score(key, card)
            if sc is None:
                continue
            total, dims = sc
            if total < 75:
                card["text"] = enrich(str(card.get("text") or ""))
                low.append((key, round(total, 2)))
        print("第%d轮：<75分 %d 张 %s" % (rnd, len(low), low[:6]), flush=True)
        if not low:
            break
    miss = []
    for key in todo:
        sc = score(key, PERSONAS.get(key) or {})
        if sc and sc[0] < 75:
            miss.append((key, sc[0]))
    print("≥75通过：%d/%d；仍<75：%s" % (len(todo) - len(miss), len(todo), miss), flush=True)

if __name__ == "__main__":
    TEST = ["harry", "wukong", "holmes", "kratos", "natsu", "miku", "simayi", "anna", "lighthouse_keeper", "zelda"]
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        main(TEST)
        from agent.persona import PERSONAS
        import json as _j
        with open(os.path.join(ROOT, "data", "persona_enriched_test.json"), "w", encoding="utf-8") as f:
            _j.dump({k: PERSONAS[k] for k in TEST}, f, ensure_ascii=False, indent=1)
        print("test done")
    else:
        main()
        from agent.persona import PERSONAS
        from agent.config import save_config
        # 回写补足后的 text（仅当有改动）；PERSONAS 是内存 dict，回写文件需按需
        print("全量 done")
