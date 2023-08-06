# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from logging import error

from portmod.atom import Atom
from portmod.globals import env
from portmod.l10n import l10n
from portmod.loader import load_installed_pkg


def validate(args):
    # Check that mods in the DB correspond to mods in the mods directory
    for category in os.listdir(env.prefix().INSTALLED_DB):
        if not category.startswith("."):
            for mod in os.listdir(os.path.join(env.prefix().INSTALLED_DB, category)):
                # Check that mod is installed
                if not os.path.exists(
                    os.path.join(env.prefix().PACKAGE_DIR, category, mod)
                ):
                    error(l10n("in-database-not-installed", atom=f"{category}/{mod}"))

                # Check that pybuild can be loaded
                if not load_installed_pkg(Atom(f"{category}/{mod}")):
                    error(
                        l10n(
                            "in-database-could-not-load",
                            atom=Atom(f"{category}/{mod}"),
                        )
                    )

    # Check that all mods in the mod directory are also in the DB
    for category in os.listdir(env.prefix().PACKAGE_DIR):
        for mod in os.listdir(os.path.join(env.prefix().PACKAGE_DIR, category)):
            if not os.path.exists(
                os.path.join(env.prefix().INSTALLED_DB, category, mod)
            ):
                error(l10n("installed-not-in-database", atom=f"{category}/{mod}"))
