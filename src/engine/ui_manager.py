"""
UI Manager for the Octopus Ink Slime game.
Handles creation and management of UI elements like buttons, labels, and progress bars.
"""

import pygame
import pygame.freetype
from typing import Dict, List, Tuple, Callable, Optional, Union
from enum import Enum
from src.utils.constants import WHITE, BLACK


class UIElementType(Enum):
    """Types of UI elements supported by the UI Manager."""
    BUTTON = 1
    LABEL = 2
    PROGRESS_BAR = 3
    PANEL = 4
    IMAGE = 5


class UIElement:
    """Base class for all UI elements."""
    
    def __init__(self, rect: pygame.Rect, element_id: str):
        """
        Initialize a UI element.
        
        Args:
            rect: The position and size of the element
            element_id: Unique identifier for the element
        """
        self.rect = rect
        self.element_id = element_id
        self.visible = True
        self.enabled = True
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        """
        Add a child UI element.
        
        Args:
            child: The child UI element to add
        """
        self.children.append(child)
        child.parent = self
    
    def get_absolute_rect(self) -> pygame.Rect:
        """
        Get the absolute rectangle of this element, accounting for parent position.
        
        Returns:
            Absolute rectangle in screen coordinates
        """
        if self.parent:
            parent_rect = self.parent.get_absolute_rect()
            return pygame.Rect(
                parent_rect.x + self.rect.x,
                parent_rect.y + self.rect.y,
                self.rect.width,
                self.rect.height
            )
        return self.rect
    
    def update(self, dt: float):
        """
        Update the UI element.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update children
        for child in self.children:
            if child.visible:
                child.update(dt)
    
    def render(self, surface: pygame.Surface):
        """
        Render the UI element.
        
        Args:
            surface: Pygame surface to render to
        """
        # Render children
        for child in self.children:
            if child.visible:
                child.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle a pygame event.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Handle children events first (in reverse order for proper layering)
        for child in reversed(self.children):
            if child.visible and child.enabled:
                if child.handle_event(event):
                    return True
        
        return False


class Button(UIElement):
    """Interactive button UI element."""
    
    def __init__(self, rect: pygame.Rect, element_id: str, text: str, 
                 callback: Callable, 
                 bg_color: Tuple[int, int, int] = (100, 100, 200),
                 hover_color: Tuple[int, int, int] = (150, 150, 255),
                 text_color: Tuple[int, int, int] = WHITE,
                 font_size: int = 24):
        """
        Initialize a button.
        
        Args:
            rect: The position and size of the button
            element_id: Unique identifier for the button
            text: Text to display on the button
            callback: Function to call when the button is clicked
            bg_color: Background color of the button
            hover_color: Background color when mouse is hovering over the button
            text_color: Color of the button text
            font_size: Size of the button text
        """
        super().__init__(rect, element_id)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.hovered = False
        self.pressed = False
        
        # Initialize font
        self.font = pygame.font.Font(None, font_size)
    
    def update(self, dt: float):
        """
        Update the button state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        super().update(dt)
        
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.get_absolute_rect().collidepoint(mouse_pos)
    
    def render(self, surface: pygame.Surface):
        """
        Render the button.
        
        Args:
            surface: Pygame surface to render to
        """
        abs_rect = self.get_absolute_rect()
        
        # Draw button background
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, abs_rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, abs_rect, width=2, border_radius=5)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=abs_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Render children
        super().render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the button.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Check if children handled the event
        if super().handle_event(event):
            return True
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.pressed = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.hovered:
                self.callback()
                self.pressed = False
                return True
            self.pressed = False
            
        return False


class Label(UIElement):
    """Text label UI element."""
    
    def __init__(self, rect: pygame.Rect, element_id: str, text: str,
                 text_color: Tuple[int, int, int] = WHITE,
                 font_size: int = 24,
                 align: str = "center"):
        """
        Initialize a label.
        
        Args:
            rect: The position and size of the label
            element_id: Unique identifier for the label
            text: Text to display
            text_color: Color of the text
            font_size: Size of the text
            align: Text alignment ("left", "center", or "right")
        """
        super().__init__(rect, element_id)
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.align = align
        
        # Initialize font
        self.font = pygame.font.Font(None, font_size)
    
    def render(self, surface: pygame.Surface):
        """
        Render the label.
        
        Args:
            surface: Pygame surface to render to
        """
        abs_rect = self.get_absolute_rect()
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        
        # Position text based on alignment
        if self.align == "left":
            text_rect = text_surface.get_rect(midleft=(abs_rect.left, abs_rect.centery))
        elif self.align == "right":
            text_rect = text_surface.get_rect(midright=(abs_rect.right, abs_rect.centery))
        else:  # center
            text_rect = text_surface.get_rect(center=abs_rect.center)
        
        surface.blit(text_surface, text_rect)
        
        # Render children
        super().render(surface)


