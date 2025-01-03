local M = {}
local Util = require("morta.util")

M.url = "https://github.com/blink/blink-cmp"

---@param colors table
---@param config table
function M.get(colors, config)
  return {
    BlinkCmpWindow = { bg = colors.bg_dark },
    BlinkCmpBorder = { fg = colors.purple, bg = colors.bg_dark },
    BlinkCmpSelected = { bg = colors.selection },
    BlinkCmpScrollbar = { bg = colors.purple },

    BlinkCmpMatch = { fg = colors.gold, bold = true },
    BlinkCmpMatchFuzzy = { fg = colors.gold, italic = true },
    BlinkCmpUnmatched = { fg = colors.comment },

    BlinkCmpItemIcon = { fg = colors.purple },
    BlinkCmpItemKind = { fg = colors.blue },
    BlinkCmpItemMenu = { fg = colors.comment, italic = true },
    BlinkCmpItemAbbr = { fg = colors.fg },
    BlinkCmpItemAbbrDeprecated = { fg = colors.comment, strikethrough = true },

    BlinkCmpDoc = { bg = colors.bg_dark },
    BlinkCmpDocBorder = { fg = colors.purple, bg = colors.bg_dark },
    BlinkCmpDocHighlight = { bg = Util.blend_bg(colors.purple, 0.1) },

    BlinkCmpSourceAI = { fg = colors.type },
    BlinkCmpSourceLSP = { fg = colors.blue },
    BlinkCmpSourceSnippet = { fg = colors.string },
    BlinkCmpSourceFile = { fg = colors.gold },
    BlinkCmpSourceBuffer = { fg = colors.red },
  }
end

return M

