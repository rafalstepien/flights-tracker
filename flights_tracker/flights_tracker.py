import uvicorn

from flights_tracker.azair_tracker.tracker import AZairTracker

app = AZairTracker()

if __name__ == "__main__":
    uvicorn.run("flights_tracker:app", host="127.0.0.1", port=5000, log_level="info")
