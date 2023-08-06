"""Provides the MapEditor class."""

from pathlib import Path
from typing import Optional

from ..hat_directions import DOWN, LEFT, RIGHT, UP
from ..pyglet import key
from .box import Box
from .box_level import BoxLevel


class MapEditor(BoxLevel):
    """A level which can be used for editing maps.

    When this level talks about a map, it talks about a collection of
    :class:`earwax.Box` instances.
    """

    filename: Optional[Path] = None
    map_name: str = 'Untitled Map'
    map_identifier: Optional[str] = None

    def __attrs_post_init__(self) -> None:
        """Add the initial box if there is none, and add extra actions."""
        if not self.boxes:
            self.add_box(
                Box(
                    self.game, self.coordinates.copy(), self.coordinates.copy()
                )
            )
        self.action(
            'Move forwards', symbol=key.W, hat_direction=UP
        )(self.move())
        self.action(
            'Turn around', symbol=key.S, hat_direction=DOWN
        )(self.turn(180))
        self.action(
            'Turn left', symbol=key.A, hat_direction=LEFT
        )(self.turn(-45))
        self.action(
            'Turn right', symbol=key.D, hat_direction=RIGHT
        )(self.turn(45))
        self.action(
            'Show coordinates', symbol=key.C, joystick_button=0
        )(self.show_coordinates())
        self.action(
            'Show facing direction', symbol=key.F, joystick_button=3
        )(self.show_facing())
        self.action(
            'Describe current box', symbol=key.X, joystick_button=2
        )(self.describe_current_box)
        self.action(
            'Show nearest door', symbol=key.Z, joystick_button=1
        )
        return super().__attrs_post_init__()
