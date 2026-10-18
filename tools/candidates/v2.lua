local M = {}

M.colors = {
  -- Base colors - Preserved for optimal T1 (halation fix was counterproductive)
  bg = "#1E1F2D", -- Balanced mid-dark base (original preserved for T1)
  bg_dark = "#14151E", -- True foundational black with controlled blue channel
  bg_highlight = "#2B2D41", -- Improved clarity while maintaining softness
  bg_float = "#26283B", -- APCA-safe floating window background

  -- Primary accent colors - Phase 2 optimized for T2 Oklab separation
  purple = "#D8A8FF", -- Phase 2: boosted chroma for keyword/operator separation
  red = "#F581A0", -- Ethereal rose sigil (CVD-safe warm-magenta shift)
  blue = "#A0BDFD", -- Celestial soft blue (reduced fringe risk)
  gold = "#E0AF68", -- Arcane gold (harmonic balance point)

  -- Text colors - Preserved for optimal T1 (halation fix was counterproductive)
  fg = "#D9E0FF", -- Main ethereal white (original preserved for T1)
  fg_dark = "#A9B1D6", -- Subtle secondary text
  fg_gutter = "#7884A0", -- APCA-verified gutter color

  -- UI elements - Soft mystical accents
  border = "#72799C", -- APCA ≥ 3:1 non-text standard
  cursor = "#D8A8FF", -- Match purple (Phase 2 optimized)
  selection = "#2F3555", -- More visible while staying soft
  none = "NONE",

  -- Syntax highlighting - Soft divine palette (scientifically tuned)
  string = "#9FD893", -- Balanced green (reduced dominance in JSON/YAML)
  keyword = "#F581A0", -- Matches red (slight magenta shift for CVD)
  func = "#A0BDFD", -- Soft arcane blue (improved hue spacing)
  constant = "#E0AF68", -- Matches gold
  type = "#55D2E9", -- Softer cyan (hue moved toward green for CVD split)
  variable = "#D9E0FF", -- Same as fg — improved stability
  comment = "#8C97C0", -- APCA AA 4.5:1 compliant (scientifically verified)

  -- Special highlights - Softer signals (CVD-optimized)
  warning = "#f0c078", -- Brighter gold, distinct from constant for CVD
  error = "#F07998", -- Soft error red (safer luminance curve)
  info = "#96b4f3", -- Calm informational blue
  hint = "#96b4f3", -- Uses info color (distinct from type for CVD)

  -- Git colors - Harmonized commit markers (CVD-optimized)
  git_add = "#9ECE6A", -- Organic green
  git_change = "#E0AF68", -- Gold alias
  git_delete = "#f07998", -- Uses error color (distinct from keyword for CVD)

  -- Additional UI backgrounds (CVD-optimized with distinct hues)
  diff = {
    add = "#213a1c", -- Dark green tint (from string color)
    change = "#382b4d", -- Dark purple tint (from operator, avoids blue-green CVD confusion)
    delete = "#541e2d", -- Dark red tint (from error color)
  },
}

-- Set alias colors for backward compatibility
M.colors.gray = M.colors.fg_gutter
M.colors.cyan = M.colors.type

return M
