from fastapi import FastAPI

from routers.stats import stats_router

app = FastAPI()


@app.get("/")
def read_root():
    """
    A simple entry point to return a greeting message.
    """
    return {"message": "Analysis"}


app.include_router(stats_router, prefix="/stats", tags=["stats for devices"])
