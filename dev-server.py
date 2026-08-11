#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# API 경로 → 저장할 파일 매핑
API_FILES = {
    '/api/seo': ('data/seo.json', 'SEO 설정'),
    '/api/settings': ('data/settings.json', '사이트 설정'),
}

class DevHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path in API_FILES:
            fname, label = API_FILES[self.path]
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                os.makedirs('data', exist_ok=True)
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'msg': f'{label}이(가) 저장되었습니다.'}).encode('utf-8'))
                print(f"✅ {label} 저장됨 → {fname}")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
                print(f"❌ 오류: {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # 로그 출력 줄임
        pass

def main():
    server = HTTPServer(('localhost', 8000), DevHandler)
    print("🔗 개발 서버 시작: http://localhost:8000")
    print("📝 admin.html에서 SEO 설정을 수정하세요.")
    print("💾 저장하면 data/seo.json이 자동으로 수정됩니다.")
    print("\n중지하려면 Ctrl+C를 누르세요.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n서버 종료")
        server.shutdown()

if __name__ == '__main__':
    main()
