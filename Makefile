.PHONY: test clean

repl:
	. env/bin/activate; ipython

clean:
	python setup.py clean
	find hackpad-cli -type f -name "*.pyc" -exec rm {} \;

env: env/bin/activate

env/bin/activate: requirements.txt setup.py
	test -d env || virtualenv -p python3 --no-site-packages env
	. env/bin/activate ; pip install -U pip wheel
	. env/bin/activate ; pip install -r requirements.txt
	touch env/bin/activate
