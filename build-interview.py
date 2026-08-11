# -*- coding: utf-8 -*-
"""messeze 인터뷰 성과 상세 페이지 생성기 (searchpolaris /result 벤치마크)
실행: python build-interview.py → interview/{slug}.html"""
import io, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "interview")
os.makedirs(OUT, exist_ok=True)

# ---- 공용 헤더/푸터: services/visibility.html에서 추출 (동일 깊이 ../ 경로) ----
src = io.open(os.path.join(ROOT, "services", "visibility.html"), encoding="utf-8").read()
m = re.search(r'(<header class="nav".*?</header>\s*<script>.*?</script>)', src, re.S)
HEADER = m.group(1)
m2 = re.search(r'(<footer.*?</footer>)', src, re.S)
FOOTER = m2.group(1)

U = "https://images.unsplash.com/photo-{}?w=160&h=160&fit=crop&crop=faces&q=72&auto=format"
P = "https://images.pexels.com/photos/{}/pexels-photo-{}.jpeg?auto=compress&cs=tinysrgb&w=160&h=160&fit=crop"

C = []
def c(**kw): C.append(kw)

c(slug="parts", tag="정밀부품 제조", com="○○정밀", who="김○○ 대표", photo=U.format("1622902046580-2b47f47f5471"),
  title="검색량 없던 정밀부품 제조사가<br>AI 답변에 등장하기까지",
  quote="검색량이 없어 홍보를 반쯤 포기했었는데, 이제 AI가 먼저 우리를 추천합니다.",
  period="16주", plan="프리미엄",
  metrics=[("0→7","AI 인용 질문 수","핵심 질문 9개 중"),("87%","AI 답변 등장률","4개 엔진 평균"),("14건","축적 콘텐츠·기사","언론 6건 포함"),("2배","월 신규 문의","시작 전 대비")],
  before="항공·의료용 정밀부품이라 검색량 자체가 적고, 홈페이지는 5년 전 이미지 위주 구축형. '정밀부품 소량 제작'을 AI에 물으면 경쟁사 2곳만 나오고 우리는 없었습니다.",
  actions=[("AI 가시성 진단","4개 엔진 × 질문 9개 테스트 — 인용 0건 확인, 경쟁사 출처 분해"),("홈페이지 구조 정비","이미지 속 인증·설비 정보를 텍스트로, 기업·FAQ 스키마 탑재"),("콘텐츠 축적","질문에 답하는 칼럼 월 4편 + 블로그 4채널 변주 발행"),("언론 배포","수출바우처 선정·설비 증설 소식 보도자료 6건 기사화")],
  weeks=[("시작",0),("4주",22),("8주",48),("12주",70),("16주",87)],
  qa=[("가장 큰 변화는 무엇인가요?","문의 전화가 달라졌어요. '어떻게 아셨어요?'라고 물으면 'AI가 추천해서요'라는 답이 옵니다. 예전엔 없던 경로죠."),
      ("반신반의하지 않으셨나요?","솔직히 했습니다. 검색량도 없는 업종이라. 그런데 8주차 리포트에서 처음 우리 이름이 AI 답변에 잡힌 걸 보고 생각이 바뀌었어요."),
      ("어떤 기업에 추천하시나요?","우리처럼 제품은 자신 있는데 알릴 방법이 없던 B2B 제조사요. 광고보다 이게 맞는 방향이라고 봅니다.")])

