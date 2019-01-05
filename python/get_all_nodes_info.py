#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from ansible.plugins.callback import CallbackBase
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from collections import namedtuple
#实例化解析yml
loader = DataLoader()
#实例化资产管理
'''
    2.4+的inventory必须有sources参数，参数路径为动态执行的那个脚本！这里很坑我研究了一天！
'''
inventory = InventoryManager(loader=loader,sources='hosts') 
#实例化变量管理
variable_manager = VariableManager(loader=loader,inventory=inventory)
Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'diff'])
options = Options(connection='smart',
                       remote_user=None,
                       ack_pass=None,
                       sudo_user=None,
                       forks=5,
                       sudo=None,
                       ask_sudo_pass=False,
                       verbosity=5,
                       module_path=None,
                       become=None,
                       become_method=None,
                       become_user=None,
                       check=False,
                       diff=False,
                       listhosts=None,
                       listtasks=None,
                       listtags=None,
                       syntax=None)
play_source =  dict(
        hosts = 'all', 
        gather_facts = 'yes',
        tasks = [
            dict(action=dict(module='facter', args='')),
            # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result
    def v2_runner_on_failed(self, result):
        self.host_failed[result._host.get_name()] = result
callback = ModelResultsCollector()
passwords = dict()
# 传入自定义的callback
tqm = TaskQueueManager(
          inventory=inventory,
          variable_manager=variable_manager,
          loader=loader,
          options=options,
          passwords=passwords,
          stdout_callback=callback,
      )
result = tqm.run(play)
# 自定义格式化输出，执行结果数据在result对象的_result属性里
result_raw = {'success':{},'failed':{},'unreachable':{}}
for host,result in callback.host_ok.items():
    result_raw['success'][host] = result._result
for host,result in callback.host_failed.items():
    result_raw['failed'][host] = result._result

datas = json.dumps(result_raw,indent=4)

title = ['age','birthday','collegeName','degree','gender','graduateTime','graduateYears','idNo','message','name','photo','photoStyle','specialty','startTime','studyResult','studyType','success']
book = xlwt.Workbook() # 创建一个excel对象
sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True) # 添加一个sheet页
for i in range(len(title)): # 循环列
    sheet.write(0,i,title[i]) # 将title数组中的字段写入到0行i列中


for i in range(len(datas)):#循环列表，取出每一个用户信息
    b = datas[i]#第i个用户信息
    massage = b['data']#得到用户详细信息
    l = [massage[k] for k in title]#将列表信息与title匹配的字段顺序输出
    for k1 in range(len(l)): #　循环列表
        sheet.write(1+i,k1,l[k1]) #　将信息写入第i+1行第k1列中
book.save('demo.xls')#保存excel


#if __name__ == '__main__':
#    writeM()
