from random import Random

from randovania.game_description.game_description import GameDescription
from randovania.game_description.game_patches import GamePatches
from randovania.games.prime3.generator.item_pool.energy_cells import add_energy_cells
from randovania.games.prime3.layout.corruption_configuration import CorruptionConfiguration
from randovania.generator.pickup_pool import PoolResults
from randovania.layout.base.base_configuration import BaseConfiguration


def corruption_specific_pool(results: PoolResults, configuration: BaseConfiguration, game: GameDescription,
                             base_patches: GamePatches, rng: Random):
    assert isinstance(configuration, CorruptionConfiguration)
    # Adding Energy Cells to pool
    results.extend_with(add_energy_cells(game.resource_database))
