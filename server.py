import json; #For JSON parsing from request bodies.
from functools import cached_property;

#Basic server and URL struff:
from http.cookies import SimpleCookie;
from http.server import BaseHTTPRequestHandler;
from urllib.parse import parse_qsl, urlparse;
from http.server import HTTPServer;

import cipher; #Custom cipher module.


#The structure of the web server originated from:
#https://realpython.com/python-http-server/#serve-static-and-dynamic-content-programmatically
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

		#The main page at the root redirects to the front page.
		if(self.url.path == "/"):
			self.send_response(302)
			self.send_header('Location', "./public/front.html")
			self.end_headers();

			return;

		#Serve all files in the public folder.
		if(len(urlParts) > 1 and urlParts[0] == "public"):
			try:
				with open('./' + "/".join(urlParts),"r") as file:
					give = file.read();

				#Send a response indicating that everything is ok.
				self.send_response(200);

				#Send the appropriate content type depending on this file.
				if(urlParts[-1].endswith(".html")):
					self.send_header("Content-Type", "text/html")
				elif(urlParts[-1].endswith(".js")):
					self.send_header("Content-Type", "text/javascript")
				elif(urlParts[-1].endswith(".css")):
					self.send_header("Content-Type", "text/css")
				self.end_headers();

				#Then write and give the content.
				self.wfile.write(give.encode("utf-8"));
			except OSError:
				#If an OSError occurs with opening or reading the file, the path was likely wrong and return a 400 error.
				self.send_error(400, "Could not serve content.")
			except:
				#If a miscellaneous error occurs not related to finding and opening the file, return a 404 error.
				self.send_error(404, "Could not serve content.")
			return;

		#Below are all of the handlers for each cipher type/
		if(self.url.path == "/cipher_caesar"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				data["key"] = data["key"] * (-1 if data["revert"] else 1);
				send = cipher.caesarCipher(data["text"],data["key"]).encode("utf-8");
			except:
				self.send_error(400, "Could not cipher string.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

		if(self.url.path == "/cipher_place"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				data["key"] = data["key"] * (-1 if data["revert"] else 1);
				send = cipher.inPlaceCaesarCipher(data["text"],data["key"]).encode("utf-8");
			except:
				self.send_error(400, "Could not cipher string.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

		if(self.url.path == "/cipher_point"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				data["key"] = data["key"] * (-1 if data["revert"] else 1);
				send = cipher.codePointCaesarCipher(data["text"],data["key"],data["lower"],data["upper"]).encode("utf-8");
			except:
				self.send_error(400, "Could not cipher string.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

		if(self.url.path == "/cipher_algebraic"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				if(data["revert"]):
					send = cipher.AlgebraicCipher.decryptAll(data["key"],data["text"]).encode("utf-8");
				else:
					send = cipher.AlgebraicCipher.encryptAll(data["key"],data["text"]).encode("utf-8");
			except:
				self.send_error(400, "Could not cipher string.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

		if(self.url.path == "/cipher_symbol"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				send = cipher.symbolMapCipher(data['alphabet'],data["key"],data["text"],data["revert"]).encode("utf-8");
			except Exception as e:
				print(e)
				self.send_error(400, "Could not cipher string.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

		#Since the length of the Symbol Map Cipher matters, and because it might not be immediately obvious thanks to keywords like "alphabet-standard"
		#or "bigraphic", the server allows the ability to read a key and getn its true length.
		if(self.url.path == "/cipher_symbol_key_length"):
			try:
				data = json.loads(self.post_data.decode("utf-8"));
				send = str(len(cipher.escapeCustomKey1(data["key"]))).encode("utf-8");
			except Exception as e:
				print(e)
				self.send_error(400, "Could not get key length.")
			else:
				self.send_response(200);
				self.send_header("Content-Type", "text/plain");
				self.end_headers();
				self.wfile.write(send);
			return;

	#Handle posts and gets the same way.
	def do_POST(self):
		self.do_GET()

#Start a server on port 8080 if the file is being ran directly.
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), WebRequestHandler);
    server.serve_forever();
