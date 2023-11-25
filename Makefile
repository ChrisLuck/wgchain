unittest:
	python3 -m unittest test/cfgread.py

run:
	python3 wgchain/wgchain.py test/protonDE84.conf test/ovpn45.conf

clean:
	rm *.conf
