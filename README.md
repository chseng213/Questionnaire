# Questionnaire
* [Questionnaire](#questionnaire)
  * [目录结构](#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84)
  * [测试环境](#%E6%B5%8B%E8%AF%95%E7%8E%AF%E5%A2%83)
    * [安装虚拟环境](#%E5%AE%89%E8%A3%85%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83)
    * [debug启动](#debug%E5%90%AF%E5%8A%A8)
  * [服务部署](#%E6%9C%8D%E5%8A%A1%E9%83%A8%E7%BD%B2)
    * [安装supervisor](#%E5%AE%89%E8%A3%85supervisor)
    * [启动supervisor](#%E5%90%AF%E5%8A%A8supervisor)
  * [接口文档](#%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3eolinker%E5%AF%BC%E5%87%BA%
E7%9A%84)
  * [工具](#%E5%B7%A5%E5%85%B7)
    * [common\_abort](#common_abort)
    * [CommonJsonRet](#commonjsonret)
    * [AuthToken](#authtoken)
    * [agument ,parse,resource重写](#agument-parseresource%E9%87%8D%E5%86%99)
    
用flask创建简单的调查问卷接口
## 目录结构
```
│  .gitignore
│  config.py   //配置文件
│  ext_app.py   // 第三方插件 
│  log.py       // log
│  manager.py   //程序入口
│  Pipfile      //环境包
│  Pipfile.lock //
│  README.md    //    
│  sql          // sql 结构以及字段说明
├─app
│  │  api.py    //resource
│  │  models.py // 数据库模型
│  │  urls.py   // api对象以及路由
│  │  utils.py  // 工具
│  │  __init__.py   //create_app
│
├─log       
│      apps.log     // 日志
```

## 测试环境
### 安装虚拟环境
**使用pipenv安装虚拟环境**
```
pipenv install
```
**或者使用virtualenv**
``` 
# 使用-p指定python版本 virtualenv -p /usr/bin/python2.7 ENV2.7
virtualenv venv
source venv/bin/active
pip install -r requirements.txt

```

### debug启动
``` 
# 1.
pipenv run python manager.py runserver 

#2.
source venv/bin/active
python manager.py runserver 
```

## 服务部署
### 安装supervisor
```
yum -y install supervisor
```

### 启动supervisor
``` 
supervisord -c /etc/supervisord.conf
vim /etc/supervisord.d/survey.ini
supervisorctl reload
```

## 接口文档(eolinker导出的)
``` 
[
    {
        "baseInfo": {
            "apiName": "问卷内容",
            "apiURI": "/questionnaire/{questionnaire_id}",
            "apiProtocol": 0,
            "apiSuccessMock": "{\r\n    \"code\": 200,\r\n    \"msg\": \"\",\r\n    \"data\": {\r\n        \"end_at\": 1655454,\r\n        \"create_at\": 14514545,\r\n        \"description\": \"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\",\r\n        \"title\": \"问卷1\",\r\n        \"start_at\": 14514545,\r\n        \"is_delete\": 0,\r\n        \"id\": 1,\r\n        \"questions\": [\r\n            {\r\n                \"number\": 1,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 1,\r\n                \"question\": \"wenti 1\",\r\n                \"id\": 1,\r\n                \"required\": 1,\r\n                \"answers\": [\r\n                    {\r\n                        \"answer\": \"1231\",\r\n                        \"id\": 1,\r\n                        \"number\": 1,\r\n                        \"question_id\": 1\r\n                    },\r\n                    {\r\n                        \"answer\": \"21311\",\r\n                        \"id\": 2,\r\n                        \"number\": 2,\r\n                        \"question_id\": 1\r\n                    }\r\n                ]\r\n            },\r\n            {\r\n                \"number\": 2,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 2,\r\n                \"question\": \"wenti2\",\r\n                \"id\": 2,\r\n                \"required\": 0,\r\n                \"answers\": [\r\n                    {\r\n                        \"answer\": \"fdsf\",\r\n                        \"id\": 3,\r\n                        \"number\": 1,\r\n                        \"question_id\": 2\r\n                    },\r\n                    {\r\n                        \"answer\": \"gdfsgf\",\r\n                        \"id\": 4,\r\n                        \"number\": 2,\r\n                        \"question_id\": 2\r\n                    }\r\n                ]\r\n            },\r\n            {\r\n                \"number\": 3,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 3,\r\n                \"question\": \"问题3\",\r\n                \"id\": 3,\r\n                \"required\": 0,\r\n                \"answers\": []\r\n            }\r\n        ],\r\n        \"has_participated\": 1\r\n    },\r\n    \"success\": true\r\n}",
            "apiFailureMock": "{\r\n    \"code\": 401,\r\n    \"msg\": \"Authentication error\",\r\n    \"data\": {},\r\n    \"success\": false\r\n}",
            "apiRequestType": 1,
            "apiStatus": 9,
            "starred": 0,
            "apiNoteType": 1,
            "apiNoteRaw": "",
            "apiNote": "",
            "apiRequestParamType": 0,
            "apiRequestRaw": "",
            "apiRequestBinary": null,
            "apiFailureStatusCode": "200",
            "apiSuccessStatusCode": "200",
            "apiFailureContentType": "text/html; charset=UTF-8",
            "apiSuccessContentType": "text/html; charset=UTF-8",
            "apiRequestParamJsonType": 0,
            "advancedSetting": null,
            "beforeInject": null,
            "afterInject": null,
            "createTime": "2020-09-10 09:29:54",
            "apiUpdateTime": "2020-09-10 09:32:34",
            "apiTag": ""
        },
        "responseHeader": [],
        "headerInfo": [
            {
                "headerName": "Authorization",
                "headerValue": "",
                "paramNotNull": "0",
                "default": 0,
                "paramName": "app中用户token"
            }
        ],
        "authInfo": {
            "status": "0"
        },
        "requestInfo": [],
        "urlParam": [],
        "restfulParam": [
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "问卷id",
                "paramKey": "questionnaire_id",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0
            }
        ],
        "resultInfo": [
            {
                "paramNotNull": "0",
                "paramType": "3",
                "paramName": "状态码 ",
                "paramKey": "code",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "消息",
                "paramKey": "msg",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "13",
                "paramName": "数据内容",
                "paramKey": "data",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": [
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷id",
                        "paramKey": "id",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷创建时间",
                        "paramKey": "create_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷结束时间",
                        "paramKey": "end_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷开始时间",
                        "paramKey": "start_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "假删除",
                        "paramKey": "is_delete",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "0",
                        "paramName": "问卷标题",
                        "paramKey": "title",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "0",
                        "paramName": "问卷描述",
                        "paramKey": "description",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "是否已参加  1:已参加  0:未参加",
                        "paramKey": "has_participated",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "12",
                        "paramName": "问题数组",
                        "paramKey": "questions",
                        "paramValue": "[\n    {\n        \"number\": 1,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 1,\n        \"question\": \"wenti 1\",\n        \"id\": 1,\n        \"required\": 1,\n        \"answers\": [\n            {\n                \"answer\": \"1231\",\n                \"id\": 1,\n                \"number\": 1,\n                \"question_id\": 1\n            },\n            {\n                \"answer\": \"21311\",\n                \"id\": 2,\n                \"number\": 2,\n                \"question_id\": 1\n            }\n        ]\n    },\n    {\n        \"number\": 2,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 2,\n        \"question\": \"wenti2\",\n        \"id\": 2,\n        \"required\": 0,\n        \"answers\": [\n            {\n                \"answer\": \"fdsf\",\n                \"id\": 3,\n                \"number\": 1,\n                \"question_id\": 2\n            },\n            {\n                \"answer\": \"gdfsgf\",\n                \"id\": 4,\n                \"number\": 2,\n                \"question_id\": 2\n            }\n        ]\n    },\n    {\n        \"number\": 3,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 3,\n        \"question\": \"问题3\",\n        \"id\": 3,\n        \"required\": 0,\n        \"answers\": []\n    }\n]",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": [
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问卷id",
                                "paramKey": "questionnaire_id",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题id",
                                "paramKey": "id",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题编号",
                                "paramKey": "number",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题类型   1:单选  2 :多选  3:客观",
                                "paramKey": "answer_type",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "是否必填  1:必填  0:非必填",
                                "paramKey": "required",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "0",
                                "paramName": "问题内容",
                                "paramKey": "question",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "12",
                                "paramName": "问题答案数组",
                                "paramKey": "answers",
                                "paramValue": "[\n    {\n        \"answer\": \"1231\",\n        \"id\": 1,\n        \"number\": 1,\n        \"question_id\": 1\n    },\n    {\n        \"answer\": \"21311\",\n        \"id\": 2,\n        \"number\": 2,\n        \"question_id\": 1\n    }\n]",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": [
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "3",
                                        "paramName": "问题id",
                                        "paramKey": "question_id",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    },
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "3",
                                        "paramName": "答案id",
                                        "paramKey": "id",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    },
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "0",
                                        "paramName": "答案内容",
                                        "paramKey": "answer",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    },
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "3",
                                        "paramName": "答案编号",
                                        "paramKey": "number",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "paramNotNull": "0",
                "paramType": "8",
                "paramName": "判断请求成功与否",
                "paramKey": "success",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            }
        ],
        "resultParamJsonType": 0,
        "resultParamType": 0,
        "structureID": "[]",
        "databaseFieldID": "[]",
        "globalStructureID": "[]",
        "fileID": null,
        "requestParamSetting": [],
        "resultParamSetting": [],
        "soapVersion": null,
        "customInfo": [],
        "dataStructureList": [],
        "globalDataStructureList": [],
        "testCastList": [],
        "mockExpectationList": [],
        "apiManagerID": 174003,
        "createUserID": 174003,
        "updateUserID": 174003,
        "apiType": "http"
    },
    {
        "baseInfo": {
            "apiName": "问卷提交",
            "apiURI": "/questionnaire/{questionnaire_id}",
            "apiProtocol": 0,
            "apiSuccessMock": "{\r\n    \"code\": 200,\r\n    \"msg\": \"ok\",\r\n    \"data\": {},\r\n    \"success\": true\r\n}",
            "apiFailureMock": "{\r\n    \"code\": 401,\r\n    \"msg\": \"Authentication error\",\r\n    \"data\": {},\r\n    \"success\": false\r\n}",
            "apiRequestType": 0,
            "apiStatus": 9,
            "starred": 0,
            "apiNoteType": 1,
            "apiNoteRaw": "",
            "apiNote": "",
            "apiRequestParamType": 2,
            "apiRequestRaw": "",
            "apiRequestBinary": null,
            "apiFailureStatusCode": "200",
            "apiSuccessStatusCode": "200",
            "apiFailureContentType": "text/html; charset=UTF-8",
            "apiSuccessContentType": "text/html; charset=UTF-8",
            "apiRequestParamJsonType": 1,
            "advancedSetting": null,
            "beforeInject": null,
            "afterInject": null,
            "createTime": "2020-09-10 09:29:54",
            "apiUpdateTime": "2020-09-10 09:41:42",
            "apiTag": ""
        },
        "responseHeader": [],
        "headerInfo": [
            {
                "headerName": "Content-Type",
                "headerValue": "application/json",
                "paramNotNull": "0",
                "paramName": "application/json"
            },
            {
                "headerName": "Authorization",
                "headerValue": "",
                "paramNotNull": "0",
                "default": 0,
                "paramName": "app中用户token"
            }
        ],
        "authInfo": {
            "status": "0"
        },
        "requestInfo": [
            {
                "paramNotNull": "0",
                "paramType": "3",
                "paramName": "问题id",
                "paramKey": "question_id",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "客观题填写答案,非客观题填null",
                "paramKey": "answer",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "3",
                "paramName": "答案id,客观题填null",
                "paramKey": "answer_id",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            }
        ],
        "urlParam": [],
        "restfulParam": [
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "问卷id",
                "paramKey": "questionnaire_id",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0
            }
        ],
        "resultInfo": [
            {
                "paramNotNull": "0",
                "paramType": "8",
                "paramName": "判断请求成功与否",
                "paramKey": "success",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "状态码",
                "paramKey": "code",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "消息",
                "paramKey": "msg",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "13",
                "paramName": "空对象",
                "paramKey": "data",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            }
        ],
        "resultParamJsonType": 0,
        "resultParamType": 0,
        "structureID": "[]",
        "databaseFieldID": "[]",
        "globalStructureID": "[]",
        "fileID": null,
        "requestParamSetting": [],
        "resultParamSetting": [],
        "soapVersion": null,
        "customInfo": [],
        "dataStructureList": [],
        "globalDataStructureList": [],
        "testCastList": [],
        "mockExpectationList": [],
        "apiManagerID": 174003,
        "createUserID": 174003,
        "updateUserID": 174003,
        "apiType": "http"
    },
    {
        "baseInfo": {
            "apiName": "问卷结果",
            "apiURI": "/questionnaire/{questionnaire_id}/result",
            "apiProtocol": 0,
            "apiSuccessMock": "{\r\n    \"code\": 200,\r\n    \"msg\": \"\",\r\n    \"data\": {\r\n        \"end_at\": 1599753600,\r\n        \"create_at\": 1599634178,\r\n        \"is_delete\": 0,\r\n        \"title\": \"Win Goal调查问卷\",\r\n        \"start_at\": 1599634178,\r\n        \"description\": \"尊敬的Win Goal用户\\n\\r您好！\\n\\r为了给您提供更加优质的服务，现针对win goal消息推送功能进行问卷调查，敬请您花几分钟时间来填写我们的问卷，本问卷实行匿名制，所有数据只用于统计分析，请您放心填写。另外真实且完整填写问卷的用户，win goal将赠送50000积分作为答谢！\",\r\n        \"id\": 1,\r\n        \"questions\": [\r\n            {\r\n                \"required\": 1,\r\n                \"number\": 1,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 1,\r\n                \"question\": \"请问你现在的手机系统版本是？\",\r\n                \"id\": 1,\r\n                \"answers\": [\r\n                    {\r\n                        \"name\": \"IOS\",\r\n                        \"value\": 0\r\n                    },\r\n                    {\r\n                        \"name\": \"Android\",\r\n                        \"value\": 8\r\n                    },\r\n                    {\r\n                        \"name\": \"其他\",\r\n                        \"value\": 4\r\n                    }\r\n                ]\r\n            },\r\n            {\r\n                \"required\": 1,\r\n                \"number\": 2,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 1,\r\n                \"question\": \"当前您是否开启了win goal APP信息推送：\",\r\n                \"id\": 2,\r\n                \"answers\": [\r\n                    {\r\n                        \"name\": \"是的，开启了接收信息推送\",\r\n                        \"value\": 3\r\n                    },\r\n                    {\r\n                        \"name\": \"以前开启过，现在已关闭\",\r\n                        \"value\": 4\r\n                    },\r\n                    {\r\n                        \"name\": \"一直关闭\",\r\n                        \"value\": 7\r\n                    }\r\n                ]\r\n            },\r\n            {\r\n                \"required\": 1,\r\n                \"number\": 3,\r\n                \"questionnaire_id\": 1,\r\n                \"answer_type\": 2,\r\n                \"question\": \"如果您关闭推送，关闭的原因是：（可多选\",\r\n                \"id\": 3,\r\n                \"answers\": [\r\n                    {\r\n                        \"name\": \"没有关闭\",\r\n                        \"value\": 3\r\n                    },\r\n                    {\r\n                        \"name\": \"推送条数太多\",\r\n                        \"value\": 4\r\n                    },\r\n                    {\r\n                        \"name\": \"推送内容我不感兴趣\",\r\n                        \"value\": 4\r\n                    },\r\n                    {\r\n                        \"name\": \"推送时间不合理\",\r\n                        \"value\": 2\r\n                    },\r\n                    {\r\n                        \"name\": \"推送消息不及时\",\r\n                        \"value\": 0\r\n                    },\r\n                    {\r\n                        \"name\": \"太多APP推送，消息过载\",\r\n                        \"value\": 0\r\n                    },\r\n                    {\r\n                        \"name\": \"不记得了\",\r\n                        \"value\": 0\r\n                    },\r\n                    {\r\n                        \"name\": \"其它\",\r\n                        \"value\": 0\r\n                    }\r\n                ]\r\n            }\r\n        ]\r\n    },\r\n    \"success\": true\r\n}",
            "apiFailureMock": "{\r\n    \"code\": 404,\r\n    \"msg\": \"Questionnaire not found\",\r\n    \"data\": {},\r\n    \"success\": false\r\n}",
            "apiRequestType": 1,
            "apiStatus": 9,
            "starred": 0,
            "createTime": "2020-09-10 09:53:33",
            "apiNoteType": 1,
            "apiNoteRaw": "",
            "apiNote": "",
            "apiRequestParamType": 0,
            "apiRequestRaw": "",
            "apiRequestBinary": null,
            "apiFailureStatusCode": "200",
            "apiSuccessStatusCode": "200",
            "apiFailureContentType": "text/html; charset=UTF-8",
            "apiSuccessContentType": "text/html; charset=UTF-8",
            "apiRequestParamJsonType": 0,
            "beforeInject": null,
            "afterInject": null,
            "apiUpdateTime": "2020-09-10 09:53:33",
            "apiTag": "",
            "advancedSetting": null
        },
        "headerInfo": [],
        "authInfo": {
            "status": "0"
        },
        "requestInfo": [],
        "urlParam": [],
        "restfulParam": [
            {
                "paramKey": "questionnaire_id",
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "问卷id"
            }
        ],
        "resultInfo": [
            {
                "paramNotNull": "0",
                "paramType": "8",
                "paramName": "判断接口请求成功与否",
                "paramKey": "success",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "3",
                "paramName": "状态码",
                "paramKey": "code",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "0",
                "paramName": "消息",
                "paramKey": "msg",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": []
            },
            {
                "paramNotNull": "0",
                "paramType": "13",
                "paramName": "数据",
                "paramKey": "data",
                "paramValue": "",
                "paramLimit": "",
                "paramNote": "",
                "paramValueList": [],
                "default": 0,
                "childList": [
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷id",
                        "paramKey": "id",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷创建时间",
                        "paramKey": "create_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "假删除   1:删除   0:未删除",
                        "paramKey": "is_delete",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷开始时间",
                        "paramKey": "start_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "3",
                        "paramName": "问卷结束时间",
                        "paramKey": "end_at",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "0",
                        "paramName": "问卷标题",
                        "paramKey": "title",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "0",
                        "paramName": "问卷描述",
                        "paramKey": "description",
                        "paramValue": "",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": []
                    },
                    {
                        "paramNotNull": "0",
                        "paramType": "12",
                        "paramName": "问题结果统计数组",
                        "paramKey": "questions",
                        "paramValue": "[\n    {\n        \"required\": 1,\n        \"number\": 1,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 1,\n        \"question\": \"请问你现在的手机系统版本是？\",\n        \"id\": 1,\n        \"answers\": [\n            {\n                \"name\": \"IOS\",\n                \"value\": 0\n            },\n            {\n                \"name\": \"Android\",\n                \"value\": 8\n            },\n            {\n                \"name\": \"其他\",\n                \"value\": 4\n            }\n        ]\n    },\n    {\n        \"required\": 1,\n        \"number\": 2,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 1,\n        \"question\": \"当前您是否开启了win goal APP信息推送：\",\n        \"id\": 2,\n        \"answers\": [\n            {\n                \"name\": \"是的，开启了接收信息推送\",\n                \"value\": 3\n            },\n            {\n                \"name\": \"以前开启过，现在已关闭\",\n                \"value\": 4\n            },\n            {\n                \"name\": \"一直关闭\",\n                \"value\": 7\n            }\n        ]\n    },\n    {\n        \"required\": 1,\n        \"number\": 3,\n        \"questionnaire_id\": 1,\n        \"answer_type\": 2,\n        \"question\": \"如果您关闭推送，关闭的原因是：（可多选\",\n        \"id\": 3,\n        \"answers\": [\n            {\n                \"name\": \"没有关闭\",\n                \"value\": 3\n            },\n            {\n                \"name\": \"推送条数太多\",\n                \"value\": 4\n            },\n            {\n                \"name\": \"推送内容我不感兴趣\",\n                \"value\": 4\n            },\n            {\n                \"name\": \"推送时间不合理\",\n                \"value\": 2\n            },\n            {\n                \"name\": \"推送消息不及时\",\n                \"value\": 0\n            },\n            {\n                \"name\": \"太多APP推送，消息过载\",\n                \"value\": 0\n            },\n            {\n                \"name\": \"不记得了\",\n                \"value\": 0\n            },\n            {\n                \"name\": \"其它\",\n                \"value\": 0\n            }\n        ]\n    }\n]",
                        "paramLimit": "",
                        "paramNote": "",
                        "paramValueList": [],
                        "default": 0,
                        "childList": [
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题id",
                                "paramKey": "id",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问卷id",
                                "paramKey": "questionnaire_id",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题编号",
                                "paramKey": "number",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "问题类型   1:单选  2: 多选  3:客观",
                                "paramKey": "answer_type",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "3",
                                "paramName": "是否必填 1:是 0:否",
                                "paramKey": "required",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "0",
                                "paramName": "问题内容",
                                "paramKey": "question",
                                "paramValue": "",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": []
                            },
                            {
                                "paramNotNull": "0",
                                "paramType": "12",
                                "paramName": "答案 统计数组",
                                "paramKey": "answers",
                                "paramValue": "[\n    {\n        \"name\": \"IOS\",\n        \"value\": 0\n    },\n    {\n        \"name\": \"Android\",\n        \"value\": 8\n    },\n    {\n        \"name\": \"其他\",\n        \"value\": 4\n    }\n]",
                                "paramLimit": "",
                                "paramNote": "",
                                "paramValueList": [],
                                "default": 0,
                                "childList": [
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "0",
                                        "paramName": "答案内容",
                                        "paramKey": "name",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    },
                                    {
                                        "paramNotNull": "0",
                                        "paramType": "3",
                                        "paramName": "回答该答案的次数",
                                        "paramKey": "value",
                                        "paramValue": "",
                                        "paramLimit": "",
                                        "paramNote": "",
                                        "paramValueList": [],
                                        "default": 0,
                                        "childList": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "responseHeader": [],
        "resultParamJsonType": 0,
        "resultParamType": 0,
        "structureID": "[]",
        "databaseFieldID": "[]",
        "globalStructureID": "[]",
        "fileID": null,
        "requestParamSetting": [],
        "resultParamSetting": [],
        "customInfo": [],
        "dataStructureList": [],
        "globalDataStructureList": [],
        "testCastList": [],
        "mockExpectationList": [],
        "apiManagerID": 174003,
        "createUserID": 174003,
        "updateUserID": 174003,
        "apiType": "http"
    }
]
```

## 工具
### common_abort
> 替代自带abort,返回格式化json

**使用方法**
``` 
# 也可将数据键值对传
common_abort(401, **{
                "code": 401,
                "msg": "Authentication error",
                "data": {},
                "success": False
            })
            
```

### CommonJsonRet
> 特定的结构marsh_with无法满足

**使用方法**
``` 
# 调用实例  获取实例对象属性构成的字典
CommonJsonRet(404, False, "Questionnaire not found", {})()
```

### AuthToken
> 调用第三方验证用户,并传用户id给装饰的方法

**使用方法**

```
@AuthToken()
def foo(*args,**kwargs,user_id):
    pass
    
```

### agument ,parse,resource重写

> 重写类中异常处理方法,或者实例化方法
