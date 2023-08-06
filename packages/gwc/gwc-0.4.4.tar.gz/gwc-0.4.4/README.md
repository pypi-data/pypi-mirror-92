# GWC
 genedock发布用于工作流及任务管理的python命令行工具
 
# 使用
```shell
 pip install gwc
 gwc -h
```

# 发版说明
统一使用genedock gitlab ci流程发版，规则如下：

1. 合并到master分支会发布到私有pypi库https://pypi.genedock.com/, 用于stg测试
2. 合并到stable分支会发布到公有pypi库https://pypi.org(同步到镜像源会需要时间)

版本号说明:

发包使用pbr插件，打包时会检测对应分支的tag，所以在合并master与stable之前，需要将master和stable添加最新版本的tag，以要发布的版本命名

例如要发布gwc版本0.4.4到私有库，则在gwc的master分支创建tag，name为0.4.4，合并代码到master后，ci会执行pipeline发布到私有库