import json;
from functools import cached_property;
from http.cookies import SimpleCookie;
from http.server import BaseHTTPRequestHandler;
from urllib.parse import parse_qsl, urlparse;
from http.server import HTTPServer;

class WebRequestHandler(BaseHTTPRequestHandler):

	def get_response(self):
		return json.dumps(
			{
				"path": self.url.path,
				"query_data": self.query_data,
				"post_data": self.post_data.decode("utf-8"),
				"form_data": self.form_data,
				"cookies": {
					name: cookie.value
					for name, cookie in self.cookies.items()
				},
			}
		);

	@cached_property
	def url(self):
		return urlparse(self.path)

	@cached_property
	def query_data(self):
		return dict(parse_qsl(self.url.query))

	@cached_property
	def post_data(self):
		content_length = int(self.headers.get("Content-Length", 0))
		return self.rfile.read(content_length)

	@cached_property
	def form_data(self):
		return dict(parse_qsl(self.post_data.decode("utf-8")))

	@cached_property
	def cookies(self):
		return SimpleCookie(self.headers.get("Cookie"))

	def do_GET(self):

		urlParts = self.url.path.split('/');
		urlParts = [string for string in urlParts if string.strip()];

		if(self.url.path == "/"):
			with open('./public/front.html',"r") as file:
				page = file.read();

			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			self.wfile.write(page.encode("utf-8"))
			return;

		if(len(urlParts) > 1 and urlParts[0] == "public"):
			with open('./' + "/".join(urlParts),"r") as file:
				give = file.read();
				self.wfile.write(give.encode("utf-8"))
				self.send_response(200)

	def do_POST(self):
		self.do_GET()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), WebRequestHandler)
    server.serve_forever()
