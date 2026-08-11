# -*- coding: utf-8 -*-
import os, html.parser

PATH = r"C:/Users/zsgre/macro-daily/index.html"
BLOCK = r"C:/Users/zsgre/macro-daily/_evening_block.html"

with open(PATH, "r", encoding="utf-8") as f:
    original = f.read()
with open(BLOCK, "r", encoding="utf-8") as f:
    new_evening = f.read().strip()

# Check markers
for m in ["<!-- MORNING-START -->","<!-- MORNING-END -->","<!-- EVENING-START -->","<!-- EVENING-END -->"]:
    if original.count(m) != 1:
        raise SystemExit(f"MARKER COUNT ERROR: {m} count={original.count(m)}")

# Splice: keep content before EVENING-START and after EVENING-END
before = original.split("<!-- EVENING-START -->", 1)[0]
after  = original.split("<!-- EVENING-END -->", 1)[1]
result = before + "<!-- EVENING-START -->\n" + new_evening + "\n<!-- EVENING-END -->" + after

# Update header date line
result = result.replace(
    "2026年8月11日 · 星期二 · 悉尼时间（早间版）",
    "2026年8月11日 · 星期二 · 悉尼时间（早间版 07:30 已发 · 晚间版 20:00 已更新）"
)

# Update footer badge
result = result.replace(
    '生成时间 2026-08-11 悉尼时间 · 版本 v2.8（早间版·油价掀翻宽松交易 + RBA 决议日 · 含 📖 小白解读）',
    '生成时间 2026-08-11 20:00 悉尼时间 · 版本 v2.9（晚间版·收盘复盘：RBA 按兵4.35% + A股冲高回落 + 明晚美CPI + 小白解读）'
)

# Also ensure footer "每日 07:30 早间版 / 20:00 晚间版" line stays; update badge only.

# Validate HTML well-formedness (tags balance) + marker counts + required content
class V(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.errors=[]
        self.void={'meta','br','hr','img','input','link','area','base','col','embed','source','track','wbr'}
    def handle_starttag(self,t,a):
        if t not in self.void: self.stack.append(t)
    def handle_endtag(self,t):
        if t in self.void: return
        if self.stack and self.stack[-1]==t: self.stack.pop()
        elif t in self.stack:
            while self.stack and self.stack[-1]!=t: self.stack.pop()
            if self.stack: self.stack.pop()
        else: self.errors.append(f"stray </{t}>")
v=V(); v.feed(result)
if v.stack: print("WARN unbalanced open tags remain:", v.stack[:10])
if v.errors: print("WARN end-tag errors:", v.errors[:10])

# Marker re-check after edits
for m in ["<!-- MORNING-START -->","<!-- MORNING-END -->","<!-- EVENING-START -->","<!-- EVENING-END -->"]:
    print(m, "count=", result.count(m))

# Required content checks
checks = {
    "小白解读 present": "小白解读" in result,
    "evening v2.9 badge": "v2.9" in result,
    "RBA 4.35%": "4.35%" in result,
    "ASX 9250.6": "9,250.6" in result,
    "上证 3934.09": "3,934.09" in result,
    "明晚美CPI calendar": "美国 7 月 CPI" in result,
    "header updated": "晚间版 20:00 已更新" in result,
}
for k,val in checks.items():
    print(("OK " if val else "MISSING ")+k)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(result)
print("WROTE", PATH, "bytes=", len(result.encode("utf-8")))

# cleanup temp
try:
    os.remove(BLOCK); print("removed temp block")
except Exception as e:
    print("could not remove temp:", e)
