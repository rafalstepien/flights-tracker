import uvicorn

from flights_tracker.azair_tracker.tracker import AZairTracker
from flights_tracker.routes import routes

app = AZairTracker()
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
