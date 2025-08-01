__all__ = ["build_report"]

import traceback


def build_report(reader_processor, publisher, parser, config):
    try:
        actual_log_date = reader_processor.run()

        analytics = parser.calculate_analytics()
        if analytics:
            publisher.publish(analytics, actual_log_date)

    except BaseException:
        config.logger.error(traceback.format_exc())
