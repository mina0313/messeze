# -*- coding: utf-8 -*-
"""messeze 블로그 정적 페이지 생성기 (salesmap.kr/blog 기능 미러)
실행: python build-blog.py  →  blog/index.html + blog/posts/*.html 생성"""
import os, json, io

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(ROOT, "blog", "posts")
os.makedirs(POSTS_DIR, exist_ok=True)

# ---------------- 공통 토큰/스타일 ----------------
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
.foot{background:#070D1C;color:#7C879D;padding:52px 0 38px;margin-top:0}
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
.cover{position:absolute;inset:0;width:100%;height:100%;display:block;object-fit:cover;z-index:0}
.card .thumb::after,.pcover::after,.rcard .thumb::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(16,31,63,.06) 42%,rgba(9,17,35,.55));z-index:1;pointer-events:none}
.card .thumb .tag,.pcover .tag{z-index:2}
.card:hover .thumb .cover,.rcard:hover .thumb .cover{transform:scale(1.06);transition:transform .6s ease}
.card .thumb .cover,.rcard .thumb .cover{transition:transform .6s ease}
"""

def mega(p):
    return f"""<div class="mega" id="mega"><div class="wrap mega-in">
<a class="mega-brand" href="{p}index.html"><span class="bw2">messeze</span><p>사람에게만 보이는 홍보에서,<br>AI가 읽는 홍보로</p></a>
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
(function(){const p=document.getElementById('mega'),t=document.querySelector('.nav-menu'),b=document.getElementById('burger');if(!p)return;let m;const o=()=>{clearTimeout(m);p.classList.add('on')},c=()=>{m=setTimeout(()=>p.classList.remove('on'),140)};if(t){t.addEventListener('mouseenter',o);t.addEventListener('mouseleave',c);}if(window.matchMedia('(hover:hover)').matches){p.addEventListener('mouseenter',o);p.addEventListener('mouseleave',c);}if(b){b.addEventListener('click',()=>{const on=p.classList.toggle('on');b.classList.toggle('on',on);});p.addEventListener('click',e=>{if(e.target.closest('a')){p.classList.remove('on');b.classList.remove('on');}});}})();
</script>"""

LOGO = """<svg viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4H23a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H14l-4 4.5V22H7a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3Z"/><line x1="9.5" y1="10" x2="20.5" y2="10"/><line x1="9.5" y1="13.5" x2="20.5" y2="13.5"/><line x1="9.5" y1="17" x2="16.5" y2="17"/></svg>"""

