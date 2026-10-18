local M = {}

-- Morta v3 palette.
--
-- Built by constrained optimisation in Oklab against three hard requirements:
--   1. APCA Lc floors per role (contrast), measured on the real background
--   2. worst-case pairwise Oklab dE, evaluated under normal vision AND
--      protanopia / deuteranopia / tritanopia simulation
--   3. a chroma ceiling, to bound Helmholtz-Kohlrausch brightness illusion,
--      lateral chromatic aberration and afterimage propensity
--
-- The palette is deliberately SMALL. sRGB cannot keep more than about seven
-- colours mutually distinct at these contrast levels, so extra roles are
-- aliases onto the accent set rather than new hues.

M.colors = {
  -- Background depth stack. Every step is >= 0.034 in Oklab L, safely above
  -- the mesopic just-noticeable difference, so layers stay separable at night.
  bg = "#16161f",
  bg_dark = "#0f0e16",
  bg_float = "#1f1f2a",
  bg_highlight = "#272735",
  selection = "#32344f",

  -- Body text. Lc 96 puts it in APCA's "preferred" band for extended reading.
  fg = "#ebeeff",
  variable = "#ebeeff",

  -- Syntax accents. Mutually >= 0.103 Oklab dE in normal vision and >= 0.048
  -- under dichromacy. Lightness is laddered so the set stays separable even
  -- when hue information is destroyed.
  string = "#cdf89e",  -- Lc 94
  type = "#81ebd4",  -- Lc 82
  constant = "#efca8c",  -- Lc 77
  func = "#94d0f8",  -- Lc 73
  keyword = "#ffadca",  -- Lc 70
  operator = "#b2abff",  -- Lc 61

  -- Recessive tier. Near-achromatic and strictly below every accent in
  -- lightness. punct covers the highest-frequency, lowest-information tokens.
  fg_dark = "#a6adc1",  -- Lc 57
  punct = "#a6adc1",  -- Lc 57
  comment = "#94a2b5",  -- Lc 50
  fg_gutter = "#858a9b",  -- Lc 39
  border = "#737786",  -- Lc 30

  -- Diagnostics. Rare and spatially isolated (gutter, virtual text, undercurl),
  -- so they carry a larger chroma budget than syntax without raising the
  -- average on-screen chroma much. error is kept clear of keyword.
  error = "#faac9c",  -- Lc 67
  warning = "#ffdd7e",  -- Lc 87
  info = "#a4e8ff",  -- Lc 86
  hint = "#8cffc5",  -- Lc 92

  -- Git
  git_add = "#cdf89e",
  git_change = "#efca8c",
  git_delete = "#faac9c",

  -- Misc
  cursor = "#b2abff",
  none = "NONE",

  diff = {
    add = "#152b10",
    change = "#312103",
    delete = "#3c1816",
  },
}

-- Hue aliases. Other modules already reference these names; they are aliases
-- rather than distinct colours on purpose, so the palette stays at the size the
-- sRGB gamut can actually keep separated.
M.colors.red = M.colors.keyword
M.colors.blue = M.colors.func
M.colors.gold = M.colors.constant
M.colors.purple = M.colors.operator
M.colors.cyan = M.colors.type
M.colors.green = M.colors.string
M.colors.yellow = M.colors.constant
M.colors.magenta = M.colors.operator
M.colors.gray = M.colors.fg_gutter
M.colors.termminal_white = M.colors.fg

return M
