local M = {}

M.colors = {
  -- Base colors - Gentle mystical undertones with better contrast
  bg = "#1D1E2C", -- luminance ~0.018 (optimal for pop)
  bg_dark = "#13141D", -- deeper base layer
  bg_highlight = "#2A2C40", -- slightly clearer highlight
  bg_float = "#25273A", -- Floating window background with better contrast

  -- Primary accent colors - Softer ethereal tones
  purple = "#CEB0FF", -- Softer mystical purple
  red = "#F581A0", -- Softer rose sigil
  blue = "#A0BDFD", -- Softer celestial blue
  gold = "#E0AF68", -- REFINED: Better "Saliency" fit (was #E6B97A)

  -- Text colors - Enhanced contrast for better readability
  fg = "#D9E0FF", -- Softer ethereal white (still with good contrast)
  fg_dark = "#A9B1D6", -- Slightly softer calm secondary
  fg_gutter = "#7884A0", -- Enhanced gutter text (better contrast)

  -- UI elements - Soft mystical accents with better accessibility
  border = "#72799C", -- REFINED: Meets 3:1 Non-Text CR (was #686D8E)
  cursor = "#CEB0FF", -- Matching softer purple
  selection = "#2F3555", -- Darker selection for better visibility
  none = "NONE", -- Transparent value

  -- Syntax highlighting - Softer divine palette
  string = "#9ECE6A", -- Softer nature green (unchanged)
  keyword = "#F581A0", -- Softer rose sigil (alias for red)
  func = "#A0BDFD", -- Softer arcane runes (alias for blue)
  constant = "#E0AF68", -- REFINED: Alias for new gold
  type = "#55D2E9", -- Softer cyan
  variable = "#D9E0FF", -- Softer gentle spirit (matches main fg)
  comment = "#8C97C0", -- REFINED: Meets 4.5:1 AA Text CR (was #808AAB)

  -- Special highlights - Softer signals
  warning = "#ddae6a", -- Softer warm warning (unchanged)
  error = "#F07998", -- Softer soft error (unchanged)
  info = "#96b4f3", -- Softer calm info (unchanged)
  hint = "#55D2E9", -- Softer serene hint (alias for type)

  -- Git colors - Softer markers
  git_add = "#9ECE6A", -- Softer blessed green
  git_change = "#E0AF68", -- REFINED: Alias for new gold
  git_delete = "#F581A0", -- Softer soft removal

  -- Additional colors for UI consistency
  diff = {
    add = "#243526", -- Background for additions (warm green undertone)
    change = "#2F3142", -- Background for changes (subtle warm undertone)
    delete = "#3C2730", -- Background for deletions (warm red undertone)
  },
}

-- Set alias colors for backward compatibility
M.colors.gray = M.colors.fg_gutter
M.colors.cyan = M.colors.type

return M
