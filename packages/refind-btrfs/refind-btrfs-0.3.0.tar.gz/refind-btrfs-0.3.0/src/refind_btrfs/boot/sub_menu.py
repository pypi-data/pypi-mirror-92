# region Licensing
# SPDX-FileCopyrightText: 2020 Luka Žaja <luka.zaja@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

""" refind-btrfs - Generate rEFInd manual boot stanzas from Btrfs snapshots
Copyright (C) 2020  Luka Žaja

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# endregion

from __future__ import annotations

from typing import List, Optional

from refind_btrfs.common import constants
from refind_btrfs.common.enums import GraphicsParameter, RefindOption
from refind_btrfs.device.subvolume import Subvolume
from refind_btrfs.utility import helpers

from .boot_options import BootOptions


class SubMenu:
    def __init__(
        self,
        name: str,
        loader_path: Optional[str],
        initrd_path: Optional[str],
        graphics: Optional[bool],
        boot_options: Optional[BootOptions],
        add_boot_options: BootOptions,
        is_disabled: bool,
    ) -> None:
        self._name = name
        self._loader_path = loader_path
        self._initrd_path = initrd_path
        self._graphics = graphics
        self._boot_options = boot_options
        self._add_boot_options = add_boot_options
        self._is_disabled = is_disabled

    def __str__(self) -> str:
        main_indent = constants.TAB
        option_indent = main_indent * 2
        result: List[str] = []

        name = self.name

        result.append(f"{main_indent}{RefindOption.SUB_MENU_ENTRY.value} {name} {{")

        loader_path = self.loader_path

        if not helpers.is_none_or_whitespace(loader_path):
            result.append(f"{option_indent}{RefindOption.LOADER.value} {loader_path}")

        initrd_path = self.initrd_path

        if not helpers.is_none_or_whitespace(initrd_path):
            result.append(f"{option_indent}{RefindOption.INITRD.value} {initrd_path}")

        graphics = self.graphics

        if graphics is not None:
            value = (
                GraphicsParameter.ON.value if graphics else GraphicsParameter.OFF.value
            )
            result.append(f"{option_indent}{RefindOption.GRAPHICS.value} {value}")

        boot_options = self.boot_options

        if not boot_options is None:
            boot_options_str = str(boot_options)

            if not helpers.is_none_or_whitespace(boot_options_str):
                result.append(
                    f"{option_indent}{RefindOption.BOOT_OPTIONS.value} {boot_options_str}"
                )

        add_boot_options_str = str(self.add_boot_options)

        if not helpers.is_none_or_whitespace(add_boot_options_str):
            result.append(
                f"{option_indent}{RefindOption.ADD_BOOT_OPTIONS.value} {add_boot_options_str}"
            )

        result.append(f"{main_indent}}}")

        return constants.NEWLINE.join(result)

    def is_matched_with(self, subvolume: Subvolume) -> bool:
        boot_options = self.boot_options

        return (
            boot_options.is_matched_with(subvolume)
            if boot_options is not None
            else False
        )

    def can_be_used_for_bootable_snapshot(self) -> bool:
        loader_path = self.loader_path

        if not helpers.is_none_or_whitespace(loader_path):
            return False

        boot_options = self.boot_options

        if boot_options is not None:
            return False

        initrd_path = self.initrd_path

        if initrd_path is not None:
            return initrd_path != constants.EMPTY_STR

        return True

    @property
    def name(self) -> str:
        return self._name

    @property
    def loader_path(self) -> Optional[str]:
        return self._loader_path

    @property
    def initrd_path(self) -> Optional[str]:
        return self._initrd_path

    @property
    def graphics(self) -> Optional[bool]:
        return self._graphics

    @property
    def boot_options(self) -> Optional[BootOptions]:
        return self._boot_options

    @property
    def add_boot_options(self) -> BootOptions:
        return self._add_boot_options

    @property
    def is_disabled(self) -> bool:
        return self._is_disabled