# ---------------- 글 데이터 (회의록 §10 가이드 주제) ----------------
POSTS = [
 dict(slug="aeo-geo-seo", cat="AI 가시성", title="AEO·GEO·SEO, 무엇이 어떻게 다른가요?",
  desc="검색 최적화의 세 축을 처음 듣는 분도 이해할 수 있게 정리했습니다. AI 검색 시대에 기업이 먼저 챙겨야 할 순서까지.",
  date="2026-07-10", grad="linear-gradient(135deg,#101F3F,#2B5CFF)",
  body="""
<p>기업 홍보 담당자라면 최근 <b>AEO, GEO</b>라는 낯선 단어를 자주 들으셨을 겁니다. 오랫동안 알던 SEO와 무엇이 다른 걸까요? 결론부터 말하면, 세 가지는 서로 대체 관계가 아니라 <b>'누가 읽느냐'가 다른 최적화</b>입니다.</p>
<h2>SEO — 검색엔진이 읽습니다</h2>
<p>SEO(Search Engine Optimization)는 네이버·구글 같은 검색엔진이 우리 페이지를 잘 이해하고 상위에 올리도록 만드는 작업입니다. 키워드, 제목 구조, 내부 링크, 페이지 속도 같은 요소가 핵심이었죠. 지금까지의 온라인 마케팅은 대부분 여기에 집중해 왔습니다.</p>
<h2>AEO — AI가 '답변'으로 인용하도록</h2>
<p>AEO(Answer Engine Optimization)는 ChatGPT·Gemini·Perplexity 같은 AI가 사용자의 질문에 답할 때 <b>우리 기업의 정보를 인용하도록</b> 만드는 최적화입니다. AI는 링크 목록을 보여주는 게 아니라 하나의 답을 만들어 냅니다. 그 답 안에 들어가려면 다음이 필요합니다.</p>
<ul>
<li>고객이 실제로 물어볼 질문에 대한 명확한 답변형 콘텐츠</li>
<li>여러 신뢰 가능한 출처(언론, 홈페이지, 전문 칼럼)에서 확인되는 일관된 정보</li>
<li>기계가 읽기 쉬운 구조화된 페이지</li>
</ul>
<h2>GEO — 생성형 AI 검색 전반에 대응</h2>
<p>GEO(Generative Engine Optimization)는 AEO를 포함하는 더 넓은 개념으로, 생성형 AI 기반 검색 경험 전반에서 우리 기업이 발견되고 추천되도록 만드는 전략입니다. 콘텐츠뿐 아니라 기업 정보의 축적 방식, 출처의 다양성, 최신성 관리까지 포함합니다.</p>
<blockquote>핵심은 이것입니다. <b>검색량이 없는 B2B·제조기업도 AI에게는 발견될 수 있습니다.</b> AI는 검색량이 아니라 '읽을 수 있는 정보의 양과 신뢰도'로 기업을 판단하기 때문입니다.</blockquote>
<h2>그래서 무엇부터 해야 하나요?</h2>
<p>순서는 명확합니다. ① 현재 AI 검색에서 우리 기업이 어떻게 인식되는지 진단하고 ② 고객이 AI에게 물어볼 핵심 질문을 5~6개 정의한 뒤 ③ 질문별로 답이 되는 콘텐츠를 홈페이지·언론·외부 채널에 꾸준히 축적하는 것. 이 사이클을 매달 반복하면 대략 3개월 시점부터 AI 검색에 반영되기 시작합니다.</p>
"""),
 dict(slug="indexed-not-cited", cat="AI 가시성", title="구글엔 나오는데 왜 ChatGPT엔 안 나올까요?",
  desc="분명 색인은 됐는데 AI 답변엔 우리 회사가 없습니다. 색인과 인용은 다른 관문이기 때문입니다. 인용되는 페이지의 조건까지.",
  date="2026-07-14", grad="linear-gradient(135deg,#0E2148,#3D6BFF)",
  body="""
<p>홈페이지를 구글에서 검색하면 잘 나옵니다. 그런데 같은 내용을 ChatGPT나 Perplexity에 물어보면 우리 회사 이야기는 어디에도 없습니다. 분명 '색인'은 됐는데 왜 AI는 우리를 인용하지 않을까요? 답은 간단합니다. <b>색인과 인용은 완전히 다른 관문</b>이기 때문입니다.</p>
<h2>색인은 '수집', 인용은 '신뢰'입니다</h2>
<p>색인(indexing)은 검색엔진이 우리 페이지를 발견해 저장해 두는 단계입니다. 검색 결과에 뜨려면 반드시 필요하지만, 그저 '창고에 들어간 것'에 가깝습니다. 반면 AI가 답을 만들 때 우리 정보를 <b>근거로 골라 쓰는 것(인용)</b>은 훨씬 높은 문턱입니다. AI는 저장된 수많은 문서 중 '믿을 수 있고, 답으로 쓰기 좋은' 것만 추려서 인용합니다.</p>
<h2>색인됐는데 인용되지 않는 4가지 이유</h2>
<ul>
<li><b>답이 아니라 홍보문이라서.</b> AI는 질문에 대한 명확한 답을 찾습니다. '업계 최고의 파트너'가 아니라 '무엇을, 어디까지, 어떤 조건으로' 하는지가 필요합니다.</li>
<li><b>정보가 이미지·PDF에 갇혀서.</b> 화면엔 보여도 텍스트로 읽히지 않으면 AI에게는 없는 정보입니다.</li>
<li><b>출처가 하나뿐이라서.</b> AI는 여러 곳에서 교차 확인되는 사실을 신뢰합니다. 자사 홈페이지 한 곳의 주장만으로는 확신을 주지 못합니다.</li>
<li><b>회사(엔티티)가 웹에서 흐릿해서.</b> 상호·소재지·업종·대표 제품이 일관되게 정리돼 있지 않으면 AI는 '누구인지' 확신하지 못합니다.</li>
</ul>
<blockquote>색인은 '보이는 것', 인용은 '선택받는 것'입니다. 검색 1페이지에 있어도 AI 답변엔 없을 수 있습니다.</blockquote>
<h2>인용되는 페이지는 무엇이 다른가</h2>
<p>AI가 즐겨 인용하는 페이지에는 공통점이 있습니다. ① 질문형 제목과 첫 문단에 바로 나오는 결론, ② 사람뿐 아니라 기계도 읽는 구조화 데이터, ③ 언론·전문 채널 등 여러 출처에서 반복 확인되는 사실, ④ 최근까지 업데이트된 최신성. 이 네 가지가 갖춰질수록 '색인된 문서'에서 '인용되는 근거'로 올라섭니다.</p>
<h2>우리는 지금 어디쯤일까</h2>
<p>확인법은 의외로 단순합니다. 고객이 실제로 물어볼 질문 5~6개를 정해, 주요 AI에 그대로 물어보세요. 우리 회사가 등장하는지, 어떤 출처로 인용되는지, 경쟁사는 어디까지 나오는지 — 이 격차가 그대로 할 일 목록이 됩니다. 색인은 시작일 뿐입니다. 인용까지 가야 비로소 AI 검색에 '노출된' 것입니다.</p>
"""),
 dict(slug="measuring-geo", cat="AI 가시성", title="AI 검색 성과, 무엇으로 측정하나요?",
  desc="클릭 수만으로는 AI 검색 성과가 잡히지 않습니다. 인용률·엔진 커버리지·크롤 신호까지, GEO를 재는 5가지 지표와 추적법.",
  date="2026-07-15", grad="linear-gradient(135deg,#101F3F,#0BBF8C)",
  body="""
<p>"AI 검색 최적화, 그래서 효과가 있긴 한가요?" 가장 많이 받는 질문입니다. 문제는 기존 방식으로는 이 효과가 잘 안 잡힌다는 데 있습니다. AI 검색은 클릭이 일어나기 <b>전에</b>, 답변 안에서 승부가 나기 때문입니다. 그래서 재는 지표부터 달라야 합니다.</p>
<h2>클릭 수만 봐서는 안 보입니다</h2>
<p>전통적인 SEO는 검색 순위·클릭·유입으로 성과를 쟀습니다. 하지만 AI가 답을 요약해 주는 시대에는, 사용자가 링크를 누르지 않고도 우리 회사를 '알고' 지나갑니다. 눈에 보이는 클릭은 줄어도, AI 답변 속 노출은 늘 수 있습니다. 이 변화를 담으려면 다음 다섯 가지를 봅니다.</p>
<h2>GEO 성과를 재는 5가지 지표</h2>
<ul>
<li><b>① 인용률.</b> 핵심 질문 세트 중 우리 회사가 AI 답변에 등장하는 비율. 가장 직접적인 지표입니다.</li>
<li><b>② 엔진 커버리지.</b> ChatGPT·Gemini·Perplexity·네이버 등 몇 개 엔진이 우리를 인식하는지. 한 곳이 아니라 폭이 중요합니다.</li>
<li><b>③ 노출 맥락.</b> 첫 번째로 추천되는지, 경쟁사와 나란히인지, 어떤 출처(언론·홈페이지·칼럼)를 근거로 인용되는지.</li>
<li><b>④ 크롤 신호.</b> 서버·CDN 로그로 AI 봇이 실제로 우리 페이지를 읽어갔는지 확인합니다. 인용의 전제 조건입니다.</li>
<li><b>⑤ 기반 지표.</b> Core Web Vitals 같은 기술 점수, 구조화 데이터 적용률, 콘텐츠 발행량 — 결과를 만드는 토대입니다.</li>
</ul>
<blockquote>중요한 건 '한 번 재는 것'이 아니라 '같은 자로 매달 재는 것'입니다. 변화의 방향이 곧 전략의 성패입니다.</blockquote>
<h2>감이 아니라 데이터로</h2>
<p>매달 동일한 질문 세트로 다시 측정하면, 지난달 대비 인용률이 올랐는지·어떤 엔진이 새로 우리를 인식했는지가 숫자로 남습니다. messeze는 이 지표들을 월간 리포트로 정리해, 무엇을 얼마나 했고 어떻게 바뀌었는지 투명하게 공유하고 다음 달 우선순위를 함께 정합니다. 측정할 수 없으면 개선할 수 없습니다 — AI 검색도 마찬가지입니다.</p>
"""),
 dict(slug="llms-txt", cat="AI 가시성", title="llms.txt, 정말 효과가 있을까요?",
  desc="AI에게 우리 사이트를 안내하는 llms.txt — 지금 넣어야 할까요? 무엇인지, 현재 실효성, 그리고 우리가 취할 현실적인 태도.",
  date="2026-07-12", grad="linear-gradient(135deg,#0E2148,#5B7CFF)",
  body="""
<p>최근 GEO를 이야기할 때 <b>llms.txt</b>라는 파일이 자주 등장합니다. "이것만 넣으면 AI에 잘 잡힌다"는 말도 들리죠. 결론부터 말하면, 넣어서 손해는 없지만 <b>이것 하나로 노출이 해결되지는 않습니다.</b> 왜 그런지, 우리는 어떤 태도를 취해야 하는지 정리했습니다.</p>
<h2>llms.txt가 뭔가요?</h2>
<p>사이트 최상단(루트)에 두는 간단한 텍스트 파일입니다. 검색 크롤러에게 규칙을 알려주는 robots.txt처럼, <b>AI에게 "우리 사이트의 핵심은 여기입니다"라고 안내</b>하려는 제안입니다. 보통 마크다운으로 회사·서비스의 요점과 중요한 페이지 링크를 정리해 둡니다. AI가 방대한 페이지를 헤매지 않고 핵심을 빠르게 파악하도록 돕자는 취지죠.</p>
<h2>그런데, 정말 효과가 있을까요?</h2>
<p>여기서부터는 냉정하게 볼 필요가 있습니다. 현재 주요 AI 업체들이 llms.txt를 공식적으로 '반드시 읽고 반영한다'고 밝힌 경우는 많지 않습니다. 실제로 이 파일 하나로 유입이나 인용이 뚜렷하게 늘었다는 검증 데이터도 아직 제한적입니다. 표준으로 자리 잡는 과정에 있는, <b>'제안 단계'의 기술</b>이라고 보는 편이 정확합니다.</p>
<blockquote>llms.txt는 '있으면 좋은 보조 신호'입니다. 핵심 엔진이 이 파일을 반드시 본다는 보장은 아직 없습니다.</blockquote>
<h2>그럼 넣지 말아야 하나요?</h2>
<p>아닙니다. 넣는 비용이 거의 들지 않고 위험도 없기 때문에, <b>얹어두는 것 자체는 합리적</b>입니다. 다만 순서를 헷갈리면 안 됩니다. llms.txt를 만들었다고 AI 노출이 해결됐다고 착각하는 것이 가장 위험합니다.</p>
<h2>진짜 효과는 어디서 나오나</h2>
<p>AI가 우리를 인용하게 만드는 힘은 여전히 기본기에서 나옵니다. ① 기계가 읽을 수 있는 페이지 구조와 구조화 데이터, ② 질문에 정면으로 답하는 콘텐츠, ③ 언론·외부 채널까지 여러 출처에서 확인되는 신뢰. llms.txt는 이 토대 위에 얹는 <b>마지막 5%</b>일 뿐입니다. 순서는 언제나 기본기가 먼저입니다. 얹어두되, 기대는 현실적으로 — 그것이 llms.txt를 대하는 올바른 태도입니다.</p>
"""),
 dict(slug="ai-hallucination-brand", cat="AI 가시성", title="AI가 우리 회사를 틀리게 말할 때",
  desc="AI가 없는 사실을 지어내거나 오래된 정보로 답하면 그대로 브랜드 타격이 됩니다. 왜 생기는지, 기업이 미리 대비하는 법.",
  date="2026-07-13", grad="linear-gradient(135deg,#12203F,#4A6BFF)",
  body="""
<p>고객이 AI에게 우리 회사를 물었는데, AI가 <b>틀린 답</b>을 내놓는다면 어떨까요? 있지도 않은 제품을 말하거나, 몇 년 전 폐기한 정보를 사실처럼 답하거나, 경쟁사와 혼동하기도 합니다. 사람은 "AI가 틀렸겠지"라고 걸러주지 않습니다. 그 답을 그대로 믿죠. 그래서 AI의 오류는 곧 브랜드의 손실이 됩니다.</p>
<h2>왜 AI는 틀린 답을 만들까</h2>
<p>AI는 모르면 '모른다'고 하기보다, 그럴듯한 답을 <b>지어내는(환각, hallucination)</b> 경향이 있습니다. 특히 우리 회사에 대해 읽을 수 있는 정확한 정보가 부족하면, AI는 빈칸을 추정·오래된 캐시·엉뚱한 타사 정보로 메웁니다. <b>정보의 공백이 곧 오류의 원인</b>입니다.</p>
<blockquote>침묵은 공백을 남기고, 공백은 오류로 채워집니다. AI가 틀리게 말하는 회사는, 대개 스스로 말하지 않은 회사입니다.</blockquote>
<h2>기업이 지금 대비하는 법</h2>
<ul>
<li><b>1차 정보를 명확·최신으로.</b> 회사 개요, 제품 스펙, 가격 정책, 자주 묻는 질문을 홈페이지에 정확하게, 그리고 최근 날짜로 정리합니다.</li>
<li><b>사실을 기계가 읽게.</b> 구조화 데이터(Organization·Product·FAQ 스키마)로 핵심 사실을 명시하면 AI가 추정할 여지가 줄어듭니다.</li>
<li><b>여러 출처에서 일관되게.</b> 홈페이지·언론·외부 채널의 정보가 서로 어긋나지 않게 맞춰 두면 AI가 무엇이 맞는지 확신합니다.</li>
<li><b>주기적으로 모니터링.</b> 매달 주요 AI에 우리 회사를 물어보고, 틀린 답이 나오면 그 근거가 될 콘텐츠를 보강합니다.</li>
</ul>
<h2>기다리기보다, 먹이는 쪽이 빠릅니다</h2>
<p>최근 해외에서는 AI 답변 오류의 책임을 누구에게 물을지에 대한 논의도 시작됐습니다. 하지만 제도가 정리되기를 기다리는 사이에도 고객은 AI에게 묻습니다. 가장 현실적인 방어는, AI가 참고할 <b>정확한 정보를 우리가 먼저, 꾸준히 제공하는 것</b>입니다. 정보를 쌓아 둔 기업만이 AI가 자신을 정확히 말하게 만들 수 있습니다.</p>
"""),
 dict(slug="ai-pr-guide", cat="AI 가시성", title="AI 검색 시대의 기업 홍보법: 무엇이 달라졌나",
  desc="고객은 이제 검색 결과를 비교하지 않고 AI에게 물어봅니다. 기업 홍보가 바뀌어야 하는 이유와 새 원칙 4가지.",
  date="2026-07-08", grad="linear-gradient(135deg,#16295C,#419CFF)",
  body="""
<p>불과 몇 년 전까지 고객은 검색창에 키워드를 넣고, 여러 사이트를 열어 비교했습니다. 지금은 다릅니다. <b>AI가 먼저 정보를 검토하고, 기업이나 제품을 추천합니다.</b> 사용자는 그 답을 보고 판단하죠. 이 변화가 기업 홍보에 주는 의미는 생각보다 큽니다.</p>
<h2>정보가 부족한 기업은 조용히 제외됩니다</h2>
<p>AI는 답변을 만들 때 여러 출처에서 확인되는 정보를 우선합니다. 홈페이지 한 곳에만 정보가 있는 기업, 몇 년 전 기사 한 건이 전부인 기업은 AI 입장에서 '확신할 수 없는 후보'입니다. 경쟁사가 언론보도·칼럼·구조화된 홈페이지로 정보를 쌓고 있다면, 추천은 그쪽으로 갑니다.</p>
<h2>새로운 홍보의 원칙 4가지</h2>
<ul>
<li><b>① 질문에서 출발하세요.</b> "우리가 알리고 싶은 것"이 아니라 "고객이 AI에게 물어볼 질문"을 먼저 정의합니다. 예: "베트남 수출 경험이 있는 ○○ 제조업체는 어디인가?"</li>
<li><b>② 출처를 여러 곳에 만드세요.</b> 같은 정보가 언론보도, 홈페이지, 전문 칼럼에서 일관되게 확인될 때 AI의 신뢰가 올라갑니다.</li>
<li><b>③ 일회성이 아니라 누적으로.</b> 기사 몇 건의 반짝 노출보다, 매달 쌓이는 정보 자산이 AI 검색에서는 훨씬 강합니다.</li>
<li><b>④ 홈페이지도 함께 정비하세요.</b> 외부 콘텐츠와 홈페이지가 분리되어 있으면 AI가 맥락을 읽지 못합니다.</li>
</ul>
<h2>검색량이 적은 기업일수록 기회입니다</h2>
<p>산업용 부품·소재·설비처럼 검색량이 적은 업종은 지금까지 블로그·검색광고로 효과를 보기 어려웠습니다. 하지만 AI 검색에서는 다릅니다. 해당 분야에 대해 '읽을 수 있는 정보'를 가진 기업이 드물기 때문에, 먼저 축적을 시작한 기업이 그 분야의 답이 됩니다.</p>
<blockquote>지금 시작하는 기업과 6개월 뒤 시작하는 기업의 격차는, 그대로 AI 추천의 격차가 됩니다.</blockquote>
"""),
 dict(slug="press-release-writing", cat="언론홍보", title="기자가 인용하는 보도자료 작성법",
  desc="보도자료는 '잘 쓴 글'이 아니라 '기사가 되기 쉬운 글'이어야 합니다. 실무에서 바로 쓰는 구조와 체크리스트.",
  date="2026-07-05", grad="linear-gradient(135deg,#0F2350,#1B3C8F)",
  body="""
<p>보도자료의 목적은 하나입니다. <b>기자가 최소한의 수정으로 기사화할 수 있게 만드는 것.</b> 화려한 수식어가 아니라 구조가 승부를 가릅니다.</p>
<h2>사실과 핵심을 앞에 배치하세요</h2>
<p>기자는 하루에도 수십 건의 보도자료를 받습니다. 첫 두 문단 안에 '누가·무엇을·왜 지금'이 없으면 나머지는 읽히지 않습니다. 회사 소개부터 길게 시작하는 보도자료가 가장 흔한 실패 사례입니다.</p>
<h2>기사가 되기 쉬운 구조</h2>
<ul>
<li><b>제목:</b> 업계 관점의 뉴스 가치를 담아 한 줄로. 자사 자랑이 아니라 '변화'를 담습니다.</li>
<li><b>리드문:</b> 핵심 사실 요약. 이 문단만 실려도 기사가 되도록.</li>
<li><b>본문:</b> 배경 → 세부 내용 → 의미 순. 수치와 근거를 포함.</li>
<li><b>인용문:</b> 대표 코멘트는 사실 전달이 아니라 방향성과 의지를 담을 것.</li>
<li><b>회사 소개(보일러플레이트):</b> 맨 끝에 3~4줄로.</li>
</ul>
<h2>피해야 할 표현</h2>
<p>'국내 최초', '업계 최고' 같은 근거 없는 최상급 표현은 기사화 가능성을 떨어뜨립니다. 검증 가능한 사실(인증 취득, 수출 계약, 선정 실적)로 대체하세요. 과장 표현이 많은 보도자료는 스팸으로 분류되기도 합니다.</p>
<h2>애드버토리얼과는 목적이 다릅니다</h2>
<p>보도자료는 기자에게 뉴스거리를 제공하는 것이고, 애드버토리얼은 지면을 확보해 우리가 원하는 메시지를 싣는 것입니다. 신제품 출시·인증·수출 성과처럼 뉴스 가치가 있으면 보도자료, 서비스 소개나 브랜드 스토리는 애드버토리얼이 적합합니다. 두 가지를 상황에 맞게 조합하는 것이 실전 언론홍보입니다.</p>
<blockquote>그리고 잊지 마세요 — 발행된 기사는 AI가 기업을 이해하는 <b>가장 신뢰도 높은 출처</b>가 됩니다. 보도자료 한 건도 AEO 관점에서 설계하면 가치가 두 배가 됩니다.</blockquote>
"""),
 dict(slug="advertorial-vs-press", cat="언론홍보", title="언론홍보와 애드버토리얼, 뭐가 다른가요?",
  desc="비용, 형식, 노출 방식, 활용 시점까지 — 두 방식의 차이를 표로 정리하고 기업 상황별 조합 전략을 제안합니다.",
  date="2026-07-01", grad="linear-gradient(135deg,#1B3C8F,#2B5CFF)",
  body="""
<p>언론홍보를 처음 검토하는 기업이 가장 헷갈리는 것이 <b>일반 보도자료 배포와 애드버토리얼(기사형 광고)의 차이</b>입니다. 명확히 구분하면 예산 낭비를 크게 줄일 수 있습니다.</p>
<h2>한눈에 보는 차이</h2>
<ul>
<li><b>보도자료 배포:</b> 기자에게 뉴스거리를 제공 → 기자가 판단해 기사화. 비용은 낮지만 게재가 보장되지 않고, 내용도 기자가 결정합니다. 그만큼 <b>신뢰도는 가장 높습니다.</b></li>
<li><b>애드버토리얼:</b> 매체 지면을 구매해 기사 형식으로 게재. 게재가 보장되고 내용을 우리가 정합니다. 다만 매체·독자에 따라 광고로 인식될 수 있습니다.</li>
</ul>
<h2>언제 무엇을 쓰나요?</h2>
<p><b>뉴스 가치가 있을 때</b> — 신제품 출시, 인증 취득, 수출 계약, 정부사업 선정, 전시회 참가 — 는 보도자료가 우선입니다. 실제 기사화되면 비용 대비 효과가 가장 큽니다.</p>
<p><b>뉴스거리가 약하지만 알리고 싶은 것</b> — 서비스 상세 소개, 기술력 설명, 브랜드 스토리 — 는 애드버토리얼이 적합합니다. 원하는 메시지를 원하는 시점에 확실히 실을 수 있으니까요.</p>
<h2>AI 검색 관점에서는 '조합'이 답입니다</h2>
<p>AI는 답변을 만들 때 여러 출처를 교차 확인합니다. 보도자료 기반 기사와 애드버토리얼, 그리고 홈페이지·전문 칼럼의 정보가 일관되게 쌓여 있을 때 기업 정보의 신뢰도가 가장 높아집니다. 한 가지 방식만 반복하는 것보다, 월 단위로 두 방식을 계획적으로 섞는 것이 AEO·GEO 관점에서 효과적입니다.</p>
<blockquote>기사 몇 건을 사는 것이 아니라, <b>기업 정보 자산을 설계한다</b>는 관점으로 접근하세요.</blockquote>
"""),
 dict(slug="exhibition-pr", cat="언론홍보", title="전시회 전후, 기업 홍보는 이렇게 합니다",
  desc="전시회 참가비의 효과를 두 배로 만드는 사전·현장·사후 홍보 타임라인. 수출상담회에도 그대로 적용됩니다.",
  date="2026-06-27", grad="linear-gradient(135deg,#101F3F,#0BBF8C)",
  body="""
<p>전시회·수출상담회는 제조기업이 1년 중 가장 큰 비용을 쓰는 마케팅 활동입니다. 그런데 많은 기업이 부스 준비에만 집중하고, <b>홍보는 전시회장 안에서만</b> 합니다. 아까운 일입니다.</p>
<h2>사전 홍보 (D-30 ~ D-7)</h2>
<ul>
<li>참가 확정 시점에 <b>참가 보도자료</b>를 배포합니다. "○○전시회에서 신제품 △△ 첫 공개" 형태가 기사화되기 좋습니다.</li>
<li>홈페이지에 전시회 안내 페이지를 만들고 부스 위치·전시 품목·미팅 신청을 담습니다. 바이어가 사전 검색할 때 발견되는 지점입니다.</li>
<li>해외 전시회라면 현지어 보도자료와 현지 매체 배포를 준비합니다.</li>
</ul>
<h2>현장 (전시 기간)</h2>
<ul>
<li>부스 방문 바이어·미팅 기록을 남기고, 현장 사진을 확보합니다. 사후 콘텐츠의 재료입니다.</li>
<li>현장 이슈(계약 체결, 대규모 상담)가 있으면 당일 짧은 보도자료로 속보성 기사를 노립니다.</li>
</ul>
<h2>사후 홍보 (D+1 ~ D+30)</h2>
<ul>
<li><b>성과 보도자료</b>: 상담 건수, 계약·MOU, 바이어 반응을 정리해 배포합니다. 사전 기사와 이어지면 매체가 받아쓰기 좋습니다.</li>
<li>전시회 후기 칼럼을 홈페이지·블로그에 발행합니다. "○○ 전시회에 참가한 한국 기업"을 AI에게 묻는 바이어에게 답이 되는 콘텐츠입니다.</li>
<li>수집한 바이어에게 보낼 후속 자료에 기사 링크를 포함하면 신뢰도가 올라갑니다.</li>
</ul>
<blockquote>전시회 홍보의 진짜 가치는 전시 기간 3일이 아니라, <b>그 전후로 쌓이는 기록</b>에 있습니다. 이 기록은 다음 해 바이어가 AI에게 물을 때 다시 일합니다.</blockquote>
"""),
 dict(slug="export-pr-strategy", cat="수출·해외 PR", title="수출기업을 위한 국가별 PR 전략",
  desc="베트남·중국·미국은 언론 환경도, 바이어가 정보를 찾는 방식도 다릅니다. 국가별 접근법과 공통 원칙.",
  date="2026-06-22", grad="linear-gradient(135deg,#16295C,#7FA0FF)",
  body="""
<p>해외 바이어도 이제 AI에게 묻습니다. "한국에서 ○○을 만드는 신뢰할 만한 제조사는?" 이 질문에 답이 되려면, <b>목표 시장의 언어와 매체에 우리 기업 정보가 존재해야</b> 합니다. 한국어 콘텐츠만으로는 닿지 않습니다.</p>
<h2>공통 원칙: 현지어 출처 만들기</h2>
<p>국가가 어디든 순서는 같습니다. ① 현지 바이어가 물어볼 질문 정의 → ② 현지어 콘텐츠 제작(홈페이지 다국어 페이지, 보도자료) → ③ 현지 매체·채널 배포 → ④ 반복 축적. 특히 인증·수출 실적·생산 능력처럼 바이어가 확인하고 싶어 하는 정보를 현지어로 명확히 제공하는 것이 핵심입니다.</p>
<h2>베트남 — 성장 시장, 낮은 진입 장벽</h2>
<p>한국 기업에 대한 관심이 높고 현지 매체의 기사화 문턱이 상대적으로 낮습니다. 베트남어 보도자료와 현지 온라인 매체 배포로 비교적 빠르게 출처를 만들 수 있습니다. 전시회·상담회 연계 홍보 효과도 큽니다.</p>
<h2>중국 — 플랫폼 중심 생태계</h2>
<p>구글이 아닌 바이두, 그리고 위챗·샤오홍슈 같은 플랫폼 안에서 정보가 유통됩니다. 중국어 콘텐츠는 필수이고, 어떤 플랫폼에 축적할지 전략이 먼저 서야 합니다. B2B라면 산업 전문 매체와 전시회 연계가 효과적입니다.</p>
<h2>미국 — 신뢰 출처의 기준이 높음</h2>
<p>영문 보도자료의 품질 기준이 높고, 업계 전문지(trade media)의 영향력이 큽니다. 회사 소개보다 데이터와 사례 중심의 콘텐츠가 통합니다. 영문 홈페이지의 완성도가 낮으면 다른 노력이 모두 할인됩니다.</p>
<blockquote>수출바우처 등 정부지원사업으로 해외 홍보 비용을 상당 부분 커버할 수 있습니다. 참여 기업이라면 바우처 항목에 <b>해외 언론홍보·다국어 콘텐츠</b>를 포함해 설계하세요.</blockquote>
"""),
 dict(slug="manufacturer-case", cat="사례", title="검색량 없는 제조기업이 AI에 발견되기까지",
  desc="산업용 부품 제조사를 가정한 3개월 시나리오 — 진단, 질문 설계, 콘텐츠 축적이 실제로 어떻게 진행되는지.",
  date="2026-06-18", grad="linear-gradient(135deg,#0F2350,#2B5CFF)",
  body="""
<p>메세지의 운영 방식을 가장 쉽게 이해하는 방법은 한 기업의 3개월을 따라가 보는 것입니다. 아래는 산업용 정밀부품 제조사 A사를 가정한 시나리오입니다. (특정 기업의 실제 사례가 아닌, 표준 운영 과정을 설명하기 위한 예시입니다.)</p>
<h2>0주차 — 진단: "AI는 A사를 모른다"</h2>
<p>주요 AI 검색에 A사 관련 질문을 던져 봅니다. "국내에서 항공용 정밀부품을 소량 생산하는 업체는?" — A사는 등장하지 않습니다. 홈페이지는 있지만 제품 사양 PDF뿐이고, 언론 기사는 5년 전 1건. AI가 읽을 수 있는 정보가 사실상 없는 상태입니다.</p>
<h2>1~2주차 — 질문 설계</h2>
<p>A사 대표·영업팀과 온보딩 미팅에서 핵심 질문 6개를 정의합니다. 소량 생산, 특정 인증, 수출 경험, 납기 대응 등 <b>실제 바이어가 묻는 언어</b>로요. 이 질문들이 3개월 콘텐츠 계획의 뼈대가 됩니다.</p>
<h2>1개월차 — 첫 축적</h2>
<ul>
<li>홈페이지에 질문-답변 구조의 서비스 페이지 신설 (AEO 구조 적용)</li>
<li>신규 설비 도입 보도자료 1건 배포 → 산업 전문지 2곳 기사화</li>
<li>"항공부품 소량 생산, 무엇을 확인해야 하나" 전문 칼럼 발행</li>
</ul>
<h2>2개월차 — 출처 넓히기</h2>
<ul>
<li>수출 성과 애드버토리얼 1건, 외부 채널(블로그·워드프레스) 콘텐츠 4건</li>
<li>인증 취득 보도자료 → 기사화. 이 시점부터 같은 정보가 서로 다른 출처 4곳에서 확인됩니다.</li>
</ul>
<h2>3개월차 — 변화 확인</h2>
<p>같은 질문을 다시 AI에 던집니다. 이번에는 A사가 후보로 등장하고, 근거로 언론 기사와 홈페이지가 인용됩니다. 월간 리포트에는 질문별 노출 현황과 다음 달 보완 과제가 담깁니다. 축적은 여기서 멈추지 않고 매달 반복됩니다 — 그것이 구독형 관리의 이유입니다.</p>
<blockquote>같은 3개월이라도, 시작이 빠른 기업이 그 분야의 '기본 답변'이 됩니다.</blockquote>
"""),
]

