import sys
import time
import calendar
import psutil
import os
import requests
import json


def reality_check(obj: list or dict, check):
    if check in obj:
        return True
    else:
        return False


def platform():
    return sys.platform


def timestamp():
    t = time.gmtime()
    tc = calendar.timegm(t)
    return tc


def py():
    return sys.version


def running(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


def group(obj: list or tuple, seperator: str):
    return seperator.join(obj)


def allapps():
    lst = []
    try:
        for proc in psutil.process_iter():
            lst.append(proc.name())
    except:
        pass
    return lst


class exe:
    def __init__(self):
        self.requirements = ("shell", "bash", "crosh", "command_prompt","terminal")
        self.executable = self.requirements

    def check(self, terminal):
        if terminal in self.executable:
            return True
        else:
            return False

    def shell(self):
        try:
            os.system("python3")
        except:
            os.system("python")
executable=exe()
class Client(object):
  def __init__(self,url):
    self.url=url
  def content(self):
    self.base=requests.get(self.url)
    return self.base.content
class API(object):
  def __init__(self,url):
    self.api=url
  def headers(self,header=None):
    self.headers=header
  def load(self):
    try:
      api=requests.get(self.api,headers=self.headers)
      return json.loads(api.content)
    except:
      pass
      api=requests.get(self.api)
      return json.loads(api.content)