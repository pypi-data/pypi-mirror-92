# -*- coding: utf-8 -*-
import gdpy

# 以下代码展示了Tasks相关操作，例如获取、列出、启动、删除等

# 首先初始化Auth信息
auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')

# 创建一个Tasks对象
# 确定所需要访问的域和访问资源的账户，以下以北京域，public账号下的资源为例
task = gdpy.Tasks(auth, 'cn-beijing-api.genedock.com', 'public')

# 如果需要操作wdl类型的任务，请使用以下方式初始化
# task = gdpy.Tasks(auth, 'cn-beijing-api.genedock.com', 'public', task_type='wdl')

# 列举所有的tasks
task_list_result = task.list_tasks()
# 获取所有task的详细内容
print task_list_result.task_list
# 该次获取到的tasks的数量
print task_list_result.count
# 所能访问到的该账户下所有tasks的数量
print task_list_result.total

# 获取某个task
# task_id可以从list_task中获取，也可以从GeneDock网站页面的任务详情中获取
task_get_result = task.get_task('task_id')
# 获取该task的详情
print task_get_result.response.text

# 获取某个task下的jobs以便于查看改task的进度
job_get_result = task.get_jobs('task_id')
# 查看所有jobs详情
print job_get_result.jobs
# 获取所有jobs的数量
print job_get_result.count

# 通过参数文件（yml或json）启动某个任务
# 1. 首先需要编写改任务的配置文件parameter_file，记录本次务的详细配置，所需要的输入文件和参数等
# 2. 需要获取到该任务所用的workflow名称workflow_name和版本号workflow_version
workflow_version = 1
active_workflow_result = task.active_workflow('parameter_file', 'workflow_name', workflow_version)

# 也可以直接调用 create_task 启动任务, 需要提供parameters对象（字典）
params = {}  # 参数项

# 如果是WDL工作流任务，参数项应该这样填写
params = {
    "inputs": {
        "input 1": "value 1",
        "input 2": "value 2"
    },
    "output_dir": "<account>:/path/to/dir/"  # 目录以 "/" 结尾
}
# 如果是GWL工作流任务，参数项应该这样填写
params = {
    "name": "<Please input the task's name in here>",
    "description": "<Please input the task's description in here>",
    "Inputs": {},
    "Outputs": {},
    "Parameters": {},
    "Property": {},
}

active_workflow_result = task.create_task('workflow_name', workflow_version, parameters=params)

# 情况一: 如果不是分块任务，返回的属性是 task_id， task_name
# 任务成功启动后的task_id
print active_workflow_result.task_id  # string
# 任务成功启动后的task_name
print active_workflow_result.task_name  # string

# 情况二: 如果是分块任务，返回的属性是 split， splitting
# 分块任务成功启动后已分块的文件 split
# list: [{u'name': u'test:/home/test.fq.gz', u'enid': u'5c26'}]
print active_workflow_result.split
# 分块任务成功启动后正在分块的文件 splitting
# list: [{u'enid': u'5c34', u'name': u'test:/home/test_2.fq.gz', u'submit':True}]
print active_workflow_result.splitting


# 删除某个任务 (WDL任务暂不支持删除)
delete_task_result = task.delete_task('task_id')

# 停止某个任务
stop_task_result = task.stop_task('task_id')
# 获取停止任务详情 （返回状态码为204则内容为空）
print stop_task_result.response.text

# 重启某个任务 (WDL任务暂不支持删除)
resart_task_result = task.restart_task('task_id')

# 获取指定job的command（只能获取tool属于自己账号的job的cmd，不允许获取公共工具相关的job的cmd）
get_job_cmd_result = task.get_job_cmd('job_id')
# 获取command详情
print get_job_cmd_result.response.text
# 只获取command
print get_job_cmd_result.cmd

# 获取指定job详情
get_job_info_result = task.get_job_info('job_id')
print get_job_info_result.response.text
