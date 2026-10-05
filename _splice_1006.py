import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('_morning_1006.html', 'r', encoding='utf-8') as f:
    newblock = f.read()

pattern = re.compile(r'<!-- MORNING-START -->.*?<!-- MORNING-END -->', re.DOTALL)
html, n = pattern.subn(newblock, html, count=1)
assert n == 1, f"MORNING region not replaced, n={n}"

# title
assert '<title>宏观政策洞察日报 · 2026-10-05</title>' in html
html = html.replace('<title>宏观政策洞察日报 · 2026-10-05</title>',
                     '<title>宏观政策洞察日报 · 2026-10-06</title>')

# date line
old_date = '2026年10月5日 · 星期一 · 悉尼时间（🌅 早间版 07:30 已更新 · 🌆 晚间版 20:00 待更新）'
assert old_date in html
html = html.replace(old_date,
                    '2026年10月6日 · 星期二 · 悉尼时间（🌅 早间版 07:30 已更新 · 🌆 晚间版 20:00 待更新）')

# full badge (single replace)
old_badge = ('生成时间 2026-10-05 07:30 悉尼时间 · 版本 v2.64'
             '（早间版·周一·非农崩改写剧本&10月加息概率从七成崩两成&长债仍贴5%&美元破101&胡塞袭沙特炼油厂油价反复&人民币强&黄金疲弱&小白解读）')
new_badge = ('生成时间 2026-10-06 07:30 悉尼时间 · 版本 v2.65'
             '（早间版·周二·美元破102&长债再逼5.3%&油价回落至100&金价企稳&人民币强&A股10/8开&小白解读）')
assert old_badge in html, "old badge not found"
html = html.replace(old_badge, new_badge)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# sanity checks
checks = ['2026-10-06', 'v2.65', '小白解读', 'MORNING-START', 'MORNING-END',
          'EVENING-START', 'EVENING-END', 'section class="oz"', 'AUD/USD（澳元）', '0.695',
          '美元破102', '油价回落至百元']
for c in checks:
    if c not in html:
        raise SystemExit(f"MISSING: {c}")

if '2026-10-05' in html:
    print("WARN: '2026-10-05' still present somewhere")
print("OK: morning block replaced and metadata updated; bytes =", len(html.encode('utf-8')))
