#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/copy.json의 문구를 HTML에 새겨 넣는다.
data-copy="키" 속성이 붙은 요소의 내용을 교체한다.
관리자에서 copy.json을 저장하면 GitHub Actions가 이 스크립트를 돌려 정적 HTML에 반영한다.
(자바스크립트 치환이 아니라 HTML에 직접 새기므로 AI 크롤러가 그대로 읽는다.)

실행: python build-copy.py            → copy.json 값을 HTML에 주입
      python build-copy.py --extract  → 현재 HTML 문구로 copy.json 생성/갱신
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
COPY_FILE = os.path.join(ROOT, 'data', 'copy.json')

# 카피를 관리할 페이지 (파일명 → copy.json 안의 그룹명)
PAGES = {
    'index.html': 'home',
    'pricing.html': 'pricing',
}

# data-copy="키" 요소의 여는 태그 ~ 닫는 태그
TAG_RE = re.compile(
    r'(<(\w+)[^>]*\bdata-copy="([^"]+)"[^>]*>)(.*?)(</\2>)',
    re.S
)


def extract():
    """현재 HTML 문구를 읽어 copy.json 생성"""
    data = {}
    if os.path.exists(COPY_FILE):
        with io.open(COPY_FILE, encoding='utf-8') as f:
            data = json.load(f)

    for fname, group in PAGES.items():
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            continue
        with io.open(path, encoding='utf-8') as f:
            html = f.read()
        found = {}
        for m in TAG_RE.finditer(html):
            key = m.group(3)
            found[key] = m.group(4).strip()
        data.setdefault(group, {})
        # 새 키만 추가하고 기존 값은 보존
        for k, v in found.items():
            data[group].setdefault(k, v)
        print(f'  {fname}: {len(found)}개 문구')

    os.makedirs(os.path.dirname(COPY_FILE), exist_ok=True)
    with io.open(COPY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'OK: {COPY_FILE} 생성')


def inject():
    """copy.json 값을 HTML에 주입"""
    if not os.path.exists(COPY_FILE):
        print('data/copy.json이 없습니다. --extract로 먼저 생성하세요.')
        return
    with io.open(COPY_FILE, encoding='utf-8') as f:
        data = json.load(f)

    for fname, group in PAGES.items():
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path) or group not in data:
            continue
        with io.open(path, encoding='utf-8') as f:
            html = f.read()
        copy = data[group]
        changed = [0]

        def rep(m):
            key = m.group(3)
            if key in copy and copy[key] != m.group(4).strip():
                changed[0] += 1
                return m.group(1) + copy[key] + m.group(5)
            return m.group(0)

        html = TAG_RE.sub(rep, html)
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  {fname}: {changed[0]}개 문구 반영')
    print('OK: 카피 주입 완료')


if __name__ == '__main__':
    if '--extract' in sys.argv:
        extract()
    else:
        inject()
