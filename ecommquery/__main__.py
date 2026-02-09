import logging
import code
import sys

from ecommquery.about import about


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Application started")

    code.interact(banner=about.BANNER, local=locals())

    return 0

if __name__ == "__main__":
    sys.exit(main())


