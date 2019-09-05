#!/bin/bash
# Requrements: apt install git zip rename
#
#set -x #echo on

rm -rf temp
mkdir temp
cd temp
echo " * Unpack Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O install_miniconda.sh
bash install_miniconda.sh -b -f -p miniconda3 -s -u
rm -rf runtime
mkdir -v runtime


echo " * Copy required packages from Miniconda..."
cp -R miniconda3/pkgs/python-3*/* runtime
cp -R miniconda3/pkgs/xz-*/*
cp -R miniconda3/pkgs/sqlite-*/* runtime
cp -R miniconda3/pkgs/readline-*/* runtime
#cp -R miniconda3/pkgs/ncurses-*/* runtime
cp -R miniconda3/pkgs/libffi-*/* runtime
cp -R miniconda3/pkgs/libstdcxx-*/* runtime
#cp -R miniconda3/pkgs/idna-*/* runtime
#cp -R miniconda3/pkgs/cffi-*/* runtime
cp -R miniconda3/pkgs/bzip2-*/* runtime
cp -R miniconda3/pkgs/openssl-*/* runtime
cp -R miniconda3/pkgs/zlib-*/* runtime
cp -R miniconda3/pkgs/setuptools-*/* runtime
cp -R miniconda3/pkgs/pip-*/* runtime
#cp -R miniconda3/pkgs/certifi-*/* runtime
#cp -R miniconda3/pkgs/idna-*/* runtime
cp -R miniconda3/pkgs/ca-certificates-*/* runtime
cp -R miniconda3/pkgs/xz-*/* runtime

echo -n " * Detecting python version..."
py_ver=$(ls runtime/lib | grep ^python3\\.)
echo $py_ver

echo " * Copy sitecustomize.py to fix ssl cacert path..."
cp ../script/sitecustomize.py runtime/lib/$py_ver/

echo " * Installing required packages..."
runtime/bin/python3 -m pip install -U gevent msgpack coincurve base58 rsa PySocks pyasn1 websocket_client gevent-websocket bencode.py python-bitcoinlib maxminddb
runtime/bin/python3 -m pip install --no-deps -U merkletools


echo " * Cleanup..."
rm -rf runtime/info
rm -rf runtime/include
rm -rf runtime/compiler_compat
rm -rf runtime/info
rm -rf runtime/man
rm -rf runtime/share
rm -rf runtime/ssl/misc
rm -rf runtime/*conda*
rm runtime/ssl/cert.pem
rm runtime/ssl/*cnf*

find runtime/bin ! -name $py_ver ! -name openssl -delete
mv runtime/bin/$py_ver runtime/bin/python3

rm runtime/lib/*.a
rm runtime/lib/*.la
rm runtime/lib/libpython3*
rm -rf runtime/lib/pkgconfig
rm -rf runtime/lib/engines-*

find runtime | grep -E "(__pycache__|\.pyc|\.pyo|\.c|\.h|\.html|\.pxd|test|testing|tests)$" | xargs rm -rf


echo " * Remove library symlinks"
find runtime/lib -type l -delete


echo " * Rename .so files to keep only the major version (to avoid use of symlinks)"
find runtime/lib -maxdepth 1 -type f -name *.so.* -not -name *libcrypto* -not -name *libssl* \
-exec rename 's/(\.so\.[0-9]+)\..*$/$1/' {} +


echo " * Cleanup site-packages..."
rm -rf runtime/lib/$py_ver/site-packages/pip
rm -rf runtime/lib/$py_ver/site-packages/setuptools
rm -rf runtime/lib/$py_ver/site-packages/*-info


echo " * Strip binaries..."
du -hs runtime
find runtime | xargs file | grep "executable" | grep ELF | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null
du -hs runtime


echo " * Strip shared objects..."
du -hs runtime
find runtime | xargs file | grep "shared object" | grep ELF | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null
du -hs runtime


echo " * Remove unnecessary stdlib packages..."
rm -rf runtime/lib/$py_ver/lib2to3
rm -rf runtime/lib/$py_ver/tkinter
rm -rf runtime/lib/$py_ver/turtledemo
rm -rf runtime/lib/$py_ver/unittest
rm -rf runtime/lib/$py_ver/pydoc_data
rm -rf runtime/lib/$py_ver/idlelib
rm -rf runtime/lib/$py_ver/ensurepip
rm -rf runtime/lib/$py_ver/distutils
rm -rf runtime/lib/$py_ver/config-*


echo "* Zip stdlib..."
cd runtime/lib/$py_ver/
zip -r ../${py_ver/./}.zip . -x site-packages/\* -x lib-dynload/\*
cd ../../..


echo "* Remove unpacked stdlib..."
find runtime/lib/$py_ver/* ! -name site.py ! -name os.py ! -name sitecustomize.py ! -path */site-packages* ! -path */lib-dynload* -delete


echo -n "* Testing https request..."
runtime/bin/python3 -c 'assert len(__import__("urllib.request").request.urlopen("https://zeronet.io").read()) > 0; print("ok")'


echo -n "* Runtime size: "
du -hs runtime

cd ..

rm -rf build
mkdir -v build

cd build

git clone https://github.com/HelloZeroNet/ZeroNet.git core
mv ../temp/runtime runtime

rm -rf core/.git

cp ../script/ZeroNet.sh .
chmod +x ZeroNet.sh

cd ..

echo -n "ZeroBundle generated to build directory"
