"""




"""
import os
import json

from .context import QAContext
from .qatest import QATest
from . import html_tree_export, html_table_export


class _SessionRootTest(QATest):

    SESSION = None

    @classmethod
    def get_sub_test_types(cls):
        return cls.SESSION._test_types

    def can_fix(self, context):
        return False, "Can't fix the whole world :/"


class Session(object):
    class ObjectReprJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError:
                return repr(obj)

    def __init__(self):
        super(Session, self).__init__()

        # This is sooooooooooo hacky !!! ^o^
        # I'll burn in hell for this :p
        class Root(_SessionRootTest):
            SESSION = self

        self._test_types = []
        self._root_test_type = Root

        self._stop_on_fail = None
        self._allow_auto_fix = None
        self._context = QAContext(None)

        self._runs = []

    def register_test_types(self, test_types):
        self._test_types.extend(test_types)

    def register_tests_from_file(self, filename):
        """
        WARNING: only use this on trusted files !

        The python code in `filename` file must declare a `get_root_tests()`
        function returning a list of test types to register.

        The code can also use the gloable name `SESSION` which contains
        the session being configured.
        """
        if not os.path.isfile(filename):
            raise ValueError("{} is not a file !".format(filename))

        with open(filename, "rb") as fp:
            content = fp.read()

        self.register_tests_from_string(content, filename)

    def register_tests_from_string(self, code_string, virtual_filename):
        """
        WARNING: only use this with trusted data ! The `code_string` has
        the ability to wipe your server clean or tell anything to your
        mother in law !

        The python code in `code_string` string must declare a `get_root_tests()`
        function returning a list of test types to register.

        The code can also use the gloable name `SESSION` which contains
        the session being configured.

        The `virtual_filename` string will be used as the "source filename" in
        reports and some exceptions.
        """
        compiled = compile(code_string, virtual_filename, "exec")
        namespace = {"SESSION": self, "__filename__": virtual_filename}
        exec(compiled, namespace, namespace)
        getter_name = "get_root_tests"
        getter = namespace.get(getter_name)
        if getter is None:
            raise Exception(
                'Could not find a "{}()" function in {}. '
                "No test registered.".format(getter_name, virtual_filename)
            )

        try:
            test_types = getter()
        except Exception as err:
            import traceback

            traceback.print_exc()
            raise Exception(
                'Error executing "{}()" from {}: {}'.format(
                    getter_name, virtual_filename, err
                )
            )

        for TestType in test_types:
            TestType._forced_filename = virtual_filename
        self._test_types.extend(test_types)

    def context_set(self, **values):
        self._context.update(**values)

    def set_stop_on_fail(self, stop_on_fail):
        """
        `stop_on_fail` can be True, False, or None for default behavior
        """
        self._context.set_stop_on_fail(stop_on_fail)

    def set_allow_auto_fix(self, allow_auto_fix):
        """
        `allow_auto_fix` can be True, False, or None for default behavior
        """
        self._context.set_allow_auto_fix(allow_auto_fix)

    def run(self):
        root_test = self._root_test_type()
        self._runs.append(root_test)

        # use a copy of the context, tests will modify it:
        context = QAContext(self._context)

        # run all the tests:
        result = root_test.run(context)
        return result

    def to_lines(self):
        lines = []
        for run in self._runs:
            lines.extend(run.to_lines())
        return lines

    def to_dict_list(self):
        ret = []
        for run in self._runs:
            ret.append(run.to_dict())
        return ret

    def to_json(self):
        as_dict_list = self.to_dict_list()
        return json.dumps(as_dict_list, cls=self.ObjectReprJSONEncoder)

    def to_json_file(self, filename, force_overwrite=False):
        as_list = self.to_dict_list()
        if os.path.exists(filename) and not force_overwrite:
            raise ValueError("filename {} already exists !".format(filename))
        with open(filename, "w") as fp:
            json.dump(as_list, fp, cls=self.ObjectReprJSONEncoder)

    def to_html_tree(self, filename, force_overwrite=False):
        session_json = self.to_json()
        content = html_tree_export.html_tree(session_json)
        if os.path.exists(filename) and not force_overwrite:
            raise ValueError("filename {} already exists !".format(filename))
        with open(filename, "w") as fp:
            fp.write(content)

    def to_html(self, filename, force_overwrite=False, config={}):
        session_json = self.to_json()
        content = html_table_export.html_table(session_json, config)
        if os.path.exists(filename) and not force_overwrite:
            raise ValueError("filename {} already exists !".format(filename))
        with open(filename, "w") as fp:
            fp.write(content)
