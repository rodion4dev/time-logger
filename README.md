# Маленькое приложение для подсчёта затраченного на задачи времени

## Использование в консоли
```shell
python -m time_logger --help
```

## API
* time_logger.crud
    * read_data
    * update_data
    * read_task
    * update_task
    * backup_data
* time_logger.service
    * log_start
    * log_stop
    * calculate_time
    * import_database
    * remove_application_data
    * check_application_directory
    * lock_task
    * unlock_task
    * backup_database
* time_logger.time
    * extract_time
    * format_time
    * calculate_interval
    * convert_minutes