class ProgressBar(UIElement):
    """Progress bar UI element."""
    
    def __init__(self, rect: pygame.Rect, element_id: str,
                 value: float = 0.0,
                 min_value: float = 0.0,
                 max_value: float = 1.0,
                 bg_color: Tuple[int, int, int] = (50, 50, 50),
                 fill_color: Tuple[int, int, int] = (0, 200, 0),
                 border_color: Tuple[int, int, int] = BLACK,
                 show_text: bool = False,
                 text_color: Tuple[int, int, int] = WHITE,
                 font_size: int = 18):
        """
        Initialize a progress bar.
        
        Args:
            rect: The position and size of the progress bar
            element_id: Unique identifier for the progress bar
            value: Initial value of the progress bar
            min_value: Minimum value of the progress bar
            max_value: Maximum value of the progress bar
            bg_color: Background color
            fill_color: Fill color for the progress indicator
            border_color: Border color
            show_text: Whether to show the value as text
            text_color: Color of the text
            font_size: Size of the text
        """
        super().__init__(rect, element_id)
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        self.show_text = show_text
        self.text_color = text_color
        
        # Initialize font if showing text
        if show_text:
            self.font = pygame.font.Font(None, font_size)
    
    def set_value(self, value: float):
        """
        Set the current value of the progress bar.
        
        Args:
            value: New value
        """
        self.value = max(self.min_value, min(value, self.max_value))
    
    def get_percentage(self) -> float:
        """
        Get the current value as a percentage.
        
        Returns:
            Value as a percentage (0-100)
        """
        range_size = self.max_value - self.min_value
        if range_size <= 0:
            return 0
        return ((self.value - self.min_value) / range_size) * 100
    
    def render(self, surface: pygame.Surface):
        """
        Render the progress bar.
        
        Args:
            surface: Pygame surface to render to
        """
        abs_rect = self.get_absolute_rect()
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, abs_rect, border_radius=3)
        
        # Calculate fill width
        fill_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * abs_rect.width)
        fill_rect = pygame.Rect(abs_rect.x, abs_rect.y, fill_width, abs_rect.height)
        
        # Draw fill
        if fill_width > 0:
            pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=3)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, abs_rect, width=1, border_radius=3)
        
        # Draw text if enabled
        if self.show_text:
            text = f"{self.get_percentage():.1f}%"
            text_surface = self.font.render(text, True, self.text_color)
            text_rect = text_surface.get_rect(center=abs_rect.center)
            surface.blit(text_surface, text_rect)
        
        # Render children
        super().render(surface)


class Panel(UIElement):
    """Container panel for grouping UI elements."""
    
    def __init__(self, rect: pygame.Rect, element_id: str,
                 bg_color: Optional[Tuple[int, int, int]] = None,
                 border_color: Optional[Tuple[int, int, int]] = None,
                 border_width: int = 0,
                 border_radius: int = 0):
        """
        Initialize a panel.
        
        Args:
            rect: The position and size of the panel
            element_id: Unique identifier for the panel
            bg_color: Background color (None for transparent)
            border_color: Border color (None for no border)
            border_width: Border width in pixels
            border_radius: Border radius for rounded corners
        """
        super().__init__(rect, element_id)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
    
    def render(self, surface: pygame.Surface):
        """
        Render the panel.
        
        Args:
            surface: Pygame surface to render to
        """
        abs_rect = self.get_absolute_rect()
        
        # Draw background if specified
        if self.bg_color:
            pygame.draw.rect(surface, self.bg_color, abs_rect, 
                             border_radius=self.border_radius)
        
        # Draw border if specified
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, abs_rect, 
                             width=self.border_width, border_radius=self.border_radius)
        
        # Render children
        super().render(surface)


