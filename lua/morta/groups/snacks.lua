local Util = require("morta.util")

local M = {}

M.url = "https://github.com/folke/snacks.nvim"

-- Get snacks.nvim highlights
---@param colors table
---@param config table
function M.get(colors, config)
  local none = config.transparent_background and "NONE" or colors.bg

  return {

    SnacksNotifierDebug = { fg = colors.fg, bg = none },
    SnacksNotifierBorderDebug = { fg = Util.blend_bg(colors.purple, 0.3), bg = none },
    SnacksNotifierIconDebug = { fg = colors.purple, italic = true },
    SnacksNotifierTitleDebug = { fg = colors.purple, italic = true },
    SnacksNotifierError = { fg = colors.fg, bg = none },
    SnacksNotifierBorderError = { fg = Util.blend_bg(colors.red, 0.3), bg = none },
    SnacksNotifierIconError = { fg = colors.red, italic = true },
    SnacksNotifierTitleError = { fg = colors.red, italic = true },
    SnacksNotifierInfo = { fg = colors.fg, bg = none },
    SnacksNotifierBorderInfo = { fg = Util.blend_bg(colors.blue, 0.3), bg = none },
    SnacksNotifierIconInfo = { fg = colors.blue, italic = true },
    SnacksNotifierTitleInfo = { fg = colors.blue, italic = true },
    SnacksNotifierTrace = { fg = colors.fg, bg = none },
    SnacksNotifierBorderTrace = { fg = Util.blend_bg(colors.type, 0.3), bg = none },
    SnacksNotifierIconTrace = { fg = colors.type, italic = true },
    SnacksNotifierTitleTrace = { fg = colors.type, italic = true },
    SnacksNotifierWarn = { fg = colors.fg, bg = none },
    SnacksNotifierBorderWarn = { fg = Util.blend_bg(colors.gold, 0.3), bg = none },
    SnacksNotifierIconWarn = { fg = colors.gold, italic = true },
    SnacksNotifierTitleWarn = { fg = colors.gold, italic = true },

    SnacksDashboardDesc = { fg = colors.type, italic = true },
    SnacksDashboardFooter = { fg = colors.purple },
    SnacksDashboardHeader = { fg = colors.purple },
    SnacksDashboardIcon = { fg = colors.gold },
    SnacksDashboardKey = { fg = colors.red, italic = true },
    SnacksDashboardSpecial = { fg = colors.blue },
    SnacksDashboardDir = { fg = colors.fg_dark, italic = true },

    SnacksProfilerIconInfo = { bg = Util.blend_bg(colors.blue, 0.2), fg = colors.blue },
    SnacksProfilerBadgeInfo = { bg = Util.blend_bg(colors.blue, 0.1), fg = colors.blue },
    SnacksScratchKey = { link = "SnacksProfilerIconInfo" },
    SnacksScratchDesc = { link = "SnacksProfilerBadgeInfo" },
    SnacksProfilerIconTrace = { bg = Util.blend_bg(colors.purple, 0.2), fg = colors.purple },
    SnacksProfilerBadgeTrace = { bg = Util.blend_bg(colors.purple, 0.1), fg = colors.purple },

    SnacksIndent = { fg = colors.fg_gutter, nocombine = true },
    SnacksIndentScope = { fg = colors.gold, nocombine = true },
    SnacksZenIcon = { fg = colors.type, italic = true },
    SnacksInputIcon = { fg = colors.purple },
    SnacksInputBorder = { fg = colors.gold },
    SnacksInputTitle = { fg = colors.gold, italic = true },
  }
end

return M

