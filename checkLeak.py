# -*- coding: utf-8 -*-

import sys
import os
import Foundation
import objc
import AppKit
from datetime import date, time, datetime, timedelta

#工程路径
projectPath = "/Users/yuyang/Documents/techwolf/mobile_ios"
#不检测路径
noPath = ['ThirdLibs','iosTools']
#False:检测所有,True:不检测不检测路径和动画产生的self
NormalCheck = True

def notify(self, title, subtitle, text, url):
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    notification.setSubtitle_(str(subtitle))
    notification.setInformativeText_(str(text))
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setHasActionButton_(True)
    notification.setOtherButtonTitle_("View")
    notification.setUserInfo_({"action":"open_url", "value":url})
    NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
def userNotificationCenter_didActivateNotification_(self, center, notification):
    userInfo = notification.userInfo()
    if userInfo["action"] == "open_url":
        import subprocess
        subprocess.Popen(['open', userInfo["value"]])
        
def runTask(func, day=0, hour=0, min=0, second=0):
  # Init time
  now = datetime.now()
  strnow = now.strftime('%Y-%m-%d %H:%M:%S')
  print "now:",strnow
  # First next run time
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  next_time = now + period
  strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
  print "next run:",strnext_time
  while True:
      # Get system current time
      iter_now = datetime.now()
      iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
      if str(iter_now_time) == str(strnext_time):
          # Get every start work time
          print "start work: %s" % iter_now_time
          # Call task func
          func()
          print "task done."
          # Get next iteration time
          iter_time = iter_now + period
          strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
          print "next_iter: %s" % strnext_time
          # Continue next iteration
          continue
          
#get all files
def scan_files(directory,prefix=None,postfix=None,exceptPath=None):
    files_list=[]
    def addStr(path):
        if exceptPath:
            count=0
            for pathString in exceptPath:
                if int(path.find(pathString))==-1:
                    count+=1
            if count == len(exceptPath):
                files_list.append(path)
        else:
            files_list.append(path)

    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    addStr(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    addStr(os.path.join(root,special_file))
            else:
                addStr(os.path.join(root,special_file))

    return files_list
    
#remove note
def removeNote(content):
    text = content
    for i in range(0,len(text)):
        if i+1<len(text):
            if text[i]=="/" and text[i+1]=="/":
                text = text[:i] + text[text.find('\n',i):]
                i=text.find('\n',i)
    for i in range(0,len(text)):
        left = text.find('/*',i)
        right = text.find('*/',i)
        if left>0 and right>0 and right>left:
            line = ''
            for j in range(left,right):
                if text[j]=='\n':
                    line = line + '\n'
            text =  text[:left] + line + text[right:]
            i=right
            left = -1
            right = -1
    return text
    
#tell weather is legal or not
def isLegal(content):
    if content=='_' or content.isdigit() or content.isalpha():
        return False
    return True
    
#get file content
def getFileContent(path):
    if path.strip()=='':
        print 'error------------>path is empty'
        return
    file_object = open(path)
    try:
        all_the_text=file_object.read()
        all_the_text=removeNote(all_the_text)
        i = int(all_the_text.find('^'))
        if i > -1 and i < len(all_the_text):
            print("--------------in File:" + path + "---------------")
            i=0
            lastTemp=0
            while (i<len(all_the_text)):
                temp = int(all_the_text.find('^',i+1,len(all_the_text)))
                if NormalCheck :
                    if temp > -1:
                        if all_the_text[temp-11:temp] == 'animations:':
                            temp=-1
                        if all_the_text[temp-11:temp] == 'completion:' and all_the_text[temp+1:temp+16] == '(BOOL finished)':
                            temp=-1
                if temp == -1 or temp == lastTemp:
                    break
                if temp + 1 < len(all_the_text):
                    if all_the_text[temp+1] == ')':
                        break
                if temp > -1 and temp<len(all_the_text):
                    leftCount=0
                    rightCount=0
                    tempLeft=0
                    tempRight=0
                    lastNum=0
                    for j in range(temp,len(all_the_text)):
                        if all_the_text[j]=='{':
                            leftCount+=1
                            if tempLeft==0:
                                tempLeft=j
                        if all_the_text[j]=='}':
                            rightCount+=1
                            tempRight=j
                        isRightBlock=True

                        if all_the_text.find('@implementation',temp,tempLeft)>-1 and tempLeft>0 and tempRight>tempLeft:
                            isRightBlock=False
                        if leftCount > 0 and rightCount > 0 and leftCount==rightCount and isRightBlock:
                            while(tempLeft < tempRight):
                                k=all_the_text.find('self',tempLeft,tempRight)
                                if k>0 and isLegal(all_the_text[k-1]) and isLegal(all_the_text[k+4]):
                                    num=1
                                    for m in range(0,k):
                                        if all_the_text[m]=='\n':
                                            num+=1
                                    if num>lastNum:
                                        outputStr = 'num:' + str(num) + ' maybe have self !!!!!'
                                        print outputStr
                                        notiStr = path.split('/')[len(path.split('/')) - 1] + '\n' + outputStr
                                        notify('self',title='maybe have self',subtitle=path,text=notiStr,url='')
                                        lastNum=num
                                tempLeft+=4
                            tempLeft=0
                            tempRight=0
                            leftCount=0
                            rightCount=0
                            break
                    i=temp
                    lastTemp=temp

    finally:
        file_object.close()
    return
    
#get the path
def start():
    print("===============path==============")
    print(projectPath)
    #get all files
    excPath=None
    if NormalCheck:
        excPath=noPath
    files_list=scan_files(projectPath,postfix=".m",exceptPath=excPath)
    print("=============all " + str(len(files_list)) + " files==========")
    for filePath in files_list:
        print filePath
    print("==============================================================")
    for filePath in files_list:
        getFileContent(filePath)

start()
runTask(start, day=0, hour=0, min=10,second=0)