local M = {}

M.url = "https://github.com/Saghen/blink.cmp"

function M.get(colors, config)
  return {
    BlinkCmpDoc = { fg = colors.fg, bg = colors.bg_float },
    BlinkCmpDocBorder = { fg = colors.border, bg = colors.bg_float },
    BlinkCmpGhostText = { fg = colors.gray },
    BlinkCmpKindCodeium = { fg = colors.cyan, bg = colors.none },
    BlinkCmpKindCopilot = { fg = colors.cyan, bg = colors.none },
    BlinkCmpKindDefault = { fg = colors.fg_dark, bg = colors.none },
    BlinkCmpKindSupermaven = { fg = colors.cyan, bg = colors.none },
    BlinkCmpKindTabNine = { fg = colors.cyan, bg = colors.none },
    BlinkCmpLabel = { fg = colors.fg, bg = colors.none },
    BlinkCmpLabelDeprecated = { fg = colors.gray, bg = colors.none, strikethrough = true },
    BlinkCmpLabelMatch = { fg = colors.blue, bg = colors.none },
    BlinkCmpMenu = { fg = colors.fg, bg = colors.bg_float },
    BlinkCmpMenuBorder = { fg = colors.border, bg = colors.bg_float },
    BlinkCmpSignatureHelp = { fg = colors.fg, bg = colors.bg_float },
    BlinkCmpSignatureHelpBorder = { fg = colors.border, bg = colors.bg_float },
  }
end

return M

