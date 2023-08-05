# -*- coding: utf-8 -*-

import gdpy

# 以下代码展示了tools相关操作，例如获取、列出、创建、修改、删除等

# 首先初始化Auth信息
auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')

# 创建一个tools对象
# 确定所需要访问的域和访问资源的账户，以下以北京域，public账号下的资源为例
tool = gdpy.Tools(auth, 'cn-beijing-api.genedock.com', 'public')

# 列出该账号下所有可以访问的tools
list_tool_result = tool.list_tools()
# 查看tool列表详情
print list_tool_result.tools
# 列出的tool的数量
print list_tool_result.count

# 获取某个tool
# 如果不指定版本号，则返回一个包含所有版本的tool的数组
get_tool_result = tool.get_tool('tool_name', tool_version)
# 查看获取的tool的详情
print get_tool_result.response.text

# 初始化一个新的tool(创建)
# 创建新tool时不需要提供具体的tool配置，只需要提供tool_name, tool_version(初次创建为1)，以及tool描述
# 如需创建新的可使用tool，请在初始化tool(create_tool)之后配合修改操作使用(put_tool)
create_tool_result = tool.create_tool('tool_name', 1, 'new tool')

# 修改tool
# 需要提供一个parameter_file配置文件，记录该tool的配置
# 如果和create_tool配合使用，请注意需要和配置文件中的tool_name保持一致
put_tool_result = tool.put_tool('parameter_file')

# 删除tool
# 必须指定版本号
delete_tool_result = tool.delete_tool('tool_name', tool_version)