c(slug="export", tag="수출기업", com="○○인더스트리", who="이○○ 마케팅팀장", photo=U.format("1548142813-c348350df52b"),
  title="보도자료만 뿌리던 수출기업,<br>해외 바이어가 AI로 찾아오기까지",
  quote="보도자료만 뿌리던 걸, 이제 AI가 읽는 자산으로 쌓습니다.",
  period="24주", plan="엔터프라이즈",
  metrics=[("3배","해외 바이어 문의","시작 전 대비"),("0→11","AI 인용 질문 수","한·영 질문 14개 중"),("22건","축적 콘텐츠·기사","현지어 보도 8건"),("92%","AI 답변 등장률","4개 엔진 평균")],
  before="매년 전시회마다 보도자료를 냈지만 일회성으로 끝났습니다. 바이어가 ChatGPT에 '베트남 수출 경험 있는 한국 제조사'를 물으면 우리는 어디에도 없었습니다.",
  actions=[("AI 가시성 진단","한국어·영어 질문 14개로 4개 엔진 테스트, 해외 노출 0 확인"),("홈페이지 정비","영문 페이지 신설 + 수출 실적·인증 구조화 데이터"),("콘텐츠 축적","수출·인증 스토리 칼럼과 4채널 발행(영문 포함)"),("해외 언론 확장","베트남·중국 현지어 보도자료 8건 현지 매체 게재")],
  weeks=[("시작",0),("6주",26),("12주",55),("18주",78),("24주",92)],
  qa=[("왜 직접 안 하고 맡기셨나요?","할 인력이 없었어요. 진단부터 현지어 배포까지 전담팀이 다 대신해주니 저는 확인만 하면 됐습니다."),
      ("해외 반응이 실제로 있나요?","현지 기사가 나간 뒤 베트남 바이어 문의가 눈에 띄게 늘었고, '기사 보고 연락했다'는 메일도 받았습니다."),
      ("가장 만족스러운 점은요?","흩어져 사라지던 보도자료가 이제 검색과 AI에 남는 자산이 됐다는 점이요.")])

c(slug="material", tag="산업소재", com="○○소재", who="박○○ 대표", photo=U.format("1611403119860-57c4937ef987"),
  title="특허는 있는데 아무도 몰랐던 소재기업,<br>AI가 먼저 설명하는 회사로",
  quote="특허는 있는데 아무도 몰랐어요. 이제 AI가 우리 소재를 먼저 설명합니다.",
  period="16주", plan="프리미엄",
  metrics=[("0→6","AI 인용 질문 수","핵심 질문 8개 중"),("81%","AI 답변 등장률","4개 엔진 평균"),("12건","축적 콘텐츠·기사","기술 칼럼 8편"),("2배","기술 문의","시작 전 대비")],
  before="특허 12건에 KS 인증까지 있었지만 홈페이지엔 제품 사진뿐. '내열 경량 소재 국내 공급사'를 물으면 대기업 계열사만 나왔습니다.",
  actions=[("AI 가시성 진단","경쟁사가 인용되는 출처(논문·전문지) 분해"),("홈페이지 정비","특허·물성 데이터를 표와 텍스트로 공개, 스키마 탑재"),("기술 칼럼 축적","소재 선정 가이드형 칼럼 8편 + 4채널 변주"),("전문지 보도","산업 전문지 2곳 신소재 소개 기사화")],
  weeks=[("시작",0),("4주",18),("8주",42),("12주",65),("16주",81)],
  qa=[("어떤 게 가장 놀라웠나요?","경쟁사 대신 우리가 먼저 인용되는 걸 처음 봤을 때요. 대기업 사이에 우리 이름이 있었습니다."),
      ("기술 내용을 어떻게 전달하셨나요?","전화 인터뷰 한 번에 30분씩, 나머지는 팀이 알아서 전문가 글로 만들어줬습니다."),
      ("효과를 언제 체감하셨나요?","12주쯤부터요. 견적 요청 메일에 '자료 잘 봤다'는 말이 붙기 시작했습니다.")])

c(slug="equip", tag="자동화 설비", com="○○오토메이션", who="최○○ 이사", photo=U.format("1534528741775-53994a69daeb"),
  title="잘 만들기만 하던 설비회사,<br>AI가 도입 사례까지 소개하는 회사로",
  quote="설비는 잘 만드는데 알리질 못했는데, 이제 AI가 사례까지 소개합니다.",
  period="20주", plan="프리미엄",
  metrics=[("0→8","AI 인용 질문 수","핵심 질문 10개 중"),("84%","AI 답변 등장률","4개 엔진 평균"),("16건","축적 콘텐츠·기사","도입 사례 6편"),("1.8배","상담 요청","시작 전 대비")],
  before="20년 업력에 시공 실적은 많았지만 온라인엔 흔적이 없었습니다. '소규모 라인 맞춤 자동화 업체'를 물으면 플랫폼 광고 업체만 나왔습니다.",
  actions=[("AI 가시성 진단","질문 10개 테스트 — 실적은 많은데 읽을 출처가 0"),("홈페이지 정비","시공 실적을 사례 페이지로 구조화, FAQ 스키마"),("사례 콘텐츠 축적","도입 전후를 담은 사례 칼럼 6편 + 4채널"),("언론 배포","스마트공장 구축 사례 보도 4건")],
  weeks=[("시작",0),("5주",20),("10주",46),("15주",68),("20주",84)],
  qa=[("콘텐츠를 직접 만드셨나요?","아니요. 현장 사진과 짧은 설명만 넘기면 팀이 도입 스토리로 정리해 매달 발행해줬습니다."),
      ("고객 반응이 달라졌나요?","상담 전에 이미 사례를 읽고 오셔서 대화가 빨라졌습니다. '그 사례처럼 해달라'고 하세요."),
      ("계속 하실 건가요?","네. 쌓일수록 유리해지는 구조라 멈출 이유가 없습니다.")])

