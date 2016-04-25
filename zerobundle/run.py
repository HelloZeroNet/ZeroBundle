import zipfile
import os
import re
import sys
import cStringIO as StringIO


# Request https SSL error workaround
def httpRequest(url, as_file=False):
    if url.startswith("http://"):
        import urllib
        response = urllib.urlopen(url)
    else:  # Hack to avoid Python gevent ssl errors
        import socket
        import httplib
        import ssl

        host, request = re.match("https://(.*?)(/.*?)$", url).groups()

        conn = httplib.HTTPSConnection(host, timeout=15)
        sock = socket.create_connection((conn.host, conn.port), conn.timeout, conn.source_address)
        conn.sock = ssl.wrap_socket(sock, conn.key_file, conn.cert_file)
        conn.request("GET", request)
        response = conn.getresponse()
        if response.status in [301, 302, 303, 307, 308]:
            response = httpRequest(response.getheader('Location'))
    return response


def download(url, target_dir):
    print "Downloading %s to %s directory." % (url, target_dir)
    file = httpRequest(url)
    data = StringIO.StringIO()
    while True:
        buff = file.read(1024 * 16)
        if not buff:
            break
        data.write(buff)
        print ".",
    print "Downloaded."

    print "Extracting...",
    zip = zipfile.ZipFile(data)
    for inner_path in zip.namelist():
        inner_path = inner_path.replace("\\", "/")  # Make sure we have unix path
        print ".",
        dest_path = re.sub("^[^/]*-master.*?/", target_dir + "/", inner_path)  # Change -master dir with target_dir
        if target_dir not in dest_path:
            dest_path = target_dir+"/"+dest_path

        if ".." in dest_path:
            continue
        if not dest_path:
            continue

        dest_dir = os.path.dirname(dest_path)

        if dest_dir and not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        if dest_dir != dest_path.strip("/"):
            data = zip.read(inner_path)
            open(dest_path, 'wb').write(data)

    print "Done."


def getDir(url):
    return re.match(".*/(.+?)$", url).group(1)


if __name__ == "__main__":
    if ";" in sys.argv[1]:
        urls = sys.argv[1].split(";")
    else:
        urls = [sys.argv[1]]
    script = " ".join(['"%s"' % arg for arg in sys.argv[2:]])
    for url in urls:
        target_dir = getDir(url)
        if ".zip" not in url:
            if "github.com" in url:
                url += "/archive/master.zip"
            elif "gitlab.com" in url:
                url += "/repository/archive.zip?ref=master"
            elif "gogs.io" in url:
                url += "/archive/master.zip"

        if not os.path.isdir(target_dir):
            try:
                download(url, target_dir)
                break
            except Exception, err:
                print "Error downloading from %s: %s" % (url, err)
    print "Starting %s/%s..." % (target_dir, script)
    os.chdir(target_dir)
    os.execv("../Python/python", ["../Python/python", '%s' % script.strip("\"'")])
