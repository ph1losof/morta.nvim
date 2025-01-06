local M = {}

M.url = "https://github.com/hrsh7th/nvim-cmp"

function M.get(colors, config)
  return {
    CmpDocumentation = { fg = colors.fg, bg = colors.bg_float },
    CmpDocumentationBorder = { fg = colors.border, bg = colors.bg_float },
    CmpGhostText = { fg = colors.gray },
    CmpItemAbbr = { fg = colors.fg, bg = colors.none },
    CmpItemAbbrDeprecated = { fg = colors.gray, bg = colors.none, strikethrough = true },
    CmpItemAbbrMatch = { fg = colors.blue, bg = colors.none },
    CmpItemAbbrMatchFuzzy = { fg = colors.blue, bg = colors.none },
    CmpItemKindCodeium = { fg = colors.cyan, bg = colors.none },
    CmpItemKindCopilot = { fg = colors.cyan, bg = colors.none },
    CmpItemKindSupermaven = { fg = colors.cyan, bg = colors.none },
    CmpItemKindDefault = { fg = colors.fg_dark, bg = colors.none },
    CmpItemKindTabNine = { fg = colors.cyan, bg = colors.none },
    CmpItemMenu = { fg = colors.comment, bg = colors.none },
  }
end

return M 
