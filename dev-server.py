#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class DevHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/seo':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                # data/seo.json 저장
                os.makedirs('data', exist_ok=True)
                with open('data/seo.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                # 응답
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'msg': 'SEO 설정이 저장되었습니다.'}).encode('utf-8'))
                print(f"✅ SEO 설정 저장됨")
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
