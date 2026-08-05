#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import os

SEO_FILE = 'data/seo.json'

def load_seo():
    with open(SEO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def inject_seo(html_content, page_config, site_config):
    """HTML에 SEO 메타 태그를 주입"""
    title = page_config.get('title', '')
    description = page_config.get('description', '')
    keywords = page_config.get('keywords', '')
    noindex = page_config.get('noindex', False)
    og_image = site_config.get('ogImage', '')
    head_code = page_config.get('headCode', '')

    # <head> 태그 찾기
    head_match = re.search(r'(<head[^>]*>)', html_content, re.IGNORECASE)
    if not head_match:
        print(f"  ❌ <head> 태그를 찾을 수 없음")
        return html_content

    head_tag = head_match.group(1)
    head_end = head_match.end()

    # 기존 메타 태그 제거
    # <title>
    html_content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{title}</title>',
        html_content,
        flags=re.IGNORECASE
    )
    if '<title>' not in html_content:
        insert_content = f'<title>{title}</title>\n'
        html_content = html_content[:head_end] + insert_content + html_content[head_end:]

    # <meta name="description">
    if re.search(r'<meta\s+name=["\']?description["\']?', html_content, re.IGNORECASE):
        html_content = re.sub(
            r'<meta\s+name=["\']?description["\']?\s+content=["\']?[^"\']*["\']?/?[^>]*>',
            f'<meta name="description" content="{description}">',
            html_content,
            flags=re.IGNORECASE
        )
    else:
        insert_pos = html_content.find('</head>')
        insert_content = f'<meta name="description" content="{description}">\n'
        html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]

    # <meta name="keywords">
    if keywords:
        if re.search(r'<meta\s+name=["\']?keywords["\']?', html_content, re.IGNORECASE):
            html_content = re.sub(
                r'<meta\s+name=["\']?keywords["\']?\s+content=["\']?[^"\']*["\']?/?[^>]*>',
                f'<meta name="keywords" content="{keywords}">',
                html_content,
                flags=re.IGNORECASE
            )
        else:
            insert_pos = html_content.find('</head>')
            insert_content = f'<meta name="keywords" content="{keywords}">\n'
            html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]

    # <meta property="og:image">
    if og_image:
        if re.search(r'<meta\s+property=["\']?og:image["\']?', html_content, re.IGNORECASE):
            html_content = re.sub(
                r'<meta\s+property=["\']?og:image["\']?\s+content=["\']?[^"\']*["\']?/?[^>]*>',
                f'<meta property="og:image" content="{og_image}">',
                html_content,
                flags=re.IGNORECASE
            )
        else:
            insert_pos = html_content.find('</head>')
            insert_content = f'<meta property="og:image" content="{og_image}">\n'
            html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]

    # noindex 처리
    if noindex:
        if not re.search(r'<meta\s+name=["\']?robots["\']?\s+content=["\']?noindex', html_content, re.IGNORECASE):
            insert_pos = html_content.find('</head>')
            insert_content = f'<meta name="robots" content="noindex,nofollow">\n'
            html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]
    else:
        # noindex 제거 (다른 robots 설정 유지)
        html_content = re.sub(
            r'<meta\s+name=["\']?robots["\']?\s+content=["\']?noindex[^"\']*["\']?/?[^>]*>',
            '',
            html_content,
            flags=re.IGNORECASE
        )

    # 맞춤 HEAD 코드 추가
    if head_code.strip():
        insert_pos = html_content.find('</head>')
        insert_content = f'{head_code}\n'
        html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]

    return html_content

def main():
    if not os.path.exists(SEO_FILE):
        print(f"❌ {SEO_FILE}을 찾을 수 없습니다.")
        return

    seo = load_seo()
    site_config = {
        'ogImage': seo.get('ogImage', '')
    }

    print("🔗 SEO 메타 태그 주입 시작...\n")

    for page_name, page_config in seo.get('pages', {}).items():
        file_path = page_config.get('file')
        if not file_path or not os.path.exists(file_path):
            print(f"  ⚠️  {page_name} ({file_path}): 파일을 찾을 수 없음")
            continue

        print(f"  📝 {page_name} ({file_path})...")

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        html_content = inject_seo(html_content, page_config, site_config)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"     ✅ 완료")

    print("\n✅ SEO 메타 태그 주입 완료!")

if __name__ == '__main__':
    main()
