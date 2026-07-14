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
<a class="mega-brand" href="{p}index.html"><span class="bw2">messeze</span><p>검색량이 없어도,<br>AI가 먼저 추천하는 회사로</p></a>
<div class="mega-col"><h5>서비스</h5>
<a href="{p}services/visibility.html"><b>AI 가시성 평가</b><span>AI가 우리 회사를 아는지부터</span></a>
<a href="{p}services/website-renewal.html"><b>홈페이지 수정·리뉴얼</b><span>AI가 읽는 구조로 정비</span></a>
<a href="{p}services/website-build.html"><b>홈페이지 제작</b><span>질문이 페이지가 되는 설계</span></a>
<a href="{p}services/own-blog.html"><b>자사 블로그 운영</b><span>도메인에 쌓이는 전문성</span></a>
<a href="{p}services/channels.html"><b>외부 채널 운영</b><span>네이버·티스토리·구글 블로거</span></a>
<a href="{p}services/press.html"><b>언론 배포</b><span>기자 매칭 · 보도자료 · 기사화</span></a></div>
<div class="mega-col"><h5>무료 도구</h5>
<a href="{p}check.html"><b>AI 가시성 체크</b><span>URL만 넣으면 30초 진단</span></a>
<a href="{p}pricing.html#quiz"><b>30초 플랜 추천</b><span>3가지 질문으로 플랜 찾기</span></a>
<div class="gap"></div><h5>요금</h5>
<a href="{p}pricing.html"><b>플랜 비교</b><span>기본형 · 성장형 · 기업형</span></a>
<a href="{p}pricing.html#faq"><b>요금 FAQ</b><span>약정 · 수량 · 바우처 연계</span></a></div>
<div class="mega-col"><h5>리소스</h5>
<a href="{p}blog/index.html"><b>블로그</b><span>AI 검색 시대의 홍보 인사이트</span></a>
<a href="{p}glossary/index.html"><b>용어사전</b><span>SEO·AEO·GEO·PR 용어 35개</span></a>
<div class="gap"></div><h5>많이 읽는 글</h5>
<a href="{p}blog/posts/aeo-geo-seo.html"><b>AEO·GEO·SEO 차이</b><span>세 가지 최적화 쉽게 정리</span></a>
<a href="{p}blog/posts/manufacturer-case.html"><b>제조기업 3개월 시나리오</b><span>AI에 발견되기까지</span></a></div>
</div></div>"""

MEGA_JS = """<script>
(function(){const p=document.getElementById('mega'),t=document.querySelector('.nav-menu'),b=document.getElementById('burger');if(!p)return;let m;const o=()=>{clearTimeout(m);p.classList.add('on')},c=()=>{m=setTimeout(()=>p.classList.remove('on'),140)};if(t){t.addEventListener('mouseenter',o);t.addEventListener('mouseleave',c);}if(window.matchMedia('(hover:hover)').matches){p.addEventListener('mouseenter',o);p.addEventListener('mouseleave',c);}if(b){b.addEventListener('click',()=>{const on=p.classList.toggle('on');b.classList.toggle('on',on);});p.addEventListener('click',e=>{if(e.target.closest('a')){p.classList.remove('on');b.classList.remove('on');}});}})();
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
</div><div class="foot-b"><span>© 2026 messeze</span><span>검색량이 없어도, AI가 먼저 추천하는 회사로</span></div></div></footer>"""

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
