import sqarf

from kabaret import flow

from .extra_tests import ExtraTestsConfig
from .qareport import QAReports


class QARun(flow.Action):
    """
    This Action will run all test types specified
    by `self.get_test_types()` in a context
    with a `TESTED` key containing the parent
    object.

    In short: Subclass it, override the `get_test_types()`
    method and use is as a child of the object to test.

    """

    _BUTTON_RUN_TEST = "Run Tests"
    _BUTTON_GOTO_REPORTS = "Browse Reports"
    _BUTTON_GOTO_CUSTOM_TESTS = "Configure Custom Tests"

    _tested = flow.Parent()
    reports = flow.Child(QAReports).ui(hidden=True)
    custom_test_config = flow.Child(ExtraTestsConfig).ui(hidden=True)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set("This will run all QA tests on {}".format(self._tested.oid()))
        return [
            self._BUTTON_RUN_TEST,
            self._BUTTON_GOTO_REPORTS,
            self._BUTTON_GOTO_CUSTOM_TESTS,
        ]

    def run(self, button):
        if button == self._BUTTON_GOTO_REPORTS:
            return self.get_result(goto=self.reports.oid())
        if button == self._BUTTON_GOTO_CUSTOM_TESTS:
            return self.get_result(goto=self.custom_test_config.oid())

        self.message.set("Running tests.")
        report = self.run_tests(self.log_message)
        return self.get_result(goto=report.oid())

    def log_message(self, message):
        text = self.message.get() + message + "\n"
        self.message.set(text)

    def get_test_types(self):
        raise NotImplementedError()

    def run_tests(self, messager):
        """
        Run all the test types returned by `get_test_types()`,
        store the report in `self.reports` and return the
        report object.
        """
        messager("Starting test session")
        session = sqarf.Session()
        session.register_test_types(self.get_test_types())

        messager("Loading extra test files")
        for filename in self.custom_test_config.get_extra_filenames():
            messager("   " + filename)
            session.register_tests_from_file(filename)
            messager("   Ok.")

        code = self.custom_test_config.get_extra_code()
        if code:
            messager("Loading extra test code")
            session.register_tests_from_string(code, "flow_custom_tests")
            messager("   Ok.")

        key = "TESTED"
        o = self._tested
        messager("Adding context {}=<{}>".format(key, o.oid()))
        session.context_set(TESTED=o)

        messager("Running Tests")
        session.run()

        messager("Saving Report")
        json_report = session.to_json()
        return self.reports.store_report(json_report)