c(slug="clinic", tag="병원·의원", com="○○치과의원", who="정○○ 원장", photo=P.format("8376281","8376281"),
  title="개원 3년차 동네 치과,<br>'이 근처 임플란트 잘하는 곳' 답이 되기까지",
  quote="광고비 경쟁엔 한계가 있었어요. 이제 AI가 우리 진료 사례를 근거로 추천합니다.",
  period="12주", plan="베이직",
  metrics=[("0→5","AI 인용 질문 수","지역 질문 7개 중"),("89%","AI 답변 등장률","지역 질문 기준"),("11건","축적 콘텐츠","진료 가이드 칼럼"),("1.6배","신규 예약 문의","시작 전 대비")],
  before="네이버 광고 단가는 계속 오르는데 효과는 떨어졌습니다. 환자들이 AI에게 '이 근처 임플란트 잘하는 치과'를 묻기 시작했는데, 답엔 프랜차이즈 치과만 나왔습니다.",
  actions=[("AI 가시성 진단","지역+진료 질문 7개 테스트, 경쟁 치과 출처 분석"),("홈페이지 정비","진료 과목·의료진·장비를 텍스트로, 지역·의료기관 스키마"),("진료 가이드 축적","'임플란트 전 확인할 것' 등 환자 질문형 칼럼 발행"),("블로그 채널 운영","네이버 블로그 지역 콘텐츠 병행")],
  weeks=[("시작",0),("3주",28),("6주",58),("9주",76),("12주",89)],
  qa=[("병원에도 효과가 있나요?","지역 질문이라 오히려 빨랐습니다. 12주 만에 '근처 치과' 질문 답변에 들어갔어요."),
      ("의료광고 규제는 문제없었나요?","과장 없이 진료 정보와 사례 중심이라 오히려 안전합니다. 심의 기준도 함께 챙겨줍니다."),
      ("광고와 비교하면 어떤가요?","광고는 끄면 끝인데 이건 쌓입니다. 광고비 일부를 여기로 옮긴 게 맞았다고 봅니다.")])

c(slug="b2b", tag="B2B 솔루션", com="○○시스템", who="한○○ 영업이사", photo=P.format("17049771","17049771"),
  title="영업사원 인맥에만 의존하던 B2B 솔루션,<br>AI가 만들어주는 인바운드 문의",
  quote="영업이 뛰어야만 문의가 오던 회사였는데, 이제 AI가 먼저 우리를 소개합니다.",
  period="16주", plan="프리미엄",
  metrics=[("0→7","AI 인용 질문 수","핵심 질문 9개 중"),("85%","AI 답변 등장률","4개 엔진 평균"),("15건","축적 콘텐츠·기사","비교 가이드 5편"),("2.2배","인바운드 문의","시작 전 대비")],
  before="제품력은 인정받는데 신규 고객은 전부 영업 인맥. 담당자들이 도입 검토 때 AI에게 '이런 솔루션 어디가 잘해?'를 묻는데 우리는 등장하지 않았습니다.",
  actions=[("AI 가시성 진단","도입 검토 질문 9개 테스트, 경쟁사 인용 출처 분해"),("홈페이지 정비","기능·도입효과를 질문-답 구조로 재편, 스키마"),("비교·가이드 콘텐츠","'도입 전 체크리스트' 등 검토자용 칼럼 축적"),("언론 배포","고객사 도입 성과 보도 5건")],
  weeks=[("시작",0),("4주",21),("8주",49),("12주",70),("16주",85)],
  qa=[("B2B에서 정말 효과가 있나요?","도입 검토자들이 AI로 1차 조사를 합니다. 그 목록에 들어가느냐가 미팅 기회를 가릅니다."),
      ("영업팀 반응은 어떤가요?","'어디서 보고 연락했다'는 콜드하지 않은 문의가 들어오니 영업팀이 제일 좋아합니다."),
      ("도입 팁이 있다면요?","검토자가 물어볼 질문을 정하는 첫 미팅에 영업팀을 꼭 참여시키세요. 질문이 정확해집니다.")])

