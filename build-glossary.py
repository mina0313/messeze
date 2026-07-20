# -*- coding: utf-8 -*-
"""messeze SEO·AEO·GEO·PR 용어사전 생성기 (rinda /glossary + next-t /seo/glossary 통합형)
실행: python build-glossary.py  →  glossary/index.html + glossary/terms/*.html"""
import os, json, io

ROOT = os.path.dirname(os.path.abspath(__file__))
TERMS_DIR = os.path.join(ROOT, "glossary", "terms")
os.makedirs(TERMS_DIR, exist_ok=True)

CSS = """
:root{--ink:#0A1930;--navy:#101F3F;--body:#4A5568;--mut:#8B95A7;--cobalt:#2B5CFF;--cobalt-dk:#1E46D9;
--sky:#EAF1FF;--sky-2:#F5F8FD;--mint:#0BBF8C;--line:#E5EAF2;--line-2:#D8E0EC;
--sans:'Pretendard',system-ui,-apple-system,sans-serif;--disp:'Poppins',var(--sans);--maxw:1140px;
--sh-sm:0 1px 2px rgba(10,25,48,.05),0 4px 14px rgba(10,25,48,.05);--sh:0 12px 34px rgba(16,31,63,.10)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--ink);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
h1,h2,h3,h4{font-weight:800;letter-spacing:-.03em;line-height:1.3;word-break:keep-all}
.co{color:var(--cobalt)}
.nav{position:sticky;top:0;z-index:70;background:rgba(255,255,255,.88);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;height:72px;gap:40px}
.brand{display:flex;align-items:center;gap:9px}
.brand svg{width:25px;height:25px}
.brand .bw{font-family:var(--disp);font-weight:600;font-size:21px;letter-spacing:-.025em}
.nav-menu{display:flex;gap:6px;font-size:15px;font-weight:600;color:var(--body)}
.nav-menu a{padding:9px 13px;border-radius:10px}
.nav-menu a:hover{background:var(--sky-2);color:var(--ink)}
.nav-menu a.on{color:var(--cobalt)}
.nav-r{margin-left:auto}
.nav-cta{font-weight:700;font-size:14.5px;background:var(--ink);color:#fff;padding:12px 20px;border-radius:12px;transition:.18s}
.nav-cta:hover{background:var(--cobalt)}
.nav-burger{display:none;background:none;border:0;cursor:pointer;padding:10px 4px 10px 10px;flex:0 0 auto}
.nav-burger span{display:block;width:22px;height:2.5px;background:var(--ink);border-radius:2px;margin:4.5px 0;transition:.22s}
.nav-burger.on span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-burger.on span:nth-child(2){opacity:0}
.nav-burger.on span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.foot{background:#070D1C;color:#7C879D;padding:52px 0 38px}
.foot-in{display:flex;justify-content:space-between;gap:36px;flex-wrap:wrap}
.foot .brand{color:#fff;margin-bottom:14px}
.foot p{font-size:13.5px;line-height:1.7;max-width:320px}
.foot-b{margin-top:38px;padding-top:22px;border-top:1px solid #141C30;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:12.5px;color:#4E5A73}
.cta-band{background:var(--ink);border-radius:24px;padding:46px 40px;display:flex;justify-content:space-between;align-items:center;gap:26px;flex-wrap:wrap;color:#fff;position:relative;overflow:hidden;margin:70px auto}
.cta-band::before{content:"";position:absolute;inset:0;background:radial-gradient(520px 280px at 90% 100%,rgba(43,92,255,.4),transparent 60%)}
.cta-band h3{font-size:clamp(20px,2.6vw,27px);color:#fff;position:relative}
.cta-band p{color:#AEB9D2;font-size:14.5px;margin-top:8px;position:relative}
.cta-band .btn{position:relative;background:var(--cobalt);color:#fff;font-weight:700;font-size:15px;padding:15px 26px;border-radius:14px;display:inline-flex;transition:.18s}
.cta-band .btn:hover{background:#4270FF}
.mega{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 30px 60px rgba(16,31,63,.14);opacity:0;visibility:hidden;transform:translateY(-8px);transition:.22s;padding:32px 0 36px;z-index:80}
.mega.on{opacity:1;visibility:visible;transform:none}
.mega-in{display:grid;grid-template-columns:225px 1fr 1fr 1fr;gap:36px;align-items:stretch}
.mega-brand{background:linear-gradient(160deg,#101F3F,#2B5CFF);border-radius:18px;padding:24px 22px;display:flex;flex-direction:column;justify-content:flex-end;min-height:225px;color:#fff;transition:.2s}
.mega-brand:hover{transform:translateY(-3px)}
.mega-brand .bw2{font-family:var(--disp);font-weight:600;font-size:22px}
.mega-brand p{font-size:12.5px;color:#C7D6FF;margin-top:8px;line-height:1.55;font-weight:600}
.mega-col h5{font-size:11.5px;color:var(--mut);font-weight:800;letter-spacing:.05em;margin:0 0 8px 12px}
.mega-col .gap{height:20px}
.mega-col a{display:block;padding:9px 12px;border-radius:12px;transition:.15s}
.mega-col a b{font-size:14.2px;display:block;letter-spacing:-.01em}
.mega-col a span{font-size:12.2px;color:var(--mut);display:block;margin-top:1px}
.mega-col a:hover{background:var(--sky-2)}
.mega-col a:hover b{color:var(--cobalt)}
@media(max-width:900px){.nav-menu{display:none}.nav-burger{display:block}.mega{max-height:calc(100vh - 72px);overflow:auto}.mega-in{grid-template-columns:1fr;gap:18px}.mega-brand{min-height:auto;padding:18px 20px}}
"""

def mega(p):
    return f"""<div class="mega" id="mega"><div class="wrap mega-in">
<a class="mega-brand" href="{p}index.html"><span class="bw2">messeze</span><p>사람에게만 보이는 홍보에서,<br>AI가 읽는 홍보로</p></a>
<div class="mega-col"><h5>서비스</h5>
<a href="{p}services.html"><b style="color:var(--cobalt)">서비스 전체 보기 →</b><span>6가지 서비스를 한눈에</span></a>
<a href="{p}services/visibility.html"><b>AI 가시성 평가</b><span>AI가 우리 회사를 아는지부터</span></a>
<a href="{p}services/website-renewal.html"><b>홈페이지 수정·리뉴얼</b><span>AI가 읽는 구조로 정비</span></a>
<a href="{p}services/website-build.html"><b>홈페이지 제작</b><span>질문이 페이지가 되는 설계</span></a>
<a href="{p}services/own-blog.html"><b>자사 블로그 운영</b><span>도메인에 쌓이는 전문성</span></a>
<a href="{p}services/channels.html"><b>외부 채널 운영</b><span>네이버·티스토리·구글 블로거</span></a>
<a href="{p}services/press.html"><b>언론 배포</b><span>기자 매칭 · 보도자료 · 기사화</span></a></div>
<div class="mega-col"><h5>무료 도구</h5>
<a href="{p}check.html"><b>AI 가시성 진단</b><span>URL만 넣으면 30초 진단</span></a>
<a href="{p}tools.html#home"><b>홈페이지 건강검진</b><span>6가지 체크로 점수 확인</span></a>
<a href="{p}tools.html#seo"><b>SEO 점수 확인</b><span>검색 기본기 자가 점검</span></a>
<a href="{p}tools.html#pr"><b>PR 플랜 추천</b><span>3가지 질문으로 플랜 찾기</span></a>
<a href="{p}tools.html#blog"><b>블로그 운영 진단</b><span>AI 신뢰 구조인지 진단</span></a>
<div class="gap"></div><h5>요금</h5>
<a href="{p}pricing.html"><b>플랜 비교</b><span>소상공인형 · 기업형 · 엔터프라이즈</span></a>
<a href="{p}pricing.html#faq"><b>요금 FAQ</b><span>약정 · 수량 · 바우처 연계</span></a></div>
<div class="mega-col"><h5>리소스</h5>
<a href="{p}blog/index.html"><b>블로그</b><span>AI 검색 시대의 홍보 인사이트</span></a>
<a href="{p}glossary/index.html"><b>용어사전</b><span>SEO·AEO·GEO·PR 용어 35개</span></a>
<div class="gap"></div><h5>많이 읽는 글</h5>
<a href="{p}blog/posts/aeo-geo-seo.html"><b>AEO·GEO·SEO 차이</b><span>세 가지 최적화 쉽게 정리</span></a>
<a href="{p}blog/posts/manufacturer-case.html"><b>제조기업 3개월 시나리오</b><span>AI에 발견되기까지</span></a></div>
</div></div>"""

MEGA_JS = """<script>
(function(){const p=document.getElementById('mega'),t=document.querySelector('.nav-menu'),b=document.getElementById('burger');if(!p)return;let m;const o=()=>{clearTimeout(m);p.classList.add('on')},c=()=>{m=setTimeout(()=>p.classList.remove('on'),140)};if(t){t.addEventListener('mouseenter',o);t.addEventListener('mouseleave',c);t.querySelectorAll('a').forEach(a=>a.addEventListener('mouseenter',o));}if(window.matchMedia('(hover:hover)').matches){p.addEventListener('mouseenter',o);p.addEventListener('mouseleave',c);}if(b){b.addEventListener('click',()=>{const on=p.classList.toggle('on');b.classList.toggle('on',on);});p.addEventListener('click',e=>{if(e.target.closest('a')){p.classList.remove('on');b.classList.remove('on');}});}})();
</script>"""

LOGO = """<svg viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4H23a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H14l-4 4.5V22H7a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3Z"/><line x1="9.5" y1="10" x2="20.5" y2="10"/><line x1="9.5" y1="13.5" x2="20.5" y2="13.5"/><line x1="9.5" y1="17" x2="16.5" y2="17"/></svg>"""

FONT_LINKS = """<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">"""

def nav(depth, on="glossary"):
    p = "../" * depth
    return f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="{p}index.html">{LOGO}<span class="bw">messeze</span></a>
<nav class="nav-menu">
<a href="{p}services.html">서비스</a>
<a href="{p}pricing.html">요금</a>
<a href="{p}check.html">AI 가시성 체크</a>
<a href="{p}blog/index.html">블로그</a>
<a class="on" href="{p}glossary/index.html">용어사전</a>
<a href="{p}faq.html">FAQ</a>
</nav>
<div class="nav-r"><a class="nav-cta" href="{p}index.html#final">무료 진단 받기</a></div>
<button class="nav-burger" id="burger" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
</div>
{mega(p)}
</header>
{MEGA_JS}"""

def foot(depth):
    p = "../" * depth
    return f"""<footer class="foot"><div class="wrap"><div class="foot-in">
<div><a class="brand" href="{p}index.html">{LOGO}<span class="bw">messeze</span></a>
<p>기업의 정보를 언론과 AI 검색에 지속적으로 축적하는 구독형 기업 PR 서비스.</p></div>
</div><div class="foot-b"><span>© 2026 messeze</span><span>사람에게만 보이는 홍보에서, AI가 읽는 홍보로</span></div></div></footer>"""

def cta(depth):
    p = "../" * depth
    return f"""<div class="wrap"><div class="cta-band">
