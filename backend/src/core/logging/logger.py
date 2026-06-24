import logging
import structlog


def configure_logger() -> None:
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO
        ),
    )


logger = structlog.get_logger()