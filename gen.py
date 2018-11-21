#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from os import walk, mkdir, listdir
from os.path import isfile, isdir, join

srcDir = 'src'
siteDir = 'site'

# test direxist
if not isdir(srcDir):
	exit('{}: source dir not exist'.format(srcDir))

if not isdir(siteDir):
	exit('{}: site dir not exist'.format(siteDir))

# Init inside vars
menuList = []
pagesDir = join(srcDir,'pages')

		
# read global configuration
with open(join(srcDir,'global.json'),'r') as configFile:
	globalConf = json.load(configFile, encoding='utf-8')
print(globalConf)
globalConf['templatesDir']    = join(srcDir,globalConf['templatesDir'])
globalConf['mainTemplate']    = join(globalConf['templatesDir'],globalConf['mainTemplate'])
globalConf['menuTemplate']    = join(globalConf['templatesDir'],globalConf['menuTemplate'])
globalConf['contentTemplate'] = join(globalConf['templatesDir'],globalConf['contentTemplate'])

# Firstly generate menu list
pages = listdir(pagesDir)
pages.sort()
for i in pages:
	dirPath = join(pagesDir,i)
	confFilePath = join(dirPath,'conf.json')
	if isdir(dirPath) and isfile(confFilePath):
		with open(confFilePath) as confFile:
			conf = json.load(confFile,encoding='utf-8')
			if conf['menu']=='True':
				conf['path'] = dirPath
				print('Adding {} {} to menu'.format(conf['title'], conf['link']))
				menuList.append(conf)
				
# Next generate pages
with open(globalConf['menuTemplate']) as f:
	menuTemplateStr = f.read()
with open(globalConf['mainTemplate']) as f:
	mainTemplateStr = f.read()
with open(globalConf['contentTemplate']) as f:
	contentTemplateStr = f.read()

for page in listdir(pagesDir):
	dirPath = join(pagesDir,page)
	confFilePath = join(dirPath,'conf.json')
	if isdir(dirPath) and isfile(confFilePath):
		with open(confFilePath) as confFile:
			pageConf = json.load(confFile,encoding='utf-8')
			#generate menu
			menuBlock = ''
			for menuItem in menuList:
				if (dirPath == menuItem['path']): menuItem['active'] = 'class="active"'
				else: menuItem['active'] = ''
				menuBlock += menuTemplateStr.format(**menuItem)
			print('Menu for {}'.format(conf['title']))
			print(menuBlock)

			




