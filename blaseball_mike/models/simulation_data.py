from dateutil.parser import parse

from .base import Base
from .league import League
from .. import database, chronicler


class SimulationData(Base):
    """
    Represents the current simulation state.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load()
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls):
        """Returns the current simulation state"""
        return cls(database.get_simulation_data())

    @classmethod
    def load_at_time(cls, time):
        """Returns the simulation state at a given time"""
        if isinstance(time, str):
            time = parse(time)

        updates = chronicler.get_sim_updates(before=time, order="desc", count=1)
        if len(updates) == 0:
            return None
        return cls(dict(updates[0]["data"], timestamp=time))

    @Base.lazy_load("_league_id", cache_name="_league")
    def league(self):
        return League.load_by_id(self._league_id)

    @Base.lazy_load("_next_election_end")
    def next_election_end(self):
        return parse(self._next_election_end)

    @Base.lazy_load("_next_phase_time")
    def next_phase_time(self):
        return parse(self._next_phase_time)

    @Base.lazy_load("_next_season_start")
    def next_season_start(self):
        return parse(self._next_season_start)

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1
