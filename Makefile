unittest:
	python3 -m unittest test/cfgread.py

run:
	python3 wgchain/wgchain.py protonDE84_ovpn45 test/protonDE84.conf test/ovpn45.conf

realworld:
	python3 wgchain/wgchain.py NL347_ams36 2023_07_09_wgchain/NL347.conf 2023_07_09_wgchain/ams36.conf

clean:
	rm *.conf || true
	rm activate.sh || true
