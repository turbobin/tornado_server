## 一、表结构

### 用户表

```sql
CREATE TABLE `user_info` (
  `user_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '用户唯一id',
  `sex` tinyint(2) NOT NULL DEFAULT '0' COMMENT '性别:1男，2女，0未知',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '帐号状态:0-正常 9-删除',
  `rank` int(11) NOT NULL DEFAULT '0' COMMENT '用户等级',
  `height` int(11) NOT NULL DEFAULT '0' COMMENT '身高:cm',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT '体重:g',
  `blood_type` varchar(10) NOT NULL DEFAULT '' COMMENT '血型',
  `blood_pressure` varchar(16) NOT NULL DEFAULT '0/0' COMMENT '血压: 收缩压/舒张压',
  `blood_sugar` tinyint(4) NOT NULL DEFAULT '0' COMMENT '血糖百分比',
  `heart_rate` tinyint(4) NOT NULL DEFAULT '0' COMMENT '心率',
  `phone` varchar(16) NOT NULL DEFAULT '' COMMENT '用户手机号',
  `birthday` int(11) NOT NULL DEFAULT '0' COMMENT '生日',
  `province` varchar(32) NOT NULL DEFAULT '' COMMENT '来源省份',
  `nick` varchar(64) NOT NULL DEFAULT '' COMMENT '用户昵称',
  `passwd` varchar(64) NOT NULL DEFAULT '' COMMENT '用户加密密码',
  `email` varchar(32) NOT NULL DEFAULT '' COMMENT '用户email',
  `city` varchar(32) NOT NULL DEFAULT '' COMMENT '来源城市',
  `area` varchar(32) NOT NULL DEFAULT '' COMMENT '区域',
  `source` varchar(32) NOT NULL DEFAULT '' COMMENT '帐号来源, android_app; ios_app; cms_seed; mobileweb ',
  `ip` varchar(16) NOT NULL DEFAULT '' COMMENT '最后一次登录ip',
  `love_sports` varchar(64) NOT NULL DEFAULT '' COMMENT '喜爱的运动, 以,分隔',
  `signature` varchar(256) NOT NULL DEFAULT '' COMMENT '个人签名',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上次登录时间',
  `reg_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `phone_type` varchar(64) NOT NULL DEFAULT '' COMMENT '手机型号',
  `os` varchar(64) NOT NULL DEFAULT '' COMMENT '手机操作系统版本号',
  `ver` varchar(16) NOT NULL DEFAULT '' COMMENT '注册时所用的app版本号',
  `device_id` varchar(128) NOT NULL DEFAULT '' COMMENT '设备id',
  `channel` varchar(64) DEFAULT 'unknown' COMMENT '渠道',
  `last_login_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上次登录时间',
  `head_val` varchar(32) NOT NULL DEFAULT '' COMMENT '头像动态key',
  PRIMARY KEY (`user_id`),
  KEY `idx_phone` (`phone`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='WaterWolrd用户信息表'
```

### 用户id 自增表

```sql
CREATE TABLE `user_tickets64_innodb` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=255848543 DEFAULT CHARSET=utf8
```

### 手机短信发送记录

```sql
CREATE TABLE `phone_code_tickets64` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` int(11) NOT NULL DEFAULT '0' COMMENT '验证码',
  `phone` varchar(16) NOT NULL DEFAULT '' COMMENT '手机号',
  `content` text COMMENT '短信内容',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8 COMMENT='手机验证码记录'
```

### 微信登录授权表信息

```sql
CREATE TABLE `openid_info` (
  `open_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'openid',
  `source` varchar(32) NOT NULL DEFAULT '' COMMENT '来源',
  `user_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '用户唯一id',
  `status` tinyint(2) NOT NULL DEFAULT '2' COMMENT '状态  0:已注册; 2:预分配',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上报时间',
  `nick` varchar(64) NOT NULL DEFAULT '' COMMENT '昵称',
  `sex` tinyint(2) NOT NULL DEFAULT '0' COMMENT '性别: 1男性，2女性，0未知',
  `head_url` varchar(256) NOT NULL DEFAULT '' COMMENT '微信头像',
  `union_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'unionid',
  `type` tinyint(2) NOT NULL DEFAULT '0' COMMENT '1 qq 2 wx 3 wx_pub',
  PRIMARY KEY (`open_id`),
  KEY `user_id` (`user_id`),
  KEY `union_id` (`union_id`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='微信QQ授权登录信息表'
```

### 

---

### 日志事件

```sql
CREATE TABLE `log_id` (
  `biz` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增长id',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0:正常 1:下线',
  `biz_name` varchar(255) NOT NULL DEFAULT '' COMMENT '业务名',
  `data_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'graylog报表链接',
  `username` varchar(255) NOT NULL DEFAULT '' COMMENT '业务负责人',
  `note` varchar(255) NOT NULL DEFAULT '' COMMENT '备注',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  `android_limit_vers` varchar(1000) NOT NULL DEFAULT '' COMMENT 'android端限制上报版本号，多个版本用英文逗号分开',
  `ios_limit_vers` varchar(1000) NOT NULL DEFAULT '' COMMENT 'ios端限制上报版本号，多个版本用英文逗号分开',
  PRIMARY KEY (`biz`)
) ENGINE=InnoDB AUTO_INCREMENT=228 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC
```

```sql
CREATE TABLE `log_id_event` (
  `id_` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增长id',
  `biz` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '业务id',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0:正常 1:下线',
  `event` int(11) NOT NULL DEFAULT '0' COMMENT '事件id',
  `event_name` varchar(255) NOT NULL DEFAULT '' COMMENT '事件描述',
  `platform` varchar(255) NOT NULL DEFAULT 'all' COMMENT '平台 server/ios/android/web',
  `data_url` varchar(1024) NOT NULL DEFAULT '' COMMENT 'graylog数据',
  `username` varchar(255) NOT NULL DEFAULT '' COMMENT '事件负责人',
  `note` varchar(255) NOT NULL DEFAULT '' COMMENT '备注',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  `hash_id` int(11) NOT NULL DEFAULT '0' COMMENT '抽样上报',
  PRIMARY KEY (`id_`),
  UNIQUE KEY `biz` (`biz`,`event`)
) ENGINE=InnoDB AUTO_INCREMENT=1581 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC
```

### 日志规则

```sql
CREATE TABLE `log_report_rule` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增长id',
  `hash_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度百分比, 0:全量',
  `short_message` varchar(255) NOT NULL DEFAULT '' COMMENT '业务类型',
  `description` varchar(511) NOT NULL DEFAULT '' COMMENT '业务描述',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0:正常 1:下线',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `short_message` (`short_message`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC
```

