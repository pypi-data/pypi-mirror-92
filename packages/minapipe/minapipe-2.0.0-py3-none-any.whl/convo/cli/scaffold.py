import argparse
import os
import sys
from typing import List, Text

from convo import telemetry
from convo.cli import SubParsersAction
import convo.train
from convo.cli.shell import shell
from convo.cli.utils import create_output_path
from convo.shared.utils.cli import print_success, print_error_and_exit
from convo.shared.constants import (
    DOCS_BASE_URL,
    DEFAULT_CONFIG_PATH,
    DEFAULT_DOMAIN_PATH,
    DEFAULT_DATA_PATH,
)


def add_subparser(
    subparsers: SubParsersAction, parents: List[argparse.ArgumentParser]
) -> None:
    """Add all init parsers.

    Args:
        subparsers: subparser we are going to attach to
        parents: Parent parsers, needed to ensure tree structure in argparse
    """
    scaffold_parser = subparsers.add_parser(
        "init",
        parents=parents,
        help="Creates a new project, with example training data, "
        "actions, and config files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    scaffold_parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Automatically choose default options for prompts and suppress warnings.",
    )
    scaffold_parser.add_argument(
        "--init-dir",
        default=None,
        help="Directory where your project should be initialized.",
    )

    scaffold_parser.set_defaults(func=run)


def print_train_or_instructions(args: argparse.Namespace, path: Text) -> None:
    import questionary

    print_success("Finished creating project structure.")

    should_train = (
        questionary.confirm("Do you want to train an initial model? 💪🏽")
        .skip_if(args.no_prompt, default=True)
        .ask()
    )

    if should_train:
        print_success("Training an initial model...")
        config = os.path.join(path, DEFAULT_CONFIG_PATH)
        training_files = os.path.join(path, DEFAULT_DATA_PATH)
        domain = os.path.join(path, DEFAULT_DOMAIN_PATH)
        output = os.path.join(path, create_output_path())

        args.model = convo.train(domain, config, training_files, output)

        print_run_or_instructions(args)

    else:
        print_success(
            "No problem 👍🏼. You can also train a model later by going "
            "to the project directory and running 'convo train'."
        )


def print_run_or_instructions(args: argparse.Namespace) -> None:
    from convo.core import constants
    import questionary

    should_run = (
        questionary.confirm(
            "Do you want to speak to the trained assistant on the command line? 🤖"
        )
        .skip_if(args.no_prompt, default=False)
        .ask()
    )

    if should_run:
        # provide defaults for command line arguments
        attributes = [
            "endpoints",
            "credentials",
            "cors",
            "auth_token",
            "jwt_secret",
            "jwt_method",
            "enable_api",
            "remote_storage",
        ]
        for a in attributes:
            setattr(args, a, None)

        args.port = constants.DEFAULT_SERVER_PORT

        shell(args)
    else:
        if args.no_prompt:
            print(
                "If you want to speak to the assistant, "
                "run 'convo shell' at any time inside "
                "the project directory."
            )
        else:
            print_success(
                "Ok 👍🏼. "
                "If you want to speak to the assistant, "
                "run 'convo shell' at any time inside "
                "the project directory."
            )


def init_project(args: argparse.Namespace, path: Text) -> None:
    create_initial_project(path)
    print("Created project directory at '{}'.".format(os.path.abspath(path)))
    print_train_or_instructions(args, path)


def create_initial_project(path: Text) -> None:
    from distutils.dir_util import copy_tree

    copy_tree(scaffold_path(), path)


def scaffold_path() -> Text:
    import pkg_resources

    return pkg_resources.resource_filename(__name__, "initial_project")


def print_cancel() -> None:
    print_success("Ok. You can continue setting up by running 'convo init' 🙋🏽‍♀️")
    sys.exit(0)


def _ask_create_path(path: Text) -> None:
    import questionary

    should_create = questionary.confirm(
        f"Path '{path}' does not exist 🧐. Create path?"
    ).ask()
    if should_create:
        os.makedirs(path)
    else:
        print_success("Ok. You can continue setting up by running " "'convo init' 🙋🏽‍♀️")
        sys.exit(0)


def _ask_overwrite(path: Text) -> None:
    import questionary

    overwrite = questionary.confirm(
        "Directory '{}' is not empty. Continue?".format(os.path.abspath(path))
    ).ask()
    if not overwrite:
        print_cancel()


def run(args: argparse.Namespace) -> None:
    import questionary

    print_success("Welcome to Convo! 🤖\n")
    if args.no_prompt:
        print(
            f"To get started quickly, an "
            f"initial project will be created.\n"
            f"If you need some help, check out "
            f"the documentation at {DOCS_BASE_URL}.\n"
        )
    else:
        print(
            f"To get started quickly, an "
            f"initial project will be created.\n"
            f"If you need some help, check out "
            f"the documentation at {DOCS_BASE_URL}.\n"
            f"Now let's start! 👇🏽\n"
        )

    if args.init_dir is not None:
        path = args.init_dir
    else:
        path = (
            questionary.text(
                "Please enter a path where the project will be "
                "created [default: current directory]",
                default=".",
            )
            .skip_if(args.no_prompt, default=".")
            .ask()
        )

    if args.no_prompt and not os.path.isdir(path):
        print_error_and_exit(f"Project init path '{path}' not found.")

    if path and not os.path.isdir(path):
        _ask_create_path(path)

    if path is None or not os.path.isdir(path):
        print_cancel()

    if not args.no_prompt and len(os.listdir(path)) > 0:
        _ask_overwrite(path)

    telemetry.track_project_init(path)

    init_project(args, path)
