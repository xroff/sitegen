#!/usr/bin/env python3

import json
from os import walk, mkdir
from os.path import isfile, join

srcDir = 'src'
siteDir = 'site'


# Init inside vars
menuList = []

class MenuButton:
	stitle=''
	link=''
	def __init__(self, menuJson):
		f_menuJson = open(menuJson)
		data = json.load(f_menuJson)
		f_menuJson.close()
		self.title = data['title']
		self.link = data['link']
	

		

with open(srcDir + '/global.json','r') as configFile:
	globalConf = json.load(configFile)
	configFile.close()

print(globalConf)

stucture = walk(srcDir)



for (path, dirs, files) in stucture:
	dirs.sort()
	print(dirs)
	for button in dirs:
		menuJson = path + '/' + button +'/conf.json'
		if isfile(menuJson):
			menuList.append(MenuButton(menuJson))
	break

print(menuList[0].link)

#for (path, dirs, files) in stucture:
#	dirs.sort()
#	print(path, dirs, files)
#	menuJson = path+'/menu.json'
#	if isfile(menuJson):
#		f_menuJson = open(menuJson)
#		data_f_menuJson = json.load(f_menuJson)
#		menuList.append(data_f_menuJson['title'])
