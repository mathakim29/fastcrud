import logging
import uvicorn
from loguru import logger

# Intercept standard logging and redirect to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.log(level, record.getMessage())

# Redirect standard logging
logging.basicConfig(handlers=[InterceptHandler()], level=0)

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(
        "core.base:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=None  # Disable default Uvicorn logging to let Loguru handle it
    )