class Image(UIElement):
    """Image UI element."""
    
    def __init__(self, rect: pygame.Rect, element_id: str, 
                 image: Union[pygame.Surface, str],
                 scale_mode: str = "fit"):
        """
        Initialize an image element.
        
        Args:
            rect: The position and size of the image
            element_id: Unique identifier for the image
            image: Either a pygame Surface or a path to an image file
            scale_mode: How to scale the image ("fit", "fill", "stretch", or "none")
        """
        super().__init__(rect, element_id)
        
        # Load image if string path is provided
        if isinstance(image, str):
            self.original_image = pygame.image.load(image).convert_alpha()
        else:
            self.original_image = image
            
        self.scale_mode = scale_mode
        self.scaled_image = self._scale_image()
    
    def _scale_image(self) -> pygame.Surface:
        """
        Scale the image according to the scale mode.
        
        Returns:
            Scaled image surface
        """
        if self.scale_mode == "none":
            return self.original_image
            
        orig_width, orig_height = self.original_image.get_size()
        target_width, target_height = self.rect.size
        
        if self.scale_mode == "stretch":
            return pygame.transform.scale(self.original_image, (target_width, target_height))
            
        # Calculate aspect ratios
        orig_aspect = orig_width / orig_height
        target_aspect = target_width / target_height
        
        if self.scale_mode == "fit":
            # Scale to fit within the rect while maintaining aspect ratio
            if orig_aspect > target_aspect:
                # Image is wider than target
                new_width = target_width
                new_height = int(new_width / orig_aspect)
            else:
                # Image is taller than target
                new_height = target_height
                new_width = int(new_height * orig_aspect)
                
        else:  # "fill"
            # Scale to fill the rect while maintaining aspect ratio
            if orig_aspect > target_aspect:
                # Image is wider than target
                new_height = target_height
                new_width = int(new_height * orig_aspect)
            else:
                # Image is taller than target
                new_width = target_width
                new_height = int(new_width / orig_aspect)
        
        return pygame.transform.scale(self.original_image, (new_width, new_height))
    
    def set_image(self, image: Union[pygame.Surface, str]):
        """
        Set a new image.
        
        Args:
            image: Either a pygame Surface or a path to an image file
        """
        if isinstance(image, str):
            self.original_image = pygame.image.load(image).convert_alpha()
        else:
            self.original_image = image
            
        self.scaled_image = self._scale_image()
    
    def render(self, surface: pygame.Surface):
        """
        Render the image.
        
        Args:
            surface: Pygame surface to render to
        """
        abs_rect = self.get_absolute_rect()
        
        # Calculate position to center the image in the rect
        image_rect = self.scaled_image.get_rect()
        image_rect.center = abs_rect.center
        
        # Draw image
        surface.blit(self.scaled_image, image_rect)
        
        # Render children
        super().render(surface)


