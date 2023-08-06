# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List

# Pip
from pipreqs import pipreqs

# Local
from .models import InstalledPackage

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: PipUtils ------------------------------------------------------------ #

class Dependencies:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def get_dependencies(cls, path: Optional[str] = None) -> List[InstalledPackage]:
        all_imports = pipreqs.get_all_imports(path or '.')
        pkg_names = pipreqs.get_pkg_names(all_imports)
        public_pkg_names = [p['name'] for p in pipreqs.get_imports_info(pkg_names)]

        installed_packages = [InstalledPackage.from_name(name, private=name not in public_pkg_names) for name in pkg_names]

        return [installed_package for installed_package in installed_packages if installed_package]

    # Alias
    get = get_dependencies



# ---------------------------------------------------------------------------------------------------------------------------------------- #