CATS = ["홈", "AI 가시성", "언론홍보", "수출·해외 PR", "사례"]

# ---------------- 썸네일 커버 (SVG, slug별) — 폴백 + aeo-geo-seo용 ----------------
_SVG_COVERS = {
"aeo-geo-seo": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c1a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".6"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><radialGradient id="c1b" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#0BBF8C" stop-opacity=".45"/><stop offset="1" stop-color="#0BBF8C" stop-opacity="0"/></radialGradient><linearGradient id="c1c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#1E46D9"/></linearGradient><filter id="c1s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="252" cy="34" r="92" fill="url(#c1a)"/><circle cx="52" cy="164" r="72" fill="url(#c1b)"/><g filter="url(#c1s)"><rect x="36" y="34" width="150" height="34" rx="17" fill="#fff"/></g><circle cx="57" cy="51" r="8" fill="none" stroke="#2B5CFF" stroke-width="3"/><line x1="63" y1="57" x2="69" y2="63" stroke="#2B5CFF" stroke-width="3" stroke-linecap="round"/><rect x="78" y="47" width="72" height="8" rx="4" fill="#C7D6FF"/><g filter="url(#c1s)"><rect x="58" y="92" width="208" height="58" rx="16" fill="#fff"/></g><rect x="74" y="108" width="26" height="26" rx="9" fill="url(#c1c)"/><text x="87" y="125" font-size="11" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">AI</text><rect x="110" y="107" width="142" height="8" rx="4" fill="#0A1930"/><rect x="110" y="123" width="104" height="7" rx="3.5" fill="#C0C9D8"/><g filter="url(#c1s)"><path d="M264 82l5 12.5 12.5 5-12.5 5-5 12.5-5-12.5-12.5-5 12.5-5z" fill="#0BBF8C"/></g></svg>""",
"ai-pr-guide": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c2a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".55"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="c2c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#1E46D9"/></linearGradient><linearGradient id="c2m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22E0AD"/><stop offset="1" stop-color="#08A97B"/></linearGradient><filter id="c2s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="250" cy="40" r="94" fill="url(#c2a)"/><g filter="url(#c2s)"><rect x="40" y="30" width="240" height="120" rx="18" fill="#fff"/></g><rect x="58" y="48" width="26" height="26" rx="9" fill="url(#c2c)"/><text x="71" y="65" font-size="11" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">AI</text><rect x="94" y="50" width="120" height="8" rx="4" fill="#0A1930"/><rect x="94" y="64" width="80" height="6" rx="3" fill="#C0C9D8"/><rect x="58" y="88" width="204" height="20" rx="8" fill="#EEF3FF"/><circle cx="72" cy="98" r="6" fill="#2B5CFF"/><rect x="86" y="95" width="96" height="6" rx="3" fill="#8FA3D9"/><rect x="224" y="90" width="30" height="16" rx="8" fill="url(#c2m)"/><rect x="58" y="116" width="204" height="20" rx="8" fill="#EEF3FF"/><circle cx="72" cy="126" r="6" fill="#2B5CFF"/><rect x="86" y="123" width="74" height="6" rx="3" fill="#8FA3D9"/><rect x="224" y="118" width="30" height="16" rx="8" fill="url(#c2m)"/></svg>""",
"press-release-writing": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c3a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#0BBF8C" stop-opacity=".4"/><stop offset="1" stop-color="#0BBF8C" stop-opacity="0"/></radialGradient><radialGradient id="c3b" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="c3c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#1E46D9"/></linearGradient><filter id="c3s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="250" cy="150" r="78" fill="url(#c3a)"/><circle cx="70" cy="30" r="60" fill="url(#c3b)"/><g filter="url(#c3s)"><rect x="74" y="26" width="150" height="132" rx="12" fill="#fff"/></g><rect x="90" y="42" width="118" height="12" rx="3" fill="#0A1930"/><rect x="90" y="62" width="118" height="6" rx="3" fill="#C7D6FF"/><rect x="90" y="74" width="88" height="6" rx="3" fill="#DCE6F7"/><rect x="90" y="92" width="52" height="38" rx="6" fill="#EEF3FF"/><rect x="150" y="92" width="58" height="6" rx="3" fill="#DCE6F7"/><rect x="150" y="104" width="58" height="6" rx="3" fill="#DCE6F7"/><rect x="150" y="116" width="40" height="6" rx="3" fill="#DCE6F7"/><rect x="90" y="140" width="72" height="9" rx="4" fill="#2B5CFF"/><g filter="url(#c3s)"><rect x="224" y="36" width="60" height="24" rx="12" fill="url(#c3c)"/></g><text x="254" y="52" font-size="10.5" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">PRESS</text></svg>""",
"advertorial-vs-press": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c4a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="c4d" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#101F3F"/><stop offset="1" stop-color="#2B5CFF"/></linearGradient><filter id="c4s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="160" cy="90" r="112" fill="url(#c4a)"/><g filter="url(#c4s)"><rect x="34" y="38" width="106" height="104" rx="12" fill="#fff"/></g><rect x="50" y="54" width="74" height="8" rx="4" fill="#2B5CFF"/><rect x="50" y="70" width="74" height="6" rx="3" fill="#DCE6F7"/><rect x="50" y="82" width="54" height="6" rx="3" fill="#DCE6F7"/><rect x="50" y="114" width="48" height="9" rx="4" fill="#0BBF8C"/><g filter="url(#c4s)"><rect x="180" y="38" width="106" height="104" rx="12" fill="#fff"/></g><rect x="196" y="54" width="74" height="8" rx="4" fill="#0BBF8C"/><rect x="196" y="70" width="74" height="6" rx="3" fill="#DCE6F7"/><rect x="196" y="82" width="54" height="6" rx="3" fill="#DCE6F7"/><rect x="196" y="114" width="48" height="9" rx="4" fill="#2B5CFF"/><g filter="url(#c4s)"><circle cx="160" cy="90" r="20" fill="url(#c4d)"/></g><text x="160" y="95" font-size="12.5" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">VS</text></svg>""",
"exhibition-pr": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c5a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#0BBF8C" stop-opacity=".45"/><stop offset="1" stop-color="#0BBF8C" stop-opacity="0"/></radialGradient><linearGradient id="c5r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#2B5CFF"/></linearGradient><linearGradient id="c5m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22E0AD"/><stop offset="1" stop-color="#08A97B"/></linearGradient><filter id="c5s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="252" cy="44" r="72" fill="url(#c5a)"/><g filter="url(#c5s)"><path d="M60 62 h140 l-13 -22 h-114 z" fill="url(#c5r)"/><rect x="68" y="62" width="124" height="66" rx="8" fill="#fff"/></g><rect x="86" y="80" width="88" height="11" rx="5" fill="#C7D6FF"/><rect x="86" y="98" width="60" height="8" rx="4" fill="#EEF3FF"/><line x1="56" y1="152" x2="264" y2="152" stroke="#fff" stroke-width="2" opacity=".45"/><circle cx="80" cy="152" r="6" fill="#fff"/><g filter="url(#c5s)"><circle cx="160" cy="152" r="9" fill="url(#c5m)"/></g><circle cx="240" cy="152" r="6" fill="#fff"/></svg>""",
"export-pr-strategy": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c6sph" cx="38%" cy="34%" r="72%"><stop offset="0" stop-color="#EAF1FF"/><stop offset="45%" stop-color="#7CA0FF"/><stop offset="100%" stop-color="#1E46D9"/></radialGradient><radialGradient id="c6a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="c6m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22E0AD"/><stop offset="1" stop-color="#08A97B"/></linearGradient><filter id="c6s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="9" stdDeviation="11" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="240" cy="46" r="80" fill="url(#c6a)"/><g filter="url(#c6s)"><circle cx="128" cy="92" r="60" fill="url(#c6sph)"/></g><g opacity=".55" stroke="#fff" fill="none" stroke-width="1.4"><ellipse cx="128" cy="92" rx="60" ry="22"/><ellipse cx="128" cy="92" rx="24" ry="60"/><line x1="68" y1="92" x2="188" y2="92"/></g><ellipse cx="110" cy="70" rx="20" ry="12" fill="#fff" opacity=".25"/><circle cx="102" cy="66" r="5" fill="#fff"/><circle cx="156" cy="80" r="5" fill="#fff"/><circle cx="120" cy="122" r="5" fill="#fff"/><g filter="url(#c6s)"><circle cx="240" cy="48" r="9" fill="url(#c6m)"/></g><path d="M156 80 Q210 42 234 48" stroke="#fff" stroke-width="2" fill="none" stroke-dasharray="2 6" stroke-linecap="round" opacity=".85"/><g filter="url(#c6s)"><path d="M232 116 l40 -14 -14 40 -8 -16 -18 -10z" fill="url(#c6m)"/></g></svg>""",
"manufacturer-case": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="c7a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="c7b" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2B5CFF"/><stop offset="1" stop-color="#7CA0FF"/></linearGradient><linearGradient id="c7m" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#08A97B"/><stop offset="1" stop-color="#22E0AD"/></linearGradient><filter id="c7s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#06122b" flood-opacity=".38"/></filter></defs><circle cx="248" cy="150" r="82" fill="url(#c7a)"/><g filter="url(#c7s)"><rect x="54" y="118" width="28" height="40" rx="6" fill="url(#c7b)" opacity=".75"/><rect x="92" y="98" width="28" height="60" rx="6" fill="url(#c7b)" opacity=".85"/><rect x="130" y="74" width="28" height="84" rx="6" fill="url(#c7b)"/><rect x="168" y="52" width="28" height="106" rx="6" fill="url(#c7b)"/><rect x="206" y="32" width="28" height="126" rx="6" fill="url(#c7m)"/></g><path d="M62 108 L106 88 L144 66 L182 46 L220 26" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g filter="url(#c7s)"><circle cx="220" cy="26" r="7" fill="#fff"/></g><path d="M240 42 l14 -16 14 16" stroke="#22E0AD" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="252" y="150" font-size="13" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif" opacity=".95">3M</text></svg>""",
"indexed-not-cited": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cv8a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><filter id="cv8s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#06122b" flood-opacity=".34"/></filter></defs><circle cx="256" cy="30" r="84" fill="url(#cv8a)"/><circle cx="44" cy="160" r="54" fill="url(#cv8a)"/><path d="M122 90 h58" stroke="#94A0B4" stroke-width="2.4" stroke-dasharray="3 6" fill="none" stroke-linecap="round"/><path d="M178 85 l7 5 -7 5" stroke="#94A0B4" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g filter="url(#cv8s)"><rect x="36" y="48" width="76" height="86" rx="20" fill="#fff"/></g><g transform="translate(55.4,60.2) scale(0.78)"><path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"/><path fill="#34A853" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z"/><path fill="#FBBC05" d="M11.69 28.18C11.25 26.86 11 25.45 11 24s.25-2.86.69-4.18v-5.7H4.34C2.85 17.09 2 20.45 2 24s.85 6.91 2.34 9.88l7.35-5.7z"/><path fill="#EA4335" d="M24 9.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 3.18 29.93 1 24 1 15.4 1 7.96 5.93 4.34 13.12l7.35 5.7c1.73-5.2 6.58-9.07 12.31-9.07z"/></g><text x="74" y="120" font-size="12.5" fill="#3C4043" text-anchor="middle" font-weight="700" font-family="Poppins,sans-serif">Google</text><circle cx="100" cy="58" r="10" fill="#0BBF8C"/><path d="M96 58l2.8 2.8 5.4-5.8" stroke="#fff" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g filter="url(#cv8s)"><rect x="208" y="48" width="76" height="86" rx="20" fill="#fff"/></g><g transform="translate(229.9,61.5) scale(1.36)" fill="#0A1930"><path d="M22.28 9.82a5.98 5.98 0 0 0-.52-4.91 6.05 6.05 0 0 0-6.51-2.9A6.07 6.07 0 0 0 4.98 4.18a5.98 5.98 0 0 0-3.998 2.9 6.05 6.05 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 22.05a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071.006zM18.44 11.6l-5.83-3.383L14.63 7.05a.076.076 0 0 1 .071-.006l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.415-.662zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L8.921 9.08V6.75a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zM7.82 12.74l-2.02-1.164a.08.08 0 0 1-.038-.057V5.936a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.216 5.32a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v3l-2.602 1.5-2.607-1.5z"/></g><text x="246" y="120" font-size="12.5" fill="#0A1930" text-anchor="middle" font-weight="700" font-family="Poppins,sans-serif">ChatGPT</text><circle cx="272" cy="58" r="10" fill="#fff" stroke="#E2574C" stroke-width="2.2"/><text x="272" y="62.5" font-size="12" fill="#E2574C" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">?</text></svg>""",
"measuring-geo": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cv9a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#22E0AD" stop-opacity=".4"/><stop offset="1" stop-color="#22E0AD" stop-opacity="0"/></radialGradient><radialGradient id="cv9b" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="cv9bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2B5CFF"/><stop offset="1" stop-color="#7CA0FF"/></linearGradient><filter id="cv9s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#06122b" flood-opacity=".38"/></filter></defs><circle cx="58" cy="30" r="78" fill="url(#cv9b)"/><circle cx="266" cy="152" r="74" fill="url(#cv9a)"/><g filter="url(#cv9s)"><rect x="28" y="34" width="264" height="112" rx="16" fill="#fff"/></g><circle cx="74" cy="88" r="26" fill="none" stroke="#EEF2F9" stroke-width="8"/><circle cx="74" cy="88" r="26" fill="none" stroke="#2B5CFF" stroke-width="8" stroke-linecap="round" stroke-dasharray="163" stroke-dashoffset="52" transform="rotate(-90 74 88)"/><text x="74" y="93" font-size="16" fill="#0A1930" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">68</text><rect x="114" y="72" width="66" height="8" rx="4" fill="#0A1930"/><rect x="114" y="88" width="48" height="6" rx="3" fill="#C0C9D8"/><rect x="196" y="112" width="12" height="18" rx="3" fill="url(#cv9bar)" opacity=".7"/><rect x="214" y="100" width="12" height="30" rx="3" fill="url(#cv9bar)" opacity=".82"/><rect x="232" y="86" width="12" height="44" rx="3" fill="url(#cv9bar)"/><rect x="250" y="70" width="12" height="60" rx="3" fill="#0BBF8C"/><path d="M202 108 L220 96 L238 82 L256 66" stroke="#0BBF8C" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="256" cy="66" r="4.5" fill="#fff" stroke="#0BBF8C" stroke-width="2"/></svg>""",
"llms-txt": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cvAa" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".55"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="cvAc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#1E46D9"/></linearGradient><filter id="cvAs" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="252" cy="40" r="90" fill="url(#cvAa)"/><circle cx="58" cy="160" r="56" fill="url(#cvAa)"/><g filter="url(#cvAs)"><path d="M96 30 h104 a10 10 0 0 1 10 10 v104 a10 10 0 0 1 -10 10 h-104 a10 10 0 0 1 -10 -10 V40 a10 10 0 0 1 10 -10 z" fill="#fff"/></g><rect x="110" y="46" width="60" height="18" rx="6" fill="url(#cvAc)"/><text x="140" y="59" font-size="10.5" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">llms.txt</text><text x="110" y="88" font-size="13" fill="#2B5CFF" font-weight="800" font-family="Poppins,sans-serif">#</text><rect x="123" y="80" width="66" height="7" rx="3.5" fill="#0A1930"/><circle cx="114" cy="104" r="2.6" fill="#0BBF8C"/><rect x="123" y="101" width="72" height="6" rx="3" fill="#DCE6F7"/><circle cx="114" cy="120" r="2.6" fill="#0BBF8C"/><rect x="123" y="117" width="72" height="6" rx="3" fill="#DCE6F7"/><circle cx="114" cy="136" r="2.6" fill="#0BBF8C"/><rect x="123" y="133" width="50" height="6" rx="3" fill="#DCE6F7"/><path d="M204 118 h12" stroke="#94A0B4" stroke-width="2.4" stroke-dasharray="3 5" stroke-linecap="round" fill="none"/><g filter="url(#cvAs)"><rect x="216" y="92" width="72" height="52" rx="14" fill="url(#cvAc)"/></g><rect x="228" y="106" width="22" height="22" rx="8" fill="#fff" opacity=".22"/><text x="239" y="121" font-size="10" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">AI</text><rect x="256" y="108" width="24" height="6" rx="3" fill="#fff" opacity=".85"/><rect x="256" y="120" width="18" height="6" rx="3" fill="#fff" opacity=".5"/></svg>""",
"ai-hallucination-brand": """<svg class="cover" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cvBa" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CA0FF" stop-opacity=".5"/><stop offset="1" stop-color="#7CA0FF" stop-opacity="0"/></radialGradient><linearGradient id="cvBc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E93FF"/><stop offset="1" stop-color="#1E46D9"/></linearGradient><filter id="cvBs" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#06122b" flood-opacity=".4"/></filter></defs><circle cx="252" cy="38" r="88" fill="url(#cvBa)"/><circle cx="50" cy="158" r="56" fill="url(#cvBa)"/><g filter="url(#cvBs)"><rect x="26" y="46" width="182" height="96" rx="16" fill="#fff"/></g><rect x="42" y="62" width="26" height="26" rx="9" fill="url(#cvBc)"/><text x="55" y="79" font-size="11" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">AI</text><rect x="76" y="64" width="90" height="7" rx="3.5" fill="#0A1930"/><rect x="76" y="78" width="70" height="6" rx="3" fill="#DCE6F7"/><rect x="42" y="104" width="122" height="8" rx="4" fill="#F4C0BB"/><line x1="42" y1="108" x2="164" y2="108" stroke="#E2574C" stroke-width="2"/><rect x="42" y="121" width="80" height="6" rx="3" fill="#DCE6F7"/><g filter="url(#cvBs)"><circle cx="216" cy="64" r="22" fill="#fff"/></g><path d="M216 52 l11.5 20 h-23 z" fill="#F5A623"/><rect x="214.6" y="59" width="2.8" height="7.5" rx="1.4" fill="#fff"/><circle cx="216" cy="70" r="1.7" fill="#fff"/><g filter="url(#cvBs)"><circle cx="254" cy="120" r="20" fill="url(#cvBc)"/></g><path d="M246 120 l6 6 10 -11.5" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
}

# 커버는 실제 사진(Unsplash 핫링크)으로 대체 — 위 SVG 딕셔너리는 폴백/참고용으로 남겨둠
_PHOTOS = {
"aeo-geo-seo":"https://images.unsplash.com/photo-1773332611528-566f16120979?w=800&h=450&fit=crop&q=70&auto=format",
"ai-pr-guide":"https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=450&fit=crop&q=70&auto=format",
"press-release-writing":"https://images.unsplash.com/photo-1631519952398-5b1d76b946e8?w=800&h=450&fit=crop&q=70&auto=format",
"advertorial-vs-press":"https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&h=450&fit=crop&q=70&auto=format",
"exhibition-pr":"https://images.unsplash.com/photo-1632383380175-812d44ec112b?w=800&h=450&fit=crop&q=70&auto=format",
"export-pr-strategy":"https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=450&fit=crop&q=70&auto=format",
"manufacturer-case":"https://images.unsplash.com/photo-1717386255773-1e3037c81788?w=800&h=450&fit=crop&q=70&auto=format",
}
COVERS = {s: f'<img class="cover" src="{u}" alt="" loading="lazy" referrerpolicy="no-referrer">' for s, u in _PHOTOS.items()}
COVERS["aeo-geo-seo"] = _SVG_COVERS["aeo-geo-seo"]  # 이 글은 사진 대신 SVG 커버
COVERS["indexed-not-cited"] = _SVG_COVERS["indexed-not-cited"]  # 신규 글 — 브랜드 SVG 커버
COVERS["measuring-geo"] = _SVG_COVERS["measuring-geo"]  # 신규 글 — 브랜드 SVG 커버
COVERS["llms-txt"] = _SVG_COVERS["llms-txt"]  # 신규 글 — 브랜드 SVG 커버
COVERS["ai-hallucination-brand"] = _SVG_COVERS["ai-hallucination-brand"]  # 신규 글 — 브랜드 SVG 커버

# ---------------- 본문 삽입 도식 (SVG figure, slug별) ----------------
FIGS = {
"aeo-geo-seo": """<figure class="fig"><svg viewBox="0 0 600 244" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><rect x="28" y="20" width="544" height="64" rx="12" fill="#fff" stroke="#E5EAF2"/><rect x="44" y="38" width="62" height="28" rx="8" fill="#8B95A7"/><text x="75" y="57" font-size="14" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">SEO</text><text x="124" y="47" font-size="15" fill="#0A1930" font-weight="700">검색엔진이 읽습니다</text><text x="124" y="68" font-size="12.5" fill="#8B95A7">네이버·구글 상위 노출 — 키워드·구조·속도</text><rect x="28" y="92" width="544" height="64" rx="12" fill="#fff" stroke="#C7D6FF"/><rect x="44" y="110" width="62" height="28" rx="8" fill="#2B5CFF"/><text x="75" y="129" font-size="14" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">AEO</text><text x="124" y="119" font-size="15" fill="#0A1930" font-weight="700">AI가 답변에 인용합니다</text><text x="124" y="140" font-size="12.5" fill="#8B95A7">질문형 콘텐츠 · 여러 출처에서 확인 · 구조화</text><rect x="28" y="164" width="544" height="64" rx="12" fill="#fff" stroke="#B7EAD9"/><rect x="44" y="182" width="62" height="28" rx="8" fill="#0BBF8C"/><text x="75" y="201" font-size="14" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">GEO</text><text x="124" y="191" font-size="15" fill="#0A1930" font-weight="700">생성형 AI 검색 전반에 대응</text><text x="124" y="212" font-size="12.5" fill="#8B95A7">정보 축적 · 최신성 · 출처 다양성까지 관리</text></svg><figcaption>SEO·AEO·GEO — '누가 읽느냐'가 다른 세 가지 최적화</figcaption></figure>""",
"ai-pr-guide": """<figure class="fig"><svg viewBox="0 0 600 268" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><g><rect x="28" y="20" width="264" height="108" rx="14" fill="#fff" stroke="#E5EAF2"/><circle cx="58" cy="54" r="16" fill="#2B5CFF"/><text x="58" y="60" font-size="15" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">1</text><text x="84" y="53" font-size="15" fill="#0A1930" font-weight="700">질문에서 출발</text><text x="46" y="92" font-size="12.5" fill="#8B95A7">고객이 AI에게 물어볼</text><text x="46" y="110" font-size="12.5" fill="#8B95A7">질문을 먼저 정의합니다</text></g><g><rect x="308" y="20" width="264" height="108" rx="14" fill="#fff" stroke="#E5EAF2"/><circle cx="338" cy="54" r="16" fill="#2B5CFF"/><text x="338" y="60" font-size="15" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">2</text><text x="364" y="53" font-size="15" fill="#0A1930" font-weight="700">출처를 여러 곳에</text><text x="326" y="92" font-size="12.5" fill="#8B95A7">언론·홈페이지·칼럼에서</text><text x="326" y="110" font-size="12.5" fill="#8B95A7">일관되게 확인되도록</text></g><g><rect x="28" y="140" width="264" height="108" rx="14" fill="#fff" stroke="#E5EAF2"/><circle cx="58" cy="174" r="16" fill="#0BBF8C"/><text x="58" y="180" font-size="15" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">3</text><text x="84" y="173" font-size="15" fill="#0A1930" font-weight="700">일회성 아닌 누적</text><text x="46" y="212" font-size="12.5" fill="#8B95A7">매달 쌓이는 정보 자산이</text><text x="46" y="230" font-size="12.5" fill="#8B95A7">AI 검색에서 강합니다</text></g><g><rect x="308" y="140" width="264" height="108" rx="14" fill="#fff" stroke="#E5EAF2"/><circle cx="338" cy="174" r="16" fill="#0BBF8C"/><text x="338" y="180" font-size="15" fill="#fff" text-anchor="middle" font-weight="800" font-family="Poppins,sans-serif">4</text><text x="364" y="173" font-size="15" fill="#0A1930" font-weight="700">홈페이지도 정비</text><text x="326" y="212" font-size="12.5" fill="#8B95A7">외부 콘텐츠와 홈페이지가</text><text x="326" y="230" font-size="12.5" fill="#8B95A7">맥락으로 연결되도록</text></g></svg><figcaption>AI 검색 시대, 기업 홍보의 새 원칙 4가지</figcaption></figure>""",
"press-release-writing": """<figure class="fig"><svg viewBox="0 0 600 292" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><g><rect x="28" y="18" width="544" height="46" rx="10" fill="#fff" stroke="#E5EAF2"/><rect x="28" y="18" width="6" height="46" rx="3" fill="#2B5CFF"/><text x="52" y="40" font-size="14.5" fill="#0A1930" font-weight="700">제목</text><text x="150" y="40" font-size="12.5" fill="#8B95A7">업계 관점의 뉴스 가치를 한 줄로 — 자랑이 아니라 '변화'</text></g><g><rect x="28" y="72" width="544" height="46" rx="10" fill="#fff" stroke="#E5EAF2"/><rect x="28" y="72" width="6" height="46" rx="3" fill="#2B5CFF"/><text x="52" y="94" font-size="14.5" fill="#0A1930" font-weight="700">리드문</text><text x="150" y="94" font-size="12.5" fill="#8B95A7">핵심 사실 요약 — 이 문단만 실려도 기사가 되도록</text></g><g><rect x="28" y="126" width="544" height="46" rx="10" fill="#fff" stroke="#E5EAF2"/><rect x="28" y="126" width="6" height="46" rx="3" fill="#2B5CFF"/><text x="52" y="148" font-size="14.5" fill="#0A1930" font-weight="700">본문</text><text x="150" y="148" font-size="12.5" fill="#8B95A7">배경 → 세부 내용 → 의미 순, 수치와 근거 포함</text></g><g><rect x="28" y="180" width="544" height="46" rx="10" fill="#fff" stroke="#E5EAF2"/><rect x="28" y="180" width="6" height="46" rx="3" fill="#0BBF8C"/><text x="52" y="202" font-size="14.5" fill="#0A1930" font-weight="700">인용문</text><text x="150" y="202" font-size="12.5" fill="#8B95A7">대표 코멘트 — 사실 전달이 아니라 방향성·의지</text></g><g><rect x="28" y="234" width="544" height="46" rx="10" fill="#fff" stroke="#E5EAF2"/><rect x="28" y="234" width="6" height="46" rx="3" fill="#8B95A7"/><text x="52" y="256" font-size="14.5" fill="#0A1930" font-weight="700">회사 소개</text><text x="150" y="256" font-size="12.5" fill="#8B95A7">보일러플레이트 — 맨 끝에 3~4줄로</text></g></svg><figcaption>기사가 되기 쉬운 보도자료 구조</figcaption></figure>""",
"advertorial-vs-press": """<figure class="fig"><svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><g><rect x="28" y="20" width="264" height="210" rx="14" fill="#fff" stroke="#C7D6FF"/><rect x="28" y="20" width="264" height="42" rx="14" fill="#2B5CFF"/><rect x="28" y="46" width="264" height="16" fill="#2B5CFF"/><text x="160" y="47" font-size="15" fill="#fff" text-anchor="middle" font-weight="800">보도자료 배포</text><text x="52" y="94" font-size="13" fill="#8B95A7">비용</text><text x="270" y="94" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">낮음</text><text x="52" y="128" font-size="13" fill="#8B95A7">게재</text><text x="270" y="128" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">미보장</text><text x="52" y="162" font-size="13" fill="#8B95A7">내용 결정</text><text x="270" y="162" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">기자</text><text x="52" y="196" font-size="13" fill="#8B95A7">신뢰도</text><text x="270" y="196" font-size="13.5" fill="#0BBF8C" text-anchor="end" font-weight="800">가장 높음</text></g><g><rect x="308" y="20" width="264" height="210" rx="14" fill="#fff" stroke="#B7EAD9"/><rect x="308" y="20" width="264" height="42" rx="14" fill="#0BBF8C"/><rect x="308" y="46" width="264" height="16" fill="#0BBF8C"/><text x="440" y="47" font-size="15" fill="#fff" text-anchor="middle" font-weight="800">애드버토리얼</text><text x="332" y="94" font-size="13" fill="#8B95A7">비용</text><text x="550" y="94" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">매체별</text><text x="332" y="128" font-size="13" fill="#8B95A7">게재</text><text x="550" y="128" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">보장</text><text x="332" y="162" font-size="13" fill="#8B95A7">내용 결정</text><text x="550" y="162" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">우리</text><text x="332" y="196" font-size="13" fill="#8B95A7">인식</text><text x="550" y="196" font-size="13.5" fill="#0A1930" text-anchor="end" font-weight="700">광고 가능</text></g></svg><figcaption>보도자료 배포 vs 애드버토리얼 — 한눈에 보는 차이</figcaption></figure>""",
"exhibition-pr": """<figure class="fig"><svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><line x1="70" y1="104" x2="530" y2="104" stroke="#D8E0EC" stroke-width="3"/><g><circle cx="130" cy="104" r="13" fill="#2B5CFF"/><text x="130" y="60" font-size="14.5" fill="#0A1930" text-anchor="middle" font-weight="700">사전 (D-30)</text><text x="130" y="150" font-size="12" fill="#8B95A7" text-anchor="middle">참가 보도자료</text><text x="130" y="168" font-size="12" fill="#8B95A7" text-anchor="middle">안내 페이지</text></g><g><circle cx="300" cy="104" r="16" fill="#0BBF8C"/><text x="300" y="58" font-size="14.5" fill="#0A1930" text-anchor="middle" font-weight="700">현장</text><text x="300" y="152" font-size="12" fill="#8B95A7" text-anchor="middle">현장 사진·기록</text><text x="300" y="170" font-size="12" fill="#8B95A7" text-anchor="middle">이슈 속보</text></g><g><circle cx="470" cy="104" r="13" fill="#2B5CFF"/><text x="470" y="60" font-size="14.5" fill="#0A1930" text-anchor="middle" font-weight="700">사후 (D+30)</text><text x="470" y="150" font-size="12" fill="#8B95A7" text-anchor="middle">성과 보도자료</text><text x="470" y="168" font-size="12" fill="#8B95A7" text-anchor="middle">후기 칼럼</text></g></svg><figcaption>전시회 홍보 타임라인 — 사전·현장·사후</figcaption></figure>""",
"export-pr-strategy": """<figure class="fig"><svg viewBox="0 0 600 232" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><g><rect x="24" y="24" width="176" height="184" rx="14" fill="#fff" stroke="#E5EAF2"/><text x="112" y="66" font-size="17" fill="#2B5CFF" text-anchor="middle" font-weight="800">베트남</text><line x1="52" y1="84" x2="172" y2="84" stroke="#EEF2F9"/><text x="112" y="116" font-size="13" fill="#0A1930" text-anchor="middle" font-weight="700">성장 시장</text><text x="112" y="146" font-size="12.5" fill="#8B95A7" text-anchor="middle">낮은 진입 장벽</text><text x="112" y="176" font-size="12.5" fill="#8B95A7" text-anchor="middle">현지어 보도 효과 큼</text></g><g><rect x="212" y="24" width="176" height="184" rx="14" fill="#fff" stroke="#E5EAF2"/><text x="300" y="66" font-size="17" fill="#2B5CFF" text-anchor="middle" font-weight="800">중국</text><line x1="240" y1="84" x2="360" y2="84" stroke="#EEF2F9"/><text x="300" y="116" font-size="13" fill="#0A1930" text-anchor="middle" font-weight="700">플랫폼 중심</text><text x="300" y="146" font-size="12.5" fill="#8B95A7" text-anchor="middle">바이두·위챗·샤오홍슈</text><text x="300" y="176" font-size="12.5" fill="#8B95A7" text-anchor="middle">플랫폼 전략 먼저</text></g><g><rect x="400" y="24" width="176" height="184" rx="14" fill="#fff" stroke="#E5EAF2"/><text x="488" y="66" font-size="17" fill="#2B5CFF" text-anchor="middle" font-weight="800">미국</text><line x1="428" y1="84" x2="548" y2="84" stroke="#EEF2F9"/><text x="488" y="116" font-size="13" fill="#0A1930" text-anchor="middle" font-weight="700">높은 신뢰 기준</text><text x="488" y="146" font-size="12.5" fill="#8B95A7" text-anchor="middle">업계 전문지 영향력</text><text x="488" y="176" font-size="12.5" fill="#8B95A7" text-anchor="middle">데이터·사례 중심</text></g></svg><figcaption>수출 3대 시장의 PR 환경 차이</figcaption></figure>""",
"manufacturer-case": """<figure class="fig"><svg viewBox="0 0 600 210" xmlns="http://www.w3.org/2000/svg" font-family="'Pretendard',system-ui,sans-serif"><line x1="66" y1="108" x2="540" y2="108" stroke="#D8E0EC" stroke-width="3"/><g><circle cx="96" cy="108" r="12" fill="#8B95A7"/><text x="96" y="66" font-size="13.5" fill="#0A1930" text-anchor="middle" font-weight="700">0주차</text><text x="96" y="150" font-size="11.5" fill="#8B95A7" text-anchor="middle">진단</text><text x="96" y="167" font-size="11.5" fill="#8B95A7" text-anchor="middle">AI는 모른다</text></g><g><circle cx="244" cy="108" r="12" fill="#3D6BFF"/><text x="244" y="66" font-size="13.5" fill="#0A1930" text-anchor="middle" font-weight="700">1개월</text><text x="244" y="150" font-size="11.5" fill="#8B95A7" text-anchor="middle">첫 축적</text><text x="244" y="167" font-size="11.5" fill="#8B95A7" text-anchor="middle">페이지·보도·칼럼</text></g><g><circle cx="392" cy="108" r="12" fill="#2B5CFF"/><text x="392" y="66" font-size="13.5" fill="#0A1930" text-anchor="middle" font-weight="700">2개월</text><text x="392" y="150" font-size="11.5" fill="#8B95A7" text-anchor="middle">출처 확대</text><text x="392" y="167" font-size="11.5" fill="#8B95A7" text-anchor="middle">4곳에서 확인</text></g><g><circle cx="510" cy="108" r="14" fill="#0BBF8C"/><text x="510" y="64" font-size="13.5" fill="#0A1930" text-anchor="middle" font-weight="700">3개월</text><text x="510" y="152" font-size="11.5" fill="#0BBF8C" text-anchor="middle" font-weight="700">AI에 등장</text><text x="510" y="169" font-size="11.5" fill="#8B95A7" text-anchor="middle">기사·홈피 인용</text></g></svg><figcaption>제조기업 A사의 3개월 — 진단에서 AI 등장까지</figcaption></figure>""",
}

FONT_LINKS = """<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">"""

def nav(depth):
    p = "../" * depth
    return f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="{p}index.html">{LOGO}<span class="bw">messeze</span></a>
<nav class="nav-menu">
<a href="{p}services.html">서비스</a>
<a href="{p}pricing.html">요금</a>
<a href="{p}check.html">AI 가시성 체크</a>
<a class="on" href="{p}blog/index.html">블로그</a>
<a href="{p}glossary/index.html">용어사전</a>
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
<div><h3>우리 회사는 AI에서 어떻게 보이고 있을까요?</h3><p>AI 가시성 무료 진단 · 보도자료 1건 무료 · 최적화 콘텐츠 3건</p></div>
<a class="btn" href="{p}index.html#final">무료 진단 신청하기</a></div></div>"""

# ---------------- 글 상세 페이지 ----------------
POST_CSS = CSS + """
.crumb{font-size:13.5px;font-weight:600;color:var(--mut);padding:34px 0 0;display:flex;gap:8px;align-items:center}
.crumb a:hover{color:var(--cobalt)}
.crumb .cat{color:var(--cobalt);font-weight:700}
.phead{max-width:760px;margin:0 auto;padding:26px 0 34px}
.phead h1{font-size:clamp(27px,3.8vw,40px);line-height:1.32}
.phead .meta{margin-top:18px;font-size:13.5px;color:var(--mut);font-weight:600;display:flex;gap:14px;align-items:center}
.phead .meta .by{color:var(--ink)}
.pcover{max-width:860px;margin:0 auto;height:360px;border-radius:22px;position:relative;overflow:hidden}
.pcover .pat{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:20px 20px}
.pcover .tag{position:absolute;left:24px;bottom:20px;font-size:13px;font-weight:800;color:#fff;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:7px 14px;border-radius:999px}
.article{max-width:720px;margin:0 auto;padding:46px 0 10px}
.article p{font-size:16.5px;color:#333C4E;line-height:1.85;margin-bottom:26px}
.article h2{font-size:22px;margin:42px 0 16px;padding-top:8px}
.article ul{margin:0 0 26px 4px;padding-left:20px;display:flex;flex-direction:column;gap:10px}
.article li{font-size:16px;color:#333C4E;line-height:1.75}
.article b{color:var(--ink)}
.article blockquote{background:var(--sky);border-left:4px solid var(--cobalt);border-radius:0 14px 14px 0;padding:20px 24px;font-size:16px;color:var(--navy);line-height:1.75;margin:34px 0}
.fig{margin:38px 0;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:var(--sky-2)}
.fig svg{display:block;width:100%;height:auto}
.fig figcaption{font-size:13px;color:var(--mut);font-weight:600;text-align:center;padding:13px 16px;border-top:1px solid var(--line);background:#fff}
.rel{max-width:860px;margin:60px auto 0;padding:0 24px}
.rel h3{font-size:20px;margin-bottom:20px}
.rel-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.rcard{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;transition:.2s;display:flex;flex-direction:column}
.rcard:hover{box-shadow:var(--sh);transform:translateY(-3px)}
.rcard .thumb{height:110px;position:relative}
.rcard .thumb .pat{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:16px 16px}
.rcard .b{padding:18px 20px 20px}
.rcard .cat{font-size:12px;font-weight:800;color:var(--cobalt)}
.rcard h4{font-size:15.5px;margin-top:8px;line-height:1.45}
.backrow{max-width:720px;margin:44px auto 0;padding:0 24px}
.backrow a{font-size:14.5px;font-weight:700;color:var(--cobalt)}
@media(max-width:700px){.rel-grid{grid-template-columns:1fr}.pcover{height:220px;border-radius:16px;margin:0 20px}}
"""

def related(post):
    others = [q for q in POSTS if q["slug"] != post["slug"]]
    same = [q for q in others if q["cat"] == post["cat"]] + [q for q in others if q["cat"] != post["cat"]]
    cards = ""
    for q in same[:2]:
        cards += f"""<a class="rcard" href="{q['slug']}.html"><div class="thumb" style="background:{q['grad']}"><span class="pat"></span>{COVERS[q['slug']]}</div>
<div class="b"><span class="cat">{q['cat']}</span><h4>{q['title']}</h4></div></a>"""
    return cards

def build_post(post):
    fig = FIGS.get(post['slug'], "")
    body = post['body']
    if fig and '<h2>' in body:
        body = body.replace('<h2>', fig + '<h2>', 1)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{post['title']} | messeze 블로그</title>
<meta name="description" content="{post['desc']}">
{FONT_LINKS}
<style>{POST_CSS}</style></head><body>
{nav(2)}
<div class="wrap crumb"><a href="../index.html">블로그</a><span>›</span><span class="cat">{post['cat']}</span></div>
<div class="wrap phead"><h1>{post['title']}</h1>
<div class="meta"><span class="by">by. messeze 편집팀</span><span>·</span><span>{post['date']}</span></div></div>
<div class="pcover" style="background:{post['grad']}"><span class="pat"></span>{COVERS[post['slug']]}<span class="tag">{post['cat']}</span></div>
<article class="article wrap">{body}</article>
<div class="backrow"><a href="../index.html">← 블로그 목록으로</a></div>
<div class="rel"><h3>함께 읽으면 좋은 글</h3><div class="rel-grid">{related(post)}</div></div>
{cta(2)}
{foot(2)}
</body></html>"""

# ---------------- 블로그 인덱스 ----------------
INDEX_CSS = CSS + """
.bhero{padding:56px 0 30px}
.bhero .row{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
.bhero h1{font-size:clamp(30px,4vw,42px)}
.bhero p{color:var(--body);font-size:16px;margin-top:10px}
.search{position:relative}
.search input{width:280px;max-width:100%;background:var(--sky-2);border:1.5px solid var(--line);border-radius:14px;padding:13px 16px 13px 42px;font-family:var(--sans);font-size:14.5px;color:var(--ink);transition:.18s}
.search input:focus{outline:none;border-color:var(--cobalt);background:#fff}
.search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:17px;height:17px;color:var(--mut)}
.tabs{display:flex;gap:8px;flex-wrap:wrap;padding:22px 0 0;border-bottom:1px solid var(--line);margin-bottom:40px}
.tabs button{font-family:var(--sans);font-weight:700;font-size:15px;background:none;border:0;border-bottom:2.5px solid transparent;color:var(--body);padding:12px 14px;cursor:pointer;transition:.15s}
.tabs button:hover{color:var(--ink)}
.tabs button.on{color:var(--cobalt);border-bottom-color:var(--cobalt)}
.group{margin-bottom:54px}
.group .gh{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px}
.group .gh h2{font-size:22px}
.group .gh a{font-size:13.5px;font-weight:700;color:var(--cobalt)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;transition:.2s;display:flex;flex-direction:column}
.card:hover{box-shadow:var(--sh);transform:translateY(-3px)}
.card .thumb{height:150px;position:relative}
.card .thumb .pat{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:18px 18px}
.card .thumb .tag{position:absolute;left:18px;bottom:14px;font-size:12px;font-weight:800;color:#fff;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:5px 12px;border-radius:999px}
.card .b{padding:20px 22px 24px;display:flex;flex-direction:column;flex:1}
.card h3{font-size:17px;line-height:1.45;letter-spacing:-.02em}
.card p{margin-top:9px;font-size:13.8px;color:var(--body);line-height:1.58;flex:1}
.card .meta{margin-top:16px;font-size:12.5px;color:var(--mut);font-weight:600}
.card .meta b{color:var(--ink)}
.empty{text-align:center;color:var(--mut);padding:60px 0;font-size:15px}
@media(max-width:900px){.grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.grid{grid-template-columns:1fr}.bhero .row{align-items:stretch}.search input{width:100%}}
"""

def build_index():
    posts_json = json.dumps([{**{k: p[k] for k in ("slug","cat","title","desc","date","grad")}, "cover": COVERS[p["slug"]]} for p in POSTS], ensure_ascii=False)
    cats_json = json.dumps(CATS, ensure_ascii=False)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>블로그 | messeze — AI 검색 시대의 기업 홍보 인사이트</title>
<meta name="description" content="AEO·GEO·SEO, 보도자료 작성법, 수출기업 PR 전략까지 — AI 검색 시대의 기업 홍보를 다루는 messeze 블로그.">
{FONT_LINKS}
<style>{INDEX_CSS}</style></head><body>
{nav(1)}
<section class="bhero"><div class="wrap">
<div class="row">
<div><h1>messeze 블로그</h1><p>AI 검색 시대의 기업 홍보, 먼저 이해하고 시작하세요.</p></div>
<div class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/></svg><input id="q" type="search" placeholder="검색어를 입력하세요"></div>
</div>
<div class="tabs" id="tabs"></div>
</div></section>
<main class="wrap" id="app"></main>
{cta(1)}
{foot(1)}
<script>
const POSTS={posts_json};
const CATS={cats_json};
const app=document.getElementById('app'),tabsEl=document.getElementById('tabs'),q=document.getElementById('q');
let cur='홈';
function card(p){{return `<a class="card" href="posts/${{p.slug}}.html">
<div class="thumb" style="background:${{p.grad}}"><span class="pat"></span>${{p.cover}}<span class="tag">${{p.cat}}</span></div>
<div class="b"><h3>${{p.title}}</h3><p>${{p.desc}}</p><div class="meta"><b>by. messeze 편집팀</b> · ${{p.date}}</div></div></a>`}}
function grid(list){{return list.length?`<div class="grid">${{list.map(card).join('')}}</div>`:`<div class="empty">검색 결과가 없습니다.</div>`}}
function render(){{
  const kw=q.value.trim().toLowerCase();
  if(kw){{
    const hits=POSTS.filter(p=>(p.title+p.desc+p.cat).toLowerCase().includes(kw));
    app.innerHTML=`<div class="group"><div class="gh"><h2>'${{q.value.trim()}}' 검색 결과 ${{hits.length}}건</h2></div>${{grid(hits)}}</div>`;
    return;
  }}
  if(cur==='홈'){{
    let html=`<div class="group"><div class="gh"><h2>최근 아티클</h2></div>${{grid(POSTS.slice(0,3))}}</div>`;
    for(const c of CATS.slice(1)){{
      const list=POSTS.filter(p=>p.cat===c);
      if(!list.length)continue;
      html+=`<div class="group"><div class="gh"><h2>${{c}}</h2><a href="#" data-cat="${{c}}" class="more">전체 보기 →</a></div>${{grid(list.slice(0,3))}}</div>`;
    }}
    app.innerHTML=html;
  }}else{{
    app.innerHTML=`<div class="group"><div class="gh"><h2>${{cur}}</h2></div>${{grid(POSTS.filter(p=>p.cat===cur))}}</div>`;
  }}
}}
function renderTabs(){{tabsEl.innerHTML=CATS.map(c=>`<button class="${{c===cur?'on':''}}" data-c="${{c}}">${{c}}</button>`).join('')}}
tabsEl.addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;cur=b.dataset.c;q.value='';renderTabs();render();scrollTo({{top:0,behavior:'smooth'}})}});
app.addEventListener('click',e=>{{const m=e.target.closest('.more');if(!m)return;e.preventDefault();cur=m.dataset.cat;renderTabs();render();scrollTo({{top:0,behavior:'smooth'}})}});
q.addEventListener('input',render);
renderTabs();render();
</script>
</body></html>"""

# ---------------- 실행 ----------------
with io.open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8") as f:
    f.write(build_index())
for p in POSTS:
    with io.open(os.path.join(POSTS_DIR, p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(build_post(p))
print("OK: blog/index.html +", len(POSTS), "posts")
