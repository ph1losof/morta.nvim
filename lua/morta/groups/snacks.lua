local M = {}

M.url = "https://github.com/folke/snacks.nvim"

function M.get(colors, config)
  return {
    -- Notifier
    SnacksNotifierDebug = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderDebug = { fg = colors.comment, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconDebug = { fg = colors.comment },
    SnacksNotifierTitleDebug = { fg = colors.comment },
    
    SnacksNotifierError = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderError = { fg = colors.error, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconError = { fg = colors.error },
    SnacksNotifierTitleError = { fg = colors.error },
    
    SnacksNotifierInfo = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderInfo = { fg = colors.info, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconInfo = { fg = colors.info },
    SnacksNotifierTitleInfo = { fg = colors.info },
    
    SnacksNotifierTrace = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderTrace = { fg = colors.purple, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconTrace = { fg = colors.purple },
    SnacksNotifierTitleTrace = { fg = colors.purple },
    
    SnacksNotifierWarn = { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierBorderWarn = { fg = colors.gold, bg = config.transparent_background and colors.none or colors.bg },
    SnacksNotifierIconWarn = { fg = colors.gold },
    SnacksNotifierTitleWarn = { fg = colors.gold },

    -- Dashboard
    SnacksDashboardDesc = { fg = colors.cyan },
    SnacksDashboardFooter = { fg = colors.blue },
    SnacksDashboardHeader = { fg = colors.blue },
    SnacksDashboardIcon = { fg = colors.blue },
    SnacksDashboardKey = { fg = colors.orange },
    SnacksDashboardSpecial = { fg = colors.purple },
    SnacksDashboardDir = { fg = colors.fg_dark },

    -- Profiler
    SnacksProfilerIconInfo = { bg = colors.bg_highlight, fg = colors.blue },
    SnacksProfilerBadgeInfo = { bg = colors.bg_highlight, fg = colors.blue },
    SnacksScratchKey = "SnacksProfilerIconInfo",
    SnacksScratchDesc = "SnacksProfilerBadgeInfo",
    SnacksProfilerIconTrace = { bg = colors.bg_highlight, fg = colors.fg_dark },
    SnacksProfilerBadgeTrace = { bg = colors.bg_highlight, fg = colors.fg_dark },
    
    -- Other
    SnacksIndent = { fg = colors.fg_gutter, nocombine = true },
    SnacksIndentScope = { fg = colors.blue, nocombine = true },
    SnacksZenIcon = { fg = colors.purple },
    SnacksInputIcon = { fg = colors.blue },
    SnacksInputBorder = { fg = colors.gold },
    SnacksInputTitle = { fg = colors.gold },
  }
end

return M 