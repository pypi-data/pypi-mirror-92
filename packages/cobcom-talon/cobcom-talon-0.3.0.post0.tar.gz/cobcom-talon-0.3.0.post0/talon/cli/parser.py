import argparse
import logging


class TalonArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        """
        Setup TALON argument parser.

        This function returns an argparse.ArgumentParser object with
        `allow_abbrev=True` and `add_help=True`.

        Parsers of subcommands must be added with the
        `TalonArgumentParser.add_talon_subcommand()` method, which wraps the
        `subcommands.add_parser()` method.

        This class is a child of argparse.ArgumentParser. It inherits all its
        properties and methods and changes the following behaviours:

        - If a subparser is defined, it is appended to a list that is readable
            at the `subcommand_parsers` property.
        - The verbosity and force arguments are added to each subparser.
        - When input arguments are parsed with `parse_args`, the verbosity is
            parsed by the `parse_verbosity` function.

        Args:
            kwargs: dict
                keyword arguments that will be passed to the constructor of
                argparse.ArgumentParser.
        """
        kwargs['allow_abbrev'] = True
        kwargs['add_help'] = True
        kwargs['prog'] = 'talon'
        super().__init__(**kwargs)

        self._talon_subparsers = self.add_subparsers()
        self._talon_subparsers.required = True
        self._talon_subparsers.dest = 'subcommand'

        self._subcommand_parsers = []

    @property
    def subcommand_parsers(self) -> list:
        """
        This property returns the list of parsers associated to each defined
        subcommand.

        Returns:
            list of parsers associated to each defined subcommand.
        """
        return self._subcommand_parsers

    def add_talon_subcommand(self, *args, **kwargs) -> argparse.ArgumentParser:
        """
        Add a talon subcommand to the parser.

        Args:
            *args: arguments that will be passed to the `add_parser` method.
            **kwargs: keyword arguments that will be passed to the `add_parser`
                method.

        Returns:
            argparse.ArgumentParser object.
        """
        sub = self._talon_subparsers.add_parser(*args, **kwargs)
        self._subcommand_parsers.append(sub)
        return sub

    def parse_args(self, *args) -> argparse.Namespace:
        for sub in self.subcommand_parsers:
            self.add_verbosity_and_force_to_parser(sub)
        arguments = super().parse_args(*args)
        self.parse_verbosity(*arguments)
        return arguments

    def add_verbosity_and_force_to_parser(self,
                                          parser: argparse.ArgumentParser):
        """
        This function adds the verbosity and force parameters to a parser.

        After calling this method, the input parser will have the following
        boolean arguments.

        - `--force`
        - `--quiet`
        - `--warn`
        - `--info`
        - `--debug`

        Args:
            parser: argparse.ArgumentParser
                Argument parser.
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help="Overwrite existing files."
        )

        verb = parser.add_mutually_exclusive_group()
        verb.add_argument(
            '--quiet',
            action='store_true',
            help='Do not display messages.'
        )
        verb.add_argument(
            '--warn',
            action='store_true',
            help='Display warning messages.'
        )
        verb.add_argument(
            '--info',
            action='store_true',
            help='Display information messages.'
        )
        verb.add_argument(
            '--debug',
            action='store_true',
            help='Display debug messages.'
        )

    def parse_verbosity(self, args: argparse.Namespace):
        """
        This function applies the wanted verbosity level in logging specified
        by the parsed arguments given in input.

        The default level is logging.WARNING.

        Args:
            args: argparse.Namespace
                Namespace parsed from inputs.
        """
        level = logging.WARNING
        if args.debug:
            level = logging.DEBUG
        if args.info:
            level = logging.INFO
        if args.warn:
            level = logging.WARN
        if args.quiet:
            level = logging.CRITICAL

        logging.getLogger().setLevel(level)
