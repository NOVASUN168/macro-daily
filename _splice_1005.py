import io, sys

base = "C:/Users/zsgre/macro-daily"
html_path = base + "/index.html"
frag_path = base + "/_morning_1005.html"

with io.open(html_path, "r", encoding="utf-8") as f:
    html = f.read()
with io.open(frag_path, "r", encoding="utf-8") as f:
    frag = f.read()

# Validate markers exist and are unique
for marker in ["<!-- MORNING-START -->", "<!-- MORNING-END -->", "<!-- EVENING-START -->", "<!-- EVENING-END -->"]:
    assert html.count(marker) == 1, "marker count != 1: " + marker
assert frag.count("<!-- MORNING-START -->") == 1
assert frag.count("<!-- MORNING-END -->") == 1

ms = html.index("<!-- MORNING-START -->")
me = html.index("<!-- MORNING-END -->") + len("<!-- MORNING-END -->")

new_html = html[:ms] + frag + html[me:]

# Update title / date / badge
new_html = new_html.replace(
    "<title>宏观政策洞察日报 · 2026-10-03</title>",
    "<title>宏观政策洞察日报 · 2026-10-05</title>",
)
new_html = new_html.replace(
    "2026年10月3日 · 星期六 · 悉尼时间（🌅 早间版 07:30 已更新 · 🌆 晚间版 20:00 待更新）",
    "2026年10月5日 · 星期一 · 悉尼时间（🌅 早间版 07:30 已更新 · 🌆 晚间版 20:00 待更新）",
)
new_html = new_html.replace(
    "生成时间 2026-10-03 07:30 悉尼时间 · 版本 v2.63（早间版·周六·长债仍贴5%&RBA加至4.60%&美PCE弱加息预期退烧&9月非农骤降&油价重燃中东派航母&人民币强&黄金回落&小白解读）",
    "生成时间 2026-10-05 07:30 悉尼时间 · 版本 v2.64（早间版·周一·非农崩改写剧本&10月加息概率从七成崩两成&长债仍贴5%&美元破101&胡塞袭沙特炼油厂油价反复&人民币强&黄金疲弱&小白解读）",
)

# Sanity: markers still present exactly once after splice
for marker in ["<!-- MORNING-START -->", "<!-- MORNING-END -->", "<!-- EVENING-START -->", "<!-- EVENING-END -->"]:
    assert new_html.count(marker) == 1, "after-splice marker count != 1: " + marker
assert "📖 小白解读（大白话版）" in new_html
assert "2026-10-05" in new_html
assert "v2.64" in new_html

with io.open(html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("OK written, bytes=", len(new_html.encode("utf-8")))
print("小白解读 count=", new_html.count("📖 小白解读（大白话版）"))
