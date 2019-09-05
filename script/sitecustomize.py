import os
import sys


os.environ["SSL_CERT_FILE"] = os.path.normpath(os.path.dirname(sys.executable) + "/../ssl/cacert.pem")
os.environ["REQUESTS_CA_BUNDLE"] = os.environ["SSL_CERT_FILE"]