c(slug="food", tag="식품 중소기업", com="○○식품", who="오○○ 대표", photo=P.format("7964223","7964223"),
  title="30년 제조만 하던 식품회사,<br>납품처가 먼저 찾아오는 회사로",
  quote="영업 없이 30년을 버텼는데, 이제는 AI 검색이 우리 영업사원입니다.",
  period="16주", plan="베이직",
  metrics=[("0→6","AI 인용 질문 수","핵심 질문 8개 중"),("78%","AI 답변 등장률","4개 엔진 평균"),("13건","축적 콘텐츠·기사","HACCP 스토리 포함"),("1.7배","납품 문의","시작 전 대비")],
  before="OEM 납품 위주라 홍보를 해본 적이 없었습니다. 바이어가 'HACCP 인증 소스류 제조사'를 검색해도, AI에 물어도 우리는 없는 회사였습니다.",
  actions=[("AI 가시성 진단","바이어 질문 8개 테스트, 인증·설비 정보 노출 0 확인"),("홈페이지 정비","인증·생산능력·미니멈 수량을 텍스트로 공개"),("콘텐츠 축적","'OEM 파트너 고르는 법' 등 바이어용 칼럼"),("언론 배포","HACCP 갱신·설비 증설 보도 3건")],
  weeks=[("시작",0),("4주",16),("8주",38),("12주",60),("16주",78)],
  qa=[("홍보가 처음이셨는데 어려움은요?","뭘 줘야 할지 몰랐는데, 질문지에 답만 하면 되게 만들어줘서 부담이 없었습니다."),
      ("문의의 질이 달라졌나요?","네. 인증과 생산능력을 이미 알고 연락이 와서, 바로 견적 얘기로 들어갑니다."),
      ("비용 대비 어떤가요?","전시회 한 번 비용으로 1년 내내 쌓이는 걸 생각하면 비교가 안 됩니다.")])

c(slug="franchise", tag="프랜차이즈 외식", com="○○외식", who="강○○ 대표", photo=P.format("3760605","3760605"),
  title="가맹 문의가 끊겼던 외식 브랜드,<br>예비 창업자의 AI 질문에 답이 되기까지",
  quote="창업 카페 홍보만 돌리다 지쳤는데, 이제 예비 점주가 AI로 우리를 먼저 찾아냅니다.",
  period="12주", plan="베이직",
  metrics=[("0→5","AI 인용 질문 수","창업 질문 7개 중"),("82%","AI 답변 등장률","4개 엔진 평균"),("10건","축적 콘텐츠","창업 가이드 칼럼"),("1.9배","가맹 상담 신청","시작 전 대비")],
  before="예비 창업자들이 '소자본 외식 프랜차이즈 추천'을 AI에게 묻기 시작했는데, 답엔 대형 브랜드뿐. 창업 카페 바이럴은 신뢰도 효과도 떨어진 상태였습니다.",
  actions=[("AI 가시성 진단","창업 검토 질문 7개 테스트, 대형 브랜드 출처 분석"),("홈페이지 정비","창업 비용·수익 구조·지원 내용을 표로 공개"),("창업 가이드 축적","'가맹 전 확인할 7가지' 등 예비 점주용 칼럼"),("블로그 채널 운영","네이버 중심 지역·창업 콘텐츠 발행")],
  weeks=[("시작",0),("3주",24),("6주",50),("9주",68),("12주",82)],
  qa=[("바이럴 마케팅과 뭐가 다른가요?","바이럴은 글이 사라지면 끝인데, 이건 우리 홈페이지와 기사에 남아서 계속 일합니다."),
      ("가맹 문의가 실제로 늘었나요?","상담 신청서에 '조건 다 보고 왔다'는 분들이 늘었어요. 상담 시간도 짧아졌습니다."),
      ("아쉬운 점은 없나요?","더 일찍 시작 안 한 거요. 경쟁 브랜드가 먼저 쌓기 시작했으면 아찔했을 겁니다.")])


