from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/links"):
            page = b'''<!doctype html><meta charset="utf-8">
<p><a href="https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R1038_D3471_3471.txt">R1038 transcription</a></p>
<p><a href="https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R1040_D3473_3473.txt">R1040 transcription</a></p>
<iframe title="R1038 text" src="https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R1038_D3471_3471.txt" style="width:95vw;height:70vh"></iframe>'''
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return
        page = b'''<!doctype html><meta charset="utf-8">
<form method="post"><input name="name" value="transcript.txt">
<textarea name="text" style="width:95vw;height:80vh"></textarea>
<button type="submit">Save</button></form>'''
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        name = Path(form.get("name", ["transcript.txt"])[0]).name
        text = form.get("text", [""])[0]
        (ROOT / name).write_text(text, encoding="utf-8")
        reply = f"saved {name}: {len(text)} characters".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

    def log_message(self, format, *args):
        pass


HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
