from typing import Union
from pyomo.environ import ConcreteModel, Expression, NonNegativeReals, Set, units, Var
from pyomo.network import Port

import PySAM.MhkWave as MhkWave

from hopp.simulation.technologies.financial import FinancialModelType
from hopp.simulation.technologies.dispatch.power_sources.power_source_dispatch import (
    PowerSourceDispatch
)


class WaveDispatch(PowerSourceDispatch):
    wave_obj: Union[Expression, float]
    _system_model: MhkWave.MhkWave
    _financial_model: FinancialModelType
    """

    """
    def __init__(
        self,
        pyomo_model: ConcreteModel,
        indexed_set: Set,
        system_model: MhkWave.MhkWave,
        financial_model: FinancialModelType,
        block_set_name: str = 'wave',
    ):
        super().__init__(
            pyomo_model,
            indexed_set,
            system_model,
            financial_model,
            block_set_name=block_set_name,
        )

    def max_gross_profit_objective(self, hybrid_blocks):
        self.obj = Expression(
                expr=sum(
                    - (1/hybrid_blocks[t].time_weighting_factor)
                    * self.blocks[t].time_duration
                    * self.blocks[t].cost_per_generation
                    * hybrid_blocks[t].wave_generation
                    for t in hybrid_blocks.index_set()
                )
            )

    def min_operating_cost_objective(self, hybrid_blocks):
        self.obj = sum(
            hybrid_blocks[t].time_weighting_factor 
            * self.blocks[t].time_duration
            * self.blocks[t].cost_per_generation
            * hybrid_blocks[t].wave_generation
            for t in hybrid_blocks.index_set()
        )

    def _create_variables(self, hybrid):
        hybrid.wave_generation = Var(
            doc="Power generation of wind turbines [MW]",
            domain=NonNegativeReals,
            units=units.MW,
            initialize=0.0,
        )
        return hybrid.wave_generation, 0

    def _create_port(self, hybrid):
        hybrid.wave_port = Port(initialize={'generation': hybrid.wave_generation})
        return hybrid.wave_port
