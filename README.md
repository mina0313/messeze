# messeze — 구독형 기업 PR 랜딩 사이트

기업의 홈페이지·보도자료·전문 콘텐츠를 언론과 AI 검색에 지속 축적해, AI가 그 기업을 이해하고 추천하게 만드는 **구독형 기업 PR(AI 가시성 관리) 서비스** 홍보 사이트입니다.

- **라이브**: https://leegunhee010.github.io/messeze/
- **저장소**: GitHub `leegunhee010/messeze` (master 브랜치, GitHub Pages legacy build)
- 순수 정적 사이트 — 프레임워크·빌드 도구 없음. 서버 없이 브라우저로 바로 열립니다.

---

## 1. 폴더 구조

```
message-landing/
├── index.html          메인 랜딩 (직접 수정)
├── services.html       서비스 개요 — 6개 챕터 롱폼 (직접 수정)
├── pricing.html        요금 — 3티어·비교표·30초 플랜추천 퀴즈·FAQ (직접 수정)
├── check.html          AI 가시성 체크기 — URL 넣으면 100점 진단 (직접 수정)
│
├── build-services.py   → services/ 6개 서비스 상세 페이지 생성
├── build-blog.py       → blog/ 목록 + 글 7개 생성
├── build-glossary.py   → glossary/ 목록 + 용어 102개 생성
│
├── services/           ⚠️ 생성물 — 직접 수정 금지
├── blog/               ⚠️ 생성물 — 직접 수정 금지
└── glossary/           ⚠️ 생성물 — 직접 수정 금지
```

## 2. ⚠️ 가장 중요한 규칙 — 생성 파일

`services/`, `blog/`, `glossary/` 안의 HTML은 **전부 파이썬 스크립트가 굽는 파일**입니다. 직접 수정하면 다음 재생성 때 덮어써져 사라집니다.

수정 방법:

| 고치고 싶은 것 | 수정할 곳 | 재생성 명령 |
|---|---|---|
| 서비스 상세 내용 | `build-services.py`의 `S` 배열 | `python build-services.py` |
| 블로그 글 추가·수정 | `build-blog.py`의 `POSTS` 배열 | `python build-blog.py` |
| 용어 추가·수정 | `build-glossary.py`의 `T` 배열 | `python build-glossary.py` |

Python 3만 있으면 됩니다(외부 패키지 불필요).

## 3. ⚠️ 메가 메뉴 — 6곳 동기화

상단 네비 호버 시 열리는 풀폭 메뉴는 SEO를 위해 각 페이지에 정적 HTML로 **중복 구현**되어 있습니다. 메뉴 항목을 추가·수정하면 아래 6곳을 전부 고치고, py 3개는 재실행해야 합니다.

1. `index.html`
2. `services.html`
3. `pricing.html`
4. `check.html`
5. `build-services.py` (내부 `mega(p)` 템플릿) → 재실행
6. `build-blog.py` / `build-glossary.py` (같은 구조) → 재실행

## 4. 요금 구성 (2026-07 확정)

| | 소상공인형 | 기업형 ★가장 많이 찾는 | 엔터프라이즈 |
|---|---|---|---|
| 1개월 | 월 60만원 | 월 100만원 | 별도 문의 |
| 3개월 | 150만원 (17%↓) | 240만원 (20%↓) | 별도 문의 |

- 전 플랜 공통: AEO·GEO 홈페이지 가시성 평가 월 1회
- 소상공인형: 언론 보도 월 1회 · 기자 1,000명 메일 배포 ×1 · 네이버 1계정 + 티스토리 1계정 각 주 2회
- 기업형: 언론 보도 월 2회 · 기자 3,000명 ×2 · 네이버 1 + 티스토리 2 + 구글 블로거 2계정 각 주 2회 + 홈페이지 수정 또는 GEO·SEO 노출용 구축
- 가격은 표기 그대로(예시 아님). 관련 문구는 `pricing.html`(카드·비교표·퀴즈·FAQ)과 `index.html` 요금 섹션 두 곳에 있음 — 가격 변경 시 둘 다 수정

## 5. AI 가시성 체크기 (check.html)

URL을 넣으면 SEO 기본기 50점 + AI 준비도 50점, 28개 항목을 검사합니다. 정적 사이트라 대상 HTML을 CORS 프록시로 가져옵니다 — 프록시 체인 순서:

1. `corsproxy.io` (1MB 제한, 작은 파일용)
2. `r.jina.ai` + `x-return-format: html` 헤더 (대형·JS 렌더링 사이트, 핵심 경로)
3. `allorigins` (예비 — 자주 다운됨)

jina 경유 시 DOCTYPE 판정은 제외 처리되어 있습니다. 프록시가 전부 막히면 체크기가 동작하지 않으니, 장기적으로는 자체 서버 프록시로 교체 권장.

## 6. 로컬에서 보기 / 배포

```bash
# 로컬 프리뷰 (아무 정적 서버나 가능)
python -m http.server 5677

# 배포 = master에 push하면 GitHub Pages가 자동 반영
git add -A
git commit -m "변경 내용"
git push
```

## 7. 미완료 항목 (인수인계 시점 기준)

- [ ] **실제 로고 교체** — 현재 말풍선 로고는 SVG 재현본. 실제 로고 파일을 받으면 각 페이지의 `.brand svg` 교체 (py 템플릿 포함)
- [ ] **상담 폼 → 구글시트 연결** — `index.html#final`의 무료 진단 신청 폼이 아직 어디에도 저장되지 않음. Apps Script 웹앱(`/exec`) 연결 필요
- [ ] **도메인 확정 시 JSON-LD 치환** — 용어사전 구조화데이터의 `@id`가 `messeze.example` 플레이스홀더. `build-glossary.py`에서 실도메인으로 치환 후 재생성
- [ ] 서비스 워드마크 서체 = Poppins 600, 국문 본문 = Pretendard (CDN 로드)

## 8. 디자인 원칙 (수정 시 지킬 것)

- 팔레트: 잉크네이비 `#0A1930` · 코발트 `#2B5CFF` · 스카이 `#EAF1FF` · 민트 `#0BBF8C`(체크 표시)
- 완벽 대칭·균등 카드 그리드·화살표 다이어그램 금지 — 비대칭 콜라주, 스티커 라벨, 점선 손그림 화살표, 헤어라인 에디토리얼 리스트 + 형광펜 마커(`.mk`)가 이 사이트의 언어입니다. 메인의 "why" 섹션이 표본.
- 타 사이트(salesmap, rinda 등) 색·컴포넌트 값 직접 이식 금지 — 완성도만 참고
