local M = {}

local Util = require("morta.util")

M.name = "snacks"
M.url = "https://github.com/folke/snacks.nvim"

function M.get(colors, config)
  -- stylua: ignore
  local ret = {
    -- Notifier
    SnacksNotifierDebug       = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderDebug = { fg = colors.comment, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconDebug   = { fg = colors.comment },
    SnacksNotifierTitleDebug  = { fg = colors.comment },

    SnacksNotifierError       = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderError = { fg = colors.error, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconError   = { fg = colors.error },
    SnacksNotifierTitleError  = { fg = colors.error },

    SnacksNotifierInfo        = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderInfo  = { fg = colors.info, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconInfo    = { fg = colors.info },
    SnacksNotifierTitleInfo   = { fg = colors.info },

    SnacksNotifierTrace       = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderTrace = { fg = colors.purple, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconTrace   = { fg = colors.purple },
    SnacksNotifierTitleTrace  = { fg = colors.purple },

    SnacksNotifierWarn        = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderWarn  = { fg = colors.gold, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconWarn    = { fg = colors.gold },
    SnacksNotifierTitleWarn   = { fg = colors.gold },

    -- Dashboard
    SnacksDashboardDesc       = { fg = colors.type },
    SnacksDashboardFooter     = { fg = colors.blue },
    SnacksDashboardHeader     = { fg = colors.blue },
    SnacksDashboardIcon       = { fg = colors.blue },
    SnacksDashboardKey        = { fg = colors.constant },
    SnacksDashboardSpecial    = { fg = colors.purple },
    SnacksDashboardDir        = { fg = colors.fg_dark },

    -- Profiler
    SnacksProfilerIconInfo    = { bg = Util.blend_bg(colors.blue, 0.3), fg = colors.blue },
    SnacksProfilerBadgeInfo   = { bg = Util.blend_bg(colors.blue, 0.1), fg = colors.blue },
    SnacksScratchKey          = "SnacksProfilerIconInfo",
    SnacksScratchDesc         = "SnacksProfilerBadgeInfo",
    SnacksProfilerIconTrace   = { bg = Util.blend_bg(colors.fg_dark, 0.3), fg = colors.fg_dark },
    SnacksProfilerBadgeTrace  = { bg = Util.blend_bg(colors.fg_dark, 0.1), fg = colors.fg_dark },

    -- Other
    SnacksIndent              = { fg = colors.fg_gutter, nocombine = true },
    SnacksIndentScope         = { fg = colors.blue, nocombine = true },
    SnacksZenIcon             = { fg = colors.purple },
    SnacksInputIcon           = { fg = colors.blue },
    SnacksInputBorder         = { fg = colors.gold },
    SnacksInputTitle          = { fg = colors.gold },

    -- Picker
    SnacksPickerInputBorder   = { fg = colors.constant, bg = colors.bg_dark },
    SnacksPickerInputTitle    = { fg = colors.constant, bg = colors.bg_dark },
    SnacksPickerBoxTitle      = { fg = colors.constant, bg = colors.bg_dark },
    SnacksPickerSelected      = { fg = colors.purple },
    SnacksPickerToggle        = "SnacksProfilerBadgeInfo",
    SnacksPickerPickWinCurrent = { fg = colors.fg, bg = colors.purple, bold = true },
    SnacksPickerPickWin       = { fg = colors.fg, bg = colors.selection, bold = true },
  }

  -- Add rainbow indentation colors if available
  if colors.rainbow then
    for i, color in ipairs(colors.rainbow) do
      ret["SnacksIndent" .. i] = { fg = color, nocombine = true }
    end
  end

  return ret
end

return M

