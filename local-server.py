# -*- coding: utf-8 -*-
"""messeze 로컬 편집 서버 — 정적 서빙 + 관리자 로컬 저장(POST /__save__)

로컬(:5678)에서 admin.html로 수정하면 GitHub 토큰 없이 이 컴퓨터 파일에 바로 저장된다.
사이트 반영은 클로드가 커밋·푸시. 라이브 관리자는 기존 토큰 방식 그대로.
실행: python local-server.py 5678
"""
import base64
import io
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5678


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass

    def do_POST(self):
        if self.path != '/__save__':
            return self.send_error(404)
        try:
            ln = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(ln).decode('utf-8'))
            path = body.get('file', '')
            ok = False
            if '..' not in path:
                if path.startswith('data/') and path.endswith('.json') and 'content' in body:
                    json.loads(body['content'])  # JSON 검증 후 저장
                    io.open(os.path.join(ROOT, path.replace('/', os.sep)), 'w',
                            encoding='utf-8', newline='\n').write(body['content'])
                    ok = True
                elif path.startswith('assets/uploads/') and 'b64' in body:
                    os.makedirs(os.path.join(ROOT, 'assets', 'uploads'), exist_ok=True)
                    io.open(os.path.join(ROOT, path.replace('/', os.sep)), 'wb'
                            ).write(base64.b64decode(body['b64']))
                    ok = True
        except Exception:
            ok = False
        out = json.dumps({'ok': ok}).encode()
        self.send_response(200 if ok else 400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)


if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
