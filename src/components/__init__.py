"""Components package for the Entity-Component System."""

from src.components.component import Component
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.input_component import InputComponent
from src.components.ai_component import AIComponent
from src.components.health_component import HealthComponent
from src.components.weapon_component import WeaponComponent
from src.components.animation_component import AnimationComponent
from src.components.collision_component import CollisionComponent
from src.components.ink_slime_component import InkSlimeComponent
from src.components.ship_ink_load_component import ShipInkLoadComponent
from src.components.captain_component import CaptainComponent
from src.components.shield_component import ShieldComponent

__all__ = [
    'Component',
    'TransformComponent',
    'RenderComponent',
    'PhysicsComponent',
    'InputComponent',
    'AIComponent',
    'HealthComponent',
    'WeaponComponent',
    'AnimationComponent',
    'CollisionComponent',
    'InkSlimeComponent',
    'ShipInkLoadComponent',
    'CaptainComponent',
    'ShieldComponent',
]