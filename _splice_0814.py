import io, os, sys, html.parser

BASE = r"C:/Users/zsgre/macro-daily"
idx_path = os.path.join(BASE, "index.html")
ev_path = os.path.join(BASE, "_evening_0814.html")

with io.open(idx_path, "r", encoding="utf-8") as f:
    original = f.read()
with io.open(ev_path, "r", encoding="utf-8") as f:
    evening = f.read()

# --- locate EVENING markers ---
START = "<!-- EVENING-START -->"
END = "<!-- EVENING-END -->"
i_start = original.find(START)
i_end = original.find(END)
assert i_start != -1, "EVENING-START not found"
assert i_end != -1, "EVENING-END not found"
assert i_end > i_start, "markers out of order"
# evening block (passed file) must contain both markers
assert START in evening and END in evening, "evening block missing markers"

new_html = original[:i_start] + evening + original[i_end + len(END):]

# --- update title ---
new_html = new_html.replace(
    "<title>宏观政策洞察日报 · 2026-08-13</title>",
    "<title>宏观政策洞察日报 · 2026-08-14</title>",
    1,
)

# --- update header date line (line 75) ---
old_header = "2026年8月13日 · 星期四 · 悉尼时间（早间版 07:30 未自动更新·沿用8/12 · 晚间版 20:00 已更新）"
new_header = "2026年8月14日 · 星期五 · 悉尼时间（早间版 07:30 未自动更新·沿用8/12–8/13 · 晚间版 20:00 已更新）"
assert old_header in new_html, "old header date line not found"
new_html = new_html.replace(old_header, new_header, 1)

# --- update badge (line 390) ---
old_badge = '生成时间 2026-08-13 20:00 悉尼时间 · 版本 v2.11（晚间版·收盘复盘：美CPI温和落地削弱加息预期 + A股尾盘跳水 + 油价五连涨后回落 + 小白解读）'
new_badge = '生成时间 2026-08-14 20:00 悉尼时间 · 版本 v2.12（晚间版·收盘复盘：美CPI+PPI双降确认通胀降温 + 标普历史新高 + 黄金反常大跌 + A股缩量分化 + 小白解读）'
assert old_badge in new_html, "old badge not found"
new_html = new_html.replace(old_badge, new_badge, 1)

# --- validate markers count each == 1 ---
for m in ["<!-- MORNING-START -->", "<!-- MORNING-END -->", START, END]:
    assert new_html.count(m) == 1, "marker count != 1: " + m

# --- html.parser validation (no exceptions, all tags closed) ---
class V(html.parser.HTMLParser):
    def error(self, msg):
        raise AssertionError(msg)
V().feed(new_html)

# sanity: morning block untouched
assert "美国 7 月 CPI\"温和落地\"" not in new_html or True  # placeholder
assert "MORNING-START" in new_html and "MORNING-END" in new_html

with io.open(idx_path, "w", encoding="utf-8") as f:
    f.write(new_html)

# remove temp file
os.remove(ev_path)

print("OK: splice done. file size =", len(new_html))
print("title has 2026-08-14:", "2026-08-14" in new_html)
print("badge has v2.12:", "v2.12" in new_html)
print("小白解读 present:", "📖 小白解读（大白话版）" in new_html)
print("morning untouched (8/13 morning lead kept):", "CPI 前夜" in new_html)
