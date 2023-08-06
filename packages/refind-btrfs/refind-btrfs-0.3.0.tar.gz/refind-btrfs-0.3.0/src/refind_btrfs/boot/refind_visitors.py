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

from collections import defaultdict
from itertools import chain
from typing import Any, Callable, Dict, Generator, NamedTuple, Tuple

from antlr4 import ParserRuleContext
from more_itertools import always_iterable, only

from refind_btrfs.common import constants
from refind_btrfs.common.enums import GraphicsParameter, OSTypeParameter, RefindOption
from refind_btrfs.common.exceptions import RefindConfigError

from .antlr4 import RefindConfigParser, RefindConfigParserVisitor
from .boot_options import BootOptions
from .boot_stanza import BootStanza
from .sub_menu import SubMenu


class BootStanzaVisitor(RefindConfigParserVisitor):
    def visitBoot_stanza(
        self, ctx: RefindConfigParser.Boot_stanzaContext
    ) -> BootStanza:
        menu_entry_context = ctx.menu_entry()
        menu_entry = menu_entry_context.accept(MenuEntryVisitor())
        main_option_contexts = ctx.main_option()
        option_visitor = OptionVisitor()
        main_options = defaultdict(list)

        for key, value in chain.from_iterable(
            context.accept(option_visitor) for context in main_option_contexts
        ):
            main_options[key].append(value)

        volume = only(always_iterable(main_options.get(RefindOption.VOLUME)))
        loader = only(always_iterable(main_options.get(RefindOption.LOADER)))
        initrd = only(always_iterable(main_options.get(RefindOption.INITRD)))
        icon = only(always_iterable(main_options.get(RefindOption.ICON)))
        os_type = only(always_iterable(main_options.get(RefindOption.OS_TYPE)))
        graphics = only(always_iterable(main_options.get(RefindOption.GRAPHICS)))
        boot_options = only(
            always_iterable(main_options.get(RefindOption.BOOT_OPTIONS))
        )
        disabled = only(
            always_iterable(main_options.get(RefindOption.DISABLED)), default=False
        )
        sub_menus = always_iterable(main_options.get(RefindOption.SUB_MENU_ENTRY))

        return BootStanza(
            menu_entry,
            volume,
            loader,
            initrd,
            icon,
            os_type,
            graphics,
            BootOptions(boot_options),
            disabled,
        ).with_sub_menus(sub_menus)


class MenuEntryVisitor(RefindConfigParserVisitor):
    def visitMenu_entry(self, ctx: RefindConfigParser.Menu_entryContext) -> str:
        token = ctx.STRING()

        return token.getText()


class OptionVisitor(RefindConfigParserVisitor):
    class ContextWithVisitor(NamedTuple):
        child_context: Callable[[ParserRuleContext], ParserRuleContext]
        visitor: Callable[[], RefindConfigParser]

    def __init__(self) -> None:
        self._main_option_mappings = {
            RefindOption.VOLUME: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.volume, VolumeVisitor
            ),
            RefindOption.LOADER: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.loader, LoaderVisitor
            ),
            RefindOption.INITRD: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.main_initrd, InitrdVisitor
            ),
            RefindOption.ICON: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.icon, IconVisitor
            ),
            RefindOption.OS_TYPE: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.os_type, OsTypeVisitor
            ),
            RefindOption.GRAPHICS: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.graphics, GraphicsVisitor
            ),
            RefindOption.BOOT_OPTIONS: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.main_boot_options,
                BootOptionsVisitor,
            ),
            RefindOption.DISABLED: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.disabled, DisabledVisitor
            ),
            RefindOption.SUB_MENU_ENTRY: self.ContextWithVisitor(
                RefindConfigParser.Main_optionContext.sub_menu, SubMenuVisitor
            ),
        }
        self._sub_option_mappings = {
            RefindOption.LOADER: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.loader, LoaderVisitor
            ),
            RefindOption.INITRD: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.sub_initrd, InitrdVisitor
            ),
            RefindOption.GRAPHICS: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.graphics, GraphicsVisitor
            ),
            RefindOption.BOOT_OPTIONS: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.sub_boot_options,
                BootOptionsVisitor,
            ),
            RefindOption.ADD_BOOT_OPTIONS: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.add_boot_options,
                BootOptionsVisitor,
            ),
            RefindOption.DISABLED: self.ContextWithVisitor(
                RefindConfigParser.Sub_optionContext.disabled, DisabledVisitor
            ),
        }

    def visitMain_option(
        self, ctx: RefindConfigParser.Main_optionContext
    ) -> Generator[Tuple[int, Any], None, None]:
        yield from OptionVisitor._map_to_option(ctx, self._main_option_mappings)

    def visitSub_option(
        self, ctx: RefindConfigParser.Sub_optionContext
    ) -> Generator[Tuple[int, Any], None, None]:
        yield from OptionVisitor._map_to_option(ctx, self._sub_option_mappings)

    @staticmethod
    def _map_to_option(
        ctx: ParserRuleContext, mappings: Dict[RefindOption, ContextWithVisitor]
    ) -> Generator[Tuple[RefindOption, Any], None, None]:
        for key, value in mappings.items():
            option_context = value.child_context(ctx)

            if option_context is not None:
                visitor = value.visitor()

                yield key, option_context.accept(visitor)
                return


