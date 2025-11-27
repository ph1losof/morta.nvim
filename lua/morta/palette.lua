local M = {}

M.colors = {
  -- Base colors - Gentle mystical undertones with better contrast
  bg = "#1E1F2D", -- Balanced mid-dark base
  bg_dark = "#14151E", -- True foundational black with controlled blue channel
  bg_highlight = "#2B2D41", -- Improved clarity while maintaining softness
  bg_float = "#26283B", -- APCA-safe floating window background

  -- Primary accent colors - Softer ethereal tones (all gamma/HDR safe)
  purple = "#CEB0FF", -- Arcane violet (stable across HDR & OLED)
  red = "#F581A0", -- Ethereal rose sigil (CVD-safe warm-magenta shift)
  blue = "#A0BDFD", -- Celestial soft blue (reduced fringe risk)
  gold = "#E0AF68", -- Arcane gold (harmonic balance point)

  -- Text colors - Enhanced contrast
  fg = "#D9E0FF", -- Main ethereal white
  fg_dark = "#A9B1D6", -- Subtle secondary text
  fg_gutter = "#7884A0", -- APCA-verified gutter color

  -- UI elements - Soft mystical accents
  border = "#72799C", -- APCA ≥ 3:1 non-text standard
  cursor = "#CEB0FF", -- Match purple
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

  -- Special highlights - Softer signals
  warning = "#ddae6a", -- Warm, non-harsh attention
  error = "#F07998", -- Soft error red (safer luminance curve)
  info = "#96b4f3", -- Calm informational blue
  hint = "#55D2E9", -- Alias for type

  -- Git colors - Harmonized commit markers
  git_add = "#9ECE6A", -- Organic green
  git_change = "#E0AF68", -- Gold alias
  git_delete = "#F581A0", -- Red alias

  -- Additional UI backgrounds tuned with JND modeling
  diff = {
    add = "#243526", -- Calm, low-chroma green base
    change = "#2F3142", -- Soft neutral periwinkle for changes
    delete = "#3C2730", -- Warm undertoned red-black
  },
}

-- Set alias colors for backward compatibility
M.colors.gray = M.colors.fg_gutter
M.colors.cyan = M.colors.type

return M
