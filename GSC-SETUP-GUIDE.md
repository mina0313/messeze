# Google Search Console 설정 가이드

**목표**: AI 검색 성과를 측정하고, 색인 문제를 조기에 발견

---

## 1단계: 사이트 등록 (Ownership 확인)

### 1.1 Google Search Console 접속
- https://search.google.com/search-console 방문
- Google 계정으로 로그인

### 1.2 속성 추가
1. 좌측 "속성 추가" 클릭
2. URL 입력: `https://mina0313.github.io/messeze/`
3. 계속 클릭

### 1.3 Ownership 확인 (2가지 방법)

**방법 1: DNS 레코드 (권장 - GitHub Pages 사용자)**
1. 사용자 호스팅하는 도메인이 없으면 pass
2. 향후 실 도메인 연결 시 DNS TXT 레코드 추가

**방법 2: HTML 파일 (GitHub Pages용)**
1. GSC에서 제공하는 HTML 파일 다운로드
2. `messeze-live/` 루트에 파일 배치
3. Git commit & push
4. GSC에서 "확인" 클릭

→ **현재 추천**: 방법 2 (GitHub Pages + 정적 파일)

---

## 2단계: Sitemap 제출

1. GSC 좌측 메뉴 → "Sitemaps"
2. URL 입력: `https://mina0313.github.io/messeze/sitemap.xml`
3. 제출 클릭
4. 상태 확인:
   - ✅ "성공" → 모든 페이지 색인 대기
   - ⏳ "처리 중" → 24~48시간 대기
   - ⚠️ "오류" → sitemap.xml 문법 검증

---

## 3단계: Robots.txt 확인

1. GSC 좌측 → "robots.txt 테스터"
2. `robots.txt` 내용 표시됨
3. 확인사항:
   - ✅ 모든 사용자 에이전트에게 허용 (Allow: /)
   - ✅ Disallow에 admin.html, report.html 있음
   - ✅ Sitemap 경로 올바름

---

## 4단계: URL 검사 (정기 체크)

**매주 1회 다음 페이지 검사:**

### 주요 페이지
```
https://mina0313.github.io/messeze/index.html
https://mina0313.github.io/messeze/check.html
https://mina0313.github.io/messeze/pricing.html
https://mina0313.github.io/messeze/services.html
```

### 검사 방법
1. GSC 상단 검색창에 URL 입력
2. "Inspect" 클릭
3. 확인사항:
   - ✅ "URL is on Google" → 색인됨
   - ✅ "Index coverage: Good" → 크롤 신호 정상
   - ⚠️ "Discovered – not indexed" → 색인 대기 (액션: robots.txt 검증)
   - ❌ "Excluded by robots.txt" → Disallow 때문에 차단 (수정 필요)

### Core Web Vitals 확인
- LCP (Largest Contentful Paint): < 2.5초 (권장)
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1

---

## 5단계: Coverage 모니터링 (월 1회)

1. GSC 좌측 → "Coverage"
2. 그래프 확인:
   - 📈 "Valid" (초록): 정상 색인된 페이지
   - ⚠️ "Warnings" (노랑): 색인 가능하나 문제 있음
   - ❌ "Errors" (빨강): 색인 불가 페이지

### 대응
- **Errors 증가**: robots.txt, 구조화 데이터 검증
- **Warnings 증가**: 모바일 사용성, 페이지 속도 점검

---

## 6단계: 성능 리포트 (월간)

### 6.1 클릭/노출 추적
1. GSC 좌측 → "Performance"
2. 필터:
   - 날짜: 지난달 전체
   - 게 유형: 모두
3. 내보내기: 다운로드 후 Excel로 정리

**핵심 지표:**
- **클릭**: AI 검색에서 우리 페이지 방문 수
- **노출**: AI 답변·검색결과에서 우리 사이트 노출 횟수
- **CTR**: 클릭율 (노출 대비 클릭 %). 높을수록 좋음 (5% 이상 목표)
- **평균 순위**: AI 검색 결과에서 몇 번째에 나오는지

### 6.2 분석 표 만들기
```
날짜          | 클릭 | 노출  | CTR  | 순위 | 변화
2026-08-04   | 12   | 240   | 5%   | 3.2  | ↑
2026-08-11   | 15   | 285   | 5.3% | 3.1  | ↑
2026-08-18   | 18   | 330   | 5.5% | 2.9  | ↑↑
```

---

## 7단계: 질문별 추적 (AEO 핵심)

### 7.1 Search Analytics
1. GSC → "Performance"
2. 필터 "Search type" → "Web"
3. 상위 질문 10개 확인
   - "AI 가시성이란"
   - "SEO 최적화 방법"
   - "AEO 뜻"
   - 등

### 7.2 각 질문별 CTR 추적
- 어떤 질문에서 클릭이 높은가?
- 어떤 질문은 노출되지 않는가? (→ 콘텐츠 기회)

---

## 8단계: 에러 해결 가이드

| 에러 | 원인 | 해결책 |
|------|------|--------|
| Discovered – not indexed | 색인 큐 대기 | 1-2주 기다린 후 재검사 |
| Excluded by robots.txt | robots.txt에서 Disallow | robots.txt 수정 후 재배포 |
| Soft 404 | 페이지가 없음 | 페이지 존재 확인, 리다이렉트 설정 |
| Blocked by robots.txt (user-agent: *) | 모든 봇 차단 | robots.txt `Allow: /` 확인 |
| Noindex tag | 메타 태그 noindex | 페이지 HTML에서 제거 |

---

## 9단계: 월간 SEO 체크리스트

**매월 1일 실행:**

- [ ] GSC Performance 리포트 다운로드 → 이전월 대비 분석
- [ ] Coverage 에러 0 확인
- [ ] Core Web Vitals 점수 확인 (PageSpeed Insights)
- [ ] 상위 5개 질문별 CTR 기록
- [ ] 클릭/노출 추세선 그리기
- [ ] 개선 기회 페이지 3개 선정 → 콘텐츠 개선

**지표 목표 (3개월):**
- CTR: 3% → 5% 이상
- 평균 순위: 5위 → 3위 이내
- 클릭: 10 → 20+ per day

---

## 10단계: AI 크롤러 모니터링

### 10.1 GPTBot 확인
1. GSC → "robots.txt 테스터"
2. User-agent: `GPTBot` 입력
3. `/` 디렉토리 검사 → Allow 확인

### 10.2 Google-Extended 확인
1. User-agent: `Google-Extended` 입력
2. Allow 확인

→ **상태**: OpenAI/Google이 학습용으로 수집 중

---

## 다음: Analytics 연결

1. Google Analytics 계정 생성
2. GSC와 GA 연결 (Search Console 설정 → Google Analytics)
3. AI 검색에서 온 트래픽 추적

---

**기한**: 2026-08-07까지 GSC 등록 및 첫 리포트 생성
