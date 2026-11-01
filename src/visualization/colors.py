"""
MAZESolver — Color Constants
=============================
All colors used by the Pygame renderer and HUD.
See docs/ui/UI_DESIGN.md for the full color palette rationale.
"""

# Window background
BG_COLOR       = (30,  30,  30)

# Cell types
WALL_COLOR     = (44,  44,  44)   # '#' cells
OPEN_COLOR     = (240, 240, 240)  # ' ' cells (unvisited)
START_COLOR    = (0,   200,  83)  # 'S' cell
GOAL_COLOR     = (213,  0,   0)   # 'G' cell

# Algorithm animation
VISITED_COLOR  = (129, 212, 250)  # Explored nodes (blue)
PATH_COLOR     = (255, 214,   0)  # Final solution path (yellow)
FRONTIER_COLOR = (255, 109,   0)  # Current frontier head (orange)

# HUD panel
HUD_BG        = (20,  20,  20)
HUD_TEXT      = (220, 220, 220)
HUD_ACCENT    = (100, 181, 246)
HUD_DIVIDER   = (60,  60,  60)
HUD_SUCCESS   = (0,   200,  83)
HUD_FAIL      = (213,  0,   0)
HUD_SEARCHING = (255, 214,   0)

# Grid lines
BORDER_COLOR  = (80,  80,  80)

# HUD dimensions
HUD_WIDTH     = 250