# ---- 데이터 외부화: data/interviews.json가 있으면 그것을 사용, `--dump`로 최초 1회 내보내기 ----
import json as _json, sys as _sys
_DF = os.path.join(ROOT, "data", "interviews.json")
if "--dump" in _sys.argv:
    os.makedirs(os.path.dirname(_DF), exist_ok=True)
    _json.dump(C, io.open(_DF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("dumped:", _DF); _sys.exit(0)
if os.path.exists(_DF):
    C[:] = _json.load(io.open(_DF, encoding="utf-8"))

CSS = """<style>
:root{--ink:#0A1930;--body:#4A5568;--mut:#8B95A7;--cobalt:#2B5CFF;--cobalt-dk:#1E46D9;--sky:#EAF1FF;--sky-2:#F5F8FD;--mint:#0BBF8C;--line:#E5EAF2;--line-2:#D8E0EC;--sans:'Pretendard',system-ui,sans-serif;--disp:'Poppins',var(--sans);--maxw:1140px;--sh-sm:0 1px 2px rgba(10,25,48,.05),0 4px 14px rgba(10,25,48,.05);--sh:0 12px 34px rgba(16,31,63,.10)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--ink);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
h1,h2,h3{font-weight:800;letter-spacing:-.03em;line-height:1.3;word-break:keep-all}
.btn{font-weight:700;font-size:15.5px;cursor:pointer;display:inline-flex;align-items:center;gap:8px;border-radius:14px;padding:15px 26px;border:1.5px solid transparent;transition:.18s}
.btn-co{background:var(--cobalt);color:#fff;box-shadow:0 8px 22px rgba(43,92,255,.28)}
.btn-co:hover{background:var(--cobalt-dk);transform:translateY(-2px)}
/* nav (서비스 페이지에서 추출한 헤더용) */
.nav{position:sticky;top:0;z-index:70;background:rgba(255,255,255,.9);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;height:72px;gap:40px}
.nav .wrap{max-width:1480px;padding:0 clamp(16px,2.5vw,40px)}
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
.nav-burger{display:none;background:none;border:0;cursor:pointer;padding:10px 4px 10px 10px}
.nav-burger span{display:block;width:22px;height:2.5px;background:var(--ink);border-radius:2px;margin:4.5px 0;transition:.22s}
.mega{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 30px 60px rgba(16,31,63,.14);opacity:0;visibility:hidden;transform:translateY(-8px);transition:.22s;padding:32px 0 36px;z-index:80}
.mega.on{opacity:1;visibility:visible;transform:none}
.mega-in{display:grid;grid-template-columns:225px 1fr 1fr 1fr;gap:36px}
.mega-brand{background:linear-gradient(160deg,#101F3F,#2B5CFF);border-radius:18px;padding:24px 22px;display:flex;flex-direction:column;justify-content:flex-end;min-height:225px;color:#fff}
.mega-brand .bw2{font-family:var(--disp);font-weight:600;font-size:22px}
.mega-brand p{font-size:12.5px;color:#C7D6FF;margin-top:8px;line-height:1.55;font-weight:600}
.mega-col h5{font-size:11.5px;color:var(--mut);font-weight:800;letter-spacing:.05em;margin:0 0 8px 12px}
.mega-col .gap{height:20px}
.mega-col a{display:block;padding:9px 12px;border-radius:12px;transition:.15s}
.mega-col a b{font-size:14.2px;display:block}
.mega-col a span{font-size:12.2px;color:var(--mut);display:block;margin-top:1px}
.mega-col a:hover{background:var(--sky-2)}
.mega-col a:hover b{color:var(--cobalt)}
@media(max-width:900px){.nav-menu{display:none}.nav-burger{display:block}.mega{max-height:calc(100vh - 72px);overflow:auto}.mega-in{grid-template-columns:1fr;gap:18px}.mega-brand{min-height:auto}}
/* case — editorial */
.chero{padding:60px 0 0}
.crumb{font-size:13px;color:var(--mut);font-weight:600;margin-bottom:28px}
.crumb a{color:var(--cobalt)}
.cmeta{font-size:12.5px;font-weight:800;letter-spacing:.06em;color:var(--cobalt);margin-bottom:16px}
.cmeta i{font-style:normal;color:#C4CDDC;margin:0 9px;font-weight:600}
.chero h1{font-size:clamp(28px,4vw,46px);letter-spacing:-.04em;line-height:1.22}
.hfoot{display:flex;align-items:flex-end;justify-content:space-between;gap:40px;margin-top:36px;padding-bottom:38px}
.cwho{display:flex;align-items:center;gap:14px;flex:0 0 auto}
.cwho img{width:76px;height:56px;border-radius:12px;object-fit:contain;background:#fff;border:1px solid var(--line);padding:7px}
.cwho b{display:block;font-size:15px}
.cwho span{font-size:13px;color:var(--mut)}
.cquote{max-width:540px;font-size:16px;font-weight:700;line-height:1.65;color:var(--body);position:relative;padding-left:24px;word-break:keep-all;text-align:left}
.cquote::before{content:"“";position:absolute;left:0;top:-6px;font-family:Georgia,serif;font-size:36px;color:var(--cobalt);line-height:1}
@media(max-width:820px){.hfoot{flex-direction:column;align-items:flex-start;gap:22px}}
/* 성과 밴드 */
.statband{border-top:2px solid var(--ink);border-bottom:1px solid var(--line);display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr 1fr}
.statband>div{padding:26px 22px 24px;border-left:1px solid var(--line)}
.statband>div:first-child{border-left:0;padding-left:0}
.statband b{font-family:var(--disp);font-weight:700;font-size:clamp(24px,2.5vw,34px);letter-spacing:-.02em;display:block;line-height:1.1;white-space:nowrap}
.statband .hero-n b{color:var(--cobalt)}
.statband b em{font-style:normal;font-size:.52em;color:#B9C4D6;margin:0 4px;vertical-align:middle}
.statband .l{font-size:13px;font-weight:800;margin-top:9px;display:block}
.statband .s{font-size:11.5px;color:var(--mut);margin-top:2px;display:block}
@media(max-width:860px){.statband{grid-template-columns:1fr 1fr}.statband>div{padding:18px 14px;border-left:0}.statband>div:nth-child(even){border-left:1px solid var(--line)}.statband>div:nth-child(n+3){border-top:1px solid var(--line)}}
/* 에디토리얼 섹션 */
.esec{display:grid;grid-template-columns:200px 1fr;gap:48px;padding:52px 0;border-bottom:1px solid var(--line)}
.esec.last{border-bottom:0}
.esec .lab i{font-style:normal;font-family:var(--disp);font-weight:700;font-size:12.5px;color:#B9C4D6;letter-spacing:.05em;display:block}
.esec .lab b{display:block;color:var(--ink);font-size:17.5px;letter-spacing:-.02em;margin-top:7px;line-height:1.4;word-break:keep-all}
.esec .lab small{display:block;font-weight:700;font-size:11.5px;color:var(--mut);margin-top:9px;line-height:1.55}
@media(max-width:860px){.esec{grid-template-columns:1fr;gap:20px;padding:40px 0}}
.btxt{max-width:640px;font-size:15.5px;color:var(--body);line-height:1.8;word-break:keep-all}
/* 평가 세부 */
.sdet{display:grid;grid-template-columns:1fr 1fr;gap:6px 60px;max-width:880px}
.sg{font-size:11.5px;font-weight:800;letter-spacing:.05em;color:var(--mut);display:flex;justify-content:space-between;align-items:baseline;padding-bottom:10px;border-bottom:1.5px solid var(--ink)}
.sg b{color:var(--ink);font-size:13px}
.si{display:grid;grid-template-columns:92px 1fr 58px;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid var(--line)}
.si .n{font-size:13px;font-weight:700;color:var(--body);white-space:nowrap}
.si .bar{height:6px;border-radius:99px;background:#EDF1F8;position:relative}
.si .bar i{position:absolute;top:0;bottom:0;left:0;border-radius:99px;background:var(--cobalt)}
.si .bar em{position:absolute;top:-4px;width:2px;height:14px;background:#C3CCDB;border-radius:2px}
.si .v{font-size:12.8px;font-weight:800;text-align:right;color:var(--ink)}
.si .v i{font-style:normal;color:var(--mut);font-weight:700}
.sc-note{font-size:12px;color:var(--mut);margin-top:16px}
@media(max-width:860px){.sdet{grid-template-columns:1fr;gap:4px}}
/* 실행 리스트 */
.axl{max-width:880px}
.axl .r{display:grid;grid-template-columns:46px 200px 1fr;gap:20px;align-items:baseline;padding:17px 0;border-bottom:1px solid var(--line)}
.axl .r:first-child{padding-top:4px}
.axl i{font-style:normal;font-family:var(--disp);font-weight:700;font-size:13px;color:#B9C4D6}
.axl b{font-size:15.5px;letter-spacing:-.01em}
.axl p{font-size:14px;color:var(--body);line-height:1.65;word-break:keep-all}
@media(max-width:860px){.axl .r{grid-template-columns:40px 1fr}.axl p{grid-column:2}}
/* 차트 */
.wchart{max-width:640px}
.cbars{display:flex;align-items:flex-end;height:168px;border-bottom:1.5px solid var(--ink);padding-top:26px}
.cb{flex:1;display:flex;align-items:flex-end;justify-content:center;height:100%}
.cb i{width:min(42px,58%);background:var(--cobalt);position:relative;border-radius:3px 3px 0 0}
.cb i em{position:absolute;top:-23px;left:50%;transform:translateX(-50%);font-style:normal;font-family:var(--disp);font-weight:700;font-size:13px;color:var(--ink);white-space:nowrap}
.cb.zero i{background:#E3E9F4;min-height:4px}
.clabs{display:flex;margin-top:9px}
.clabs span{flex:1;text-align:center;font-size:12px;color:var(--mut);font-weight:700}
.cnote{font-size:12px;color:var(--mut);margin-top:16px}
/* 노출 질문 */
.qx{max-width:880px}
.qxr{display:flex;align-items:center;gap:20px;padding:15px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.qxr:first-child{padding-top:4px}
.qxr .t{flex:1;min-width:240px;font-size:14.8px;font-weight:700;color:var(--ink);word-break:keep-all}
.qxr .t::before{content:"Q. ";color:var(--cobalt);font-weight:800}
.qxe{display:flex;gap:16px;flex-wrap:wrap}
.qxe span{font-size:12px;font-weight:800;color:var(--ink);display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.qxe span::before{content:"✓";color:var(--mint);font-weight:800;font-size:11px}
.qxe span.off{color:#C0C9D8}
.qxe span.off::before{content:"—";color:#D4DBE6}
/* 인터뷰 */
.qa2{max-width:760px}
.qi{padding:20px 0;border-bottom:1px solid var(--line)}
.qi:first-child{padding-top:0}
.qi:last-child{border-bottom:0}
.qi .q{font-size:16px;font-weight:800;letter-spacing:-.01em;word-break:keep-all}
.qi .q i{font-style:normal;color:var(--cobalt);margin-right:9px;font-family:var(--disp)}
.qi .a{font-size:14.5px;color:var(--body);line-height:1.75;margin-top:9px;word-break:keep-all}
.qi .a i{display:none}
.ccta{background:linear-gradient(180deg,#0B1533,#101F3F 60%,#0A1224);color:#fff;text-align:center;padding:72px 0;position:relative;overflow:hidden}
.ccta::before{content:"";position:absolute;inset:0;background:radial-gradient(640px 320px at 50% -10%,rgba(43,92,255,.32),transparent 62%)}
.ccta .wrap{position:relative}
.ccta h2{color:#fff;font-size:clamp(23px,3vw,34px)}
.ccta p{color:#C9D6F5;font-size:15px;margin-top:12px}
.ccta .btn{background:#fff;color:var(--cobalt);margin-top:26px;border-radius:999px;padding:16px 32px;font-weight:800}
.ccta .btn:hover{transform:translateY(-3px)}
/* footer */
.foot{background:#0C1426;color:#8B95A7;padding:56px 0 30px;font-size:13.5px}
.foot a{color:inherit}
@media(max-width:860px){.mgrid{grid-template-columns:1fr 1fr}.alist{grid-template-columns:1fr}}
</style>"""

def bars(weeks):
    mx = max(v for _, v in weeks) or 1
    cells, labels = [], []
    for lb, v in weeks:
        h = int(v / mx * 130) + 5
        cls = ' class="cb zero"' if v == 0 else ' class="cb"'
        cells.append(f'<div{cls}><i style="height:{h}px"><em>{v}%</em></i></div>')
        labels.append(f'<span>{lb}</span>')
    return "".join(cells), "".join(labels)

ENGINES = ["구글 AI", "ChatGPT", "Gemini", "Claude"]

def esec(no, name, body, small="", last=False):
    sm = f"<small>{small}</small>" if small else ""
    return f'<div class="esec{" last" if last else ""}"><div class="lab"><i>{no}</i><b>{name}</b>{sm}</div><div>{body}</div></div>'

def qxs(x):
    rows = []
    for q, on in x.get("questions", []):
        chips = "".join(f'<span{"" if e in on else " class=\"off\""}>{e}</span>' for e in ENGINES)
        rows.append(f'<div class="qxr"><div class="t">{q}</div><div class="qxe">{chips}</div></div>')
    return f'<div class="qx">{"".join(rows)}</div><div class="sc-note">가시성 진단 질문 세트 기준 · 각 엔진의 답변에 인용 또는 추천으로 등장하는 질문입니다.</div>'

def sdet(x):
    s = x["score"]
    def rows(items):
        out = []
        for n, mx, b, a in items:
            pa = round(a / mx * 100)
            pb = round(b / mx * 100)
            out.append(f'<div class="si"><span class="n">{n}</span><span class="bar"><i style="width:{pa}%"></i><em style="left:{pb}%"></em></span><span class="v">{a}<i>/{mx}</i></span></div>')
        return "".join(out)
    seo, ai = s["items"][:3], s["items"][3:]
    seo_a, ai_a = sum(i[3] for i in seo), sum(i[3] for i in ai)
    return f"""<div class="sdet">
<div><div class="sg"><span>SEO 기본기 · 50점</span><b>{seo_a}점</b></div>{rows(seo)}</div>
<div><div class="sg"><span>AI 준비도 · 50점</span><b>{ai_a}점</b></div>{rows(ai)}</div>
</div>
<div class="sc-note">회색 눈금은 도입 전 점수입니다.</div>"""

def page(x):
    s = x["score"]
    stats = f'<div class="hero-n"><b>{s["before"]}<em>→</em>{s["after"]}</b><span class="l">AI 가시성 점수</span><span class="s">100점 만점 · {x["period"]}</span></div>'
    stats += "".join(f'<div><b>{n}</b><span class="l">{l}</span><span class="s">{sm}</span></div>' for n, l, sm in x["metrics"])
    acs = "".join(f'<div class="r"><i>{i+1:02d}</i><b>{t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(x["actions"]))
    qas = "".join(f'<div class="qi"><div class="q"><i>Q.</i>{q}</div><div class="a">{a}</div></div>' for q, a in x["qa"])
    cells, labels = bars(x["weeks"])
    chart = f'<div class="wchart"><div class="cbars">{cells}</div><div class="clabs">{labels}</div><div class="cnote">동일 질문 세트를 주기적으로 재실행해 측정한 AI 답변 등장률입니다. (4개 엔진 평균)</div></div>'
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{x['com']} 성과 인터뷰 | messeze — {x['tag']}</title>
<meta name="description" content="{x['tag']} {x['com']}의 messeze 도입 성과 — {x['period']} 동안의 AI 가시성 변화와 인터뷰.">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
{CSS}
</head>
<body>
{HEADER}

<section class="chero"><div class="wrap">
<div class="crumb"><a href="../interview.html">← 인터뷰 목록</a></div>
<div class="cmeta">{x['tag']}<i>|</i>{x['period']} 진행<i>|</i>{x['plan']} 플랜</div>
<h1>{x['title']}</h1>
<div class="hfoot">
<div class="cwho"><img src="{x['photo']}" alt="{x['com']}" referrerpolicy="no-referrer"><div><b>{x['com']}</b><span>{x['who']} · {x['tag']}</span></div></div>
<blockquote class="cquote">{x['quote']}</blockquote>
</div>
</div></section>

<section style="padding:0 0 30px"><div class="wrap">
<div class="statband">{stats}</div>
{esec("01", "평가 세부", sdet(x), "messeze AI 가시성 평가 기준")}
{esec("02", "시작 전", f'<p class="btxt">{x["before"]}</p>')}
{esec("03", "실행한 것", f'<div class="axl">{acs}</div>')}
{esec("04", "주차별 변화", chart, "AI 답변 등장률")}
{esec("05", "노출 질문", qxs(x), "지금 등장하는 질문")}
{esec("06", f"{x['who']} 인터뷰", f'<div class="qa2">{qas}</div>', last=True)}
</div></section>

<section class="ccta"><div class="wrap">
<h2>우리 회사도 이렇게 될 수 있을까요?</h2>
<p>현재 AI 노출 상태를 무료로 진단해 드립니다. 결과를 보고 결정하세요.</p>
<a class="btn" href="../index.html#final">무료 진단 신청 →</a>
</div></section>

{FOOTER}
</body></html>"""

for x in C:
    io.open(os.path.join(OUT, x["slug"] + ".html"), "w", encoding="utf-8").write(page(x))
print("OK:", len(C), "case pages → interview/")