class UIManager:
    """Manages UI elements and layouts."""
    
    def __init__(self, screen_size: Tuple[int, int]):
        """
        Initialize the UI manager.
        
        Args:
            screen_size: The size of the screen (width, height)
        """
        self.screen_size = screen_size
        self.elements: Dict[str, UIElement] = {}
        self.root_elements: List[UIElement] = []
        self.focused_element = None
        
        # Initialize default font
        pygame.font.init()
        self.default_font = pygame.font.Font(None, 24)
    
    def add_element(self, element: UIElement, parent_id: Optional[str] = None) -> str:
        """
        Add a UI element.
        
        Args:
            element: The UI element to add
            parent_id: ID of the parent element, or None for root elements
            
        Returns:
            The ID of the added element
        """
        self.elements[element.element_id] = element
        
        if parent_id:
            if parent_id not in self.elements:
                raise ValueError(f"Parent element with ID '{parent_id}' not found")
            
            parent = self.elements[parent_id]
            parent.add_child(element)
        else:
            self.root_elements.append(element)
            
        return element.element_id
    
    def remove_element(self, element_id: str):
        """
        Remove a UI element.
        
        Args:
            element_id: ID of the element to remove
        """
        if element_id not in self.elements:
            return
            
        element = self.elements[element_id]
        
        # Remove from parent's children
        if element.parent:
            element.parent.children.remove(element)
        else:
            if element in self.root_elements:
                self.root_elements.remove(element)
        
        # Remove from elements dictionary
        del self.elements[element_id]
    
    def get_element(self, element_id: str) -> Optional[UIElement]:
        """
        Get a UI element by ID.
        
        Args:
            element_id: ID of the element to get
            
        Returns:
            The UI element, or None if not found
        """
        return self.elements.get(element_id)
    
    def create_button(self, rect: pygame.Rect, element_id: str, text: str, 
                      callback: Callable, parent_id: Optional[str] = None, **kwargs) -> str:
        """
        Create and add a button.
        
        Args:
            rect: The position and size of the button
            element_id: Unique identifier for the button
            text: Text to display on the button
            callback: Function to call when the button is clicked
            parent_id: ID of the parent element, or None for root elements
            **kwargs: Additional arguments to pass to the Button constructor
            
        Returns:
            The ID of the created button
        """
        button = Button(rect, element_id, text, callback, **kwargs)
        return self.add_element(button, parent_id)
    
    def create_label(self, rect: pygame.Rect, element_id: str, text: str, 
                     parent_id: Optional[str] = None, **kwargs) -> str:
        """
        Create and add a label.
        
        Args:
            rect: The position and size of the label
            element_id: Unique identifier for the label
            text: Text to display
            parent_id: ID of the parent element, or None for root elements
            **kwargs: Additional arguments to pass to the Label constructor
            
        Returns:
            The ID of the created label
        """
        label = Label(rect, element_id, text, **kwargs)
        return self.add_element(label, parent_id)
    
    def create_progress_bar(self, rect: pygame.Rect, element_id: str, 
                           parent_id: Optional[str] = None, **kwargs) -> str:
        """
        Create and add a progress bar.
        
        Args:
            rect: The position and size of the progress bar
            element_id: Unique identifier for the progress bar
            parent_id: ID of the parent element, or None for root elements
            **kwargs: Additional arguments to pass to the ProgressBar constructor
            
        Returns:
            The ID of the created progress bar
        """
        progress_bar = ProgressBar(rect, element_id, **kwargs)
        return self.add_element(progress_bar, parent_id)
    
    def create_panel(self, rect: pygame.Rect, element_id: str, 
                    parent_id: Optional[str] = None, **kwargs) -> str:
        """
        Create and add a panel.
        
        Args:
            rect: The position and size of the panel
            element_id: Unique identifier for the panel
            parent_id: ID of the parent element, or None for root elements
            **kwargs: Additional arguments to pass to the Panel constructor
            
        Returns:
            The ID of the created panel
        """
        panel = Panel(rect, element_id, **kwargs)
        return self.add_element(panel, parent_id)
    
    def create_image(self, rect: pygame.Rect, element_id: str, image: Union[pygame.Surface, str],
                    parent_id: Optional[str] = None, **kwargs) -> str:
        """
        Create and add an image.
        
        Args:
            rect: The position and size of the image
            element_id: Unique identifier for the image
            image: Either a pygame Surface or a path to an image file
            parent_id: ID of the parent element, or None for root elements
            **kwargs: Additional arguments to pass to the Image constructor
            
        Returns:
            The ID of the created image
        """
        image_element = Image(rect, element_id, image, **kwargs)
        return self.add_element(image_element, parent_id)
    
    def update(self, dt: float):
        """
        Update all UI elements.
        
        Args:
            dt: Time delta in seconds since last update
        """
        for element in self.root_elements:
            if element.visible:
                element.update(dt)
    
    def render(self, surface: pygame.Surface):
        """
        Render all UI elements.
        
        Args:
            surface: Pygame surface to render to
        """
        for element in self.root_elements:
            if element.visible:
                element.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle a pygame event.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Handle events in reverse order (top to bottom)
        for element in reversed(self.root_elements):
            if element.visible and element.enabled:
                if element.handle_event(event):
                    return True
        
        return False
    
    def set_element_text(self, element_id: str, text: str) -> bool:
        """
        Set the text of a text-based UI element.
        
        Args:
            element_id: ID of the element
            text: New text
            
        Returns:
            True if successful, False otherwise
        """
        element = self.get_element(element_id)
        if not element:
            return False
            
        if hasattr(element, 'text'):
            element.text = text
            return True
            
        return False
    
    def set_progress_bar_value(self, element_id: str, value: float) -> bool:
        """
        Set the value of a progress bar.
        
        Args:
            element_id: ID of the progress bar
            value: New value
            
        Returns:
            True if successful, False otherwise
        """
        element = self.get_element(element_id)
        if not element or not isinstance(element, ProgressBar):
            return False
            
        element.set_value(value)
        return True
    
    def set_element_visible(self, element_id: str, visible: bool) -> bool:
        """
        Set the visibility of a UI element.
        
        Args:
            element_id: ID of the element
            visible: Whether the element should be visible
            
        Returns:
            True if successful, False otherwise
        """
        element = self.get_element(element_id)
        if not element:
            return False
            
        element.visible = visible
        return True
    
    def set_element_enabled(self, element_id: str, enabled: bool) -> bool:
        """
        Set whether a UI element is enabled.
        
        Args:
            element_id: ID of the element
            enabled: Whether the element should be enabled
            
        Returns:
            True if successful, False otherwise
        """
        element = self.get_element(element_id)
        if not element:
            return False
            
        element.enabled = enabled
        return True
        
    def clear_ui(self):
        """
        Clear all UI elements.
        This is useful when transitioning between states.
        """
        self.elements = {}
        self.root_elements = []
        self.focused_element = None