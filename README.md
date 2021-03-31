# Маленькое приложение для подсчёта затраченного на задачи времени

## Использование в консоли
```shell
python -m time_logger --help
```

## API
* time_logger.crud.read_data
* time_logger.crud.update_data
* time_logger.service.log_start
* time_logger.service.log_stop
* time_logger.service.calculate_time
* time_logger.time.extract_time
* time_logger.time.format_time
* time_logger.time.calculate_interval
* time_logger.time.convert_minutes
