# -*- coding: utf-8 -*-
from splinter import Browser
import time
import base64
from PIL import Image
import pytesseract
import urllib2
import os
import ConfigParser
from mail import SJTU_Mail

class Electsys():

    def __init__(self):
        def config_init():
            cf = ConfigParser.ConfigParser()
            cf.read("config.ini")
            self.user = cf.get('login','user')
            self.password =  base64.b64decode(cf.get('login','pass'))
            self.have_tab = cf.get('tab','have')
            self.xxq = int(cf.get('tab','have'))
            self.delay = cf.get('course','delay')
            if self.xxq==0:
                self.xklc = int(cf.get('course','xklc'))
                self.path = cf.get('course','path').split('>')
                step_tmp = [['bx','xx','ts'][int(self.path[0])-1],[6,8,8][int(self.path[0])-1]]
                name_tmp = "xklc%d_%s%d"
                self.step = [cf.get('id',name_tmp%(self.xklc,step_tmp[0],i)) for i in range(step_tmp[1])]
                n = 1
                for index,data in enumerate(self.step):
                    if "%02d" in data:
                        self.step[index] = self.step[index]%(int(self.path[n])+2)
                        n = n+1
            else:
                self.xklc = int(cf.get('course','xklc'))
                self.path = cf.get('course','path').split('>')
                step_tmp = ['xxq',6]
                name_tmp = "xklc%d_%s%d"
                self.step = [cf.get('id',name_tmp%(self.xklc,step_tmp[0],i)) for i in range(step_tmp[1])]
                n = 0
                for index,data in enumerate(self.step):
                    if "%02d" in data:
                        self.step[index] = self.step[index]%(int(self.path[n])+1)
                        n = n+1
                
        try:
            config_init()
            self.mail_sender = SJTU_Mail(self.user,self.password)
            self.browser = Browser('chrome')
            url = "http://electsys.sjtu.edu.cn/edu/"
            self.browser.visit(url)
        except Exception,e:
            print e
            raise NameError('Init error')

    def login(self):
        self.browser.find_by_tag('a')[2].click()
        flag = False
        while True:
            self.browser.fill('captcha',self.recognize())
            self.browser.fill('user',self.user)
            self.browser.fill('pass',self.password)
            xpath = '//*[@id="form-input"]/div[4]/input'
            self.browser.find_by_xpath(xpath).click()
            flag = self.browser.is_text_present(u'请正确填写验证码')
            if not flag:
                break
        if self.browser.is_text_present(u'请正确填写你的用户名和密码'):
            raise NameError('Username or password error')

    def close_tab(self):
        if self.have_tab=='1':
            tab = self.browser.driver.window_handles[1]
            self.browser.driver.switch_to_window(tab)
            self.browser.driver.close()
            self.browser.driver.switch_to_window(self.browser.driver.window_handles[0])

    def goto_course(self):
        if self.xxq==0:
            url = 'http://electsys.sjtu.edu.cn/edu/student/elect/electwarning.aspx?xklc=%d'%(self.xklc)
            self.browser.visit(url)
            self.browser.click_link_by_id('CheckBox1')
            self.browser.find_by_id('btnContinue').click()
            for i in range(len(self.step)-4):
                self.browser.click_link_by_id(self.step[i])
        else:
            url = 'http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?xklc=%d&lb=3'%(self.xklc)
            self.browser.visit(url)
            for i in range(len(self.step)-4):
                self.browser.click_link_by_id(self.step[i])

    def grab(self):
        start = time.time()
        end = start + 30*60
        start_step = len(self.step)-4
        while True:
            time.sleep(float(self.delay))
            print 1
            self.browser.click_link_by_id(self.step[start_step])
            self.browser.click_link_by_id(self.step[start_step+1])
            if not self.browser.is_text_present(u'该课该时间段人数已满'):
                self.browser.click_link_by_id(self.step[start_step+3])
                self.mail_sender.send_mail('electsys-splinter','Grab course successful')
            else:
                self.browser.click_link_by_id(self.step[start_step+2])
                now = time.time()
                if now>end:
                    raise NameError('Maybe time out, restart')

    def quit(self):
        self.browser.driver.close()

    def recognize(self):
        def format_captcha(captcha):
            temp = ''
            for i in captcha:
                if (ord(i)>=48 and ord(i)<=57) or (ord(i)>=65 and ord(i)<=90) or (ord(i)>=97 and ord(i)<=122):
                    temp = temp + i
            if temp=='':
                temp = 'aaaa'
            return temp
        cookie = self.browser.cookies.all()
        opener = urllib2.build_opener()
        opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'))
        opener.addheaders.append(('Host','jaccount.sjtu.edu.cn'))
        opener.addheaders.append(('Referer',self.browser.url))
        opener.addheaders.append(('Cookie',  "; ".join('%s=%s' % (k,v) for k,v in cookie.items())))
        f = opener.open("https://jaccount.sjtu.edu.cn/jaccount/captcha?1488154642719")
        data = f.read()
        with file('captcha.png','wb') as f:
            f.write(data)
        img = Image.open("captcha.png").convert('L')
        result = format_captcha(pytesseract.image_to_string(img,lang="eng"))
        return result

if __name__ == '__main__':    
    while True:
        try:
            test = Electsys()
            test.login()
            test.close_tab()
            test.goto_course()
            test.grab()
        except Exception,e:
            print e
            test.quit()
        time.sleep(10)
