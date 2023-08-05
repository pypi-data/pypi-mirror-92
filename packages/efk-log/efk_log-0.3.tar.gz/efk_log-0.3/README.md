# Efk-log

## Quick start

> Called from where the project was launched.



### En

1. Logs in json format are easily collected in es and can be easily indexed on top of kibana for related fields.

2. Note that it is important to avoid index value conflicts, as different value types for the same index name can cause conflicts.

3. Use the supervisor to guard the service processes started by gunicorn when starting a multi-process service, in conjunction with the supervisor's logging feature.

   1. file_path=None

   2. supervisor-related parameters are sliced to avoid large log files.

      ```
      stdout_logfile_maxbytes = 50MB   ; max # logfile bytes b4 rotation (default 50MB)
      stdout_logfile_backups = 10 ; # of stdout logfile backups (default 10)
      stdout_logfile = /data/logs/efk-log/efk-log.log
      ```

### Zh

1. json 格式的日志 方便收集到es中可方便对相关字段在kibana上面创建索引

2. 需要注意的是，要避免索引值的冲突，相同的索引名，数值类型不同就会造成冲突

3. 多进程启动 服务时候配合 supervisor 的日志功能使用，使用supervisor 守护gunicorn 启动的服务进程

   1. file_path=None

   2. supervisor 相关参数 进行切分，避免日志文件太大

      ```
      stdout_logfile_maxbytes = 50MB   ; max # logfile bytes b4 rotation (default 50MB)
      stdout_logfile_backups = 10 ; # of stdout logfile backups (default 10)
      stdout_logfile = /data/logs/efk-log/efk-log.log
      ```



### Flask 

```
LogJsonFormat(file_path=None, console=True, project='efk-log')
```

### Celery

```
from celery.signals import setup_logging

@setup_logging.connect
def set_log(*args, **kwargs):
    LogJsonFormat(file_path=None, console=True, project='celery-prd')
```



### Demo

```
from efk_log import LogJsonFormat

if __name__ == '__main__':
    LogJsonFormat(file_path=None, console=True, project='efk-log')

    import logging

    LOGGER = logging.getLogger(__name__)

    LOGGER.info('get user info', extra={'metrics': {
        'cid': 'xxxxxx'
    }})

    try:
        2 / 0
    except Exception as e:
        LOGGER.exception('except...', exc_info=e)

    LOGGER.error('error')
```

