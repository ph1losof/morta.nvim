local M = {}

local Util = require("morta.util")

M.name = "blink_cmp"
M.url = "https://github.com/Saghen/blink.cmp"

function M.get(colors, config)
  -- stylua: ignore
  local ret = {
    BlinkCmpDoc                 = { fg = colors.fg, bg = colors.bg_dark },
    BlinkCmpDocBorder           = { fg = colors.blue, bg = colors.bg_dark },
    BlinkCmpGhostText           = { fg = colors.fg_gutter },
    BlinkCmpKindCodeium         = { fg = colors.type, bg = colors.none },
    BlinkCmpKindCopilot         = { fg = colors.type, bg = colors.none },
    BlinkCmpKindDefault         = { fg = colors.fg_dark, bg = colors.none },
    BlinkCmpKindSupermaven      = { fg = colors.type, bg = colors.none },
    BlinkCmpKindTabNine         = { fg = colors.type, bg = colors.none },
    BlinkCmpLabel               = { fg = colors.fg, bg = colors.none },
    BlinkCmpLabelDeprecated     = { fg = colors.fg_gutter, bg = colors.none, strikethrough = true },
    BlinkCmpLabelMatch          = { fg = colors.blue, bg = colors.none },
    BlinkCmpMenu                = { fg = colors.fg, bg = colors.bg_dark },
    BlinkCmpMenuBorder          = { fg = colors.blue, bg = colors.bg_dark },
    BlinkCmpSignatureHelp       = { fg = colors.fg, bg = colors.bg_dark },
    BlinkCmpSignatureHelpBorder = { fg = colors.blue, bg = colors.bg_dark },
    -- LSP Kind Groups
    BlinkCmpKindField           = { fg = colors.blue, bg = colors.none },
    BlinkCmpKindProperty        = { fg = colors.blue, bg = colors.none },
    BlinkCmpKindEvent           = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindText            = { fg = colors.string, bg = colors.none },
    BlinkCmpKindEnum            = { fg = colors.purple, bg = colors.none },
    BlinkCmpKindKeyword         = { fg = colors.keyword, bg = colors.none },
    BlinkCmpKindConstant        = { fg = colors.constant, bg = colors.none },
    BlinkCmpKindConstructor     = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindReference       = { fg = colors.purple, bg = colors.none },
    BlinkCmpKindFunction        = { fg = colors.func, bg = colors.none },
    BlinkCmpKindStruct          = { fg = colors.type, bg = colors.none },
    BlinkCmpKindClass           = { fg = colors.type, bg = colors.none },
    BlinkCmpKindModule          = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindOperator        = { fg = colors.purple, bg = colors.none },
    BlinkCmpKindVariable        = { fg = colors.variable, bg = colors.none },
    BlinkCmpKindFile            = { fg = colors.blue, bg = colors.none },
    BlinkCmpKindUnit            = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindSnippet         = { fg = colors.red, bg = colors.none },
    BlinkCmpKindFolder          = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindMethod          = { fg = colors.func, bg = colors.none },
    BlinkCmpKindValue           = { fg = colors.gold, bg = colors.none },
    BlinkCmpKindEnumMember      = { fg = colors.constant, bg = colors.none },
    BlinkCmpKindInterface       = { fg = colors.type, bg = colors.none },
    BlinkCmpKindColor           = { fg = colors.red, bg = colors.none },
    BlinkCmpKindTypeParameter   = { fg = colors.type, bg = colors.none },
  }

  return ret
end

return M
