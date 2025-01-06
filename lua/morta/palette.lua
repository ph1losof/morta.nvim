local M = {}

M.colors = {
  -- Base colors - Gentle mystical undertones
  bg = "#1A1B26", -- Soft void background (from Tokyo Night)
  bg_dark = "#16161e", -- Darker depth
  bg_highlight = "#292e42", -- Gentle mystical highlight

  -- Primary accent colors - Soothing ethereal tones
  purple = "#bb9af7", -- Soft mystical purple (from Tokyo Night)
  red = "#F9778B", -- Soft rose sigil
  blue = "#7aa2f7", -- Calm celestial blue
  gold = "#e0af68", -- Warm divine gold

  -- Text colors - Gentle contrast
  fg = "#c0caf5", -- Soft ethereal white (from Tokyo Night)
  fg_dark = "#a9b1d6", -- Calm secondary
  fg_gutter = "#3b4261", -- Subtle shadow

  -- UI elements - Soft mystical accents
  border = "#29394f", -- Gentle borders
  cursor = "#bb9af7", -- Matching soft purple
  selection = "#2e3c64", -- Calm selection

  -- Syntax highlighting - Soothing divine palette
  string = "#9ece6a", -- Gentle nature green
  keyword = "#F9778B", -- Soft rose sigil
  func = "#7aa2f7", -- Calm arcane runes
  constant = "#ff9e64", -- Warm amber
  type = "#2ac3de", -- Serene cyan
  variable = "#c0caf5", -- Gentle spirit
  comment = "#565f89", -- Quiet whispers

  -- Special highlights - Gentle signals
  warning = "#e0af68", -- Warm warning
  error = "#F9778B", -- Soft error
  info = "#7aa2f7", -- Calm info
  hint = "#1abc9c", -- Serene hint

  -- Git colors - Gentle markers
  git_add = "#9ece6a", -- Blessed green
  git_change = "#e0af68", -- Calm change
  git_delete = "#F9778B", -- Soft removal

  -- Terminal colors - Soothing palette
  terminal_black = "#1a1b26",
  terminal_blue = "#7aa2f7",
  terminal_cyan = "#2ac3de",
  terminal_green = "#9ece6a",
  terminal_magenta = "#bb9af7",
  terminal_red = "#F9778B",
  terminal_white = "#c0caf5",
  terminal_yellow = "#e0af68",
}

return M
