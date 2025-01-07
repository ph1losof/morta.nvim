local M = {}

M.colors = {
  -- Base colors - Gentle mystical undertones with better contrast
  bg = "#1B1C29", -- Darker background with less purple tint for better contrast
  bg_dark = "#14151F", -- Darker depth with less purple tint
  bg_highlight = "#292B3E", -- More neutral highlight for better text separation
  bg_float = "#1F2134", -- Floating window background with better contrast

  -- Primary accent colors - Softer ethereal tones
  purple = "#c5a6f5", -- Softer mystical purple (HSL [0.733, 0.805, 0.778] -> [0.733, 0.811, 0.808], Contrast 7.25:1 -> 8.15:1)
  red = "#ee6f90", -- Softer rose sigil (S: 0.900 -> 0.792)
  blue = "#96b4f3", -- Softer celestial blue (HSL [0.613, 0.791, 0.737] -> [0.613, 0.798, 0.772], Contrast 7.21:1 -> 8.13:1)
  gold = "#ddae6a", -- Softer divine gold (S: 0.659 -> 0.626)

  -- Text colors - Enhanced contrast for better readability
  fg = "#D2DAFD", -- Softer ethereal white (still with good contrast)
  fg_dark = "#A9B1D6", -- Slightly softer calm secondary
  fg_gutter = "#606980", -- Enhanced gutter text (better contrast)

  -- UI elements - Soft mystical accents with better accessibility
  border = "#686D8E", -- Enhanced borders (meets 3:1 for UI components)
  cursor = "#c5a6f5", -- Matching softer purple (updated for higher contrast)
  selection = "#2F3555", -- Darker selection for better visibility
  none = "NONE", -- Transparent value

  -- Syntax highlighting - Softer divine palette
  string = "#9ECE6A", -- Softer nature green (unchanged)
  keyword = "#ee6f90", -- Softer rose sigil (updated)
  func = "#96b4f3", -- Softer arcane runes (updated for higher contrast)
  constant = "#ddae6a", -- Softer warm amber (updated)
  type = "#4ec8de", -- Softer cyan (HSL [0.525, 0.676, 0.516] -> [0.525, 0.689, 0.591], Contrast 7.61:1 -> 8.55:1)
  variable = "#D2DAFD", -- Softer gentle spirit (matches main fg)
  comment = "#8086A3", -- Enhanced whispers (meets minimum contrast)

  -- Special highlights - Softer signals
  warning = "#ddae6a", -- Softer warm warning (updated)
  error = "#ee6f90", -- Softer soft error (updated)
  info = "#96b4f3", -- Softer calm info (updated for higher contrast)
  hint = "#4ec8de", -- Softer serene hint (updated for higher contrast)

  -- Git colors - Softer markers
  git_add = "#9ECE6A", -- Softer blessed green (unchanged)
  git_change = "#ddae6a", -- Softer calm change (updated)
  git_delete = "#ee6f90", -- Softer soft removal (updated)

  -- Additional colors for UI consistency
  diff = {
    add = "#2B3328", -- Background for additions (warm green undertone)
    change = "#333340", -- Background for changes (subtle warm undertone)
    delete = "#37292E", -- Background for deletions (warm red undertone)
  },
}

-- Set alias colors for backward compatibility
M.colors.gray = M.colors.fg_gutter
M.colors.cyan = M.colors.type

return M
