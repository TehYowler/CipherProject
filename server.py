import json;
from functools import cached_property;
from http.cookies import SimpleCookie;
from http.server import BaseHTTPRequestHandler;
from urllib.parse import parse_qsl, urlparse;
from http.server import HTTPServer;
import cipher;
import http;

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
			self.send_response(302)
			self.send_header('Location', "./public/front.html")
			self.end_headers();

			return;

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

		if(self.url.path == "/cookie_save"):
			try:
				cookies_string = self.headers.get('Cookie');

				cookies = SimpleCookie();
				if(cookies_string):
					cookies.load(cookies_string);

				if('stored_cipher_cookie' not in cookies):
					cookies['stored_cipher_cookie'] = "[]";

				dataReq = json.loads(self.post_data.decode("utf-8"));
				try:
					dataCookie = json.loads(cookies['stored_cipher_cookie'].value);
				except json.JSONDecodeError:
					raise Exception("Malformed cookie data!");

				if("remove" in dataReq):
					dataReq["remove"] = int(dataReq["remove"]);
					# print(dataReq["remove"])
					dataCookie = dataCookie[0:dataReq["remove"]] + dataCookie[dataReq["remove"] + 1:];
				else:
					dataCookie.append(dataReq);

				cookies['stored_cipher_cookie'] = json.dumps(dataCookie);
				self.send_response(200);
				for morsel in cookies.values():
					morsel['max-age'] = 2147483647;
					self.send_header("Set-Cookie", morsel.OutputString());
				self.end_headers();
			except Exception as e:
				print(e)
				self.send_error(400, "Could not save cookie.")
			return;

		if(self.url.path == "/cookie_get"):
			try:
				cookies_string = self.headers.get('Cookie');

				cookies = SimpleCookie();
				if(cookies_string):
					cookies.load(cookies_string);

				if('stored_cipher_cookie' not in cookies):
					cookies['stored_cipher_cookie'] = "[]";

				self.send_response(200);
				self.send_header("Content-Type", "text/plain")
				self.end_headers();
				self.wfile.write(cookies['stored_cipher_cookie'].value.encode("utf-8"));

			except Exception as e:
				print(e)
				self.send_error(400, "Could not save cookie.")
			return;

		if(len(urlParts) > 1 and urlParts[0] == "public"):
			with open('./' + "/".join(urlParts),"r") as file:
				give = file.read();

			self.send_response(200)
			if(urlParts[-1].split(".")[-1] == "html"):
				self.send_header("Content-Type", "text/html")
			elif(urlParts[-1].split(".")[-1] == "js"):
				self.send_header("Content-Type", "text/javascript")
			self.end_headers()
			self.wfile.write(give.encode("utf-8"))

	def do_POST(self):
		self.do_GET()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), WebRequestHandler)
    server.serve_forever()
