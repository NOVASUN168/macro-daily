# -*- coding: utf-8 -*-
import io

p = r"C:/Users/zsgre/macro-daily/index.html"
with io.open(p, encoding="utf-8") as f:
    h = f.read()

# 1) MORNING-START before the morning ver-head
a1 = u'  <div class="ver-head">\n    <span class="vt sun">🌅 早间版</span>'
assert a1 in h, "anchor1 missing"
h = h.replace(a1, u'<!-- MORNING-START -->\n  <div class="ver-head">\n    <span class="vt sun">🌅 早间版</span>', 1)

# 2) MORNING-END + EVENING-START between morning abc </section> and evening ver-head
a2 = (u'  </section>\n\n\n  <div class="ver-head">\n'
      u'    <span class="vt moon">🌆 晚间版</span>')
assert a2 in h, "anchor2 missing"
h = h.replace(a2,
    u'  </section>\n<!-- MORNING-END -->\n\n<!-- EVENING-START -->\n'
    u'  <div class="ver-head">\n    <span class="vt moon">🌆 晚间版</span>', 1)

# 3) EVENING-END before footer
a3 = u'本页链接永久有效，手机浏览器收藏即可天天看最新版。</div>\n\n\n  <footer>'
assert a3 in h, "anchor3 missing"
h = h.replace(a3,
    u'本页链接永久有效，手机浏览器收藏即可天天看最新版。</div>\n<!-- EVENING-END -->\n\n  <footer>', 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(h)

for m in ["MORNING-START","MORNING-END","EVENING-START","EVENING-END"]:
    print(m, h.count("<!-- "+m+" -->"))
print("title 0915:", "2026-09-15" in h and "2026-09-14" not in h)
print("小白解读:", h.count("小白解读"))
