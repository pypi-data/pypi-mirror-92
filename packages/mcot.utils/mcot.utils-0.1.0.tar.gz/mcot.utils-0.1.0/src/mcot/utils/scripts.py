"""Utilities to create a common interface to all the scripts."""
import argparse
import ast
import importlib
import pkgutil
import sys

from loguru import logger

from .log import setup_log


def get_docstring(filename):
    """Extracts the filename from the docstring.

    :param filename: path to python file
    :return: module-level docstring (None if undefined)
    """
    with open(filename) as f:
        base = ast.parse(f.read())
    return ast.get_docstring(base)


def run_script(module, argc=None):
    """Run script from command line.

    :param add_to_parser: function that takes an argument parser and adds information to it
    :param run_from_args: function that runs the script based on the arguments of the parser
    :param argc: command line arguments
    """
    doc_string = module.__doc__

    logger.enable('mcot')
    script_logger = logger.opt(depth=1)
    if hasattr(module, 'main'):
        setup_log()
        script_logger.info('starting script')
        try:
            module.main(args)
        except:
            script_logger.exception('Failed script')
    else:
        parser = argparse.ArgumentParser(doc_string)
        module.add_to_parser(parser)


        args = parser.parse_args(argc)

        setup_log()

        script_logger.info('starting script')
        try:
            module.run_from_args(args)
        except Exception:
            script_logger.exception('failed script')
            raise
    script_logger.info('finished script')


class ScriptDirectories(object):
    """All script directories that have been registered.

    All .py files within this directory are considered scripts (except
    __init__ and __main__) Any sub-directories are considered sub-
    scripts (as long as they contain a __init__)
    """
    def __init__(self, names=()):
        self.modules = [(None, importlib.import_module(name)) for name in names]

    def add(self, name: str, group):
        """Adds a new script directory.

        In the __init__ of the script directory add:

        mcot.utils.scripts.directories.add(__name__)

        :param name: __name__ of the script directory
        :param group: what group to put the scripts in (set to None for no group)
        """
        self.modules.append((group, importlib.import_module(name)))

    def all_scripts(self, ):
        scripts = {}

        def process(module, script_dict):
            for module_info in pkgutil.iter_modules(module.__path__):
                if module_info.name.startswith('_'):
                    continue
                full_name = f'{module.__name__}.{module_info.name}'
                if module_info.name in script_dict:
                    raise ValueError(f"Dual script definition for {module_info.name}")
                if module_info.ispkg:
                    script_dict[module_info.name] = {}
                    process(
                        importlib.import_module(full_name),
                        script_dict[module_info.name]
                    )
                else:
                    script_dict[module_info.name] = full_name

        for name, module in self.modules:
            if name in scripts:
                raise ValueError(f"Dual script definition for {name}")
            if name is None:
                process(module, scripts)
            else:
                scripts[name] = {}
                process(module, scripts[name])
        return scripts

    @staticmethod
    def _scripts2string(scripts, indent=0):
        if isinstance(scripts, dict):
            res = "\n"
            for name in sorted(scripts):
                res = res + " " * indent + f"- {name}: " + ScriptDirectories._scripts2string(scripts[name], indent + 2)
            return res + ""
        else:
            fn = pkgutil.find_loader(scripts).get_filename()
            res = get_docstring(fn)
            if res is None:
                return "\n"
            return res.splitlines()[0] + "\n"

    def __call__(self, args=None):
        """Runs a script identified by the arguments.

        :param args: optionally group name and script name together with the script arguments (default: sys.argv[1:])
        """
        if args is None:
            args = sys.argv[1:]
        if len(args) == 0:
            choose_script, args = (), None
        elif '.' in args[0]:
            choose_script, args = args[0].split('.'), args[1:]
        else:
            choose_script, args = args, None

        current_group = []
        scripts = self.all_scripts()
        while len(choose_script) != 0 and isinstance(scripts, dict) and choose_script[0] in scripts.keys():
            current_group.append(choose_script[0])
            scripts = scripts[choose_script[0]]
            choose_script = choose_script[1:]

        if isinstance(scripts, dict):
            print('Usage: mcot [<script_group>...] <script_name> <args>...')
            if len(current_group) == 0:
                print('Available scripts:')
            else:
                print(f'Available scripts in script group {".".join(current_group)}:')
            print(self._scripts2string(scripts)[1:])
            print('')
            print("Error: Incomplete or invalid script name provided")
            exit(1)
        if args is None:
            args = choose_script
        elif len(choose_script) != 0:
            raise ValueError(f"Script already fully define before processing .{'.'.join(choose_script)}")

        script = importlib.import_module(scripts)
        run_script(script, args)


def load_all_mcot():
    mcot = importlib.import_module("mcot")
    script_modules = []
    for module_info in pkgutil.iter_modules(mcot.__path__):
        if module_info.ispkg:
            try:
                name = f"mcot.{module_info.name}._scripts"
                importlib.import_module(name)
                script_modules.append(name)
            except ImportError as e:
                pass
    return script_modules


def run(argv=None):
    modules = load_all_mcot()
    directories = ScriptDirectories(modules)
    directories(argv)
