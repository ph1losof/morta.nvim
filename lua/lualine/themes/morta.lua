local colors = require("morta.palette").colors

return {
  normal = {
    a = { fg = colors.bg_dark, bg = colors.purple, gui = "bold" },
    b = { fg = colors.fg, bg = colors.bg_dark },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
  insert = {
    a = { fg = colors.bg_dark, bg = colors.string, gui = "bold" },
    b = { fg = colors.fg, bg = colors.bg_dark },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
  visual = {
    a = { fg = colors.bg_dark, bg = colors.blue, gui = "bold" },
    b = { fg = colors.fg_dark, bg = colors.bg_dark },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
  replace = {
    a = { fg = colors.bg_dark, bg = colors.red, gui = "bold" },
    b = { fg = colors.fg_dark, bg = colors.bg_dark },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
  command = {
    a = { fg = colors.bg_dark, bg = colors.gold, gui = "bold" },
    b = { fg = colors.fg_dark, bg = colors.bg_dark },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
  inactive = {
    a = { fg = colors.termminal_white, bg = colors.bg_float },
    b = { fg = colors.fg, bg = colors.bg_float },
    c = { fg = colors.fg, bg = colors.bg_float },
  },
}
