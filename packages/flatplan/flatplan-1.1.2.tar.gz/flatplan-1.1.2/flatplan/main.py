#!/usr/bin/env python3

# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

import fire
from json import dumps
from os.path import expanduser
from sys import exit, stdin, stdout
from typing import Optional
from .configuration import DEFAULT_ENCODING
from .flattener import Flattener
from .hooks import HookContext, RemoveResourceByTagHook
from .logging import setup_logger


def run(
    debug: Optional[bool] = False,
    output: Optional[str] = "",
    path: Optional[str] = "",
    remove: Optional[str] = "",
) -> None:
    """
    Starts the execution of the Flatplan application.

    Parameters
    ----------
    debug : bool, optional
        whether we show debug log messages or not, default: false

    output : str, optional
        a file path where we will save the flattened plan file in JSON format, default it writes to stdout

    path : str, optional
        a path pointing to the location of the terraform plan in JSON format, default it reads from stdin

    remove : str, optional
        a string containing the name of the tag and the its value separated by an equal sign that will be used to
        remove resources from the plan, example "remove=true", default is empty

    Returns
    -------
    None.
    """

    logger = setup_logger("flatplan", debug)
    f_in = stdin
    f_out = stdout

    logger.debug("Flattening...")

    if path:
        logger.debug(f"Reading plan from {path}")
        f_in = open(expanduser(path), "r", encoding=DEFAULT_ENCODING)

    if output:
        logger.debug(f"Output will be saved to {output}")
        f_out = open(expanduser(output), "w+", encoding=DEFAULT_ENCODING)

    flattener = Flattener(f_in.read(), logger=logger)
    plan = flattener.flatten()

    context = HookContext(
        debug=debug, output=output, path=path, plan=plan, remove=remove
    )

    hooks = [RemoveResourceByTagHook(context, logger)]

    for hook in hooks:
        plan = hook.run()
        context.plan = plan

    json_plan = dumps(plan)

    f_out.write(f"{json_plan}\n")
    f_in.close()
    f_out.close()

    logger.debug("Flattened!")


def main() -> None:  # pragma: no cover
    """
    A wrapper for the _run function also providing CLI parameter parsing.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    fire.Fire(run)
    exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
