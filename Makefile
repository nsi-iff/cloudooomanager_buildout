PYTHON=python
PIP=pip

all: clean pip gstreamer argparse redisapi buildout nsicloudooomanager nsimultimedia restfulie should_dsl cyclone funkload test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pip:
	easy_install pip

restfulie:
	$(PIP) install restfulie

cyclone:
	pip install twisted cyclone

nsicloudooomanager:
	@rm -Rf nsi.cloudooomanager-0.1
	@rm -rf nsi.sam-0.1.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.cloudooomanager-0.1.tar.gz
	tar -vzxf nsi.cloudooomanager-0.1.tar.gz
	cd nsi.cloudooomanager-0.1 && ${PYTHON} setup.py install
	@rm -Rf nsi.cloudooomanager-0.1
	@rm -rf nsi.cloudooomanager-0.1.tar.gz

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

argparse:
	sudo apt-get install python-argparse -y

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testCloudoooManager.py
