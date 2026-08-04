# -*- coding: utf-8 -*-
"""messeze 월간 SEO/성능 모니터링 스크립트
실행: python monitor-performance.py
결과: performance-report-YYYY-MM.json"""
import json, os, sys, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

# 모니터링할 페이지
PAGES = [
    {'url': 'https://mina0313.github.io/messeze/', 'name': '홈'},
    {'url': 'https://mina0313.github.io/messeze/index.html', 'name': '홈(index)'},
    {'url': 'https://mina0313.github.io/messeze/check.html', 'name': 'AI 가시성 진단'},
    {'url': 'https://mina0313.github.io/messeze/pricing.html', 'name': '요금'},
    {'url': 'https://mina0313.github.io/messeze/services.html', 'name': '서비스'},
    {'url': 'https://mina0313.github.io/messeze/blog/index.html', 'name': '블로그'},
    {'url': 'https://mina0313.github.io/messeze/glossary/index.html', 'name': '용어사전'},
    {'url': 'https://mina0313.github.io/messeze/interview.html', 'name': '인터뷰'},
]

def get_lighthouse_report(url):
    """Lighthouse CLI로 성능 측정 (로컬)"""
    # 참고: lighthouse CLI 설치 필요 (npm install -g lighthouse)
    # 또는 PageSpeed Insights API 대체
    report = {
        'url': url,
        'timestamp': datetime.datetime.now().isoformat(),
        'note': 'Lighthouse CLI 필요 또는 PageSpeed Insights API 사용'
    }
    return report

def create_monthly_report():
    """월간 성능 리포트 생성"""
    now = datetime.datetime.now()
    report_date = now.strftime('%Y-%m')

    report = {
        'date': report_date,
        'generated': now.isoformat(),
        'pages': [],
        'checklist': {
            'gsc_registered': False,  # ← 수동 입력 필요
            'sitemap_submitted': True,  # ← 이미 완료
            'robots_txt_valid': True,   # ← 이미 완료
            'coverage_errors': 0,       # ← GSC에서 확인
            'core_web_vitals_good': 0,  # ← PageSpeed Insights에서 확인
        },
        'metrics': {
            'clicks_previous_month': 0,  # ← GSC Performance에서 입력
            'impressions_previous_month': 0,  # ← GSC에서 입력
            'ctr_percentage': 0.0,  # ← 계산: clicks/impressions*100
            'avg_position': 0.0,  # ← GSC에서 입력
        },
        'improvements': [
            {'page': '', 'priority': 'high', 'action': ''},  # ← 수동 입력
            {'page': '', 'priority': 'medium', 'action': ''},
            {'page': '', 'priority': 'low', 'action': ''},
        ]
    }

    # 각 페이지 체크
    for page in PAGES:
        page_report = {
            'name': page['name'],
            'url': page['url'],
            'checks': {
                'indexed': None,  # ← GSC URL Inspector에서 "URL is on Google"
                'mobile_friendly': None,  # ← GSC Mobile Usability에서 확인
                'core_web_vitals': None,  # ← PageSpeed Insights
                'lcp_seconds': None,  # LCP < 2.5s
                'fid_ms': None,  # FID < 100ms
                'cls_score': None,  # CLS < 0.1
            }
        }
        report['pages'].append(page_report)

    # 리포트 파일 저장
    report_file = os.path.join(REPORT_DIR, f'performance-report-{report_date}.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report_file, report

def print_checklist():
    """월간 체크리스트 출력"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║           messeze SEO/성능 월간 체크리스트                      ║
╚════════════════════════════════════════════════════════════════╝

📋 필수 확인 사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Google Search Console
   □ https://search.google.com/search-console 로그인
   □ 속성 "https://mina0313.github.io/messeze/" 확인
   □ Sitemap 제출 상태: ✓ (이미 완료)
   □ Coverage 에러 0 확인
   □ Performance 리포트 다운로드

2️⃣  PageSpeed Insights (각 페이지별)
   □ https://pagespeed.web.dev/
   □ 다음 페이지들 체크:
     - https://mina0313.github.io/messeze/
     - https://mina0313.github.io/messeze/check.html
     - https://mina0313.github.io/messeze/pricing.html
   □ Core Web Vitals 점수 기록 (Good/Needs improvement/Poor)
   □ LCP, FID, CLS 값 기록

3️⃣  성능 지표 입력
   □ GSC → Performance에서:
     ✓ 이전월 "클릭" 수
     ✓ 이전월 "노출" 수
     ✓ "평균 순위"
   □ 상위 5개 검색어 기록

4️⃣  에러/경고 확인
   □ Coverage 에러 있는가? (있으면 robots.txt 검증)
   □ Mobile Usability 경고?
   □ Rich Result 오류?

5️⃣  개선 기회 (3개 선정)
   □ CTR이 낮은 페이지 (< 3%)?
   □ 노출되지만 클릭 없는 질문?
   □ Core Web Vitals "Poor"인 페이지?

📊 입력 양식
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

이전월 클릭 수: ___
이전월 노출 수: ___
이전월 평균 순위: ___
이전월 평균 CTR: ___% (계산: 클릭/노출*100)

상위 검색어 3개:
  1. __________ (클릭: ___, 노출: ___)
  2. __________ (클릭: ___, 노출: ___)
  3. __________ (클릭: ___, 노출: ___)

개선할 페이지:
  1. __________ → 액션: ________________
  2. __________ → 액션: ________________
  3. __________ → 액션: ________________

📈 목표
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3개월 목표:
  • CTR: 3% → 5% 이상
  • 평균 순위: 5위 → 3위 이내
  • 월간 클릭: 10 → 20+ per day
  • Core Web Vitals: Good 비율 80% 이상

""")

if __name__ == '__main__':
    report_file, report = create_monthly_report()
    print(f"✓ 리포트 템플릿 생성: {report_file}")
    print(f"✓ 총 {len(report['pages'])}개 페이지 모니터링")
    print_checklist()
