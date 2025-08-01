__all__ = ["Publisher"]

import json
import os
import shutil

from src.utils.publisher.template import get_template


class Publisher:
    def __init__(self, config):
        self.config = config
        self.template = get_template()

    def publish(self, analytics, log_date):
        table_json = self._jsonify(analytics)
        report = self.template.replace("$table_json", table_json)

        self._create_report_file(report, log_date)
        self._copy_js_script()

    def _jsonify(self, analytics):
        return json.dumps([atom_analytics.to_dict() for atom_analytics in analytics])

    def _create_report_file(self, report, log_date):
        filename = log_date.strftime("report-%y%m%d.html")
        absolute_report_path = "/".join([self.config.report_dir, filename])

        try:
            with open(absolute_report_path, "w", encoding=self.config.encoding) as f:
                f.write(report)
        except OSError as e:
            self.config.logger.error(
                f"Ошибка при создании или записи файла отчёта: {e}"
            )

    def _copy_js_script(self):
        project_root = os.getcwd()
        src_path = os.path.join(
            project_root, "data", "templates", "report", "jquery.tablesorter.min.js"
        )
        dst_path = os.path.join(self.config.report_dir, "jquery.tablesorter.min.js")

        try:
            shutil.copy2(src_path, dst_path)
        except (OSError, shutil.Error) as e:
            self.config.logger.error(f"Ошибка при копировании js скрипта: {e}")
