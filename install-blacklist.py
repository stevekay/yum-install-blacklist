#!/usr/bin/python
# install-blacklist.py
#
# https://github.com/stevekay/yum-install-blacklist

from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE

from yum import config
import re

requires_api_version = '2.3'
plugin_type = (TYPE_CORE, TYPE_INTERACTIVE)

badrpms = ''

def postreposetup_hook(conduit):
	global badrpms
	repos=conduit.getRepos().listEnabled()
	for repo in repos:
		md = repo.repoXML
		x = str(md.tags['content'])
		x = x[16:]
		x = x[:-3]
		badrpms = x.split(",")

def exclude_hook(conduit):
	global badrpms
	rpmdb = conduit.getRpmDB()
	pkgs = conduit.getPackages()
	for pkg in pkgs:
        	name = pkg.name
		installed = rpmdb.searchNevra(name, None, None, None, None)
		for foo in badrpms:
			if(re.match(foo,name)):
				installed = rpmdb.searchNevra(name, None, None, None, None)
				if len(installed) == 0:
					conduit.delPackage(pkg)
