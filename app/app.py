from fastapi import FastAPI

from routers.device import device_mgmt_router

app = FastAPI()


@app.get("/")
def read_root():
    """
    A simple entry point to return a greeting message.
    """
    return {"message": "Unnamed system for gpn"}


app.include_router(
    device_mgmt_router, prefix="/dev", tags=["device and user management"]
)
