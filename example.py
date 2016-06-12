#!/usr/bin/python
# coding:utf8
from __future__ import unicode_literals
import theTaleApi
import getpass
import sys
reload(sys)
sys.setdefaultencoding('utf8')
api = theTaleApi.theTaleApi('exampleApp-1.0', False)
api.login(raw_input('Email: '), getpass.getpass())
accId = str(api.authorisation_state()['data']['account_id'])
info = api.show(accId)['data']
print('Идентификатор: ' + str(info['id']))
print('Имя: ' + info['name'])
api.logout()
