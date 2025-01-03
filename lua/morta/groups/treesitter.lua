local M = {}
local Util = require("morta.util")

M.url = "https://github.com/nvim-treesitter/nvim-treesitter"

---@param colors table
---@param config table
function M.get(colors, config)
  local ret = {

    ["@annotation"] = "PreProc",
    ["@attribute"] = "PreProc",
    ["@boolean"] = "Boolean",
    ["@character"] = "Character",
    ["@character.printf"] = "SpecialChar",
    ["@character.special"] = "SpecialChar",

    ["@comment"] = "Comment",
    ["@comment.error"] = { fg = colors.error },
    ["@comment.hint"] = { fg = colors.hint },
    ["@comment.info"] = { fg = colors.info },
    ["@comment.note"] = { fg = colors.hint },
    ["@comment.todo"] = { fg = colors.warning },
    ["@comment.warning"] = { fg = colors.warning },

    ["@constant"] = "Constant",
    ["@constant.builtin"] = "Special",
    ["@constant.macro"] = "Define",
    ["@constructor"] = { fg = colors.purple },
    ["@constructor.tsx"] = { fg = colors.blue },

    ["@diff.delta"] = "DiffChange",
    ["@diff.minus"] = "DiffDelete",
    ["@diff.plus"] = "DiffAdd",

    ["@function"] = "Function",
    ["@function.builtin"] = "Special",
    ["@function.call"] = "@function",
    ["@function.macro"] = "Macro",
    ["@function.method"] = "Function",
    ["@function.method.call"] = "@function.method",

    ["@keyword"] = { fg = colors.purple, italic = config.styles.keywords.italic },
    ["@keyword.conditional"] = "Conditional",
    ["@keyword.coroutine"] = "@keyword",
    ["@keyword.debug"] = "Debug",
    ["@keyword.directive"] = "PreProc",
    ["@keyword.directive.define"] = "Define",
    ["@keyword.exception"] = "Exception",
    ["@keyword.function"] = { fg = colors.purple, italic = config.styles.functions.italic },
    ["@keyword.import"] = "Include",
    ["@keyword.operator"] = "@operator",
    ["@keyword.repeat"] = "Repeat",
    ["@keyword.return"] = "@keyword",
    ["@keyword.storage"] = "StorageClass",

    ["@label"] = { fg = colors.blue },
    ["@markup"] = "@none",
    ["@markup.emphasis"] = { italic = true },
    ["@markup.environment"] = "Macro",
    ["@markup.environment.name"] = "Type",
    ["@markup.heading"] = "Title",
    ["@markup.italic"] = { italic = true },
    ["@markup.link"] = { fg = colors.type },
    ["@markup.link.label"] = "SpecialChar",
    ["@markup.link.label.symbol"] = "Identifier",
    ["@markup.link.url"] = "Underlined",
    ["@markup.list"] = { fg = colors.blue },
    ["@markup.list.checked"] = { fg = colors.git_add },
    ["@markup.list.markdown"] = { fg = colors.gold, bold = true },
    ["@markup.list.unchecked"] = { fg = colors.blue },
    ["@markup.math"] = "Special",
    ["@markup.raw"] = "String",
    ["@markup.raw.markdown_inline"] = { bg = colors.bg_dark, fg = colors.blue },
    ["@markup.strikethrough"] = { strikethrough = true },
    ["@markup.strong"] = { bold = true },
    ["@markup.underline"] = { underline = true },

    ["@module"] = "Include",
    ["@module.builtin"] = { fg = colors.red },
    ["@namespace.builtin"] = "@variable.builtin",
    ["@none"] = {},

    ["@number"] = "Number",
    ["@number.float"] = "Float",
    ["@operator"] = { fg = colors.purple },

    ["@property"] = { fg = colors.git_add },
    ["@punctuation.bracket"] = { fg = colors.fg_dark },
    ["@punctuation.delimiter"] = { fg = colors.purple },
    ["@punctuation.special"] = { fg = colors.purple },
    ["@punctuation.special.markdown"] = { fg = colors.gold },

    ["@string"] = "String",
    ["@string.documentation"] = { fg = colors.gold },
    ["@string.escape"] = { fg = colors.purple },
    ["@string.regexp"] = { fg = colors.blue },

    ["@tag"] = "Label",
    ["@tag.attribute"] = "@property",
    ["@tag.delimiter"] = "Delimiter",
    ["@tag.delimiter.tsx"] = { fg = Util.blend_bg(colors.blue, 0.7) },
    ["@tag.tsx"] = { fg = colors.red },
    ["@tag.javascript"] = { fg = colors.red },

    ["@type"] = "Type",
    ["@type.builtin"] = { fg = Util.blend_bg(colors.blue, 0.8) },
    ["@type.definition"] = "Typedef",
    ["@type.qualifier"] = "@keyword",
    ["@variable"] = { fg = colors.fg, italic = config.styles.variables.italic },
    ["@variable.builtin"] = { fg = colors.red },
    ["@variable.member"] = { fg = colors.git_add },
    ["@variable.parameter"] = { fg = colors.gold },
    ["@variable.parameter.builtin"] = { fg = Util.blend_bg(colors.gold, 0.8) },
  }

  local rainbow_colors = {
    colors.red,
    colors.gold,
    colors.git_add,
    colors.blue,
    colors.purple,
    colors.type,
  }
  for i, color in ipairs(rainbow_colors) do
    ret["@markup.heading." .. i .. ".markdown"] = { fg = color, bold = true }
  end

  return ret
end

return M
