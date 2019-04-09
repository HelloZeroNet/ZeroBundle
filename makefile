build:
	dpkg -b pkg-debian ZeroBundle-linux64.deb
	mv ZeroBundle-linux64.deb dist/

clean:
	rm dist/*.deb

.PHONY: build clean
