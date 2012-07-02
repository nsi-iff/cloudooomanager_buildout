PYTHON=python
PIP=pip

all: clean argparse pip buildout nsicloudooomanager restfulie should_dsl cyclone funkload test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pip:
	easy_install pip

argparse:
	pip install argparse

restfulie:
	$(PIP) install restfulie

cyclone:
	pip install twisted cyclone

nsicloudooomanager:
	pip install https://github.com/nsi-iff/nsi.cloudooomanager/zipball/master
	pip install https://github.com/nsi-iff/nsi.sam/zipball/master

should_dsl:
	pip install should-dsl

funkload:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot -y
	pip install funkload

granualte_test:
	cd tests && python testPerformanceCloudoooManager.py

load_test:
	bin/cloudooomanager_ctl start
	bin/add-user.py test test
	cd tests && fl-run-bench testFunkLoad.py VideoConvertBench.test_convert
	cd tests && fl-build-report --html cloudooomanager-bench.xml -r funkload_report
	bin/cloudooomanager_ctl stop
	bin/del-user.py test

load_test_report:
	cd tests && fl-build-report --html cloudooomanager-bench.xml -r funkload_report

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testCloudoooManager.py
