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

from abc import ABC, abstractmethod
from logging import Logger
from typing import Dict, Optional
from .logging import setup_logger


class HookContext:
    """
    A class that can be used as a context for the hook to provide information necessary during the hook run.

    ...

    Methods
    -------
    None.
    """

    debug: bool
    output: str
    path: str
    plan: Dict
    remove: str

    def __init__(
        self,
        plan: Dict,
        debug: Optional[bool] = False,
        output: Optional[str] = "",
        path: Optional[str] = "",
        remove: Optional[str] = "",
    ) -> None:
        """
        Constructs all the necessary attributes for the HookContext object.

        Parameters
        ----------
        plan : Dict
            the terraform plan after being processed by Flattener class

        debug : bool, optional
            whether we show debug log messages or not, default: false

        output : str, optional
            a file path where we will save the flattened plan file in JSON format, default is empty

        path : str, optional
            a path pointing to the location of the terraform plan in JSON format, default is empty

        remove : str, optional
            a string containing the name of the tag and the its value separated by an equal sign that will be used to
            remove resources from the plan, example "remove=true", default is empty
        """
        self.debug = debug
        self.output = output
        self.path = path
        self.plan = plan
        self.remove = remove


class Hook(ABC):
    """
    An abstract class that can be used as a hook (interface) for the Flattener class to provide additional features.

    ...

    Methods
    -------
    run() -> Dict :
        runs the hook
    """

    _context: HookContext

    def __init__(self, context: HookContext, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the Hook object.

        Parameters
        ----------
        context : HookContext
            the context in which the hook is inserted

        logger : logging.Logger, optional
            the logger object to be used

        Returns
        -------
        None.
        """
        self._context = context
        self._logger = (
            logger if logger is not None else setup_logger("hook", debug=True)
        )

    @abstractmethod
    def run(self) -> Dict:
        """
        Runs the hook.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        pass


class RemoveResourceByTagHook(Hook):
    """
    A class that can be used as a hook to Flatplan in order to remove resources from
    the flattened plan by their tags.

    ...

    Methods
    -------
    run() -> Dict :
        runs the hook
    """

    def run(self) -> Dict:
        """
        Traverses the plan and removes the resources that contain a certain tag.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        tag, value = self._context.remove.split("=")

        if tag == "":
            raise Exception(f"Malformed tag in context, {tag}={value}")

        plan = self._context.plan

        if "resources" not in plan:
            self._logger.debug("Plan does not contain resources section")
            return plan

        resources = []

        for resource in plan["resources"]:
            resource_addr = resource["address"]

            self._logger.debug(f"Checking resource '{resource_addr}'")

            try:
                tags = resource["values"]["tags"]

                if tags is not None:
                    if tag not in tags or tags[tag] != value:
                        self._logger.debug(
                            f"Resource '{resource_addr}' does not meet criteria to be removed"
                        )
                        resources.append(resource)
                    else:
                        self._logger.debug(
                            f"Resource '{resource_addr}' will be removed"
                        )
                else:
                    self._logger.debug(
                        f"Resource '{resource_addr}' does not meet criteria to be removed"
                    )
                    resources.append(resource)
            except KeyError:
                self._logger.debug(
                    f"Resource '{resource_addr}' does not meet criteria to be removed"
                )
                resources.append(resource)

        plan["resources"] = resources

        return plan
