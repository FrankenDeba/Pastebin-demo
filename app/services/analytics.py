from prometheus_fastapi_instrumentator import Instrumentator, metrics

# from ..main import app

def start_analytics(app) -> None:

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=False,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[".*admin.*", "/metrics"],
        # env_var_name="ENABLE_METRICS",
        inprogress_name="inprogress",
        inprogress_labels=True
    )

    instrumentator.add(metrics.latency(buckets=(0.005, 0.01, 0.025, 0.05, 0.1)))
    instrumentator.instrument(app)

    @app.on_event("startup")
    async def on_startup():
        print("Exposing metrics endpoint /metrics")
        instrumentator.expose(app)

__all__ = ["start_analytics"]
