# -*- coding: utf-8 -*-
"""messeze FAQ 재생성기 — data/faq.json → faq.html 마커(FAQNAV/FAQMAIN) 사이 갱신
실행: python build-faq.py"""
import io, os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "faq.html")
groups = json.load(io.open(os.path.join(ROOT, "data", "faq.json"), encoding="utf-8"))

def nav_html():
    common = [g for g in groups if g["id"].startswith("g-")]
    svc = [g for g in groups if g["id"].startswith("s-")]
    out = ['\n        <p class="fs-lab">공통</p>']
    for g in common:
        out.append(f'        <a href="#{g["id"]}">{g["title"]}<span class="cnt">{len(g["items"])}</span></a>')
    out.append('        <p class="fs-lab" style="margin-top:20px">서비스별</p>')
    for g in svc:
        out.append(f'        <a href="#{g["id"]}">{g["title"]}<span class="cnt">{len(g["items"])}</span></a>')
    return "\n".join(out) + "\n        "

def main_html():
    out = []
    for g in groups:
        qas = "\n".join(
            f'        <div class="qa"><button>{i["q"]}<span class="ico">+</span></button><div class="ans"><p>{i["a"]}</p></div></div>'
            for i in g["items"])
        out.append(f'<div class="faq-group" id="{g["id"]}">\n      <h2 class="fg-title">{g["title"]}</h2>\n      <div class="faq">\n{qas}\n      </div>\n    </div>')
    return "\n    ".join(out)

s = io.open(F, encoding="utf-8").read()
s = re.sub(r'<!--FAQNAV-->.*?<!--/FAQNAV-->', lambda m: '<!--FAQNAV-->' + nav_html() + '<!--/FAQNAV-->', s, flags=re.S)
s = re.sub(r'<!--FAQMAIN-->.*?<!--/FAQMAIN-->', lambda m: '<!--FAQMAIN-->' + main_html() + '<!--/FAQMAIN-->', s, flags=re.S)
io.open(F, "w", encoding="utf-8").write(s)
print("OK: faq.html -", len(groups), "groups,", sum(len(g["items"]) for g in groups), "items")
