# -*- coding: utf-8 -*-

import gdpy

# 以下代码展示了data相关操作，例如归档、恢复

# 首先初始化Auth信息
auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')

# 创建一个data对象
# 确定所需要访问的域和访问资源的账户，以下以北京域，public账号下的资源为例
data = gdpy.Data(auth, 'cn-beijing-api.genedock.com', 'public')

# 归档指定文件，暂时不支持归档目录；归档过程中会根据文件的大小和服务器负载会持续几分钟和几小时不等
archive_data_result = data.archive_data('data_path')

# 恢复指定的文件，服务端在接到用户的恢复请求以后，会开始恢复文件。恢复的过程会持续0到4个小时不等。恢复完成后，文件处于已恢复的状态，此状态默认保持1天。用户可以对restored状态的数据再次执行恢复操作，以延长文件的restored状态。每请求一次延长1天，最多延长至7天
restore_data_result = data.restore_data('data_path')
