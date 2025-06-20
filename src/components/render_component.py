"""Render Component for rendering entities on screen."""

import pygame
from typing import Optional, Tuple, Dict, Any
from src.components.component import Component


class RenderComponent(Component):
    """Component that handles rendering an entity on screen.
    
    The RenderComponent manages the visual representation of an entity,
    including sprites, colors, and rendering properties.
    """
    
    def __init__(self, sprite_name: Optional[str] = None):
        """Initialize the RenderComponent.
        
        Args:
            sprite_name: Name/key of the sprite asset to use
        """
        super().__init__("render")
        
        # Sprite/image properties
        self.sprite_name: Optional[str] = sprite_name
        self.sprite: Optional[pygame.Surface] = None
        self.original_sprite: Optional[pygame.Surface] = None  # For caching unmodified sprite
        
        # Color and transparency
        self.color: Tuple[int, int, int] = (255, 255, 255)  # White (no tint)
        self.alpha: int = 255  # Fully opaque
        
        # Shape-based rendering (when no sprite available)
        self.shape: str = "rect"  # "rect", "circle", "ellipse"
        self.size: Tuple[int, int] = (32, 32)  # Width, height for shapes
        
        # Rendering properties
        self.visible: bool = True
        self.layer: int = 0  # Rendering layer (higher = on top)
        
        # Sprite offset from entity position
        self.offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        
        # Flip flags
        self.flip_x: bool = False
        self.flip_y: bool = False
        
        # Blend mode
        self.blend_mode: int = 0  # pygame.BLEND_NORMAL
        
        # Debug rendering
        self.debug_draw: bool = False
        self.debug_color: Tuple[int, int, int] = (255, 0, 255)  # Magenta
        
    def update(self, dt: float) -> None:
        """Update the render component.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # RenderComponent typically doesn't need per-frame updates
        # Animation would be handled by AnimationComponent
        pass
        
    def on_add(self) -> None:
        """Called when the component is added to an entity."""
        # Load sprite if sprite_name is set
        if self.sprite_name and not self.sprite:
            self.load_sprite(self.sprite_name)
            
    def load_sprite(self, sprite_name: str) -> None:
        """Load a sprite from the asset manager.
        
        Args:
            sprite_name: Name/key of the sprite to load
        """
        # This would normally load from AssetManager
        # For now, we'll create a placeholder
        self.sprite_name = sprite_name
        # TODO: Load actual sprite from AssetManager when available
        # self.sprite = asset_manager.get_sprite(sprite_name)
        
    def render(self, surface: pygame.Surface) -> None:
        """Render the entity on the given surface.
        
        Args:
            surface: The pygame Surface to render to
        """
        if not self.visible or not self.entity:
            return
            
        # Get transform component for position
        transform = self.entity.get_component("transform")
        if not transform:
            return
            
        position = transform.get_world_position()
        
        # Apply offset
        render_pos = position + self.offset
        
        # Render sprite if available
        if self.sprite:
            sprite_to_render = self._prepare_sprite(transform)
            
            # Calculate sprite rect centered on position
            sprite_rect = sprite_to_render.get_rect()
            sprite_rect.center = (int(render_pos.x), int(render_pos.y))
            
            # Apply blend mode and render
            if self.blend_mode != 0:
                surface.blit(sprite_to_render, sprite_rect, special_flags=self.blend_mode)
            else:
                surface.blit(sprite_to_render, sprite_rect)
        else:
            # If no sprite, render a colored rectangle as placeholder
            self._render_placeholder(surface, render_pos, transform)
            
        # Debug rendering
        if self.debug_draw:
            self._render_debug(surface, position, transform)
            
    def _prepare_sprite(self, transform) -> pygame.Surface:
        """Prepare the sprite for rendering with transformations applied.
        
        Args:
            transform: The entity's transform component
            
        Returns:
            The prepared sprite surface
        """
        sprite = self.sprite
        
        # Apply scale if needed
        scale = transform.get_world_scale()
        if scale.x != 1.0 or scale.y != 1.0:
            size = sprite.get_size()
            new_size = (int(size[0] * abs(scale.x)), int(size[1] * abs(scale.y)))
            sprite = pygame.transform.scale(sprite, new_size)
            
        # Apply rotation if needed
        rotation = transform.get_world_rotation()
        if rotation != 0:
            sprite = pygame.transform.rotate(sprite, -rotation)  # Negative for correct direction
            
        # Apply flips
        if self.flip_x or self.flip_y:
            sprite = pygame.transform.flip(sprite, self.flip_x, self.flip_y)
            
        # Apply color tint
        if self.color != (255, 255, 255):
            sprite = sprite.copy()
            color_surface = pygame.Surface(sprite.get_size())
            color_surface.fill(self.color)
            sprite.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            
        # Apply alpha
        if self.alpha < 255:
            sprite = sprite.copy()
            sprite.set_alpha(self.alpha)
            
        return sprite
        
    def _render_placeholder(self, surface: pygame.Surface, position: pygame.math.Vector2,
                          transform) -> None:
        """Render a placeholder shape when no sprite is available.
        
        Args:
            surface: The surface to render to
            position: The render position
            transform: The entity's transform component
        """
        # Use configured size
        size = pygame.math.Vector2(self.size[0], self.size[1])
        
        # Apply scale
        scale = transform.get_world_scale()
        size.x *= scale.x
        size.y *= scale.y
        
        # Render based on shape type
        if self.shape == "circle":
            # Draw filled circle
            radius = int(min(size.x, size.y) / 2)
            pygame.draw.circle(surface, self.color,
                             (int(position.x), int(position.y)), radius)
            # Draw border
            pygame.draw.circle(surface, (0, 0, 0),
                             (int(position.x), int(position.y)), radius, 2)
                             
        elif self.shape == "ellipse":
            # Create rect for ellipse
            rect = pygame.Rect(
                position.x - size.x / 2,
                position.y - size.y / 2,
                size.x,
                size.y
            )
            # Draw filled ellipse
            pygame.draw.ellipse(surface, self.color, rect)
            # Draw border
            pygame.draw.ellipse(surface, (0, 0, 0), rect, 2)
            
        else:  # Default to rectangle
            # Create rect
            rect = pygame.Rect(
                position.x - size.x / 2,
                position.y - size.y / 2,
                size.x,
                size.y
            )
            # Draw filled rectangle with entity color
            pygame.draw.rect(surface, self.color, rect)
            # Draw border
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        
    def _render_debug(self, surface: pygame.Surface, position: pygame.math.Vector2, 
                     transform) -> None:
        """Render debug information.
        
        Args:
            surface: The surface to render to
            position: The entity position
            transform: The entity's transform component
        """
        # Draw position marker
        pygame.draw.circle(surface, self.debug_color, 
                         (int(position.x), int(position.y)), 3)
        
        # Draw forward direction
        forward = transform.get_forward_vector() * 20
        end_pos = position + forward
        pygame.draw.line(surface, self.debug_color,
                        (int(position.x), int(position.y)),
                        (int(end_pos.x), int(end_pos.y)), 2)
        
        # Draw collision bounds if available
        collision = self.entity.get_component("collision")
        if collision:
            rect = pygame.Rect(
                position.x - collision.width / 2,
                position.y - collision.height / 2,
                collision.width,
                collision.height
            )
            pygame.draw.rect(surface, self.debug_color, rect, 1)
            
    def set_color(self, r: int, g: int, b: int) -> None:
        """Set the color tint for the sprite.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        self.color = (
            max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b))
        )
        
    def set_alpha(self, alpha: int) -> None:
        """Set the transparency of the sprite.
        
        Args:
            alpha: Alpha value (0=transparent, 255=opaque)
        """
        self.alpha = max(0, min(255, alpha))
        
    def fade_in(self, duration: float) -> None:
        """Start a fade-in effect.
        
        Args:
            duration: Duration of the fade in seconds
        """
        # This would typically be handled by an animation system
        # For now, just set to visible
        self.alpha = 0
        self.visible = True
        # TODO: Implement with animation system
        
    def fade_out(self, duration: float) -> None:
        """Start a fade-out effect.
        
        Args:
            duration: Duration of the fade in seconds
        """
        # This would typically be handled by an animation system
        # TODO: Implement with animation system
        pass
        
    def flash(self, color: Tuple[int, int, int], duration: float) -> None:
        """Flash the sprite with a color.
        
        Args:
            color: The color to flash
            duration: Duration of the flash in seconds
        """
        # This would typically be handled by an animation system
        # TODO: Implement with animation system
        pass
        
    def __repr__(self) -> str:
        """String representation of the render component.
        
        Returns:
            A string describing the component's state
        """
        return (f"RenderComponent(sprite='{self.sprite_name}', "
                f"visible={self.visible}, layer={self.layer})")