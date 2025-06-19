import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("casbin.policy").setLevel(logging.WARNING)

logger = logging.getLogger()