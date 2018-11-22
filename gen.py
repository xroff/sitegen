#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import markdown
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
			articleList = listdir(dirPath)
			articleList.sort()
			for article in articleList:
				articlePath = join(dirPath,article)
				if isfile(articlePath):
					if article[-5:] == '.html': # only html
						print('Found html article', articlePath)                                              #Debug
						with open(articlePath) as f:
							articleText = f.read()
						contentBlock += contentTemplateStr.format(text=articleText)
					elif article[-3:] == '.md': # markdown
						print('Found markdown article', articlePath)
						with open(articlePath) as f:
							articleText = f.read()
						articleText = markdown.markdown(articleText)
						contentBlock += contentTemplateStr.format(text=articleText)
			print('Content for', pageConf['link'])
			print(contentBlock)                                                                      #Debug
			# Generate html
			pageTitle = pageConf['title'] + ' - ' + conf['title']
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




