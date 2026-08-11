#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""전 페이지에 canonical·OG·트위터 카드·구조화 데이터(Article/FAQPage)를 주입한다.
빌드 스크립트(build-blog.py 등) 실행 후에 돌려야 하며, 여러 번 실행해도 안전(멱등)."""
import html
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def _load_seo():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'seo.json')
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

SEO = _load_seo()
SITE = (SEO.get('siteUrl') or 'https://mina0313.github.io/messeze').rstrip('/')
OG_IMAGE = SEO.get('ogImage') or (SITE + '/assets/og.png')
EXCLUDE = {'admin.html', '_motion-demo.html'}
MARK_START = '<!-- auto-meta:start -->'
MARK_END = '<!-- auto-meta:end -->'

# 페이지별 OG 문구 오버라이드 (title/description 태그와 다르게 쓰고 싶을 때)
OVERRIDES = {
    'index.html': {
        'og_title': 'messeze — AI가 추천하는 기업을 만듭니다',
        'og_desc': 'AI PR · AI 검색 최적화를 구독형으로. 진단부터 홈페이지 정비, 콘텐츠·언론 축적, 월간 리포트까지 전담팀이 대신합니다.',
    },
}


def page_url(rel):
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html':
        return SITE + '/'
    if rel.endswith('/index.html'):
        return SITE + '/' + rel[:-len('index.html')]
    return SITE + '/' + rel


def grab(pat, h):
    m = re.search(pat, h, re.I | re.S)
    return m.group(1).strip() if m else ''


def strip_existing(h):
    h = re.sub(re.escape(MARK_START) + r'.*?' + re.escape(MARK_END) + r'\n?', '', h, flags=re.S)
    h = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>\n?', '', h, flags=re.I)
    h = re.sub(r'<meta\s+(?:property|name)=["\'](?:og:|twitter:|article:)[^>]*>\n?', '', h, flags=re.I)
    return h


ORG_ID = SITE + '/#organization'
SITE_ID = SITE + '/#website'

def graph_ld(rel, url, title, desc):
    """전 페이지 공통 엔티티 그래프: Organization + WebSite + WebPage(+ 메인은 Service)"""
    org = {
        '@type': 'Organization', '@id': ORG_ID,
        'name': 'messeze', 'alternateName': ['메세지', '주식회사 메세지'],
        'url': SITE + '/',
        'logo': {'@type': 'ImageObject', '@id': SITE + '/#logo', 'url': SITE + '/assets/logo.png'},
        'image': OG_IMAGE,
        'description': '기업의 정보를 언론과 AI 검색에 지속적으로 축적하는 구독형 기업 PR 서비스',
        'email': 'sales@firstmkt.co.kr', 'telephone': '+82-1600-9487',
        'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '대구광역시',
                    'addressLocality': '중구', 'streetAddress': '국채보상로 488, 3층'},
        'sameAs': ['https://github.com/mina0313/messeze'],
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support',
                         'email': 'sales@firstmkt.co.kr', 'telephone': '+82-1600-9487',
                         'availableLanguage': 'Korean'},
    }
    website = {'@type': 'WebSite', '@id': SITE_ID, 'url': SITE + '/', 'name': 'messeze',
               'publisher': {'@id': ORG_ID}, 'inLanguage': 'ko'}
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title,
            'description': desc, 'isPartOf': {'@id': SITE_ID}, 'about': {'@id': ORG_ID},
            'inLanguage': 'ko'}
    graph = [org, website, page]
    if rel == 'index.html':
        graph.append({'@type': 'Service', '@id': SITE + '/#service',
                      'name': 'messeze 구독형 기업 PR',
                      'serviceType': 'AI 검색 최적화 · 기업 PR 구독 서비스',
                      'description': '진단부터 홈페이지 정비, 콘텐츠·언론 축적, 월간 리포트까지 전담팀이 대신 실행합니다.',
                      'provider': {'@id': ORG_ID}, 'areaServed': 'KR', 'url': SITE + '/'})
    return {'@context': 'https://schema.org', '@graph': graph}


def article_ld(post, url):
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': post['title'],
        'description': post.get('desc', ''),
        'datePublished': post.get('date', ''),
        'dateModified': post.get('date', ''),
        'author': {'@type': 'Organization', 'name': 'messeze 편집팀', 'url': SITE + '/'},
        'publisher': {'@type': 'Organization', 'name': 'messeze',
                      'logo': {'@type': 'ImageObject', 'url': OG_IMAGE}},
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        'image': OG_IMAGE,
        'inLanguage': 'ko',
    }


def crumb_ld(items):
    """[(이름, URL), ...] → BreadcrumbList"""
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u}
                                for i, (n, u) in enumerate(items)]}


def interview_faq_ld(iv):
    """인터뷰 문답(qa) → FAQPage"""
    qa = [x for x in (iv.get('qa') or []) if x and len(x) >= 2]
    if not qa:
        return None
    strip = lambda s: re.sub(r'<[^>]+>', '', str(s)).strip()
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': strip(q),
                            'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in qa]}


def faq_ld(faq_data):
    qa = []
    for cat in faq_data:
        for item in cat.get('items', []):
            a = re.sub(r'<[^>]+>', '', item.get('a', ''))
            qa.append({'@type': 'Question', 'name': item.get('q', ''),
                       'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qa}


def build_block(rel, h, posts_by_slug, faq_data, interviews_by_slug):
    url = page_url(rel)
    title = grab(r'<title>(.*?)</title>', h)
    desc = grab(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', h)
    ov = OVERRIDES.get(rel.replace(os.sep, '/'), {})
    og_title = ov.get('og_title', title)
    og_desc = ov.get('og_desc', desc)

    is_post = rel.replace(os.sep, '/').startswith('blog/posts/')
    og_type = 'article' if is_post else 'website'

    e = lambda s: html.escape(s, quote=True)
    lines = [
        MARK_START,
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{e(SEO.get("siteName") or "messeze")}">',
        f'<meta property="og:locale" content="ko_KR">',
        f'<meta property="og:title" content="{e(og_title)}">',
        f'<meta property="og:description" content="{e(og_desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta name="twitter:card" content="{SEO.get("twitterCard") or "summary_large_image"}">',
        f'<meta name="twitter:title" content="{e(og_title)}">',
        f'<meta name="twitter:description" content="{e(og_desc)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]

    # 사이트 공통: 파비콘·테마컬러·검색엔진 인증·애널리틱스
    depth = rel.replace(os.sep, '/').count('/')
    pre = '../' * depth
    fav = SEO.get('favicon')
    if fav:
        ext = 'image/x-icon' if fav.endswith('.ico') else 'image/png'
        lines.append(f'<link rel="icon" type="{ext}" href="{pre}{fav}">')
    apple = SEO.get('appleIcon')
    if apple:
        lines.append(f'<link rel="apple-touch-icon" href="{pre}{apple}">')
    if SEO.get('themeColor'):
        lines.append(f'<meta name="theme-color" content="{SEO["themeColor"]}">')
    if SEO.get('googleVerify'):
        lines.append(f'<meta name="google-site-verification" content="{e(SEO["googleVerify"])}">')
    if SEO.get('naverVerify'):
        lines.append(f'<meta name="naver-site-verification" content="{e(SEO["naverVerify"])}">')
    if SEO.get('gaId'):
        gid = SEO['gaId']
        lines.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>')
        lines.append('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
                     f"gtag('js',new Date());gtag('config','{gid}');</script>")

    ld = json.dumps(graph_ld(rel.replace(os.sep, '/'), url, og_title, og_desc), ensure_ascii=False, indent=1)
    lines.append(f'<script type="application/ld+json">\n{ld}\n</script>')

    slug = os.path.splitext(os.path.basename(rel))[0]
    relu = rel.replace(os.sep, '/')
    if is_post and slug in posts_by_slug:
        post = posts_by_slug[slug]
        if post.get('date'):
            lines.append(f'<meta property="article:published_time" content="{post["date"]}T09:00:00+09:00">')
        ld = json.dumps(article_ld(post, url), ensure_ascii=False, indent=1)
        lines.append(f'<script type="application/ld+json">\n{ld}\n</script>')
        cl = json.dumps(crumb_ld([('홈', SITE + '/'), ('블로그', SITE + '/blog/'), (post['title'], url)]),
                        ensure_ascii=False, indent=1)
        lines.append(f'<script type="application/ld+json">\n{cl}\n</script>')

    if relu.startswith('interview/') and slug in interviews_by_slug:
        iv = interviews_by_slug[slug]
        fq = interview_faq_ld(iv)
        if fq:
            ld = json.dumps(fq, ensure_ascii=False, indent=1)
            lines.append(f'<script type="application/ld+json">\n{ld}\n</script>')
        cl = json.dumps(crumb_ld([('홈', SITE + '/'), ('인터뷰', SITE + '/interview.html'), (iv.get('com', slug), url)]),
                        ensure_ascii=False, indent=1)
        lines.append(f'<script type="application/ld+json">\n{cl}\n</script>')

    if relu == 'faq.html' and faq_data:
        ld = json.dumps(faq_ld(faq_data), ensure_ascii=False, indent=1)
        lines.append(f'<script type="application/ld+json">\n{ld}\n</script>')

    lines.append(MARK_END)
    return '\n'.join(lines) + '\n'


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    with open('data/posts.json', encoding='utf-8') as f:
        posts_by_slug = {p['slug']: p for p in json.load(f)}
    with open('data/faq.json', encoding='utf-8') as f:
        faq_data = json.load(f)
    try:
        with open('data/interviews.json', encoding='utf-8') as f:
            interviews_by_slug = {c['slug']: c for c in json.load(f)}
    except Exception:
        interviews_by_slug = {}

    count = 0
    for dp, dn, fn in os.walk(root):
        if '.git' in dp:
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
            if rel in EXCLUDE:
                continue
            path = os.path.join(dp, f)
            with open(path, encoding='utf-8') as fh:
                h = fh.read()
            if 'noindex' in (grab(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', h) or ''):
                continue
            h = strip_existing(h)
            block = build_block(rel, h, posts_by_slug, faq_data, interviews_by_slug)
            i = h.lower().find('</head>')
            if i < 0:
                print(f'  ⚠️ {rel}: </head> 없음, 건너뜀')
                continue
            h = h[:i] + block + h[i:]
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(h)
            count += 1
    print(f'✅ 메타 주입 완료: {count}페이지')


if __name__ == '__main__':
    main()
