import os
import json
import webbrowser
import time

try:
    json_parse_exception = json.decoder.JSONDecodeError
except AttributeError:  # Python 2
    json_parse_exception = ValueError

try:
    import maya
except ImportError:
    slang_time = time.ctime
else:
    try:
        maya.MayaDT
    except AttributeError:
        slang_time = time.ctime
    else:

        def _maya_slang_time(ts):
            return maya.MayaDT(ts).slang_time()

        slang_time = _maya_slang_time

import sqarf
import sqarf.qatest
import sqarf.html_table_export
import sqarf.html_tree_export

from kabaret import flow


class StatusSelectionValue(flow.values.MultiChoiceValue):

    CHOICES = (
        sqarf.qatest.QAResult.failed_statuses()
        + sqarf.qatest.QAResult.passed_statuses()
        + sqarf.qatest.QAResult.not_applicable_statuses()
    )


class ConfigureReportAction(flow.Action):

    _report = flow.Parent()

    filter_statuses = flow.Param([], StatusSelectionValue)
    show_logs = flow.BoolParam()
    show_times = flow.BoolParam()
    show_descriptions = flow.BoolParam()
    show_context_edits = flow.BoolParam()
    show_contexts = flow.BoolParam()
    show_debug_logs = flow.BoolParam()

    def needs_dialog(self):
        return True

    def get_buttons(self):
        config = sqarf.html_table_export.get_default_config()
        config.update(self._report._display_config.get() or {})

        self.filter_statuses.set(config["filter_statuses"] or [])
        self.show_logs.set(config["show_logs"])
        self.show_times.set(config["show_times"])
        self.show_descriptions.set(config["show_descriptions"])
        self.show_context_edits.set(config["show_context_edits"])
        self.show_contexts.set(config["show_contexts"])
        self.show_debug_logs.set(config["show_debug_logs"])

        return ["Apply"]

    def run(self, button):
        if button != "Apply":
            return

        config = dict(
            filter_statuses=self.filter_statuses.get(),
            show_logs=self.show_logs.get(),
            show_times=self.show_times.get(),
            show_descriptions=self.show_descriptions.get(),
            show_context_edits=self.show_context_edits.get(),
            show_contexts=self.show_contexts.get(),
            show_debug_logs=self.show_debug_logs.get(),
        )
        self._report._display_config.set(config)


class ExportStyleChoice(flow.values.ChoiceValue):

    CHOICES = ("Interactive Tree", "Simple Table", "JSON")

    @classmethod
    def default(cls):
        return cls.CHOICES[0]


class ExportReportAction(flow.Action):

    _report = flow.Parent()

    export_style = flow.Param(ExportStyleChoice.default(), ExportStyleChoice)
    filename = flow.Param("")
    allow_overwrite = flow.BoolParam(False)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set("")
        return ["Export", "View", "Close"]

    def run(self, button):
        if button == "Close":
            return

        if button == "View":
            IN_SAME_TAB = 0
            webbrowser.open(self.filename.get(), new=IN_SAME_TAB)
            return self.get_result(close=False)

        filename = self.filename.get().strip()
        if not filename:
            self.message.set("Please, enter a value for 'filename' !")
            return self.get_result(close=False)

        if os.path.exists(filename) and not self.allow_overwrite.get():
            self.message.set("Filename {} already exists !".format(filename))
            return self.get_result(close=False)

        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except Exception:
                self.message.set("Error creating parent folder for {}".format(filename))
                return self.get_result(close=False)

        style = self.export_style.get()
        if style == "JSON":
            content = self._report._as_json.get()
        elif style == "Simple Table":
            content = self._report.get_html_report()
        elif style == "Interactive Tree":
            content = self._report.get_html_tree_report()

        with open(filename, "w") as fp:
            fp.write(content)

        self.message.set("Export done to {}".format(filename))
        return self.get_result(close=False)


class QAReport(flow.Object):

    _as_json = flow.Param().watched()
    ran_by = flow.Computed()
    ran_on = flow.Computed()
    result = flow.Computed()
    summary = flow.Computed()
    _display_config = flow.Param().watched()
    configure = flow.Child(ConfigureReportAction)
    display = flow.Computed(cached=True).ui(
        editor="textarea",
        html=True,
        label="",
        width=800,  # does nothing, find out the proper way !
    )
    export = flow.Child(ExportReportAction)

    def _get_data(self):
        try:
            data = self._data
        except AttributeError:
            data = None
        if data is not None:
            return data

        try:
            self._data = json.loads(self._as_json.get())
        except json_parse_exception:
            self._data = []
        return self._data

    def child_value_changed(self, value):
        if value is self._display_config:
            self.display.touch()

        elif value is self._as_json:
            self._data = None
            self.ran_by.touch()
            self.ran_on.touch()
            self.result.touch()
            self.summary.touch()
            self.display.touch()

    def compute_child_value(self, value):
        if value is self.ran_by:
            self.ran_by.set("???")
            return

        if value is self.ran_on:
            data = self._get_data()
            timestamp = data and data[0]["result"]["timestamp"] or 0
            self.ran_on.set(timestamp)
            return

        if value is self.result:
            data = self._get_data()
            result = data and data[0]["result"]["status"] or "???"
            self.result.set(result)
            return

        if value is self.summary:
            data = self._get_data()
            summary = data and data[0]["result"]["summary"]
            self.summary.set(summary)

        if value is self.display:
            self.display.set(self.get_html_report())

    def get_html_tree_report(self):
        as_json = self._as_json.get()
        if not as_json:
            return (
                "<html><body><h3><font color=brown>"
                "No data to display"
                "</font></h3></body></html"
            )
        try:
            html = sqarf.html_tree_export.html_tree(
                as_json,
            )
        except Exception:
            return self._get_html_traceback()
        return html

    def get_html_report(self):
        as_json = self._as_json.get()
        if not as_json:
            return (
                "<html><body><h3><font color=brown>"
                "No data to display"
                "</font></h3></body></html"
            )

        config = self._display_config.get() or {}
        try:
            html = sqarf.html_table_export.html_table(as_json, config)
        except Exception:
            return self._get_html_traceback()
        return html

    def _get_html_traceback(self):
        import traceback

        return (
            "<HTM><BODY>"
            "<H1>There was an error generating report:</H1>"
            "<PRE>{trace}</PRE>"
            "<H1>JSON Source Data:</H1>"
            "{data}"
            "</BODY></HTML>"
        ).format(trace=traceback.format_exc(), data=self._as_json.get())


class QAReportCollection(flow.Map):
    @classmethod
    def mapped_type(cls):
        return QAReport

    def mapped_names(self, page_num=0, page_size=None):
        # We need to bake to a list, generators dont have __len__:
        return list(
            reversed(super(QAReportCollection, self).mapped_names(page_num, page_size))
        )

    def columns(self):
        return ["By", "On", "Result", "Summary"]

    def _fill_row_cells(self, row, item):
        row["By"] = item.ran_by.get()
        row["On"] = slang_time(item.ran_on.get() or 0)
        row["Result"] = item.result.get()
        row["Summary"] = item.summary.get()

    def _fill_row_style(self, style, item, row):
        if row["Result"] != "PASSED":
            style["Result_background-color"] = "#440000"
        else:
            style["Result_background-color"] = "#004400"


class QAReports(flow.Object):

    reports = flow.Child(QAReportCollection).ui(expanded=True)

    def store_report(self, json_report):
        report_name = "R{:03}".format(len(self.reports) + 1)
        report = self.reports.add(report_name)
        report._as_json.set(json_report)
        return report
