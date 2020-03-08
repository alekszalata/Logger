from src import logger

log = logger.Logger("TestLogger")

for i in range(10):
    log.random_log("testing random log", logger.Level.WARNING)

log.trace("Trace check")
log.debug("Debug check")
log.info("Info check")
log.warning("Warning check")
log.error("Error check")
print()

log.set_level(logger.Level.TRACE)
log.trace("H")
log.debug("E")
log.info("L")
log.warning("L")
log.error("0")
print()

log.config(time=True, file=True, level=False)
log.trace("B")
log.debug("Y")
log.info("E")

log.filename = "logs.log"
log.config(time=True, file=True, level=True, mode="w")
log.trace("Trace check")
log.debug("Debug check")
log.info("Info check")
log.warning("Warning check")
log.error("Error check")
