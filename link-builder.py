# -*- coding: utf-8 -*-
"""Internal linking 시스템: 블로그와 용어사전 자동 연결
실행: python link-builder.py"""
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. posts.json과 glossary.json 로드
with open(os.path.join(ROOT, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    POSTS = json.load(f)
with open(os.path.join(ROOT, 'data', 'glossary.json'), 'r', encoding='utf-8') as f:
    GLOSSARY = json.load(f)

# 2. 각 용어에 관련 블로그 매칭
def find_related_blogs(term):
    """용어가 포함된 모든 포스트 찾기"""
    ko_term = term['ko'].split('(')[0].strip()  # "AEO (답변엔진...)" → "AEO"
    en_term = term['en'].split('(')[0].strip() if '(' in term['en'] else term['en']
    slug = term['slug']

    related = []
    for post in POSTS:
        body = post.get('body', '')
        title = post.get('title', '')
        # 정규식: 단어 경계를 고려하여 용어 검색 (대소문자 무시)
        if re.search(r'\b' + re.escape(ko_term) + r'\b', body, re.IGNORECASE) or \
           re.search(r'\b' + re.escape(en_term) + r'\b', body, re.IGNORECASE):
            related.append({
                'slug': post['slug'],
                'title': post['title'],
                'cat': post['cat']
            })

    return related

# 3. glossary.json에 relatedBlogs 추가
for term in GLOSSARY:
    term['relatedBlogs'] = find_related_blogs(term)
    if term['relatedBlogs']:
        print(f"✓ {term['ko']}: {len(term['relatedBlogs'])}개 블로그 연결")

# 4. 수정된 glossary.json 저장
with open(os.path.join(ROOT, 'data', 'glossary.json'), 'w', encoding='utf-8') as f:
    json.dump(GLOSSARY, f, ensure_ascii=False, indent=1)

print(f"\n✅ glossary.json 업데이트 완료: 총 {len(GLOSSARY)}개 용어")
print(f"총 {sum(len(t.get('relatedBlogs', [])) for t in GLOSSARY)}개의 블로그 연결")