<div><h3>용어는 알겠는데, 실행할 사람이 없다면?</h3><p>진단부터 콘텐츠·언론 축적까지 — messeze 전담팀이 매달 대신 실행합니다.</p></div>
<a class="btn" href="{p}index.html#final">무료 진단 신청하기</a></div></div>"""

# ---------------- 카테고리 ----------------
CATS = [
    ("basic",  "기초 개념",      "검색과 노출을 이해하는 출발점"),
    ("ai",     "AI 검색 시대",   "AI가 답을 만드는 새 검색 환경"),
    ("onpage", "콘텐츠·온페이지","페이지 안에서 하는 최적화"),
    ("trust",  "신뢰·권위",      "외부에서 쌓이는 신뢰 신호"),
    ("pr",     "언론홍보·PR",    "언론을 통한 신뢰 출처 만들기"),
]

# ---------------- 용어 33개 ----------------
T = []
def t(slug,cat,ko,en,short,paras,why,rel):
    T.append(dict(slug=slug,cat=cat,ko=ko,en=en,short=short,paras=paras,why=why,rel=rel))

# ===== 기초 개념 =====
t("seo","basic","SEO (검색엔진최적화)","Search Engine Optimization",
"구글·네이버 같은 검색엔진의 자연 검색 결과에서 더 잘 노출되도록 사이트의 콘텐츠·구조·신뢰를 최적화하는 활동.",
["광고비를 내고 상단에 오르는 검색광고와 달리, SEO는 검색엔진이 '이 페이지가 이 질문에 가장 좋은 답'이라고 판단하게 만드는 작업입니다. 콘텐츠 품질, 페이지 구조, 기술 상태, 외부 신뢰(백링크) 등 수많은 신호가 종합적으로 평가됩니다.",
"한 번 순위에 오르면 광고처럼 예산이 끊겨도 노출이 유지되는 것이 가장 큰 장점입니다. 다만 효과가 나기까지 시간이 걸리는 누적형 작업이라, 일회성 이벤트가 아니라 꾸준한 운영이 필요합니다."],
"AI 검색(AEO·GEO)도 결국 SEO로 다져진 기본기 위에서 작동합니다. 기본기 없이 AI 노출은 없습니다.",
["aeo","geo","serp"])

t("serp","basic","SERP (검색 결과 페이지)","Search Engine Results Page",
"검색어를 입력했을 때 나오는 결과 화면 전체. 링크뿐 아니라 광고·지도·이미지·AI 요약까지 포함한다.",
["과거의 SERP는 '파란 링크 10개'였지만, 지금은 광고, 지식패널, 뉴스 묶음, 동영상, 그리고 화면 최상단의 AI 요약(AI Overview)까지 다양한 블록으로 구성됩니다. 같은 1위라도 어떤 블록 아래에 있느냐에 따라 실제 클릭은 크게 달라집니다.",
"기업 입장에서는 '몇 위인가'보다 'SERP의 어떤 요소로 등장하는가'가 중요해졌습니다. 뉴스 기사로, 지식패널로, AI 요약의 인용 출처로 — 등장 형태가 다양할수록 신뢰가 쌓입니다."],
"messeze는 기사·콘텐츠·구조화 데이터를 함께 축적해 SERP의 여러 블록에 동시에 등장하는 것을 목표로 합니다.",
["seo","ai-overview","citation"])

t("search-intent","basic","검색 의도","Search Intent",
"검색어 뒤에 숨은 사용자의 진짜 목적. 정보 탐색인지, 구매 검토인지에 따라 필요한 콘텐츠가 달라진다.",
["'정밀부품'을 검색한 사람과 '정밀부품 소량 제작 업체'를 검색한 사람은 전혀 다른 단계에 있습니다. 전자는 공부 중이고, 후자는 발주처를 찾고 있죠. 검색 의도를 읽지 못한 콘텐츠는 노출돼도 전환되지 않습니다.",
"AI 검색 시대에는 의도가 '질문 문장'으로 더 명확하게 드러납니다. \"소량 생산 가능한 국내 제조사는 어디야?\" 같은 질문 자체가 곧 의도입니다. 그래서 질문을 설계하고 그에 답하는 콘텐츠를 만드는 것이 핵심 전략이 됩니다."],
"messeze 온보딩의 첫 단계가 바로 '고객이 AI에게 물어볼 핵심 질문 5~6개 설계'입니다.",
["keyword","aeo","faq-schema"])

t("keyword","basic","키워드","Keyword",
"사용자가 검색창에 입력하는 단어나 구. 어떤 키워드를 노릴지 정하는 것이 검색 마케팅의 출발점이다.",
["키워드에는 검색량(얼마나 많이 찾는가)과 경쟁도(얼마나 많은 페이지가 노리는가)가 있습니다. 검색량이 큰 키워드는 매력적이지만 경쟁이 치열하고, 길고 구체적인 '롱테일 키워드'는 검색량은 적어도 전환율이 높습니다.",
"B2B·제조 업종은 애초에 검색량이 적어 키워드 중심 전략이 잘 통하지 않았습니다. 하지만 AI 검색에서는 검색량이 아니라 '그 주제에 대해 신뢰할 수 있는 정보가 있는가'가 기준이라, 검색량 없는 분야일수록 먼저 정보를 쌓은 기업이 유리합니다."],
"검색량이 없어서 포기했던 업종이야말로 messeze가 가장 잘 돕는 영역입니다.",
["search-intent","seo","geo"])

t("crawling-indexing","basic","크롤링·색인","Crawling · Indexing",
"검색엔진 봇이 페이지를 발견·수집(크롤링)하고 검색 가능하게 저장(색인)하는 과정. 색인되지 않으면 검색에 뜨지 않는다.",
["크롤러(봇)는 링크를 따라다니며 페이지를 수집하고, 수집된 내용은 정리되어 거대한 색인(인덱스)에 저장됩니다. 검색 결과는 이 색인에서 나옵니다. 아무리 좋은 페이지도 크롤링되지 않거나 색인에서 빠지면 존재하지 않는 것과 같습니다.",
"robots.txt로 크롤러의 접근을 안내하고, 사이트맵으로 중요한 페이지 목록을 알려주는 것이 기본기입니다. 최근에는 GPTBot 같은 AI 크롤러의 수집 허용 여부도 함께 점검해야 합니다."],
"messeze의 AI 가시성 진단은 검색엔진 크롤러와 AI 크롤러 모두의 관점에서 사이트를 점검합니다.",
["ai-crawler","structured-data","seo"])

# ===== AI 검색 시대 =====
t("aeo","ai","AEO (답변엔진 최적화)","Answer Engine Optimization",
"ChatGPT·Gemini 같은 AI가 사용자의 질문에 답할 때 우리 기업의 정보를 인용하도록 만드는 최적화.",
["검색엔진이 '링크 목록'을 보여준다면, 답변엔진(Answer Engine)은 '하나의 답'을 만들어 줍니다. AEO는 그 답 안에 우리 기업이 등장하도록 만드는 작업입니다. 질문에 정면으로 답하는 콘텐츠, 명확한 문서 구조, 신뢰할 수 있는 여러 출처가 핵심 재료입니다.",
"기존 SEO가 '키워드에 대한 순위 경쟁'이라면, AEO는 '질문에 대한 인용 경쟁'입니다. 고객이 실제로 물어볼 질문을 먼저 정의하고, 그 질문의 가장 좋은 답이 되는 것 — 이것이 AEO의 본질입니다."],
"messeze의 질문 설계 → 콘텐츠 제작 → 출처 축적 사이클이 곧 AEO 실행 과정입니다.",
["geo","citation","faq-schema"])

t("geo","ai","GEO (생성형엔진 최적화)","Generative Engine Optimization",
"생성형 AI 기반 검색 전반에서 기업·브랜드가 발견되고 추천되도록 만드는 전략. AEO를 포함하는 더 넓은 개념.",
["GEO는 개별 질문에 대한 답변 인용(AEO)을 넘어, AI가 우리 기업이라는 '존재' 자체를 정확히 이해하게 만드는 전략입니다. 구조화 데이터로 기업 정보를 선언하고, 언론·외부 채널에 일관된 정보를 축적하고, 엔티티 간 연결을 만들어 AI의 지식 속에 기업을 자리 잡게 합니다.",
"GEO에서는 키워드 포함보다 브랜드·서비스·콘텐츠 간의 엔티티 연결성이 중요합니다. 한 곳에서만 확인되는 정보보다, 여러 신뢰 출처에서 교차 확인되는 정보가 훨씬 강합니다."],
"messeze가 '기업 정보 자산 축적'을 강조하는 이유가 바로 GEO입니다. 축적된 자산이 AI의 기억이 됩니다.",
["aeo","entity","knowledge-graph"])

t("ai-search","ai","AI 검색","AI Search",
"사용자가 키워드가 아닌 질문을 던지고, AI가 여러 출처를 종합해 하나의 답으로 응답하는 검색 방식.",
["ChatGPT, Gemini, Perplexity, 그리고 구글의 AI Overview까지 — 검색의 기본 형태가 '링크 나열'에서 'AI가 만든 답'으로 이동하고 있습니다. 사용자는 더 이상 여러 사이트를 열어 비교하지 않고, AI의 답과 그 인용 출처를 확인합니다.",
"이 변화의 의미는 명확합니다. AI의 답에 등장하지 못하는 기업은 비교 대상에조차 오르지 못한다는 것. 반대로 검색량이 적은 분야에서는 정보를 먼저 쌓은 기업이 그 분야의 '기본 답'이 될 수 있습니다."],
"messeze는 주요 AI 검색에서 기업이 어떻게 인식되는지 진단하는 것부터 시작합니다.",
["ai-overview","aeo","llm"])

t("ai-overview","ai","AI 오버뷰","AI Overview (Google)",
"구글 검색 결과 최상단에 AI가 생성한 요약 답변을 보여주는 기능. 여러 출처를 인용해 답을 구성한다.",
["구글은 검색 결과 위에 AI가 만든 요약을 배치하기 시작했습니다. 사용자 상당수가 이 요약만 읽고 검색을 끝내기 때문에, 요약에 인용되는 것과 아닌 것의 차이가 급격히 커지고 있습니다.",
"AI 오버뷰는 신뢰할 수 있다고 판단한 출처들에서 내용을 가져옵니다. 잘 구조화된 콘텐츠, 질문에 명확히 답하는 문단, 권위 있는 발행 주체 — 인용되는 페이지들의 공통점입니다."],
"네이버 검색과 구글 AI 오버뷰 노출 여부는 messeze 월간 리포트의 기본 점검 항목입니다.",
["ai-search","serp","citation"])

t("llm","ai","LLM (대규모 언어모델)","Large Language Model",
"방대한 텍스트로 학습해 사람처럼 글을 이해하고 생성하는 AI 모델. ChatGPT·Gemini의 두뇌에 해당한다.",
["LLM은 학습 데이터와 실시간 검색(브라우징)을 조합해 답을 만듭니다. 학습 데이터에 우리 기업 정보가 충분히 존재하고, 검색으로도 신뢰할 수 있는 출처가 확인되면, AI는 우리 기업을 '아는 상태'로 답하게 됩니다.",
"LLM은 확률적으로 문장을 생성하기 때문에, 정보가 부족한 기업에 대해서는 아예 언급하지 않거나 부정확하게 답할 수 있습니다. 잘못된 정보가 퍼지기 전에 정확한 정보를 여러 출처에 심어두는 것이 중요한 이유입니다."],
"AI가 우리 회사를 '모르는' 상태에서 '정확히 아는' 상태로 — 그 간극을 메우는 것이 messeze의 일입니다.",
["ai-search","knowledge-graph","entity"])

t("ai-crawler","ai","AI 크롤러","AI Crawler (GPTBot 등)",
"AI 기업이 학습·답변 생성을 위해 웹을 수집하는 봇. GPTBot(OpenAI), Google-Extended 등이 있다.",
["검색엔진 크롤러처럼 AI 크롤러도 웹을 돌며 콘텐츠를 수집합니다. robots.txt에서 이들을 차단하면 AI의 학습과 답변 참고 대상에서 빠질 수 있습니다. 보호할 콘텐츠와 알려야 할 콘텐츠를 구분하는 정책이 필요합니다.",
"AI 크롤러는 자바스크립트를 실행하지 않는 경우가 많아, 서버가 응답하는 HTML에 핵심 정보가 있어야 합니다. 화면에는 보이는데 HTML 원문에는 없는 정보는 AI에게 존재하지 않는 정보입니다."],
"messeze의 AI 가시성 체크는 'AI 크롤러가 보는 조건'으로 사이트를 분석합니다.",
["crawling-indexing","structured-data","geo"])

t("citation","ai","인용 (출처 표기)","Citation",
"AI가 답변을 만들 때 근거로 삼은 출처를 표시하는 것. 인용에 포함되는 것이 AI 시대의 새로운 '상위 노출'이다.",
["Perplexity나 구글 AI 오버뷰는 답변 옆에 출처 링크를 표시합니다. 사용자는 이 출처를 신뢰의 근거로 받아들이죠. 우리 기업 관련 질문에서 우리 홈페이지·기사가 인용 목록에 있는 것 — 그것이 AI 시대의 핵심 성과 지표입니다.",
"인용되기 위해서는 첫째 질문에 명확히 답하는 콘텐츠, 둘째 발행 주체가 분명한 페이지, 셋째 다른 출처와 교차 검증되는 사실이 필요합니다. 언론 기사가 특히 강력한 인용 출처가 되는 이유는 제3자의 검증을 거친 정보이기 때문입니다."],
"messeze 리포트는 '어떤 질문에서, 어떤 출처가 인용됐는지'를 추적합니다.",
["aeo","ai-overview","press-release"])

t("entity","ai","엔티티","Entity",
"검색엔진과 AI가 인식하는 '실체' — 기업, 사람, 제품, 장소처럼 고유하게 식별되는 대상.",
["기계에게 '메세지'라는 글자는 그냥 단어지만, '기업 PR 서비스를 운영하는 회사 messeze'는 엔티티입니다. 엔티티로 인식되면 AI는 흩어진 정보들(홈페이지·기사·SNS)을 하나의 실체로 연결해 이해합니다.",
"구조화 데이터(JSON-LD)로 기업을 Organization 엔티티로 선언하고, @id와 sameAs로 다른 정보들과 연결하면, AI가 기업을 정확히 식별할 수 있게 됩니다. 엔티티 인식이 안 된 기업은 AI에게 '누군지 모르는 이름'일 뿐입니다."],
"messeze의 홈페이지 최적화는 기업을 명확한 엔티티로 선언하는 것에서 시작합니다.",
["knowledge-graph","structured-data","sameas"])

t("knowledge-graph","ai","지식그래프","Knowledge Graph",
"엔티티들과 그 관계를 그물처럼 연결해 저장한 지식 데이터베이스. 검색엔진과 AI가 세상을 이해하는 뼈대.",
["구글 검색에서 기업명을 쳤을 때 오른쪽에 뜨는 정보 패널이 지식그래프의 대표적인 얼굴입니다. '이 회사는 무엇을 하고, 어디에 있고, 무엇과 관련 있는지'가 관계망으로 저장되어 있습니다.",
"지식그래프에 올바르게 등재된 기업은 AI 답변에서도 정확하게 다뤄집니다. 등재를 위해서는 위키·언론·공식 홈페이지 등 신뢰 출처들의 일관된 정보가 필요합니다. 출처마다 회사 소개가 다르면 기계는 확신하지 못합니다."],
"여러 출처에 '같은 이야기'를 축적하는 messeze의 방식이 지식그래프 등재의 지름길입니다.",
["entity","sameas","llm"])

# ===== 콘텐츠·온페이지 =====
t("title-tag","onpage","타이틀 태그","Title Tag",
"페이지 제목을 정의하는 HTML 태그. 검색 결과의 파란 제목으로 표시되는, 온페이지 최적화의 최우선 요소.",
["<title>은 검색엔진이 페이지 주제를 파악하는 첫 신호이자, 사용자가 클릭을 결정하는 첫 문장입니다. 핵심 키워드를 앞쪽에 담되, 사람이 읽고 싶어지는 문장이어야 합니다. 페이지당 1개, 15~60자 안팎이 권장됩니다.",
"모든 페이지가 같은 타이틀을 쓰는 사이트가 의외로 많습니다. 이 경우 검색엔진은 페이지들을 구분하지 못하고, 어떤 페이지도 특정 주제의 답으로 선택받기 어려워집니다."],
"messeze 진단의 첫 체크 항목입니다 — 의외로 여기서부터 막힌 기업이 많습니다.",
["meta-description","heading-structure","seo"])

t("meta-description","onpage","메타 디스크립션","Meta Description",
"페이지 내용을 요약하는 메타 태그. 검색 결과 제목 아래 설명문으로 쓰여 클릭률에 영향을 준다.",
["직접적인 순위 요소는 아니지만, 검색 결과에서 '왜 이 페이지를 클릭해야 하는지'를 설득하는 광고 카피 역할을 합니다. 페이지마다 고유하게, 검색 의도에 맞는 핵심을 80~160자로 담는 것이 좋습니다.",
"AI 검색에서도 디스크립션은 페이지 내용을 빠르게 파악하는 요약 정보로 활용됩니다. 비어 있으면 AI와 검색엔진이 본문에서 임의로 발췌하는데, 그 결과가 기업이 원하는 메시지와 다를 수 있습니다."],
"기업이 하고 싶은 말을 한 문장으로 정리하는 것 — messeze 콘텐츠 작업의 기본기입니다.",
["title-tag","serp","aeo"])

t("heading-structure","onpage","헤딩 구조 (H1–H6)","Heading Structure",
"H1~H6 태그로 문서의 제목·소제목 위계를 표현하는 것. 사람과 기계 모두에게 글의 구조를 알려준다.",
["H1은 문서의 대표 제목(페이지당 1개), H2는 큰 단락, H3는 그 하위 — 이렇게 계층을 지키면 검색엔진과 AI가 문서의 뼈대를 즉시 파악합니다. 디자인 때문에 H1을 건너뛰고 H3부터 쓰는 사이트는 기계에게 구조가 무너진 문서로 보입니다.",
"AI는 특히 헤딩을 기준으로 내용을 발췌·인용합니다. '질문형 H2 + 명확한 답변 문단' 구조가 AI 인용에 유리한 이유입니다."],
"messeze의 AEO형 칼럼이 질문형 소제목 구조로 작성되는 이유입니다.",
["title-tag","faq-schema","aeo"])

t("alt-text","onpage","이미지 대체텍스트","Image Alt Text",
"이미지 내용을 글로 설명하는 alt 속성. 검색엔진·AI·스크린리더가 이미지를 이해하는 유일한 통로.",
["기계는 이미지를 '보지' 못합니다. alt=\"항공용 정밀부품 CNC 가공 현장\"이라는 설명이 있어야 그 이미지가 무엇인지 압니다. 이미지 검색 노출, 시각장애인 접근성, AI의 페이지 이해 모두 alt에서 출발합니다.",
"제조기업 홈페이지는 설비·제품 사진이 많은데 alt가 비어 있는 경우가 대부분입니다. 사진마다 제품명·공정명을 담은 alt만 채워도 기계가 읽는 정보량이 크게 늘어납니다."],
"messeze 홈페이지 최적화 항목 중 가장 빠르게 효과 보는 작업입니다.",
["heading-structure","crawling-indexing","seo"])

t("structured-data","onpage","구조화 데이터 (스키마)","Structured Data · Schema.org",
"페이지 내용을 기계가 이해하는 형식으로 표기하는 것. AI와 검색엔진의 엔티티 인식을 돕는 핵심 장치.",
["'우리는 정밀부품 제조사입니다'라는 문장은 사람용입니다. 기계용으로는 schema.org 어휘에 따라 '이 페이지의 발행 주체는 Organization이고, 이름은 ○○정밀이며, 업종은 제조업'이라고 선언해야 합니다. 주로 JSON-LD 형식을 씁니다.",
"구조화 데이터가 있으면 검색 결과에 별점·FAQ 같은 리치 결과로 표시될 자격이 생기고, AI는 페이지의 주체와 성격을 확신을 갖고 인용할 수 있게 됩니다."],
"messeze AI 가시성 체크의 'AI 준비도 50점' 중 30점이 구조화 데이터 항목입니다.",
["json-ld","entity","faq-schema"])

t("json-ld","onpage","JSON-LD","JSON for Linking Data",
"구조화 데이터를 표기하는 대표 형식. HTML 안에 스크립트 블록으로 삽입하며 구글이 공식 권장한다.",
["JSON-LD는 본문 HTML을 건드리지 않고 <script type=\"application/ld+json\"> 블록 하나로 기업·서비스·콘텐츠 정보를 선언할 수 있어 관리가 쉽습니다. Organization, WebSite, Article, FAQPage 등 페이지 성격에 맞는 타입을 조합합니다.",
"중요한 것은 문법 유효성과 연결성입니다. JSON 문법이 깨져 있으면 없는 것과 같고, @id로 엔티티끼리 연결하고 sameAs로 외부 프로필을 이어야 AI가 관계를 읽습니다."],
"messeze가 관리하는 홈페이지에는 검증된 JSON-LD가 기본 탑재됩니다.",
["structured-data","entity","sameas"])

t("canonical","onpage","캐노니컬 (정규 URL)","Canonical URL",
"같은 내용이 여러 주소에 있을 때 '이것이 대표 주소'라고 지정하는 태그. 평가 분산을 막는다.",
["www가 붙은 주소와 안 붙은 주소, 파라미터가 붙은 주소 — 같은 페이지가 여러 URL로 접근되면 검색엔진은 어떤 것을 대표로 삼을지 혼란스러워하고, 평가가 나뉩니다. canonical 태그로 대표를 지정하면 신호가 한 곳으로 모입니다.",
"콘텐츠를 여러 채널에 발행하는 전략을 쓸 때도 원본 표시가 중요합니다. 원본이 명확해야 검색엔진과 AI가 '출처의 원류'를 올바르게 인식합니다."],
"외부 채널 발행이 많은 messeze 운영에서 원본 관리의 기본 장치입니다.",
["crawling-indexing","structured-data","seo"])

t("faq-schema","onpage","FAQ 스키마","FAQPage Schema",
"자주 묻는 질문과 답변을 구조화 데이터로 선언하는 것. 질문-답변 쌍은 AI가 가장 인용하기 좋은 형태다.",
["FAQPage 스키마를 적용하면 '이 페이지에는 이런 질문과 이런 답이 있다'는 것을 기계가 명시적으로 알게 됩니다. 검색 결과에 질문·답변이 펼쳐지는 리치 결과 자격도 생깁니다.",
"AI 답변 엔진의 작동 방식이 곧 '질문에 답하기'이므로, 질문-답변 형태로 정리된 콘텐츠는 그 자체로 인용 후보가 됩니다. 고객 상담에서 반복되는 질문들을 FAQ로 정리하는 것부터 시작하세요."],
"messeze의 질문 설계 결과물이 바로 이 FAQ 콘텐츠와 스키마로 구현됩니다.",
["structured-data","aeo","search-intent"])

# ===== 신뢰·권위 =====
t("backlink","trust","백링크","Backlink",
"다른 사이트가 우리 페이지로 거는 링크. 검색엔진이 '추천'으로 해석하는 핵심 권위 신호.",
["논문이 많이 인용될수록 권위를 인정받듯, 신뢰할 수 있는 사이트들이 링크로 참조하는 페이지는 검색엔진에게 좋은 평가를 받습니다. 링크의 수보다 어떤 사이트가 걸었는지(질)가 중요합니다.",
"언론사 기사에서 걸리는 링크는 가장 얻기 어렵지만 가장 강력한 백링크에 속합니다. 보도자료가 기사화되면 노출 효과와 함께 권위 신호까지 얻는 셈입니다."],
"messeze의 언론 배포는 노출과 동시에 신뢰 링크 자산을 만드는 작업입니다.",
["domain-authority","press-release","eeat"])

t("eeat","trust","E-E-A-T","Experience · Expertise · Authoritativeness · Trustworthiness",
"경험·전문성·권위·신뢰 — 구글이 콘텐츠 품질을 평가하는 네 가지 관점.",
["같은 내용이라도 '누가 말했는가'에 따라 가치가 다릅니다. 실제 경험이 있는가, 전문성이 입증되는가, 업계에서 인정받는가, 믿을 수 있는가 — 구글은 이 네 축으로 콘텐츠와 발행 주체를 평가합니다.",
"기업이 E-E-A-T를 쌓는 방법은 명확합니다. 실제 실적과 사례를 콘텐츠로 남기고, 전문 분야의 글을 꾸준히 발행하고, 언론·외부 채널에서 언급되게 만드는 것. 하루아침에 안 되지만, 쌓이면 쉽게 무너지지 않습니다."],
"messeze의 '기업 정보 자산 축적'은 E-E-A-T를 기업 단위로 쌓는 작업입니다.",
["backlink","brand-mention","press-release"])

t("domain-authority","trust","도메인 권위","Domain Authority",
"한 도메인이 쌓아온 전반적 신뢰·권위의 정도. 새 콘텐츠의 초기 평가에도 영향을 준다.",
["오래 운영되며 좋은 콘텐츠와 백링크를 쌓은 도메인은 새 글을 올려도 빠르게 좋은 평가를 받습니다. 반대로 신생 도메인은 같은 품질이라도 신뢰를 얻기까지 시간이 걸립니다.",
"구글의 공식 지표는 아니고 업계 도구들이 추정하는 점수지만, '도메인 단위의 신뢰가 존재한다'는 개념 자체는 실무에서 유효합니다. 권위 있는 도메인(언론사 등)에 실리는 것이 효과적인 이유이기도 합니다."],
"자체 도메인 권위가 낮은 초기 기업일수록 언론 기사를 통한 신뢰 확보가 효율적입니다.",
["backlink","eeat","newswire"])

t("sameas","trust","sameAs (외부 프로필 연결)","sameAs Property",
"구조화 데이터에서 '이 엔티티는 저기의 그것과 같다'고 외부 프로필을 연결하는 속성.",
["홈페이지의 Organization 선언에 sameAs로 공식 SNS, 유튜브, 위키 문서 등을 연결하면, AI와 검색엔진이 흩어진 프로필들을 하나의 실체로 통합해 인식합니다. 엔티티 신뢰도를 높이는 가장 간단하고 확실한 장치입니다.",
"연결할 외부 프로필이 없다면 그것부터 만들어야 합니다. 네이버 플레이스, 링크드인 기업 페이지, 유튜브 채널 — 각 프로필의 기업 정보가 서로 일치해야 연결 효과가 삽니다."],
"messeze 진단에서 sameAs 누락은 가장 흔하게 발견되는 감점 요인입니다.",
["entity","json-ld","knowledge-graph"])

t("brand-mention","trust","브랜드 멘션","Brand Mention",
"링크 없이 텍스트로 기업·브랜드가 언급되는 것. AI 시대에 백링크만큼 중요해진 신호.",
["기사나 커뮤니티에서 링크 없이 회사 이름만 언급되어도, 검색엔진과 AI는 그것을 '이 브랜드가 실재하고 회자된다'는 신호로 읽습니다. 특히 LLM은 학습 텍스트 속 언급 빈도와 맥락으로 브랜드를 기억합니다.",
"중요한 것은 언급의 맥락입니다. '정밀부품'이라는 주제 옆에서 반복적으로 언급되는 기업은 그 분야의 엔티티로 굳어집니다. 언급이 없는 기업은 AI에게 존재하지 않는 것과 같습니다."],
"messeze의 콘텐츠·언론 축적은 결국 '좋은 맥락의 멘션'을 꾸준히 만드는 일입니다.",
["eeat","citation","press-release"])

# ===== 언론홍보·PR =====
t("press-release","pr","보도자료","Press Release",
"기업의 소식을 기자와 언론사에 제공하는 공식 문서. 기사화를 목표로 뉴스 가치 중심으로 작성한다.",
["보도자료의 목적은 기자가 최소한의 수정으로 기사를 쓸 수 있게 하는 것입니다. 핵심 사실을 앞에 배치하고(역피라미드), 검증 가능한 수치와 인용문을 담고, 과장 표현을 뺀 문서가 기사화 확률이 높습니다.",
"AI 시대에 보도자료의 가치는 더 커졌습니다. 기사화된 정보는 제3자 검증을 거친 신뢰 출처가 되어, AI가 기업을 설명할 때 인용하는 근거가 됩니다."],
"messeze는 모든 보도자료를 '기사화 가능성'과 'AI 인용 가능성' 두 기준으로 작성합니다.",
["advertorial","boilerplate","lead-paragraph"])

t("advertorial","pr","애드버토리얼","Advertorial",
"광고(Ad)와 기사(Editorial)의 합성어. 매체 지면을 확보해 기사 형식으로 싣는 콘텐츠.",
["보도자료는 기자의 선택을 받아야 하지만, 애드버토리얼은 게재가 보장되고 내용을 우리가 정합니다. 뉴스 가치가 약한 서비스 소개·브랜드 스토리를 원하는 시점에 확실히 알릴 때 적합합니다.",
"신뢰도는 일반 기사보다 낮게 평가될 수 있으므로, 보도자료 기반 기사와 조합해 운용하는 것이 효과적입니다. AI 관점에서는 애드버토리얼도 하나의 공개 출처로 축적됩니다."],
"messeze 플랜에는 보도자료와 애드버토리얼이 목적에 따라 조합되어 있습니다.",
["press-release","newswire","brand-mention"])

t("boilerplate","pr","보일러플레이트","Boilerplate",
"보도자료 말미에 붙는 회사 표준 소개문. 3~4문장으로 기업을 일관되게 설명한다.",
["모든 보도자료에 동일하게 들어가는 회사 소개 단락입니다. 설립 연도, 주력 사업, 핵심 실적을 담은 이 문단은 기사마다 반복 노출되며 기업의 '공식 정의'로 굳어집니다.",
"AI 관점에서 보일러플레이트는 훌륭한 학습 재료입니다. 여러 기사에서 동일한 기업 설명이 반복 확인되면, AI는 그 내용을 기업의 사실 정보로 신뢰하게 됩니다. 그래서 한 번 잘 쓰고 일관되게 유지하는 것이 중요합니다."],
"messeze 온보딩에서 가장 먼저 확정하는 산출물 중 하나가 보일러플레이트입니다.",
["press-release","entity","brand-mention"])

t("embargo","pr","엠바고","Embargo",
"보도자료를 미리 제공하되 '이 시점 이전에는 보도하지 말아 달라'고 약속하는 관행.",
["신제품 발표나 대형 계약처럼 시점이 중요한 소식은, 기자들에게 미리 자료를 주고 준비 시간을 확보하게 하되 발표 시각을 맞추는 엠바고를 활용합니다. 여러 매체가 같은 날 일제히 보도하면 화제성이 커집니다.",
"엠바고는 신뢰 관계 위에서 작동합니다. 관행을 이해하고 기자와의 관계를 관리하는 것도 언론홍보 실무의 일부입니다."],
"전시회·신제품 발표를 앞둔 기업이라면 messeze가 엠바고 일정까지 설계해 드립니다.",
["press-release","media-list","exhibition-pr"])

t("media-list","pr","미디어 리스트 (기자 매칭)","Media List",
"업종·주제별로 어떤 매체의 어떤 기자에게 보도자료를 보낼지 정리한 명단.",
["보도자료의 성패는 원고 품질 못지않게 '누구에게 보내는가'에 달렸습니다. 산업 담당 기자에게 소비재 소식을 보내면 스팸이 되고, 딱 맞는 출입처 기자에게 닿으면 기사가 됩니다.",
"좋은 미디어 리스트는 매체명 나열이 아니라 기자별 관심 분야·최근 기사·연락 채널이 정리된 살아있는 데이터베이스입니다. 꾸준히 관리될수록 기사화율이 올라갑니다."],
"messeze는 업종별 기자 데이터베이스를 구축해 자동 매칭하는 것을 핵심 역량으로 삼습니다.",
["press-release","newswire","embargo"])

t("newswire","pr","뉴스와이어 (배포 서비스)","Newswire Distribution",
"보도자료를 다수 매체·기자에게 일괄 배포하는 서비스 또는 그 방식.",
["개별 기자 접촉과 달리, 뉴스와이어형 배포는 등록된 다수 채널에 자료를 한 번에 뿌립니다. 도달 범위는 넓지만 기사화율은 타깃 배포보다 낮은 편이라, 두 방식을 목적에 따라 조합하는 것이 실무 정석입니다.",
"배포 결과(발송·열람·기사화)를 추적하고 다음 배포에 반영하는 순환이 중요합니다. 뿌리고 끝나는 배포는 자산이 되지 않습니다."],
"messeze는 타깃 기자 매칭과 광역 배포를 조합하고, 결과를 월간 리포트로 추적합니다.",
["media-list","press-release","domain-authority"])

t("lead-paragraph","pr","리드문","Lead Paragraph",
"기사·보도자료의 첫 문단. 누가·무엇을·왜 지금을 압축해 전체를 요약한다.",
["기자는 리드문만 보고 기사화 여부를 판단하는 경우가 많습니다. 이 문단만 실려도 기사가 되도록 핵심 사실을 다 담는 것이 원칙입니다. 회사 자랑이 아니라 '업계에 어떤 변화가 생겼는가'의 관점으로 씁니다.",
"AI에게도 리드문은 문서의 요약으로 읽힙니다. 첫 문단에 핵심이 없는 글은 사람에게도 기계에게도 선택받기 어렵습니다."],
"messeze의 보도자료 작성 기준 1번이 '리드문 승부'입니다.",
["press-release","boilerplate","meta-description"])

t("exhibition-pr","pr","전시회 홍보","Exhibition PR",
"전시회·수출상담회 참가를 전후로 언론·콘텐츠를 통해 성과를 극대화하는 홍보 활동.",
["참가 확정 시점의 사전 보도자료, 현장 이슈의 속보성 자료, 종료 후 성과 자료까지 — 전시회 하나로 최소 세 번의 뉴스 기회가 생깁니다. 부스 방문 바이어가 검색했을 때 나오는 기사들이 신뢰를 만듭니다.",
"해외 전시회라면 현지어 보도자료와 현지 매체 배포가 더해집니다. '○○ 전시회에 참가한 한국 기업'을 AI에게 묻는 바이어에게 답이 되는 콘텐츠가 남습니다."],
"수출바우처 참여 기업이라면 전시회 연계 홍보를 바우처로 진행하는 방안도 상담해 드립니다.",
["embargo","press-release","geo"])

# ===== 추가 배치 (next-t geo/seo glossary 참고) =====
t("llms-txt","ai","llms.txt","llms.txt",
"사이트가 AI에게 '무엇을, 어떻게 읽어달라'고 안내하는 텍스트 파일. 루트에 두는 AI용 이정표.",
["robots.txt가 크롤러에게 접근 규칙을 알려주듯, llms.txt는 AI 모델에게 사이트의 핵심 문서와 우선순위를 정리해 안내하려는 제안 표준입니다. 방대한 페이지 중 무엇이 신뢰할 만한 원문인지 AI가 빠르게 파악하도록 돕는 것이 목적입니다.",
"아직 모든 AI가 공식 지원하는 단계는 아니지만, 핵심 정보를 기계가 읽기 쉬운 형태로 한 곳에 정리해 두는 것 자체가 GEO에 유리합니다. 회사 소개·주요 문서·연락처를 명확한 구조로 노출하는 습관과 맞닿아 있습니다."],
"messeze 홈페이지 최적화에서 AI가 읽는 핵심 문서를 구조화하는 작업과 연결됩니다.",
["ai-crawler","structured-data","geo"])

t("rag","ai","RAG (검색 증강 생성)","Retrieval-Augmented Generation",
"AI가 답할 때 학습 지식만이 아니라 실시간으로 외부 문서를 검색해 근거로 삼는 방식.",
["LLM은 학습 시점 이후의 정보를 모르고 세부 사실을 지어낼 수 있습니다. RAG는 답변 전에 관련 문서를 먼저 검색해 가져오고, 그 내용을 근거로 답을 생성합니다. Perplexity나 브라우징이 켜진 ChatGPT가 대표적입니다.",
"RAG 구조에서는 검색 단계에서 우리 기업 정보가 걸려야 답에 반영됩니다. 학습 데이터에 없더라도 신뢰할 수 있는 최신 콘텐츠를 웹에 쌓아두면 AI가 그때그때 찾아 인용할 수 있습니다."],
"검색량이 없어도 '검색되면 인용된다' — messeze가 웹에 출처를 축적하는 이유입니다.",
["grounding","citation","ai-search"])

t("hallucination","ai","환각 (할루시네이션)","Hallucination",
"AI가 사실이 아닌 내용을 그럴듯하게 지어내는 현상. 정보가 부족한 대상일수록 잘 발생한다.",
["LLM은 확률적으로 다음 단어를 이어붙이기 때문에, 근거가 부족하면 빈칸을 그럴듯하게 메웁니다. 기업 정보가 웹에 거의 없으면 AI는 회사를 아예 언급하지 않거나 잘못된 사업 내용·실적을 지어낼 수 있습니다.",
"환각을 막는 가장 확실한 방법은 정확한 정보를 여러 신뢰 출처에 충분히 심어두는 것입니다. AI가 근거로 삼을 자료가 많고 일관될수록 지어낼 여지가 줄어듭니다."],
"AI가 우리 회사를 틀리게 말하기 전에 정확한 출처를 쌓는 것 — messeze의 예방적 역할입니다.",
["grounding","llm","citation"])

t("grounding","ai","그라운딩","Grounding",
"AI의 답변을 실제 출처에 접지시켜 사실에 기반하게 만드는 것. 환각의 반대편에 있는 개념.",
["그라운딩은 AI가 자기 기억에만 의존하지 않고 검증 가능한 외부 근거에 답을 묶는 것을 뜻합니다. 그라운딩이 잘 된 답변은 출처를 함께 제시하고, 그 출처에서 확인되는 사실만 말합니다.",
"기업 입장에서 그라운딩의 재료는 곧 우리가 만든 콘텐츠입니다. 홈페이지·기사·칼럼이 명확하고 일관될수록 AI는 그것을 접지점으로 삼아 우리 기업을 정확히 설명합니다."],
"messeze가 여러 출처에 같은 사실을 축적하는 것은 AI의 그라운딩 재료를 만드는 일입니다.",
["hallucination","citation","rag"])

t("knowledge-cutoff","ai","지식 컷오프","Knowledge Cutoff",
"AI 모델이 학습한 데이터의 마지막 시점. 그 이후 정보는 실시간 검색이 없으면 알지 못한다.",
["모델은 특정 시점까지의 데이터로 학습되며, 그 이후에 생긴 회사·제품·사건은 모르는 상태입니다. 최근 창업했거나 최근에야 정보를 쌓기 시작한 기업이 AI 답변에서 빠지는 흔한 이유입니다.",
"이 한계를 메우는 것이 실시간 웹 검색(RAG)입니다. 학습 데이터에 없어도 웹에 신뢰할 수 있는 최신 정보가 있으면 AI가 검색해 반영합니다. 그래서 지금 쌓는 정보가 중요합니다."],
"학습 시점 이후에도 발견되게 하려면 웹 축적이 필수 — messeze가 매달 쌓는 이유입니다.",
["rag","freshness","ai-search"])

t("multimodal","ai","멀티모달","Multimodal",
"텍스트뿐 아니라 이미지·표·PDF·음성 등 여러 형태의 정보를 함께 이해하는 AI의 능력.",
["최신 AI는 글만이 아니라 이미지 속 도표, 제품 사진, PDF 카탈로그까지 읽어낼 수 있습니다. 다만 이미지에 설명(대체텍스트)이 없거나 PDF가 텍스트가 아닌 스캔 이미지면 여전히 이해하지 못합니다.",
"제조기업은 사양이 이미지·PDF에 갇혀 있는 경우가 많습니다. 핵심 정보를 텍스트로도 제공하고 이미지에 alt를 채우면 멀티모달 AI가 훨씬 정확히 파악합니다."],
"messeze 홈페이지 최적화는 이미지·PDF에 갇힌 정보를 AI가 읽을 수 있게 꺼냅니다.",
["alt-text","structured-data","ai-crawler"])

t("share-of-voice","ai","인용 점유율 (AI 가시성)","Share of Voice · AI Visibility",
"특정 질문군에서 AI 답변이 우리 기업을 인용·언급하는 비중. AI 시대의 시장 점유율 지표.",
["같은 질문을 여러 AI에 반복해서 던졌을 때 우리 기업이 얼마나 자주 답에 등장하는가 — 이것이 인용 점유율입니다. 경쟁사 대비 우리가 'AI의 기본 답'에 얼마나 들어가 있는지를 보여줍니다.",
"검색 순위처럼 하나의 숫자로 딱 떨어지진 않지만, 질문별로 등장 여부와 인용 출처를 추적하면 추세를 관리할 수 있습니다. 축적이 쌓일수록 점유율이 올라가는 것이 정상적인 곡선입니다."],
"messeze 월간 리포트의 핵심 지표가 바로 질문별 인용 점유율의 변화입니다.",
["citation","brand-mention","ai-overview"])

t("self-contained","onpage","자기완결 콘텐츠","Self-contained Content",
"한 페이지·한 문단만 봐도 맥락 없이 이해되는 콘텐츠. AI가 잘라서 인용하기 좋은 형태.",
["AI는 문서 전체가 아니라 필요한 조각만 잘라 인용합니다. '앞에서 말한 것처럼'에 의존하는 문단은 잘려 나오면 뜻이 통하지 않아 인용되기 어렵습니다. 각 문단이 스스로 완결되어야 합니다.",
"자기완결형 글은 주어와 핵심을 문단마다 명시합니다. 사람에게는 다소 반복적이어도, 기계가 어디를 잘라 가든 정확한 정보가 담기도록 설계하는 것이 AEO의 기본입니다."],
"messeze의 AEO형 콘텐츠는 문단 단위로 잘려도 뜻이 통하도록 작성됩니다.",
["answer-first","heading-structure","aeo"])

t("answer-first","onpage","답변친화적 구조 (Answer-First)","Answer-First · TL;DR",
"결론·핵심 답을 문단 맨 앞에 두는 글쓰기. AI가 답으로 뽑아 쓰기 가장 좋은 구조.",
["질문에 대한 답을 서두에 먼저 제시하고 이유와 배경을 뒤에 붙이는 구조입니다. 신문 기사의 역피라미드와 같습니다. AI는 질문에 정면으로, 앞부분에서 답하는 문단을 우선 인용합니다.",
"소제목을 질문형으로 달고 바로 다음 문단에서 한두 문장으로 답한 뒤 부연하는 방식이 대표적입니다. 배경 설명부터 길게 늘어놓는 글은 AI가 답을 찾기 전에 지나칩니다."],
"messeze 칼럼은 질문형 소제목과 앞선 답변 구조로 작성됩니다.",
["self-contained","heading-structure","aeo"])

t("information-gain","onpage","정보 이득","Information Gain",
"이미 널린 내용이 아니라 그 페이지에만 있는 새로운 정보의 양. AI·검색이 높게 치는 가치.",
["누구나 아는 일반론만 반복하는 페이지는 AI에게 인용할 이유가 없습니다. 반면 실제 수치, 자체 사례, 현장 노하우처럼 다른 데서 못 찾는 정보가 담기면 그 페이지는 가져다 쓸 가치가 생깁니다.",
"제조·B2B 기업은 사실 정보 이득의 보고입니다. 공정 조건, 인증 과정, 납기 대응 사례처럼 내부에만 있던 지식을 콘텐츠로 꺼내면, 검색량이 적어도 그 분야의 유일한 답이 됩니다."],
"messeze는 기업 내부의 '남들이 모르는 정보'를 콘텐츠로 끌어내는 데 집중합니다.",
["self-contained","eeat","geo"])

t("freshness","onpage","최신성","Freshness",
"정보가 얼마나 최근에 갱신됐는지. 오래된 정보만 있는 기업은 AI 답변에서 밀려난다.",
["AI와 검색엔진은 최신 정보를 선호합니다. 몇 년 전 기사 한 건이 전부인 기업은 지금도 활동하는지 확신을 주지 못합니다. 꾸준히 갱신되는 콘텐츠는 그 자체로 신뢰 신호가 됩니다.",
"최신성은 날짜만 바꾸는 것이 아니라 실제로 새 소식·자료가 계속 더해지는 흐름을 말합니다. 매달 무언가가 쌓이는 기업과 멈춰 있는 기업의 차이는 시간이 갈수록 벌어집니다."],
"messeze가 일회성이 아니라 매달 축적을 강조하는 핵심 이유가 최신성입니다.",
["knowledge-cutoff","geo","brand-mention"])

t("internal-link","onpage","내부 링크","Internal Link",
"같은 사이트 안의 페이지끼리 연결하는 링크. 크롤링 경로와 주제 연관성을 만든다.",
["내부 링크는 검색엔진 봇이 사이트를 돌아다니는 길이자 '이 페이지들이 서로 관련 있다'는 신호입니다. 중요한 페이지일수록 여러 곳에서 링크로 이어주면 크롤링과 평가에 유리합니다.",
"주제별로 묶인 내부 링크 구조는 AI가 기업의 정보 체계를 파악하는 데도 도움이 됩니다. 서비스·사례·칼럼이 서로 연결되면 흩어진 정보가 하나의 맥락으로 읽힙니다."],
"messeze 홈페이지 정비에는 주제 중심의 내부 링크 설계가 포함됩니다.",
["anchor-text","crawling-indexing","entity"])

t("anchor-text","onpage","앵커 텍스트","Anchor Text",
"링크에 걸린 글자. 그 링크가 가리키는 페이지가 무엇에 관한 것인지 알려주는 신호.",
["'여기를 클릭' 같은 앵커 텍스트는 기계에게 아무 정보도 주지 않습니다. 반면 '항공용 정밀부품 소량 생산 사례'처럼 내용을 담은 앵커는 링크 대상 페이지의 주제를 명확히 전달합니다.",
"내부 링크든 외부 백링크든 앵커 텍스트가 자연스럽게 주제어를 담으면 검색엔진과 AI가 페이지의 정체성을 더 잘 이해합니다. 다만 억지로 키워드를 반복하면 역효과가 납니다."],
"messeze의 콘텐츠·링크 작업은 앵커 텍스트에 주제 맥락을 담는 것을 기본으로 합니다.",
["internal-link","backlink","seo"])

t("hreflang","onpage","hreflang","hreflang",
"같은 콘텐츠의 언어·지역별 버전을 검색엔진에 알려주는 태그. 수출기업 다국어 페이지의 필수 장치.",
["영문·베트남어·중국어 페이지를 만들어도 검색엔진이 어느 언어 사용자에게 무엇을 보여줄지 모르면 엉뚱한 버전이 노출됩니다. hreflang은 각 페이지의 언어·지역을 명시해 이 혼선을 막습니다.",
"다국어 페이지가 서로 hreflang으로 올바르게 연결되면, 현지 바이어가 검색·AI로 찾을 때 자기 언어 버전이 정확히 매칭됩니다. 해외 PR의 기술적 토대입니다."],
"messeze의 수출기업 다국어 콘텐츠 작업에는 hreflang 설정이 포함됩니다.",
["canonical","structured-data","geo"])

t("robots-txt","basic","robots.txt","robots.txt",
"크롤러에게 사이트의 어디를 수집해도 되는지 안내하는 파일. AI 크롤러 허용 여부도 여기서 정한다.",
["사이트 루트에 두는 robots.txt는 검색엔진·AI 봇에게 접근 가능한 영역과 그렇지 않은 영역을 알려줍니다. 실수로 중요한 페이지를 막아두면 아예 검색·AI에서 사라질 수 있어 점검이 필요합니다.",
"최근에는 GPTBot·Google-Extended 같은 AI 크롤러를 허용할지 여부도 robots.txt에서 결정합니다. 보호할 콘텐츠와 AI에 읽히고 싶은 콘텐츠를 구분하는 정책이 중요해졌습니다."],
"messeze 진단은 robots.txt가 검색·AI 크롤러를 막고 있지 않은지부터 확인합니다.",
["crawling-indexing","ai-crawler","sitemap"])

t("sitemap","basic","XML 사이트맵","XML Sitemap",
"사이트의 주요 페이지 목록을 검색엔진에 제출하는 파일. 빠짐없이 색인되도록 돕는다.",
["사이트맵은 이 사이트에 이런 페이지들이 있으니 확인해 달라는 목록입니다. 링크로만 연결된 깊은 페이지도 사이트맵에 있으면 크롤러가 놓치지 않고 색인할 가능성이 높아집니다.",
"페이지가 많거나 새로 추가되는 콘텐츠가 잦은 사이트일수록 효과가 큽니다. 사이트맵을 검색엔진 도구에 제출하고 오류를 관리하는 것이 기본 운영입니다."],
"messeze가 축적하는 콘텐츠가 빠짐없이 색인되도록 사이트맵을 관리합니다.",
["robots-txt","crawling-indexing","seo"])

t("core-web-vitals","basic","코어 웹 바이탈","Core Web Vitals",
"로딩 속도·반응성·화면 안정성을 수치화한 구글의 사용자 경험 지표. 순위에 영향을 준다.",
["페이지가 얼마나 빨리 보이는지, 입력에 얼마나 빨리 반응하는지, 화면이 갑자기 밀리지 않는지를 측정합니다. 느리고 불안정한 페이지는 사용자가 떠나고 검색 평가에서도 불리합니다.",
"화려한 효과보다 기본적인 속도·안정성이 중요합니다. 특히 모바일에서의 경험이 크게 반영되므로 이미지 최적화와 불필요한 스크립트 정리가 기본 처방입니다."],
"messeze 홈페이지 점검 항목에 코어 웹 바이탈 기본 진단이 포함됩니다.",
["seo","alt-text","crawling-indexing"])

t("redirect","basic","리다이렉트 (301·302)","Redirect",
"옛 주소를 새 주소로 자동 전환하는 것. 301(영구)·302(임시) 구분이 평가 승계를 좌우한다.",
["페이지 주소를 바꾸거나 사이트를 개편할 때 옛 URL로 들어온 방문자와 크롤러를 새 URL로 보내는 장치가 리다이렉트입니다. 301(영구)은 기존 페이지가 쌓은 평가와 링크 신뢰를 새 주소로 대부분 넘겨줍니다.",
"302(임시)나 리다이렉트 누락은 평가 단절·중복 색인 같은 문제를 일으킵니다. 홈페이지 리뉴얼 때 옛 URL 매핑을 빠뜨리면 그동안 쌓은 검색 자산이 사라질 수 있어 주의가 필요합니다."],
"messeze 홈페이지 리뉴얼은 기존 평가를 지키는 301 매핑 설계부터 시작합니다.",
["canonical","crawling-indexing","seo"])

t("link-building","trust","링크빌딩","Link Building",
"다른 신뢰 사이트가 우리 페이지로 링크를 걸도록 만드는 활동. 권위를 쌓는 정공법.",
["좋은 콘텐츠를 만들고 언론·업계 매체·파트너가 자연스럽게 인용·링크하도록 유도하는 것이 건강한 링크빌딩입니다. 돈으로 링크를 대량 구매하는 방식은 오히려 페널티 위험이 큽니다.",
"제조·B2B 기업에게 가장 강력한 링크는 언론 기사에서 나옵니다. 보도자료가 기사화되면 노출과 함께 권위 있는 백링크가 따라오는 일석이조의 링크빌딩입니다."],
"messeze의 언론 배포는 결과적으로 가장 신뢰도 높은 링크빌딩이 됩니다.",
["backlink","domain-authority","press-release"])

# ===== 2차 배치 (next-t glossary 나머지 핵심) =====
t("embedding","ai","임베딩·벡터 유사도","Embedding · Vector Similarity",
"글의 의미를 숫자 벡터로 바꿔 얼마나 비슷한 뜻인가를 계산하는 방식. AI가 관련 문서를 찾는 원리.",
["AI는 단어를 그대로 매칭하지 않고 문장의 의미를 수백 차원의 숫자(벡터)로 바꿔 저장합니다. 질문과 문서의 벡터가 가까우면 의미가 비슷하다고 판단해 근거로 가져옵니다. 똑같은 키워드가 없어도 뜻이 통하면 검색됩니다.",
"기업 입장에서는 키워드를 억지로 반복할 필요가 없다는 뜻입니다. 고객이 물어볼 법한 표현으로 자연스럽고 명확하게 쓰면, 다른 단어로 질문해도 의미가 맞아 인용될 수 있습니다."],
"messeze 콘텐츠는 키워드 나열이 아니라 의미가 분명한 문장을 지향합니다.",
["rag","search-intent","self-contained"])

t("context-window","ai","컨텍스트 윈도우","Context Window",
"AI가 한 번에 읽고 기억할 수 있는 정보의 최대 분량. 이를 넘으면 앞부분을 잊는다.",
["AI는 대화나 문서를 무한히 기억하지 못하고 정해진 분량만큼만 한 번에 다룹니다. 너무 길고 산만한 페이지는 핵심이 이 창 밖으로 밀려나 인용에서 빠질 수 있습니다.",
"그래서 핵심을 앞쪽에 두고 한 페이지가 하나의 주제에 집중하는 것이 유리합니다. 방대한 정보를 한 페이지에 몰아넣기보다 주제별로 나누는 편이 AI에게 잘 읽힙니다."],
"messeze의 질문별 페이지 설계는 AI가 핵심을 놓치지 않게 하는 구조입니다.",
["answer-first","chunking","self-contained"])

t("token","ai","토큰","Token",
"AI가 글을 처리하는 최소 단위. 단어보다 작은 조각으로, 비용·길이 제한의 기준이 된다.",
["AI는 문장을 토큰이라는 조각으로 잘라 처리합니다. 한글은 대략 한 글자가 한 토큰 안팎입니다. 컨텍스트 윈도우도, API 비용도 토큰 수로 계산됩니다.",
"실무적으로는 간결하고 밀도 높은 글이 유리하다는 의미입니다. 불필요하게 긴 문장보다 핵심을 담은 압축된 문장이 토큰을 아끼면서도 잘 인용됩니다."],
"messeze는 군더더기 없이 핵심을 담는 압축적 문장을 지향합니다.",
["context-window","information-gain","answer-first"])

t("query-fanout","ai","질의 확장 (Query Fan-out)","Query Fan-out",
"AI가 하나의 질문을 여러 개의 세부 검색으로 쪼개어 각각 자료를 모으는 방식.",
["복잡한 질문을 받으면 AI는 그것을 여러 하위 질문으로 나눠 각각 검색한 뒤 종합해 답합니다. 예를 들어 믿을 만한 부품 제조사는 인증 보유·수출 실적·소량 생산 같은 세부 질의로 확장됩니다.",
"이는 기업이 다양한 각도의 콘텐츠를 갖춰야 하는 이유입니다. 한 주제만 반복하기보다 고객이 확인하고 싶어 하는 여러 측면을 각각 다룬 콘텐츠가 있어야 여러 하위 질의에 걸립니다."],
"messeze가 핵심 질문 5~6개를 설계하는 것은 이 질의 확장에 대응하기 위함입니다.",
["search-intent","rag","faq-schema"])

t("chunking","ai","청킹 (문서 분할)","Chunking",
"긴 문서를 의미 단위 조각으로 나눠 저장·검색하는 것. AI는 문서 전체가 아니라 이 조각을 인용한다.",
["AI 검색 시스템은 긴 페이지를 통째로 다루지 않고 문단·섹션 단위 조각으로 잘라 색인합니다. 그리고 질문에 맞는 조각만 골라 근거로 씁니다. 조각이 스스로 완결적일수록 정확히 인용됩니다.",
"소제목으로 구획이 명확하고 각 구획이 한 가지를 다루는 문서는 잘 쪼개지고 잘 인용됩니다. 반대로 여러 주제가 뒤섞인 문단은 어중간하게 잘려 활용도가 떨어집니다."],
"messeze 콘텐츠의 질문형 소제목 구조는 깔끔한 청킹을 염두에 둔 설계입니다.",
["self-contained","heading-structure","context-window"])

t("author-signal","ai","저자 신호","Author Signal",
"콘텐츠를 누가 썼는지 드러내는 정보. 발행 주체가 분명할수록 AI가 신뢰한다.",
["작성자·발행 주체가 명확한 글은 익명 글보다 신뢰를 받습니다. 회사명·저자·전문성이 드러나면 AI는 검증된 출처로 취급할 근거를 얻습니다. E-E-A-T의 실무적 실행이 곧 저자 신호입니다.",
"기업 콘텐츠라면 누가 어떤 자격으로 말하는가를 페이지에 명확히 담는 것이 좋습니다. 대표·전문가 이름, 회사 정보, 관련 실적이 저자 신호를 강화합니다."],
"messeze는 기업을 명확한 발행 주체(엔티티)로 드러내 저자 신호를 키웁니다.",
["eeat","entity","structured-data"])

t("entity-resolution","ai","개체 해소","Entity Resolution",
"여러 곳에 흩어진 정보가 같은 회사·사람을 가리킨다고 AI가 판단해 하나로 묶는 과정.",
["홈페이지의 ○○정밀, 기사 속 주식회사 ○○정밀, SNS의 ○○가 같은 실체임을 기계가 알아채는 것이 개체 해소입니다. 이게 안 되면 정보가 흩어진 채로 남아 신뢰가 쌓이지 않습니다.",
"정확한 회사명 표기, 구조화 데이터의 @id·sameAs 연결, 일관된 소개 문구가 개체 해소를 돕습니다. 출처마다 회사 이름·소개가 제각각이면 AI는 같은 회사로 확신하지 못합니다."],
"messeze는 모든 출처에서 기업 정보를 일관되게 맞춰 하나의 실체로 묶이게 합니다.",
["entity","sameas","knowledge-graph"])

t("live-web-search","ai","실시간 웹 검색","Live Web Search",
"AI가 학습 지식이 아니라 지금 이 순간의 웹을 검색해 최신 정보로 답하는 기능.",
["브라우징이 켜진 ChatGPT, Perplexity, 구글 AI 오버뷰는 답하기 전에 실제 웹을 검색합니다. 학습 시점 이후의 정보나 최근 소식도 이때 반영됩니다. 지식 컷오프의 한계를 메우는 통로입니다.",
"이 기능 덕분에 지금 웹에 있는 정보가 곧바로 답에 영향을 줍니다. 최근에 쌓은 콘텐츠가 실시간 검색에 걸리면, 학습 데이터에 없던 기업도 답에 등장할 수 있습니다."],
"messeze가 매달 최신 콘텐츠를 쌓는 것은 실시간 검색에 걸리기 위한 것입니다.",
["rag","knowledge-cutoff","freshness"])

t("citation-vs-mention","ai","인용 vs 언급","Citation vs Mention",
"출처 링크로 근거에 포함되는 인용과, 링크 없이 이름만 나오는 언급의 구분.",
["AI 답변에서 기업이 등장하는 방식은 둘로 나뉩니다. 출처 목록에 링크와 함께 들어가는 인용은 신뢰의 근거가 되고, 본문에 이름만 스치는 언급은 그보다 약합니다. 둘 다 가치 있지만 지향점은 인용입니다.",
"인용을 받으려면 질문에 정면으로 답하고 검증 가능한 페이지여야 합니다. 언급에 그치는 정보를 인용 수준으로 끌어올리는 것이 콘텐츠 최적화의 목표입니다."],
"messeze 리포트는 단순 언급과 출처 인용을 구분해 추적합니다.",
["citation","brand-mention","share-of-voice"])

t("liftable-claim","onpage","인용 가능한 문장","Liftable Claim",
"그대로 떼어 인용해도 완결적이고 검증 가능한 한 문장. AI가 답에 그대로 실을 수 있는 형태.",
["15년간 항공·의료용 정밀부품을 공급하고 2024년 수출바우처에 선정된 제조사처럼, 한 문장만 떼어도 뜻이 통하고 사실로 검증되는 문장이 인용 가능한 문장입니다. AI는 이런 문장을 그대로 답에 옮깁니다.",
"모호한 수식어가 아니라 구체적 사실(연차·인증·실적)로 쓸수록 인용 가능성이 올라갑니다. 핵심 강점을 이런 문장으로 정리해 두는 것이 중요합니다."],
"messeze는 기업의 강점을 인용 가능한 사실 문장으로 벼려 콘텐츠에 심습니다.",
["self-contained","answer-first","citation"])

t("definitional-sentence","onpage","정의형 문장","Definitional Sentence",
"A는 B이다 형태로 대상을 명확히 규정하는 문장. AI가 개념·기업을 이해하는 앵커가 된다.",
["메세지는 구독형 기업 PR 서비스다처럼 주어를 분명히 규정하는 문장은 AI가 그 대상을 이해하는 기준점이 됩니다. 이런 정의 문장이 페이지 앞부분에 있으면 인용과 개체 해소가 쉬워집니다.",
"제품·서비스·회사 소개의 첫 문장을 무엇이다로 명확히 정의하세요. 돌려 말하거나 형용사만 나열하면 기계는 핵심을 잡지 못합니다."],
"messeze는 각 페이지 첫 문장을 명확한 정의형으로 잡는 것을 기본으로 합니다.",
["entity","answer-first","liftable-claim"])

t("localization","onpage","현지화","Localization",
"단순 번역을 넘어 현지 언어·표현·맥락에 맞게 콘텐츠를 다시 만드는 것. 해외 PR의 핵심.",
["기계 번역한 영문 페이지는 현지 바이어에게 어색하고 신뢰를 주기 어렵습니다. 현지화는 용어·단위·표현·강조점을 그 나라 방식으로 다시 쓰는 작업입니다. 같은 제품도 시장마다 통하는 포인트가 다릅니다.",
"현지어로 자연스럽게 쓰인 콘텐츠는 현지 검색·AI에서 훨씬 잘 잡힙니다. hreflang으로 언어별 버전을 올바르게 연결하면 효과가 배가됩니다."],
"messeze의 수출기업 다국어 작업은 번역이 아니라 현지화를 원칙으로 합니다.",
["hreflang","structured-data","geo"])

t("speakable","onpage","Speakable","Speakable",
"음성 비서가 읽어주기 좋은 부분을 표시하는 구조화 데이터. 음성 검색 노출을 돕는다.",
["schema.org의 Speakable은 페이지에서 소리 내어 읽기 적합한 문장을 지정합니다. 음성 비서가 답할 때 이 부분을 우선 활용합니다. 짧고 명확한 요약 문장이 대상이 됩니다.",
"아직 활용 범위는 제한적이지만, 핵심을 한두 문장으로 또렷하게 정리하는 습관 자체가 음성·AI 검색 모두에 유리합니다."],
"messeze의 답변친화형 문장 설계는 음성 검색 대응과도 자연스럽게 맞물립니다.",
["structured-data","answer-first","faq-schema"])

t("url-structure","onpage","URL 구조","URL Structure",
"주소를 짧고 의미 있게 구성하는 것. 사람과 기계 모두에게 페이지 내용을 알려주는 신호.",
["내용을 담은 짧은 URL은 페이지 주제를 즉시 전달합니다. 반대로 의미 없는 숫자·파라미터로 뒤엉킨 주소는 이해도 어렵고 공유·관리도 불편합니다.",
"한 번 정한 URL은 함부로 바꾸지 않는 것이 좋고, 바꿔야 한다면 301 리다이렉트로 평가를 넘겨야 합니다. 일관된 URL 체계는 사이트 전체의 신뢰를 높입니다."],
"messeze 홈페이지 구축·정비에는 의미 있는 URL 설계가 포함됩니다.",
["redirect","canonical","seo"])

t("nofollow","trust","nofollow · rel 속성","rel nofollow / sponsored / ugc",
"링크에 이 링크는 보증하지 않는다고 표시하는 속성. 광고·댓글 링크 구분에 쓴다.",
["rel=nofollow는 검색엔진에 이 링크로 권위를 넘기지 않는다는 신호입니다. 광고·후원 링크는 sponsored, 사용자 생성 링크는 ugc로 구분해 표시하는 것이 원칙입니다.",
"돈을 주고 산 링크에 nofollow를 붙이지 않으면 페널티 대상이 될 수 있습니다. 자연스럽게 얻은 언론·추천 링크와 광고 링크를 정직하게 구분하는 것이 장기적으로 안전합니다."],
"messeze의 언론 기반 링크는 대부분 신뢰도 높은 자연 링크입니다.",
["backlink","link-building","domain-authority"])

t("ranking-signals","basic","랭킹 시그널","Ranking Signals",
"검색엔진이 순위를 정할 때 종합하는 수백 가지 신호. 콘텐츠·링크·기술·사용자 반응 등.",
["검색 순위는 하나의 기준이 아니라 콘텐츠 관련성, 백링크, 페이지 속도, 모바일 대응, 사용자 클릭·체류 등 수많은 신호의 합으로 정해집니다. 어느 하나만으로 상위에 오르지 않습니다.",
"AI 검색도 비슷하게 여러 신호를 종합합니다. 그래서 한 가지에 올인하기보다 콘텐츠·신뢰·기술을 고르게 갖추는 것이 결국 가장 효율적입니다."],
"messeze 진단은 어느 신호가 약한지 균형 있게 점검하는 데서 출발합니다.",
["seo","backlink","core-web-vitals"])

t("duplicate-content","basic","중복 콘텐츠","Duplicate Content",
"같거나 거의 같은 내용이 여러 주소에 존재하는 것. 평가가 분산되고 색인에서 혼란을 준다.",
["같은 글이 여러 URL에 있으면 검색엔진은 어느 것을 대표로 삼을지 고민하고, 평가가 나뉘어 어느 쪽도 힘을 받지 못할 수 있습니다. 외부 채널에 콘텐츠를 재발행할 때 특히 주의해야 합니다.",
"canonical 태그로 원본을 지정하고 재발행 시 출처를 명확히 하면 중복 문제를 피할 수 있습니다. 원본이 분명해야 AI도 정보의 원류를 올바르게 인식합니다."],
"외부 채널 발행이 많은 messeze 운영에서 원본·중복 관리는 기본 점검 항목입니다.",
["canonical","internal-link","seo"])

t("page-speed","basic","페이지 속도","Page Speed",
"페이지가 얼마나 빨리 뜨는지. 느린 페이지는 이탈을 부르고 검색·AI 평가에서 불리하다.",
["방문자는 몇 초만 느려도 떠납니다. 검색엔진도 느린 페이지를 낮게 평가합니다. 큰 이미지, 무거운 스크립트, 최적화 안 된 서버가 흔한 원인입니다.",
"이미지 압축, 불필요한 스크립트 제거, 캐싱 같은 기본 처방으로 대부분 개선됩니다. AI 크롤러도 응답이 느리면 수집을 포기할 수 있어 속도는 노출과 직결됩니다."],
"messeze 홈페이지 점검에는 페이지 속도 기본 진단이 포함됩니다.",
["core-web-vitals","seo","crawling-indexing"])

t("organic-traffic","basic","유기적 트래픽","Organic Traffic",
"광고가 아닌 자연 검색으로 유입된 방문. 누적될수록 비용 없이 유지되는 자산이다.",
["검색광고로 들어온 방문은 예산이 끊기면 사라지지만, 유기적 트래픽은 콘텐츠와 신뢰가 쌓여 만든 자연 유입이라 지속됩니다. SEO·콘텐츠의 성과를 보여주는 핵심 지표입니다.",
"검색량이 적은 B2B·제조는 유기적 트래픽의 절대량이 작을 수 있습니다. 그래서 방문 수보다 AI 답변 인용·문의 전환 같은 질적 지표를 함께 보는 것이 현실적입니다."],
"messeze는 트래픽 수치보다 AI 인용·문의로 이어지는 질적 성과를 중시합니다.",
["seo","share-of-voice","search-console"])

t("search-console","basic","구글 서치콘솔","Google Search Console",
"구글이 내 사이트를 어떻게 보는지 알려주는 무료 도구. 색인·노출·오류를 확인한다.",
["서치콘솔은 어떤 검색어로 노출·클릭됐는지, 색인에서 빠진 페이지는 없는지, 기술적 오류는 없는지를 보여줍니다. 사이트맵 제출·색인 요청도 여기서 합니다. SEO 운영의 기본 계기판입니다.",
"수치를 보는 것 자체보다, 노출은 되는데 클릭이 없는 페이지나 색인에서 누락된 페이지 같은 문제 신호를 찾아 개선하는 데 씁니다."],
"messeze 운영은 서치콘솔 데이터로 색인·노출 상태를 정기 점검합니다.",
["crawling-indexing","sitemap","organic-traffic"])

# ---------------- GEO 심화 용어 (3차 배치) ----------------
t("self-referential-accumulation","ai","자기참조 누적","Self-Referential Accumulation",
"한 번 AI 답변에 인용된 콘텐츠가 다시 참조되며 권위가 스스로 쌓여가는 경향.",
["AI와 검색은 이미 여러 곳에서 인용되는 출처를 더 신뢰합니다. 그래서 초기에 한 번 인용의 물꼬가 트이면, 그 콘텐츠가 다른 답변·글에서 또 인용되고 그 인용이 다시 신뢰 신호가 되는 선순환이 생깁니다.",
"이는 초기 선점이 왜 중요한지를 설명합니다. 남보다 먼저 인용 가능한 콘텐츠를 쌓아두면 시간이 지날수록 격차가 벌어집니다."],
"messeze가 '지금 시작해 매달 축적'을 강조하는 이유가 바로 이 누적 효과입니다.",
["citation","share-of-voice","geo"])

t("entity-alignment","trust","엔티티 정합","Entity Alignment",
"회사·저자·제품 정보가 모든 채널에서 똑같이 연결돼 하나의 실체로 인식되는 상태.",
["AI는 흩어진 정보를 모아 '이것들이 같은 회사'라고 판단합니다. 상호명·대표자·주소·업종 표기가 채널마다 다르면 같은 기업인지 확신하지 못해 신뢰가 깎입니다.",
"엔티티 정합은 개체해소가 잘 되도록 표기를 미리 통일하는 작업입니다. sameAs·구조화 데이터로 프로필을 서로 연결하면 정합이 강해집니다."],
"messeze는 모든 채널의 기업 정보 표기를 통일해 AI가 흔들림 없이 같은 회사로 인식하게 합니다.",
["entity-resolution","sameas","knowledge-graph"])

t("signal-to-noise","ai","신호 대 잡음","Signal-to-Noise Ratio",
"페이지에서 실제 본문(신호)과 메뉴·광고·반복 영역(잡음)의 비율.",
["AI 크롤러가 페이지를 읽을 때 핵심 본문이 메뉴·배너·푸터 같은 반복 요소에 파묻혀 있으면 무엇이 진짜 내용인지 파악하기 어렵습니다. 신호 대 잡음 비가 높을수록(본문이 또렷할수록) 인용될 확률이 올라갑니다."],
"messeze는 홈페이지 정비 때 본문이 도드라지도록 구조를 다듬어 AI가 핵심을 놓치지 않게 합니다.",
["boilerplate","self-contained","information-gain"])

t("lazy-loading","ai","지연 로딩","Lazy Loading",
"필요 없는 자원을 처음 HTML에서 빼두고 화면에 필요할 때 불러오는 기법.",
["지연 로딩은 사람 방문자에겐 속도를 높여주지만, 자바스크립트를 실행하지 않는 AI 크롤러에겐 정작 중요한 콘텐츠가 처음 HTML에 없어 '빈 페이지'로 보일 수 있습니다.",
"그래서 핵심 텍스트·정보는 지연 로딩에 맡기지 말고 초기 HTML에 담아야 AI가 읽습니다."],
"messeze는 AI가 읽어야 할 핵심 정보를 초기 HTML에 노출되게 정비합니다.",
["ai-crawler","page-speed","structured-data"])

t("memory-retrieval-synthesis","ai","기억·검색·합성","Memory · Retrieval · Synthesis",
"AI가 답을 만드는 세 단계 — 학습된 기억, 외부 문서 검색, 그리고 종합 생성.",
["AI는 먼저 학습으로 익힌 지식(기억)을 떠올리고, 부족하면 외부 문서를 검색한 뒤, 이 둘을 엮어 하나의 답을 만듭니다(합성). 우리 정보가 이 세 단계 어디에도 없으면 답에 등장하지 못합니다."],
"messeze는 학습·검색·합성 모든 경로에 우리 기업 정보가 걸리도록 콘텐츠와 출처를 쌓습니다.",
["rag","parametric-knowledge","live-web-search"])

t("parametric-knowledge","ai","파라메트릭 지식","Parametric Knowledge",
"모델의 가중치 속에 학습으로 새겨진 지식. 검색 없이도 떠올리는 '기억'.",
["파라메트릭 지식은 학습 시점까지의 정보라, 지식 컷오프 이후의 사실은 담기지 않습니다. 우리 회사가 학습 데이터에 충분히 등장했다면 검색 없이도 AI가 우리를 언급할 수 있습니다."],
"널리 인용되는 콘텐츠를 꾸준히 쌓아두면 다음 모델 학습에 우리 정보가 파라메트릭 지식으로 새겨질 확률이 올라갑니다.",
["knowledge-cutoff","memory-retrieval-synthesis","rag"])

t("primary-vs-derivative","trust","1차 소스 vs 파생 자료","Primary Source vs Derivative",
"직접 만든 원본 자료(1차)와 그것을 번역·요약·재가공한 자료(파생)의 구분.",
["AI와 검색은 원본 출처를 더 신뢰하고 우선 인용합니다. 보도자료 원문, 자사 공식 페이지, 직접 작성한 칼럼은 1차 소스이고, 이를 짜깁기한 글은 파생 자료입니다."],
"messeze는 기업이 직접 발신하는 1차 소스(홈페이지·보도자료·자사 블로그)를 만들어 인용 우선순위를 높입니다.",
["citation","press-release","eeat"])

t("structured-error","ai","구조화된 오류","Structured / Authoritative Error",
"출처·구조가 붙은 채 퍼지는 오류. 그럴듯해서 AI가 사실로 받아들이기 쉽다.",
["잘못된 정보라도 표·인용·권위 있는 형식을 갖추면 AI가 신뢰하고 재인용해 오류가 굳어질 수 있습니다. 우리 회사에 대한 잘못된 정보가 이렇게 퍼지면 정정이 어렵습니다."],
"messeze는 정확한 1차 정보를 선제적으로 축적해, 잘못된 정보가 자리 잡기 전에 올바른 사실이 기본값이 되게 합니다.",
["hallucination","grounding","corpus-consensus"])

t("graphrag","ai","GraphRAG","GraphRAG",
"지식 그래프를 RAG에 결합해, 문서뿐 아니라 실체 간 관계까지 근거로 답을 만드는 방식.",
["일반 RAG가 비슷한 문장을 찾아온다면, GraphRAG는 '이 회사—이 제품—이 인증'처럼 연결된 관계망을 함께 활용해 더 정확하고 맥락 있는 답을 냅니다."],
"회사·제품·인증·수상이 그래프로 잘 연결돼 있으면 GraphRAG 기반 AI가 우리를 더 풍부하게 설명합니다.",
["rag","knowledge-graph","entity"])

t("bitemporal","ai","시간성","Bitemporal Modeling",
"사실이 참이던 기간과 시스템이 그것을 알게 된 시점을 구분해 다루는 시간 모델링.",
["'2024년에 인증을 받았다'는 사실과 'AI가 그것을 2025년에 알았다'는 시점은 다릅니다. 시간성을 구분하지 못하면 AI가 옛 정보를 현재로 말하거나 최신 변화를 놓칩니다."],
"messeze는 갱신 시점을 명확히 남겨, AI가 우리 회사의 최신 상태를 정확히 반영하게 합니다.",
["freshness","knowledge-cutoff","grounding"])

t("corpus-consensus","ai","코퍼스 합의","Corpus Consensus",
"여러 독립된 출처가 같은 사실을 일관되게 말하는 상태. AI가 사실로 확신하는 근거.",
["AI는 한 곳에만 있는 정보보다 여러 곳에서 교차 확인되는 정보를 신뢰합니다. 언론·홈페이지·블로그·외부 채널이 같은 사실을 말할 때 그 사실은 '합의된 진실'로 취급됩니다."],
"messeze는 여러 채널에 일관된 기업 정보를 배포해 코퍼스 합의를 만들고, AI가 우리를 확신하게 합니다.",
["citation-vs-mention","entity-alignment","eeat"])

t("answer-orchestration","ai","응답 정책·랭킹","Answer Orchestration",
"검색된 근거가 그대로 답이 되는 게 아니라, 정책·랭킹·필터를 거쳐 최종 출력이 정해지는 단계.",
["같은 자료를 찾아와도 AI 서비스마다 안전 정책, 출처 랭킹, 노출 필터가 달라 최종 답과 인용 출처가 달라집니다. 검색에 걸리는 것과 실제로 인용되는 것은 별개입니다."],
"messeze는 여러 AI의 응답을 관측해, 실제로 인용까지 이어지는 출처 조건에 맞춰 콘텐츠를 다듬습니다.",
["ranking-signals","share-of-voice","geo-signal"])

t("whitespace","onpage","화이트스페이스","Whitespace",
"아직 아무도 제대로 답하지 않은 주제의 공백. 선점하면 그 질문의 기본 답이 된다.",
["경쟁이 몰린 키워드보다, 고객이 궁금해하지만 좋은 답이 없는 틈새 질문을 먼저 채우면 AI가 그 주제에서 우리를 유일한 답으로 인용하기 쉽습니다."],
"messeze는 업종별로 답이 비어 있는 질문을 찾아 선제적으로 채워, 경쟁이 적은 곳에서 인용을 확보합니다.",
["information-gain","self-contained","query-fanout"])

t("observation-vs-inference","ai","관측 vs 추정","Observation vs Inference",
"실제로 측정 가능한 것(관측)과 추측만 되는 것(추정)의 경계.",
["'ChatGPT 답변에 우리 회사가 나왔다'는 관측이지만, '그래서 매출이 올랐다'는 추정입니다. GEO 성과는 관측 가능한 신호를 근거로 삼아야 과장 없이 정직합니다."],
"messeze 리포트는 관측된 AI 노출·인용만 성과로 보고하고, 추정은 추정이라고 구분해 전합니다.",
["geo-signal","share-of-voice","citation-vs-mention"])

t("closed-loop","ai","폐쇄루프 되먹임","Closed-Loop Feedback",
"관측 → 역산 → 작성 → 재관측으로 이어지는 닫힌 개선 순환.",
["AI 응답을 관측하고, 왜 그렇게 답했는지 역산하고, 부족한 부분을 콘텐츠로 채운 뒤, 다시 관측해 효과를 확인하는 순환입니다. 한 번의 작업이 아니라 매달 도는 루프입니다."],
"messeze의 월간 운영은 이 폐쇄루프 그대로 — 관측·개선·재관측을 반복해 인용을 늘립니다.",
["quality-reverse-eng","geo-signal","observation-vs-inference"])

t("temperature-sampling","ai","Temperature·샘플링","Temperature · Sampling",
"AI가 다음 단어를 고를 때의 무작위성을 조절하는 값. 같은 질문에도 답이 조금씩 달라지는 이유.",
["Temperature가 높으면 답이 다양해지고 낮으면 일관됩니다. 그래서 같은 질문을 여러 번 물어야 우리 브랜드가 얼마나 안정적으로 인용되는지 알 수 있습니다."],
"messeze는 답의 무작위성을 감안해 여러 번·여러 엔진으로 관측하여 인용 안정성을 측정합니다.",
["multi-ai-cross-analysis","observation-vs-inference","hallucination"])

t("geo-signal","ai","GEO Signal","GEO Signal",
"AI 응답에서 실제로 관측 가능한 신호(등장·인용·출처 링크)만 모아 성과의 근거로 삼는 것.",
["AI 내부 알고리즘은 볼 수 없지만, 응답에 우리가 등장했는지·인용됐는지·경쟁사 대비 얼마나 나오는지는 관측할 수 있습니다. 이 관측값이 GEO의 정직한 성과 지표입니다."],
"messeze는 GEO Signal을 정기 수집해, 짐작이 아닌 관측된 데이터로 성과를 보고합니다.",
["share-of-voice","observation-vs-inference","closed-loop"])

t("quality-reverse-eng","ai","품질 역산","Quality Reverse-Engineering",
"이미 AI에 인용되는 콘텐츠를 뜯어보고, 인용되는 기준을 거꾸로 알아내는 작업.",
["지금 AI가 인용하는 글의 구조·문장·출처 형태를 분석하면, 어떤 콘텐츠가 선택되는지 패턴이 보입니다. 그 기준에 맞춰 우리 콘텐츠를 설계합니다."],
"messeze는 인용되는 콘텐츠를 역산해, 검증된 기준에 맞춰 우리 페이지를 만듭니다.",
["closed-loop","liftable-claim","answer-first"])

t("lab-style-geo","ai","실험실형 GEO","Lab-style GEO",
"통제된 프롬프트 실험을 반복해 AI가 무엇을 인용하는지 역설계하는 방식.",
["같은 조건에서 질문을 바꿔가며 AI 반응을 실험실처럼 관찰하면, 어떤 요인이 인용을 좌우하는지 근거 있게 파악할 수 있습니다. 감이 아니라 실험으로 GEO를 다룹니다."],
"messeze는 업종별 질문을 실험적으로 관측해, 추측이 아닌 데이터로 최적화 방향을 잡습니다.",
["quality-reverse-eng","multi-ai-cross-analysis","geo-signal"])

t("multi-ai-cross-analysis","ai","다중 AI 교차분석","Multi-AI Cross-Analysis",
"ChatGPT·Gemini·Perplexity·Claude 등 여러 AI의 답을 동시에 비교 분석하는 방식.",
["엔진마다 학습 데이터와 정책이 달라 인용하는 출처가 다릅니다. 여러 AI를 교차로 보면 우리가 어디서 강하고 어디서 빠지는지, 어떤 채널을 보강해야 하는지 드러납니다."],
"messeze는 주요 AI를 함께 관측해, 특정 엔진에 치우치지 않는 균형 잡힌 노출을 만듭니다.",
["share-of-voice","geo-signal","temperature-sampling"])

CAT_BY_KEY = {c[0]: c for c in CATS}

# ---------------- 인덱스 페이지 ----------------
INDEX_CSS = CSS + """
.ghero{padding:60px 0 36px;text-align:center;background:linear-gradient(180deg,#F4F9FF,#fff)}
.ghero .eyebrow{display:inline-flex;font-size:13.5px;font-weight:700;color:var(--cobalt);margin-bottom:14px}
.ghero h1{font-size:clamp(28px,4vw,44px)}
.ghero p{font-size:16px;color:var(--body);margin:14px auto 0;max-width:520px}
.gsearch{position:relative;max-width:440px;margin:28px auto 0}
.gsearch input{width:100%;background:#fff;border:1.5px solid var(--line-2);border-radius:14px;padding:14px 16px 14px 44px;font-family:var(--sans);font-size:15px;box-shadow:var(--sh-sm);transition:.18s}
.gsearch input:focus{outline:none;border-color:var(--cobalt)}
.gsearch svg{position:absolute;left:15px;top:50%;transform:translateY(-50%);width:17px;height:17px;color:var(--mut)}
.inits{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;padding:26px 0 0;max-width:720px;margin:0 auto}
.inits button{font-family:var(--sans);font-weight:700;font-size:13.5px;min-width:38px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 11px;cursor:pointer;color:var(--body);transition:.15s}
.inits button:hover{border-color:var(--cobalt);color:var(--cobalt)}
.inits button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.gmain{padding:44px 0 10px}
.gsec{margin-bottom:52px}
.gsec .gh{display:flex;align-items:baseline;gap:12px;margin-bottom:18px}
.gsec .gh h2{font-size:21px}
.gsec .gh span{font-size:13px;color:var(--mut);font-weight:600}
.tgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.tcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;transition:.18s;display:flex;flex-direction:column}
.tcard:hover{box-shadow:var(--sh);transform:translateY(-2px);border-color:var(--line-2)}
.tcard .ko{font-size:16.5px;font-weight:800;letter-spacing:-.02em}
.tcard .en{font-size:12px;font-weight:600;color:var(--cobalt);margin-top:3px}
.tcard p{font-size:13.5px;color:var(--body);line-height:1.55;margin-top:10px;flex:1}
.tcard .go{margin-top:12px;font-size:12.5px;font-weight:800;color:var(--mut)}
.tcard:hover .go{color:var(--cobalt)}
.gempty{text-align:center;color:var(--mut);padding:50px 0;font-size:15px}
@media(max-width:900px){.tgrid{grid-template-columns:1fr 1fr}}
@media(max-width:580px){.tgrid{grid-template-columns:1fr}}
"""

def build_index():
    data = [{k: x[k] for k in ("slug","cat","ko","en","short")} for x in T]
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SEO·AEO·GEO 용어사전 | messeze — AI 검색 시대의 홍보 용어를 쉽게</title>
<meta name="description" content="SEO부터 AEO·GEO, 보도자료·애드버토리얼까지 — AI 검색 시대의 기업 홍보 용어 {len(T)}개를 쉽게 풀어낸 messeze 용어사전.">
{FONT_LINKS}
<script type="application/ld+json">{json.dumps({
  "@context":"https://schema.org","@type":"DefinedTermSet",
  "name":"messeze SEO·AEO·GEO 용어사전",
  "description":"AI 검색 시대의 기업 홍보 용어를 쉽게 풀어낸 사전",
  "hasDefinedTerm":[{"@type":"DefinedTerm","name":x["ko"],"alternateName":x["en"],"description":x["short"]} for x in T]
}, ensure_ascii=False)}</script>
<style>{INDEX_CSS}</style></head><body>
{nav(1)}
<section class="ghero"><div class="wrap">
<span class="eyebrow">무료 리소스 · {len(T)}개 용어</span>
<h1>SEO·AEO·GEO <span class="co">용어사전</span></h1>
<p>AI 검색 시대의 기업 홍보 용어를 쉽게 풀었습니다. 언론홍보(PR) 용어까지 — 홍보 담당자의 첫 사전.</p>
<div class="gsearch"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/></svg><input id="gq" type="search" placeholder="용어를 검색하세요 (예: AEO, 보도자료)"></div>
<div class="inits" id="inits"></div>
</div></section>
<main class="wrap gmain" id="gapp"></main>
{cta(1)}
{foot(1)}
<script>
const TERMS={json.dumps(data, ensure_ascii=False)};
const CATS={json.dumps([[c[0],c[1],c[2]] for c in CATS], ensure_ascii=False)};
const CHO=['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'];
const DBL={{'ㄲ':'ㄱ','ㄸ':'ㄷ','ㅃ':'ㅂ','ㅆ':'ㅅ','ㅉ':'ㅈ'}};
function initialOf(s){{
  const c=s.trim()[0];
  const code=c.charCodeAt(0);
  if(code>=0xAC00&&code<=0xD7A3){{let ch=CHO[Math.floor((code-0xAC00)/588)];return DBL[ch]||ch;}}
  if(/[a-zA-Z]/.test(c))return c.toUpperCase();
  return '#';
}}
TERMS.forEach(t=>t.init=initialOf(t.ko));
const app=document.getElementById('gapp'),initsEl=document.getElementById('inits'),gq=document.getElementById('gq');
let curInit='전체';
function card(t){{return `<a class="tcard" href="terms/${{t.slug}}.html"><span class="ko">${{t.ko}}</span><span class="en">${{t.en}}</span><p>${{t.short}}</p><span class="go">자세히 →</span></a>`}}
function grid(list){{return list.length?`<div class="tgrid">${{list.map(card).join('')}}</div>`:`<div class="gempty">검색 결과가 없습니다.</div>`}}
function render(){{
  const kw=gq.value.trim().toLowerCase();
  if(kw){{
    const hits=TERMS.filter(t=>(t.ko+t.en+t.short).toLowerCase().includes(kw));
    app.innerHTML=`<div class="gsec"><div class="gh"><h2>'${{gq.value.trim()}}' 검색 결과</h2><span>${{hits.length}}개</span></div>${{grid(hits)}}</div>`;
    return;
  }}
  if(curInit!=='전체'){{
    const hits=TERMS.filter(t=>t.init===curInit);
    app.innerHTML=`<div class="gsec"><div class="gh"><h2>${{curInit}}</h2><span>${{hits.length}}개</span></div>${{grid(hits)}}</div>`;
    return;
  }}
  app.innerHTML=CATS.map(([k,name,desc])=>{{
    const list=TERMS.filter(t=>t.cat===k);
    return `<div class="gsec"><div class="gh"><h2>${{name}}</h2><span>${{desc}} · ${{list.length}}개</span></div>${{grid(list)}}</div>`;
  }}).join('');
}}
function renderInits(){{
  const avail=[...new Set(TERMS.map(t=>t.init))];
  const ko=CHO.filter(c=>!DBL[c]&&avail.includes(c));
  const en=avail.filter(c=>/[A-Z]/.test(c)).sort();
  const all=['전체',...ko,...en];
  initsEl.innerHTML=all.map(c=>`<button class="${{c===curInit?'on':''}}" data-i="${{c}}">${{c}}</button>`).join('');
}}
initsEl.addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;curInit=b.dataset.i;gq.value='';renderInits();render();}});
gq.addEventListener('input',()=>{{curInit='전체';renderInits();render();}});
renderInits();render();
</script>
</body></html>"""

# ---------------- 용어 상세 페이지 ----------------
TERM_CSS = CSS + """
.crumb{font-size:13.5px;font-weight:600;color:var(--mut);padding:32px 0 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.crumb a:hover{color:var(--cobalt)}
.crumb .cat{color:var(--cobalt);font-weight:700}
.thead{max-width:720px;margin:0 auto;padding:26px 0 8px}
.thead h1{font-size:clamp(26px,3.6vw,38px)}
.thead .en{font-size:14.5px;font-weight:700;color:var(--cobalt);margin-top:8px}
.defbox{max-width:720px;margin:24px auto 0;background:var(--sky);border-left:4px solid var(--cobalt);border-radius:0 16px 16px 0;padding:22px 26px;font-size:16.5px;font-weight:700;line-height:1.6;color:var(--navy)}
.defbox .lb{display:block;font-size:11.5px;font-weight:800;color:var(--cobalt);letter-spacing:.04em;margin-bottom:8px}
.tbody{max-width:720px;margin:0 auto;padding:30px 0 0}
.tbody p{font-size:16px;color:#333C4E;line-height:1.85;margin-bottom:24px}
.whybox{max-width:720px;margin:8px auto 0;background:var(--ink);color:#fff;border-radius:16px;padding:24px 28px;position:relative;overflow:hidden}
.whybox::before{content:"";position:absolute;inset:0;background:radial-gradient(360px 180px at 92% 100%,rgba(43,92,255,.4),transparent 60%)}
.whybox .lb{position:relative;font-size:11.5px;font-weight:800;color:#7FA0FF;letter-spacing:.04em;margin-bottom:8px}
.whybox p{position:relative;font-size:15px;line-height:1.7;color:#DDE4F2;font-weight:600}
.rel{max-width:720px;margin:40px auto 0}
.rel h3{font-size:17px;margin-bottom:14px}
.rel .chips{display:flex;flex-wrap:wrap;gap:9px}
.rel a{font-size:13.5px;font-weight:700;background:#fff;border:1px solid var(--line);border-radius:999px;padding:9px 16px;transition:.15s}
.rel a:hover{border-color:var(--cobalt);color:var(--cobalt)}
.backrow{max-width:720px;margin:36px auto 0}
.backrow a{font-size:14px;font-weight:700;color:var(--cobalt)}
"""

def build_term(x):
    cat = CAT_BY_KEY[x["cat"]]
    rel_links = ""
    for slug in x["rel"]:
        r = next((y for y in T if y["slug"]==slug), None)
        if r: rel_links += f'<a href="{r["slug"]}.html">{r["ko"]}</a>'
    ld = json.dumps({
      "@context":"https://schema.org",
      "@graph":[
        {"@type":"DefinedTerm","@id":f"https://messeze.example/glossary/terms/{x['slug']}.html#term",
         "name":x["ko"],"alternateName":x["en"],"description":x["short"],
         "inDefinedTermSet":{"@type":"DefinedTermSet","name":"messeze SEO·AEO·GEO 용어사전"}},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"용어사전","item":"../index.html"},
          {"@type":"ListItem","position":2,"name":x["ko"]}]}
      ]}, ensure_ascii=False)
    paras = "\n".join(f"<p>{p}</p>" for p in x["paras"])
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{x['ko']} 뜻 — {x['en']} | messeze 용어사전</title>
<meta name="description" content="{x['short']}">
{FONT_LINKS}
<script type="application/ld+json">{ld}</script>
<style>{TERM_CSS}</style></head><body>
{nav(2)}
<div class="wrap crumb"><a href="../index.html">용어사전</a><span>›</span><span class="cat">{cat[1]}</span></div>
<div class="wrap thead"><h1>{x['ko']}</h1><div class="en">{x['en']}</div></div>
<div class="wrap"><div class="defbox"><span class="lb">한 줄 정의</span>{x['short']}</div></div>
<article class="wrap tbody">{paras}</article>
<div class="wrap"><div class="whybox"><div class="lb">MESSEZE 관점</div><p>{x['why']}</p></div></div>
<div class="wrap rel"><h3>관련 용어</h3><div class="chips">{rel_links}</div></div>
<div class="wrap backrow"><a href="../index.html">← 용어사전 전체 보기</a></div>
{cta(2)}
{foot(2)}
</body></html>"""

# ---------------- 실행 ----------------
with io.open(os.path.join(ROOT, "glossary", "index.html"), "w", encoding="utf-8") as f:
    f.write(build_index())
for x in T:
    with io.open(os.path.join(TERMS_DIR, x["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(build_term(x))
print("OK: glossary/index.html +", len(T), "terms")
