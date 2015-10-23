import urllib, zipfile, os,  re, sys
import cStringIO as StringIO

def download(url, target_dir):
    print "Downloading %s to %s directory." % (url, target_dir)
    file = urllib.urlopen(url)
    data = StringIO.StringIO()
    while True:
        buff = file.read(1024*16)
        if not buff: break
        data.write(buff)
        print ".",
    print "Downloaded."

    print "Extracting...",
    zip = zipfile.ZipFile(data)
    for inner_path in zip.namelist():
        inner_path = inner_path.replace("\\", "/") # Make sure we have unix path
        print ".",
        dest_path = re.sub("^[^/]*-master/", target_dir+"/", inner_path) # Change -master dir with target_dir
        if not dest_path: continue

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
    url = sys.argv[1]
    script = " ".join(['"%s"' % arg for arg in sys.argv[2:]])
    target_dir = getDir(url)
    if "github.com" in url and ".zip" not in url: # Download master brach from github
        url += "/archive/master.zip"
    if not os.path.isdir(target_dir):
        download(url, target_dir)
    print "Starting %s/%s..." % (target_dir, script)
    os.chdir(target_dir)
    os.execv("../Python/python.exe", ["../Python/python.exe", '%s' % script])
