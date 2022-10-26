from __future__ import annotations

import hikari
import typing as t

if t.TYPE_CHECKING:
    from .abc import item


class EventManager:
    def __init__(self) -> None:
        self.reg: dict[str, item.ItemHandler] = {}
        self.item_handlers: dict[item.ItemHandler, list[str]] = {}

    def add(self, item_handler: item.ItemHandler, *custom_ids: str):
        for custom_id in custom_ids:
            if handler := self.reg.get(custom_id):
                handler.stop()
            self.reg[custom_id] = item_handler

        self.item_handlers[item_handler] = custom_ids

    def pop(self, item_handler: item.ItemHandler):
        for custom_id in self.item_handlers[item_handler]:
            self.reg.pop(custom_id, None)
        self.item_handlers.pop(item_handler)

    def get(self, custom_id)  -> item.ItemHandler | None:
        return self.reg.get(custom_id)

_events = EventManager()

async def on_inter(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, (hikari.ComponentInteraction, hikari.ModalInteraction)):
        return

    if not event.interaction.message:
        return

    item_handler = (
        _events.get(event.interaction.custom_id)
        or _events.get(event.interaction.message.id)
    )
    if not item_handler:
        return

    await item_handler._process_interactions(event)


# MIT License
#
# Copyright (c) 2022-present HyperGH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
