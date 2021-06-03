virtualenv: 
	if [ ! -d p ]; then \
		python3 -m venv p; \
		. p/bin/activate && pip3 install -r requirements.txt; \
	fi
