from __future__ import annotations

import dataclasses
import platform
from pathlib import Path
from typing import TYPE_CHECKING

from randovania.game.game_enum import RandovaniaGame
from randovania.games.prime_origins.exporter.game_exporter import MPOGameExportParams
from randovania.games.prime_origins.exporter.options import MPOPerGameOptions
from randovania.games.prime_origins.layout import MPOConfiguration
from randovania.gui.dialog.game_export_dialog import GameExportDialog, spoiler_path_for

if TYPE_CHECKING:
    from randovania.interface_common.options import PerGameOptions


def _is_valid_input_dir(path: Path) -> bool:
    # Checks whether data file and runner exist.
    current_platform = platform.system()
    if current_platform == "Windows":
        return path.joinpath("data.win").exists() and path.joinpath("MetroidPrimeOrigins.exe").exists()
    if current_platform == "Linux":
        # AppImage
        return (
            path.joinpath("MetroidPrimeOrigins.AppImage").exists()
            # Flatpak/non-packed
            or (path.joinpath("assets", "game.unx").exists() and path.joinpath("runner").exists())
        )
    if current_platform == "Darwin":
        return (
            path.joinpath("MetroidPrimeOrigins.app", "Contents", "Resources", "game.ios").exists()
            and path.joinpath("MetroidPrimeOrigins.app", "Contents", "MacOS", "Mac_Runner").exists()
        )

    return False


class MPOGameExportDialog(GameExportDialog[MPOConfiguration]):
    """A window for asking the user for what is needed to export this specific game.

    The provided implementation assumes you need an ISO/ROM file, and produces a new ISO/ROM file."""

    @classmethod
    def game_enum(cls) -> RandovaniaGame:
        return RandovaniaGame.PRIME_ORIGINS

    @property
    def input_file(self) -> Path:
        return Path(self.input_file_edit.text())

    @property
    def output_file(self) -> Path:
        raise NotImplementedError("This method hasn't been implemented yet")

    @property
    def auto_save_spoiler(self) -> bool:
        raise NotImplementedError("This method hasn't been implemented yet")

    def update_per_game_options(self, per_game: PerGameOptions) -> MPOPerGameOptions:
        assert isinstance(per_game, MPOPerGameOptions)
        return dataclasses.replace(
            per_game,
            input_path=self.input_file,
            output_path=self.output_file,
        )

    def get_game_export_params(self) -> MPOGameExportParams:
        """Creates the GameExportParams for this specific game,
        based on the data provided by the user in this window."""

        spoiler_output = spoiler_path_for(self.auto_save_spoiler, self.output_file)

        return MPOGameExportParams(
            spoiler_output=spoiler_output,
            input_path=self.input_file,
            output_path=self.output_file,
        )
