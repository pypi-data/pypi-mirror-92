import configparser
import time
from datetime import datetime, timedelta
import threading
import re
import os
import base64
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from OpenSSL import crypto
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from dotenv import load_dotenv


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

load_dotenv()

config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "pybungie.ini")
config = configparser.ConfigParser()
config.read_file(open(config_file_path))
SERVER_CERTIFICATE = config['SERVER_CERTIFICATE']

exp_urlpost = r'urlPost:\'(https://.*?)\''
exp_ppft = r'<input type="hidden" name="PPFT" id=".*" value="(.*?)"/>'
TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"
BUNGIE_SIGN_IN_URI = "https://www.bungie.net/en/User/SignIn/Xuid?bru=%252f"

RETRIED_AUTH = RETRIED_TOKEN = RETRIED_RENEWAL = RETRIED_SERVER = False


class OAuth2:

    def __init__(self, api, client_id: str, client_secret: str):
        ENCODED_DATA = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
        self.__headers = {
            "Authorization": "Basic " + ENCODED_DATA,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.__api = api
        self.__httpd = HTTPServer(('127.0.0.1', 5000), SimpleHTTPRequestHandler)
        os.environ["CLIENT-ID"] = client_id
        os.environ["CLIENT-SECRET"] = client_secret
        self.__cert_gen()
        self.__start_server()
        self.__get_authorization_code()
        self.__get_tokens()
        self._enabled = True
        self.__renewal_thread = threading.Thread(target=self.__renew_tokens)
        self.__renewal_thread.start()

    @staticmethod
    def __cert_gen():
        serial_number = 0
        validity_end_in_seconds = 10 * 365 * 24 * 60 * 60
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        cert = crypto.X509()
        cert.get_subject().C = SERVER_CERTIFICATE["COUNTRY_NAME"]
        cert.get_subject().ST = SERVER_CERTIFICATE["STATE_OR_PROVINCE_NAME"]
        cert.get_subject().L = SERVER_CERTIFICATE["LOCALITY_NAME"]
        cert.get_subject().O = SERVER_CERTIFICATE["ORGANIZATION_NAME"]
        cert.get_subject().OU = SERVER_CERTIFICATE["ORGANIZATION_UNIT_NAME"]
        cert.get_subject().CN = SERVER_CERTIFICATE["COMMON_NAME"]
        cert.get_subject().emailAddress = SERVER_CERTIFICATE["EMAIL_ADDRESS"]
        cert.set_serial_number(serial_number)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validity_end_in_seconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        with open("server.pem", "w") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open("server.pem", "a") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

    def __start_server(self):
        try:
            self.__httpd.socket = ssl.wrap_socket(self.__httpd.socket, certfile='server.pem', server_side=True)
            self.server_thread = threading.Thread(target=self.__httpd.serve_forever)
            self.server_thread.start()
        except:
            global RETRIED_SERVER
            if not RETRIED_SERVER:
                RETRIED_SERVER = True
                with open('err.log', 'a') as f:
                    f.write(f'WARNING Server startup failed! {datetime.now().strftime("%m/%d/%Y at %H:%M:%S")} \n')
                self.__cert_gen()
                self.__start_server()

    def __get_authorization_code(self):
        try:
            if not self.server_thread.is_alive():
                self.__start_server()
            s = requests.Session()
            r = s.get(BUNGIE_SIGN_IN_URI)
            url_post = re.findall(exp_urlpost, r.content.decode())[0]
            ppft = re.findall(exp_ppft, r.content.decode())[0]
            payload = {'login': os.environ["XBOX-EMAIL"], 'passwd': os.environ["XBOX-PASS"], 'PPFT': ppft}
            s.post(url_post, data=payload)
            api_headers = {'X-API-Key': os.environ["X-API-KEY"], 'x-csrf': s.cookies.get_dict()['bungled']}
            r = s.get(
                f'https://www.bungie.net/en/OAuth/Authorize?client_id={os.environ["CLIENT-ID"]}&response_type=code',
                headers=api_headers,
                verify=False)
            os.environ["AUTH-CODE"] = urlparse(url=r.url).query[5:]
            self.__httpd.shutdown()
        except:
            global RETRIED_AUTH
            if not RETRIED_AUTH:
                RETRIED_AUTH = True
                with open('err.log', 'a') as f:
                    f.write(
                        f'WARNING Unable to acquire authentication code! {datetime.now().strftime("%m/%d/%Y at %H:%M:%S")}\n')
                self.__get_authorization_code()

    def __get_tokens(self):
        try:
            data = {
                'grant_type': "authorization_code",
                'code': os.getenv("AUTH-CODE"),
            }
            response = requests.post(url=TOKEN_URL, headers=self.__headers, data=data)
            response = response.json()
            os.environ["ACCESS-TOKEN"] = response['access_token']
            os.environ["REFRESH-TOKEN"] = response['refresh_token']
            self.__api._renew_headers()
        except:
            global RETRIED_TOKEN
            if not RETRIED_TOKEN:
                RETRIED_TOKEN = True
                with open('err.log', 'a') as f:
                    f.write(f'WARNING Unable to acquire tokens! {datetime.now().strftime("%m/%d/%Y at %H:%M:%S")}\n')
                self.__get_authorization_code()
                self.__get_tokens()

    def __renew_tokens(self):
        while self._enabled:
            token_expiration = datetime.now() + timedelta(minutes=59)
            while datetime.now() < token_expiration and self._enabled:
                time.sleep(5)
            try:
                data = {
                    'grant_type': "refresh_token",
                    'refresh_token': os.environ["REFRESH-TOKEN"],
                }
                response = requests.post(url=TOKEN_URL, headers=self.__headers, data=data)
                response = response.json()
                os.environ["ACCESS-TOKEN"] = response['access_token']
                os.environ["REFRESH-TOKEN"] = response['refresh_token']
                self.__api._renew_headers()
            except:
                global RETRIED_RENEWAL
                if not RETRIED_RENEWAL:
                    RETRIED_RENEWAL = True
                    with open('err.log', 'a') as f:
                        f.write(f'WARNING Unable to renew tokens! {datetime.now().strftime("%m/%d/%Y at %H:%M:%S")}\n')
                    self.__get_authorization_code()
                    self.__get_tokens()
