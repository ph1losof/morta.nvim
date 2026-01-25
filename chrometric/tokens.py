"""
chrometric/tokens.py - Central Token Registry

Defines the complete set of 51 semantic tokens for comprehensive
colorscheme analysis. Organized by functional category.

Token Categories:
- Core Syntax (14 tokens): Basic programming constructs
- Diagnostics (4 tokens): Error/warning visibility (CRITICAL)
- Diff (3 tokens): Version control colors
- Git Signs (3 tokens): Gutter indicators
- UI Elements (16 tokens): Editor chrome
- Special Comments (3 tokens): TODO/FIXME markers
- Additional UI (8 tokens): Extended editor elements
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple


class TokenRegistry:
    """
    Central registry of all analyzable semantic tokens.

    Based on:
    - TreeSitter semantic tokens
    - LSP semantic highlighting
    - Neovim highlight groups
    - VSCode token types
    """

    # =========================================================================
    # Core Syntax Tokens (14)
    # =========================================================================
    SYNTAX_CORE: List[str] = [
        "keyword",      # Control flow, declarations
        "string",       # String literals
        "function",     # Function names
        "type",         # Type names, classes
        "variable",     # Variable identifiers
        "comment",      # Comments
        "constant",     # Constants, enums
        "operator",     # Operators (+, -, =, etc.)
        "number",       # Numeric literals
        "boolean",      # true/false
        "property",     # Object properties
        "parameter",    # Function parameters
        "namespace",    # Modules, packages
        "punctuation",  # Brackets, commas, semicolons
    ]

    # =========================================================================
    # Diagnostic Tokens (4) - CRITICAL for error visibility
    # =========================================================================
    DIAGNOSTICS: List[str] = [
        "error",        # Error markers (must be highly visible)
        "warning",      # Warning markers
        "info",         # Info markers
        "hint",         # Hint markers
    ]

    # =========================================================================
    # Diff Colors (3)
    # =========================================================================
    DIFF: List[str] = [
        "diff_add",     # Added lines
        "diff_delete",  # Deleted lines
        "diff_change",  # Changed lines
    ]

    # =========================================================================
    # Git Signs (3)
    # =========================================================================
    GIT: List[str] = [
        "git_add",      # Added line indicator
        "git_delete",   # Deleted line indicator
        "git_change",   # Modified line indicator
    ]

    # =========================================================================
    # UI Elements (16)
    # =========================================================================
    UI_ELEMENTS: List[str] = [
        "bg",           # Main background
        "fg",           # Main foreground
        "cursor_line",  # Current line highlight
        "cursor_column",  # Current column highlight
        "line_nr",      # Line numbers
        "line_nr_cur",  # Current line number
        "popup_bg",     # Popup/floating window background
        "popup_fg",     # Popup/floating window foreground
        "popup_sel",    # Popup selection
        "visual",       # Visual selection
        "search",       # Search highlight
        "inc_search",   # Incremental search
        "status_line",  # Status line
        "status_line_nc",  # Inactive status line
        "vert_split",   # Vertical split separator
        "fold",         # Folded lines
    ]

    # =========================================================================
    # Additional UI (8)
    # =========================================================================
    UI_ADDITIONAL: List[str] = [
        "sign_column",  # Sign column background
        "color_column", # Color column (80 char, etc.)
        "match_paren",  # Matching parentheses
        "pmenu",        # Popup menu
        "pmenu_sel",    # Popup menu selection
        "pmenu_sbar",   # Popup menu scrollbar
        "pmenu_thumb",  # Popup menu scrollbar thumb
        "tab_line",     # Tab line
    ]

    # =========================================================================
    # Special Comments (3)
    # =========================================================================
    SPECIAL_COMMENTS: List[str] = [
        "todo",         # TODO comments
        "fixme",        # FIXME comments
        "note",         # NOTE comments
    ]

    # =========================================================================
    # Combined Token Sets
    # =========================================================================
    @classmethod
    def all_tokens(cls) -> List[str]:
        """Get all 51 tokens as a flat list."""
        return (
            cls.SYNTAX_CORE +
            cls.DIAGNOSTICS +
            cls.DIFF +
            cls.GIT +
            cls.UI_ELEMENTS +
            cls.UI_ADDITIONAL +
            cls.SPECIAL_COMMENTS
        )

    @classmethod
    def count(cls) -> int:
        """Get total token count."""
        return len(cls.all_tokens())

    # =========================================================================
    # Functional Groups (for research-backed analysis)
    # =========================================================================
    # Based on eye-tracking studies (Busjahn et al., Hindle et al.)
    FUNCTIONAL_GROUPS: Dict[str, List[str]] = {
        # Control flow - peripheral attention (can be muted)
        "control": ["keyword", "operator"],

        # Data - high attention (must be clear)
        "data": ["string", "number", "boolean", "constant"],

        # Structure - very high attention (method signatures)
        "structure": ["function", "type", "namespace"],

        # Identifiers - HIGHEST attention (most reading time)
        "identifier": ["variable", "parameter", "property"],

        # Documentation - should recede visually
        "documentation": ["comment"],

        # Diagnostics - MUST stand out regardless of adjacency
        "diagnostic": ["error", "warning", "info", "hint"],

        # UI Chrome - should be unobtrusive
        "chrome": [
            "bg", "fg", "cursor_line", "line_nr", "status_line",
            "vert_split", "fold", "sign_column",
        ],
    }

    # Inter-group distinctness requirements (minimum ΔE)
    # Higher values = more important to distinguish
    GROUP_DISTINCTNESS: Dict[Tuple[str, str], float] = {
        ("diagnostic", "identifier"): 0.25,   # Errors must pop on variables
        ("diagnostic", "structure"): 0.25,    # Errors must pop on functions
        ("diagnostic", "data"): 0.20,         # Errors must pop on literals
        ("identifier", "structure"): 0.15,    # Variables vs functions
        ("data", "identifier"): 0.12,         # Literals vs variables
        ("control", "identifier"): 0.10,      # Keywords vs variables
        ("documentation", "identifier"): 0.18,  # Comments must recede
        ("documentation", "structure"): 0.15,   # Comments vs functions
    }

    # =========================================================================
    # Critical Pairs for Analysis
    # =========================================================================
    # Pairs that MUST be distinguishable (from CVD, readability, etc.)
    CRITICAL_PAIRS: List[Tuple[str, str]] = [
        # Existing critical pairs
        ("keyword", "string"),
        ("type", "string"),
        ("type", "comment"),
        ("keyword", "comment"),
        ("variable", "function"),
        ("function", "type"),
        ("constant", "string"),

        # Diagnostic distinctness (MUST stand out)
        ("error", "warning"),
        ("error", "info"),
        ("error", "hint"),
        ("warning", "info"),
        ("error", "keyword"),      # Error vs normal code
        ("error", "string"),
        ("error", "variable"),
        ("warning", "constant"),   # Warning vs data

        # Diff visibility
        ("diff_add", "diff_delete"),
        ("diff_add", "diff_change"),
        ("diff_delete", "diff_change"),
        ("diff_add", "bg"),        # Must be visible on background
        ("diff_delete", "bg"),
        ("diff_change", "bg"),

        # Git sign visibility
        ("git_add", "git_delete"),
        ("git_add", "bg"),
        ("git_delete", "bg"),

        # Search visibility
        ("search", "bg"),
        ("search", "visual"),
        ("inc_search", "cursor_line"),

        # Special comment visibility
        ("todo", "comment"),
        ("fixme", "comment"),
        ("note", "comment"),
    ]

    # =========================================================================
    # Background Tokens (excluded from text analysis)
    # =========================================================================
    BACKGROUND_TOKENS: Set[str] = {
        "bg",
        "cursor_line",
        "cursor_column",
        "popup_bg",
        "visual",
        "fold",
        "sign_column",
        "color_column",
        "pmenu",
        "pmenu_sbar",
    }

    # =========================================================================
    # Text Tokens (included in readability analysis)
    # =========================================================================
    TEXT_TOKENS: List[str] = [
        "keyword", "string", "function", "type", "variable", "comment",
        "constant", "operator", "number", "boolean", "property", "parameter",
    ]

    # =========================================================================
    # High-Attention Tokens (from eye-tracking research)
    # =========================================================================
    # These tokens receive the most visual attention in code reading
    HIGH_ATTENTION_TOKENS: List[str] = [
        "variable",     # Highest attention
        "function",     # Very high
        "parameter",    # Very high
        "property",     # High
        "type",         # High
    ]

    # Low-attention tokens (peripheral vision)
    LOW_ATTENTION_TOKENS: List[str] = [
        "keyword",      # Navigation beacons, can be subtler
        "punctuation",  # Minimal reading time
        "comment",      # Should recede
    ]

    # =========================================================================
    # Mapping Methods
    # =========================================================================
    @classmethod
    def get_group(cls, token: str) -> str:
        """Get the functional group for a token."""
        for group, tokens in cls.FUNCTIONAL_GROUPS.items():
            if token in tokens:
                return group
        return "unknown"

    @classmethod
    def is_background(cls, token: str) -> bool:
        """Check if token is a background element."""
        return token in cls.BACKGROUND_TOKENS

    @classmethod
    def is_diagnostic(cls, token: str) -> bool:
        """Check if token is a diagnostic element."""
        return token in cls.DIAGNOSTICS

    @classmethod
    def get_attention_level(cls, token: str) -> str:
        """Get the attention level for a token (high, medium, low)."""
        if token in cls.HIGH_ATTENTION_TOKENS:
            return "high"
        elif token in cls.LOW_ATTENTION_TOKENS:
            return "low"
        else:
            return "medium"


# Aliases for backwards compatibility
SYNTAX_TOKENS = TokenRegistry.SYNTAX_CORE
TEXT_TOKENS = TokenRegistry.TEXT_TOKENS
CRITICAL_PAIRS = TokenRegistry.CRITICAL_PAIRS
BACKGROUND_TOKENS = TokenRegistry.BACKGROUND_TOKENS
