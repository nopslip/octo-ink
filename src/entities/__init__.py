"""Entities package for the Entity-Component System."""

from src.entities.entity import Entity
from src.entities.entity_manager import EntityManager
from src.entities.entity_factory import EntityFactory
from src.entities.player import Player
from src.entities.ship import Ship
from src.entities.captain import Captain
from src.entities.turtle import Turtle
from src.entities.fish import Fish
from src.entities.ink_slime import InkSlime

__all__ = [
    'Entity',
    'EntityManager',
    'EntityFactory',
    'Player',
    'Ship',
    'Captain',
    'Turtle',
    'Fish',
    'InkSlime'
]