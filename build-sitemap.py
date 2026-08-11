#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""전체 페이지를 훑어 sitemap.xml과 llms.txt를 생성한다.
빌드 스크립트·inject-meta.py 실행 후에 돌린다."""
import datetime
import json
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

SITE = 'https://mina0313.github.io/messeze'
EXCLUDE = {'admin.html', '_motion-demo.html'}


def page_url(rel):
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html':
        return SITE + '/'
    if rel.endswith('/index.html'):
        return SITE + '/' + rel[:-len('index.html')]
    return SITE + '/' + rel


def lastmod(path):
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%as', '--', path],
                             capture_output=True, text=True, timeout=10)
        d = out.stdout.strip()
        if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
            return d
    except Exception:
        pass
    return datetime.date.today().isoformat()


def tier(rel):
    """(priority, changefreq)"""
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html':
        return '1.0', 'weekly'
    if rel in ('services.html', 'pricing.html', 'check.html', 'faq.html',
               'blog/index.html', 'glossary/index.html', 'interview.html', 'tools.html'):
        return '0.9', 'weekly'
    if rel.startswith('services/') or rel.startswith('interview/'):
        return '0.8', 'monthly'
    if rel.startswith('blog/posts/'):
        return '0.7', 'monthly'
    if rel.startswith('glossary/terms/'):
        return '0.5', 'monthly'
    return '0.6', 'monthly'


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    pages = []
    for dp, dn, fn in os.walk(root):
        if '.git' in dp:
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
            if rel in EXCLUDE:
                continue
            with open(os.path.join(dp, f), encoding='utf-8') as fh:
                h = fh.read()
            if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', h, re.I):
                continue
            pages.append(rel)

    def sort_key(rel):
        pr, _ = tier(rel)
        return (-float(pr), rel)

    pages.sort(key=sort_key)

    rows = []
    for rel in pages:
        pr, cf = tier(rel)
        rows.append('  <url>\n'
                    f'    <loc>{page_url(rel)}</loc>\n'
                    f'    <lastmod>{lastmod(rel)}</lastmod>\n'
                    f'    <changefreq>{cf}</changefreq>\n'
                    f'    <priority>{pr}</priority>\n'
                    '  </url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f'✅ sitemap.xml 생성: {len(pages)}개 URL')

    # ---------------- llms.txt ----------------
    with open('data/posts.json', encoding='utf-8') as f:
        posts = json.load(f)
    with open('data/glossary.json', encoding='utf-8') as f:
        glossary = json.load(f)

    lines = [
        '# messeze',
        '',
        '> 중소기업·병원·수출기업을 위한 구독형 AI 검색 최적화 PR 서비스. '
        '홈페이지 정비, 자사 블로그·언론보도 콘텐츠 축적, 월간 리포트를 통해 '
        'ChatGPT 등 AI 검색과 구글·네이버에서 기업이 추천되도록 만든다. '
        'SEO(검색엔진 최적화), AEO(답변엔진 최적화), GEO(생성형엔진 최적화)를 다룬다.',
        '',
        '## 주요 페이지',
        f'- [서비스 안내]({SITE}/services.html): 진단·홈페이지 정비·콘텐츠·언론보도·채널 운영 전체 서비스 구조',
        f'- [AI 노출 무료 진단]({SITE}/check.html): 우리 회사가 AI 검색에 어떻게 나오는지 무료 진단 신청',
        f'- [가격 안내]({SITE}/pricing.html): 구독형 요금제 안내 (월 60만원부터)',
        f'- [FAQ]({SITE}/faq.html): 서비스 관련 자주 묻는 질문과 답변',
        f'- [업종별 인터뷰]({SITE}/interview.html): 제조·수출·병원 등 업종별 AI 검색 활용 사례',
        '',
        '## 블로그 (AI 검색 시대의 기업 홍보 인사이트)',
    ]
    for p in sorted(posts, key=lambda x: x.get('date', ''), reverse=True):
        lines.append(f"- [{p['title']}]({SITE}/blog/posts/{p['slug']}.html): {p.get('desc', '')}")
    lines += [
        '',
        '## 용어집',
        f'- [SEO·AEO·GEO 용어집]({SITE}/glossary/): AI 검색 최적화 관련 용어 {len(glossary)}선, 용어별 상세 설명 페이지 제공',
        '',
        '## 문의',
        f'- 이메일: hello@messeze.io',
        f'- 사이트: {SITE}/',
    ]
    with open('llms.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'✅ llms.txt 생성: 블로그 {len(posts)}건, 용어 {len(glossary)}건 반영')


if __name__ == '__main__':
    main()
