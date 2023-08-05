[![Build Status](https://travis-ci.com/genedock/genedock-official-python-sdk.svg?token=tdT1eRQbVcaWeBgbQX39&branch=master)](https://travis-ci.com/genedock/genedock-official-python-sdk)
# genedock-official-python-sdk
GeneDock Python SDK, 提供操作Workflow,Task,Data的API

## 环境
python2,python3

## 使用
```shell script
 pip install gdpy
```

## 发包说明

1. 合并到master分支会发布到私有pypi库https://pypi.genedock.com/, 用于stg测试
2. 合并到stable分支会发布到公有pypi库https://pypi.org(同步到镜像源会需要时间)

版本号说明:

发包使用pbr插件，打包时会检测对应分支的tag，所以在合并master与stable之前，需要将master和stable添加最新版本的tag，以要发布的版本命名

例如要发布gdpy版本0.1.10到私有库，则在gwc的master分支创建tag，name为0.1.10，合并代码到master后，ci会执行pipeline发布到私有库

具体流程:
1. 修改代码合并至master
2. 在master增加tag（这步必须在成功合并后，不然会因为tag的代码不是最新代码而发布dev包）
3. 点击ci中的manual job运行发包job发布到staging
4. 合并master至stable