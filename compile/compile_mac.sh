rm -rf build
rm -rf dist
python zeronet_mac_py2app.py py2app -O2
cd ../../ZeroNet
git pull
cd -
git clone --depth 1 file://$(pwd)/../../ZeroNet/.git dist/ZeroNet.app/Contents/Resources/core
echo "Cleanup..."
rm -rf dist/ZeroNet.app/Contents/Resources/include
rm -rf dist/ZeroNet.app/Contents/Resources/core/.git
rm -rf dist/ZeroNet.app/Contents/Resources/core/src/Test/testdata
rm dist/ZeroNet.app/Contents/Resources/core/src/lib/opensslVerify/libeay32.dll
rm dist/ZeroNet.app/Contents/Resources/core/src/lib/opensslVerify/ssleay32.dll
rm dist/ZeroNet.app/Contents/Resources/core/src/lib/opensslVerify/openssl.exe
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/libev/*.c"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/libev/*.h"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/libev/*.ppyx"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/libev/*.pxd"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/libev/*.pyx"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/*.c"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/*.h"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/*.ppyx"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/*.pxd"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "gevent/*.pyx"
zip -d dist/ZeroNet.app/Contents/Resources/lib/python2.7/site-packages.zip "pydoc_data/*"
echo "Copy __error__.sh"
cp -f tools/__error__.sh dist/ZeroNet.app/Contents/Resources/__error__.sh