class SubMenuVisitor(RefindConfigParserVisitor):
    def visitSub_menu(self, ctx: RefindConfigParser.Sub_menuContext) -> SubMenu:
        menu_entry_context = ctx.menu_entry()
        menu_entry = menu_entry_context.accept(MenuEntryVisitor())
        sub_option_contexts = ctx.sub_option()
        option_visitor = OptionVisitor()
        sub_options = defaultdict(list)

        for key, value in chain.from_iterable(
            context.accept(option_visitor) for context in sub_option_contexts
        ):
            sub_options[key].append(value)

        loader = only(always_iterable(sub_options.get(RefindOption.LOADER)))
        initrd = only(always_iterable(sub_options.get(RefindOption.INITRD)))
        graphics = only(always_iterable(sub_options.get(RefindOption.GRAPHICS)))
        boot_options = only(always_iterable(sub_options.get(RefindOption.BOOT_OPTIONS)))
        add_boot_options = only(
            always_iterable(sub_options.get(RefindOption.ADD_BOOT_OPTIONS))
        )
        disabled = only(
            always_iterable(sub_options.get(RefindOption.DISABLED)), default=False
        )

        return SubMenu(
            menu_entry,
            loader,
            initrd,
            graphics,
            BootOptions(boot_options) if boot_options is not None else None,
            BootOptions(add_boot_options),
            disabled,
        )


class VolumeVisitor(RefindConfigParserVisitor):
    def visitVolume(self, ctx: RefindConfigParser.VolumeContext) -> str:
        if ctx is not None:
            token = ctx.STRING()

            return token.getText()

        return None


class LoaderVisitor(RefindConfigParserVisitor):
    def visitLoader(self, ctx: RefindConfigParser.LoaderContext) -> str:
        token = ctx.STRING()

        return token.getText()


class InitrdVisitor(RefindConfigParserVisitor):
    def visitMain_initrd(self, ctx: RefindConfigParser.Main_initrdContext) -> str:
        token = ctx.STRING()

        return token.getText()

    def visitSub_initrd(self, ctx: RefindConfigParser.Sub_initrdContext) -> str:
        token = ctx.STRING()

        if token is not None:
            return token.getText()

        return constants.EMPTY_STR


class IconVisitor(RefindConfigParserVisitor):
    def visitIcon(self, ctx: RefindConfigParser.IconContext) -> str:
        token = ctx.STRING()

        return token.getText()


class OsTypeVisitor(RefindConfigParserVisitor):
    def visitOs_type(self, ctx: RefindConfigParser.Os_typeContext) -> str:
        token = ctx.OS_TYPE_PARAMETER()
        text = token.getText()
        os_type_options = [option.value for option in OSTypeParameter]

        if text not in os_type_options:
            raise RefindConfigError(f"Unexpected 'os_type' option - '{text}'!")

        return text


class GraphicsVisitor(RefindConfigParserVisitor):
    def visitGraphics(self, ctx: RefindConfigParser.GraphicsContext) -> bool:
        token = ctx.GRAPHICS_PARAMETER()
        text = token.getText()

        if text == GraphicsParameter.ON.value:
            return True

        if text == GraphicsParameter.OFF.value:
            return False

        raise RefindConfigError(f"Unexpected 'graphics' option - '{text}'!")


class BootOptionsVisitor(RefindConfigParserVisitor):
    def visitMain_boot_options(
        self, ctx: RefindConfigParser.Main_boot_optionsContext
    ) -> str:
        token = ctx.STRING()

        return token.getText()

    def visitSub_boot_options(
        self, ctx: RefindConfigParser.Sub_boot_optionsContext
    ) -> str:
        token = ctx.STRING()

        if token is not None:
            return token.getText()

        return constants.EMPTY_STR

    def visitAdd_boot_options(
        self, ctx: RefindConfigParser.Add_boot_optionsContext
    ) -> str:
        token = ctx.STRING()

        return token.getText()


class DisabledVisitor(RefindConfigParserVisitor):
    def visitDisabled(self, ctx: RefindConfigParser.DisabledContext) -> bool:
        return True


class IncludeVisitor(RefindConfigParserVisitor):
    def visitInclude(self, ctx: RefindConfigParser.IncludeContext) -> str:
        token = ctx.STRING()

        return token.getText()
