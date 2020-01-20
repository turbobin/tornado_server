## Python tornado 通用开箱即用后端框架

### 目录结构

```
├─tornado_server
│  ├─configs	# 配置目录
│  ├─handlers	# 业务接口
│  │  ├─auth		# 注册登录接口
│  │  ├─public		# 公共业务接口
│  │  └─user		# 用户相关接口
│  ├─jobs	# 队列相关
│  │  └─logs	# 队列日志文件目录
│  ├─logs	# 服务日志文件目录
│  └─utils	# 通用工具
```

### 功能说明

此框架采用 Python tornado 搭建，提供开箱即用的后端服务。可用于快速架构 App 、中大型网站的后台。已实现的功能如下：

- 手机号验证码注册登录
- 微信授权登录
- 接口安全签名校验
- 队列服务
- 七牛存储服务
- MySQL 数据库服务
- Redis 缓存服务
- Graylog 日志系统上报

待补充......

### 相关技术

#### 验证码短信

使用腾讯云付费短信服务

腾讯云短信 Python SDK https://cloud.tencent.com/document/product/382/11672

#### MySQL 数据库

使用 K 神的 Records 库：SQL for Humans™，没错，就是那位大名鼎鼎的 requests 库的作者。

教程：<https://github.com/kennethreitz/records>

#### 缓存

使用 Python redis 模块。需要注意的是 Python3 取出来的数据类型是 byte 类型，大多数时候需要转换一下，变成 str 类型，已在 `utils/common.py` 中添加通用函数。

#### 队列

使用 beanstalk + kafka，需要先在 `config.py` 中配置队列服务

#### 七牛存储

一般用户头像、用户上传文件需要使用七牛 CDN 存储服务。使用时同样需要在` config.py` 中配置相关 key。

#### 接口验签

签名值 sign 是将请求源串以及密钥根据一定签名方法生成的签名值，用来提高传输过程参数的防篡改性。

签名值的生成共有3个步骤：构造源串，构造密钥，生成签名值。

1.签名方式跟腾讯开发平台api签名一致，可以到腾讯开放平台找不同平台的签名sdk;
2.签名在线验证工具：<http://open.qq.com/tools>
3.签名值不需要进行encode编码

#### 日志系统

需要先搭建 GrayLog + Mongodb + Elasticsearch。

当然也可以使用 ELK 系统。

graylog 官网：<https://www.graylog.org/>

