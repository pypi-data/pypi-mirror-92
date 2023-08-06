# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List

# Local
from .package import Package
from .core import Utils

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: InstalledPackage -------------------------------------------------------- #

class InstalledPackage(Package):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        s: str,
        private: bool = False
    ):
        lines = s.split('\n')
        name = self.__get_var(lines, 'Name: ')

        if not name:
            self.invalid = True

            return

        self.invalid = False

        super().__init__(name, self.__get_var(lines, 'Version: '), private)

        self.summary = self.__get_var(lines, 'Summary: ')
        self.home_page = self.__get_var(lines, 'Home-page: ')
        self.author = self.__get_var(lines, 'Author: ')
        self.author_email = self.__get_var(lines, 'Author-email: ')
        self.license = self.__get_var(lines, 'License: ')
        self.location = self.__get_var(lines, 'Location: ')

        dependencies_str = self.__get_var(lines, 'Requires: ')
        self.requires = [d.replace('-', '_') for d in dependencies_str.split(',')] if dependencies_str else []

        dependents_str = self.__get_var(lines, 'Required-by: ')
        self.required_by = [d.strip().replace('-', '_') for d in dependents_str.split(',')] if dependents_str else []


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_name(cls, name: str, private: bool = False) -> Optional:
        package = cls(Utils.get_pip_info_str(name), private=private)

        return package if not package.invalid else package

    def get_install_name(self, include_version: bool = False) -> Optional[str]:
        return super().get_install_name(include_version=include_version) if not self.private else '{} @ git+{}'.format(super().get_install_name(include_version=include_version), self.home_page) if self.home_page else None


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __get_var(self, lines: List[str], sep: str) -> Optional[str]:
        try:
            res =  [l for l in lines if sep in l][0].split(sep)[-1].strip()

            return res if res != 'None' else None
        except:
            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #