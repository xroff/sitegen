#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from os import mkdir, listdir
from os.path import isfile, isdir, join

# default directories
srcDir = 'src'
siteDir = 'site'

# test direxist
if not isdir(srcDir):
	exit('{}: source dir not exist'.format(srcDir))
if not isdir(siteDir):
	exit('{}: site dir not exist'.format(siteDir))
	
# return list of menu items
def genMenuList(srcDir,conf):
	pagesDir = join(srcDir,conf['pagesDir'])
	menuList = []
	pages = listdir(pagesDir)
	pages.sort()
	for i in pages:
		dirPath = join(pagesDir,i)
		confPatch = join(dirPath,'conf.json')
		if isdir(dirPath) and isfile(confPatch):
			with open(confPatch) as f:
				pageConf = json.load(f,encoding='utf-8')
				if pageConf['menu']=='True':
					pageConf['path'] = dirPath
					print('Adding {} {} to menu'.format(pageConf['title'], pageConf['link']))            #Debug
					menuList.append(pageConf)
	return menuList
	
# Generate pages
def genPages(srcDir, siteDir, menuList, conf):
	pagesDir = join(srcDir,conf['pagesDir'])
	#load templates
	templatePath = join(srcDir,conf['templatesDir'])
	with open(join(templatePath,conf['menuTemplate'])) as f:
		menuTemplateStr = f.read()
		print('Menu template:', menuTemplateStr)
	with open(join(templatePath,conf['mainTemplate'])) as f:
		mainTemplateStr = f.read()
	with open(join(templatePath,conf['contentTemplate'])) as f:
		contentTemplateStr = f.read()
	for page in listdir(pagesDir):
		dirPath = join(pagesDir,page)
		confFilePath = join(dirPath,'conf.json')
		print('Look for', confFilePath)
		if isdir(dirPath) and isfile(confFilePath):
			with open(confFilePath) as f:
				pageConf = json.load(f,encoding='utf-8')
			menuBlock = ''
			contentBlock = ''
			# Generate menu block
			for menuItem in menuList:
				if (dirPath == menuItem['path']): menuItem['active'] = 'class="active"'
				else: menuItem['active'] = ''
				menuBlock += menuTemplateStr.format(**menuItem)
			print('Menu for {}'.format(pageConf['title']))                                               #Debug
			print(menuBlock)                                                                         #Debug
			# Generate contentBlock
			for article in listdir(dirPath):
				articlePath = join(dirPath,article)
				if isfile(articlePath) and article[-5:] == '.html': # only html
					print('Found article', articlePath)                                              #Debug
					with open(articlePath) as f:
						articleText = f.read()
					contentBlock += contentTemplateStr.format(text=articleText)
			print('Content for', pageConf['link'])
			print(contentBlock)                                                                      #Debug
			# Generate html
<<<<<<< HEAD
			pageTitle = pageConf['title'] + ' - ' + conf['title']
=======
			pageTitle = pageConf['title'] + conf['title']
>>>>>>> 1a7df553f94322fe3acd86846e56241f3f9243f2
			with open(join(siteDir,pageConf['link']),'w') as f:
				f.write(mainTemplateStr.format(title=pageTitle,menu=menuBlock,content=contentBlock))
				

# ============================================ Main program ===================================
	
# read global configuration
with open(join(srcDir,'global.json'),'r') as configFile:
	globalConf = json.load(configFile, encoding='utf-8')
print(globalConf)



menuList = genMenuList(srcDir,globalConf)
print('Menu list:', menuList)

genPages(srcDir, siteDir, menuList, globalConf)

				

			




