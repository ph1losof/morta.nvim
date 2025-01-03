local M = {}

M.url = "https://github.com/hrsh7th/nvim-cmp"

-- Get nvim-cmp highlights with soft candy theme
---@param colors table
---@param config table
function M.get(colors, config)
  return {

    CmpWindow = { bg = colors.bg_dark },
    CmpPmenu = { bg = colors.bg_dark },
    CmpPmenuBorder = { fg = colors.purple, bg = colors.bg_dark },
    CmpPmenuSel = { fg = colors.fg, bg = colors.selection, bold = true },
    CmpPmenuThumb = { bg = colors.purple },

    CmpItemAbbr = { fg = colors.fg },
    CmpItemAbbrDeprecated = { fg = colors.comment, strikethrough = true },
    CmpItemAbbrMatch = { fg = colors.gold, bold = true },
    CmpItemAbbrMatchFuzzy = { fg = colors.gold, italic = true },

    CmpItemKindClass = { fg = colors.gold },
    CmpItemKindConstant = { fg = colors.gold },
    CmpItemKindConstructor = { fg = colors.blue },
    CmpItemKindDefault = { fg = colors.fg_dark },
    CmpItemKindEnum = { fg = colors.gold },
    CmpItemKindEnumMember = { fg = colors.red },
    CmpItemKindEvent = { fg = colors.gold },
    CmpItemKindField = { fg = colors.blue },
    CmpItemKindFunction = { fg = colors.blue },
    CmpItemKindInterface = { fg = colors.gold },
    CmpItemKindKeyword = { fg = colors.purple },
    CmpItemKindMethod = { fg = colors.blue },
    CmpItemKindModule = { fg = colors.gold },
    CmpItemKindOperator = { fg = colors.purple },
    CmpItemKindProperty = { fg = colors.blue },
    CmpItemKindReference = { fg = colors.red },
    CmpItemKindSnippet = { fg = colors.type },
    CmpItemKindStruct = { fg = colors.gold },
    CmpItemKindText = { fg = colors.string },
    CmpItemKindTypeParameter = { fg = colors.red },
    CmpItemKindUnit = { fg = colors.gold },
    CmpItemKindValue = { fg = colors.red },
    CmpItemKindVariable = { fg = colors.red },

    CmpItemMenu = { fg = colors.comment, italic = true },
  }
end

return M

