rm -Rfv ../../ZeroNet-mac/ZeroNet.app/Contents/Resources/core
cp -fv dist/ZeroNet.app/Contents/MacOS/ZeroNet ../../ZeroNet-mac/ZeroNet.app/Contents/MacOS/ZeroNet
cp -Rv dist/ZeroNet.app/Contents/Resources/core ../../ZeroNet-mac/ZeroNet.app/Contents/Resources/
codesign --verbose=3 --force --sign "Developer ID Application: Tamas Kocsis (4977YF9Q3Z)" ../../ZeroNet-mac/ZeroNet.app
cd ../../ZeroNet-mac/
git add .
git commit -m "Update Update ZeroNet source code"
git push