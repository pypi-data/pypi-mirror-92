# -*- coding: utf-8 -*-

import gdpy

# 以下代码展示了Workflows相关操作，例如获取、列出、创建、修改、删除等

# 首先初始化Auth信息
auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')

# 创建一个Workflows对象
# 确定所需要访问的域和访问资源的账户，以下以北京域，public账号下的资源为例
workflow = gdpy.Workflows(auth, 'cn-beijing-api.genedock.com', 'public')
# 如果需要操作wdl类型的任务，请使用以下方式初始化
# task = gdpy.Workflows(auth, 'cn-beijing-api.genedock.com', 'public', workflow_type='wdl')

# 列出该账号下所有可以访问的workflows
list_workflow_result = workflow.list_workflows()
# 查看workflow列表详情
print list_workflow_result.workflows
# 列出的workflow的数量
print list_workflow_result.count

# 列出该账号下所有可以运行的workflows
list_excutable_workflow_result = workflow.list_exc_workflows()
# 查看workflow列表详情
print list_excutable_workflow_result.workflows
# 列出的workflow数量
print list_excutable_workflow_result.count

# 获取某个workflow
# 如果不指定版本号，则返回一个包含所有版本的workflow的数组
get_workflow_result = workflow.get_workflow('workflow_name_or_id', workflow_version)
# 查看获取的workflow的详情
print get_workflow_result.response.text

# 获取某个可执行的workflow
# 必须指定版本号
get_excutable_workflow_result = workflow.get_exc_workflow('workflow_name_or_id', workflow_version)
# 查看获取的workflow的详情
print get_excutable_workflow_result.response.text

# 初始化一个新的gwl workflow(创建)
# 创建新workflow时不需要提供具体的workflow配置，只需要提供workflow_name, workflow_version(初次创建为1)，以及workflow描述
# 如需创建新的可运行workflow，请在初始化workflow(create_workflow)之后配合修改操作使用(put_workflow)
create_workflow_result = workflow.create_workflow('workflow_name', 1, 'new gfw workflow')

# 初始化一个wdl workflow
create_workflow_result = workflow.create_workflow(
    'workflow_name', 1, 'new wdl workflow',
    attachment={
        "source_path": "/path/to/wdl/source/file",  # wdl主文件，必须
        "dependencies_zip": "/path/to/wdl/dependencies/zipfile"  # wdl依赖的文件包，可选
    }
)


# 更新工作流，不同类型的工作流对参数的要求不同

# 1. 更新WDL类型的工作流
put_workflow_result = workflow.update_workflow(
    name_or_id="wdl workflow id",
    version=1,
    description="update from sdk",
    attachment={
        "source_path": "/path/to/wdl/source/file",  # wdl主文件，可选
        "dependencies_zip": "/path/to/wdl/dependencies/zipfile"  # wdl依赖的文件包，可选
    },
    override=False  # 是否覆盖，默认为true, 当该项为False时，版本号会向前递增
)

# 2. 更新GWL类型的工作流
put_workflow_result = workflow.update_workflow(
    name_or_id="gwl workflow name",
    version=1,
    description="update from sdk",
    configs={},  # 工作流配置
)
# 也可以使用put_workflow接口直接修改 gwl workflow
# 需要提供一个parameter_file配置文件，记录该workflow的配置
# 如果和create_workflow配合使用，请注意需要和配置文件中的workflow_name保持一致
put_workflow_result = workflow.put_workflow('parameter_file')
# workflow预设运行配置
# 必须指定版本号
# 只可修改属于自己账号的可执行工作流的配置
# 'excutable_workflow_param_file' 文件格式可参考 'task_active.yml'
set_workflow_param_result = workflow.set_workflow_param('excutable_workflow_param_file', 'workflow_name', workflow_version)


# 删除workflow
# 必须指定版本号
delete_workflow_result = workflow.delete_workflow('workflow_name', workflow_version)
