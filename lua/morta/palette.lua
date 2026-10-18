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
  keyword = "#FE99C0", -- v2 rose, lifted to APCA Lc 62 and nudged 8° magenta to clear error
  func = "#A0BDFD", -- Soft arcane blue (improved hue spacing)
  constant = "#E0AF68", -- Matches gold
  type = "#55D2E9", -- Softer cyan (hue moved toward green for CVD split)
  variable = "#D9E0FF", -- Same as fg — improved stability
  comment = "#929DC7", -- Lc 48: readable, still dimmer than every accent

  -- Special highlights - Softer signals (CVD-optimized)
  warning = "#f0c078", -- Brighter gold, distinct from constant for CVD
  error = "#FF9C82", -- Coral: the most saturated diagnostic, clear of keyword
  info = "#A2BFFE", -- Lc 66, above hint
  hint = "#75C4BA", -- Lc 61 muted teal, the quietest diagnostic

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
-- Referenced by group files but never defined in v2, which left those groups uncoloured.
M.colors.green = M.colors.string
M.colors.yellow = M.colors.warning
M.colors.magenta = M.colors.purple
M.colors.termminal_white = M.colors.fg

return M
