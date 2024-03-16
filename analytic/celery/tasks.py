from celery import Celery

app = Celery("metrics")
app.config_from_object("celery_config")


@app.task(name="dev_stats", queue="dev_metrics")
def dev_metrics_by_device_id(device_id, start_time, stop_time, metric_key):
    pass


@app.task(name="user_stats_all", queue="user_all")
def dev_metrics_by_user_all(user_id, start_time, stop_time, metric_key):
    pass


@app.task(name="useк_stats_foreach", queue="user_foreach")
def dev_metrics_by_user_foreach(user_id, start_time, stop_time, metric_key):
    pass
