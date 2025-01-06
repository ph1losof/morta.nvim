local M = {}

function M.get(colors, config)
  return {
    -- Base
    ["@variable"] = { fg = colors.variable, italic = config.styles.variables.italic },
    ["@variable.builtin"] = { fg = colors.red, bold = true },
    ["@variable.parameter"] = { fg = colors.fg },
    ["@variable.member"] = { fg = colors.blue },

    -- Keywords
    ["@keyword"] = { fg = colors.keyword, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold },
    ["@keyword.function"] = {
      fg = colors.keyword,
      italic = config.styles.functions.italic,
      bold = config.styles.functions.bold,
    },
    ["@keyword.operator"] = { fg = colors.purple },
    ["@keyword.return"] = {
      fg = colors.keyword,
      italic = config.styles.keywords.italic,
      bold = config.styles.keywords.bold,
    },
    ["@keyword.conditional"] = {
      fg = colors.purple,
      italic = config.styles.keywords.italic,
      bold = config.styles.keywords.bold,
    },
    ["@keyword.repeat"] = {
      fg = colors.purple,
      italic = config.styles.keywords.italic,
      bold = config.styles.keywords.bold,
    },
    ["@keyword.import"] = { fg = colors.purple, bold = true },
    ["@keyword.storage"] = { fg = colors.gold, bold = config.styles.types.bold },
    ["@keyword.debug"] = { fg = colors.red, bold = true },
    ["@keyword.exception"] = { fg = colors.red, bold = true },

    -- Functions
    ["@function"] = { fg = colors.func, bold = config.styles.functions.bold, italic = config.styles.functions.italic },
    ["@function.builtin"] = { fg = colors.purple, bold = true },
    ["@function.call"] = { fg = colors.func, bold = config.styles.functions.bold },
    ["@function.method"] = { fg = colors.func, bold = config.styles.functions.bold },
    ["@function.method.call"] = { fg = colors.func, bold = config.styles.functions.bold },
    ["@constructor"] = { fg = colors.gold, bold = true },
    ["@parameter"] = { fg = colors.fg },

    -- Types
    ["@type"] = { fg = colors.type, bold = config.styles.types.bold, italic = config.styles.types.italic },
    ["@type.builtin"] = { fg = colors.type, bold = config.styles.types.bold },
    ["@type.definition"] = { fg = colors.type, bold = config.styles.types.bold },
    ["@type.qualifier"] = { fg = colors.keyword, bold = config.styles.keywords.bold },

    -- Punctuation
    ["@punctuation.bracket"] = { fg = colors.fg_dark },
    ["@punctuation.delimiter"] = { fg = colors.purple },
    ["@punctuation.special"] = { fg = colors.purple },

    -- Constants
    ["@constant"] = { fg = colors.constant, bold = config.styles.constants.bold },
    ["@constant.builtin"] = { fg = colors.purple, bold = config.styles.constants.bold },
    ["@constant.macro"] = { fg = colors.purple, bold = true },
    ["@string"] = { fg = colors.string, italic = config.styles.strings.italic },
    ["@string.escape"] = { fg = colors.red, bold = true },
    ["@string.regexp"] = { fg = colors.blue, bold = true },
    ["@string.documentation"] = { fg = colors.yellow },
    ["@character"] = { fg = colors.string },
    ["@character.special"] = { fg = colors.purple },
    ["@boolean"] = { fg = colors.purple, bold = config.styles.constants.bold },
    ["@number"] = { fg = colors.gold, bold = config.styles.constants.bold },
    ["@number.float"] = { fg = colors.gold, bold = config.styles.constants.bold },

    -- Comments
    ["@comment"] = { fg = colors.comment, italic = config.styles.comments.italic, bold = config.styles.comments.bold },
    ["@comment.error"] = { fg = colors.error, bold = true },
    ["@comment.warning"] = { fg = colors.gold, bold = true },
    ["@comment.hint"] = { fg = colors.hint },
    ["@comment.info"] = { fg = colors.info },
    ["@comment.todo"] = { fg = colors.gold, bold = true },
    ["@comment.note"] = { fg = colors.hint },

    -- Tags
    ["@tag"] = { fg = colors.blue, bold = true },
    ["@tag.attribute"] = { fg = colors.purple },
    ["@tag.delimiter"] = { fg = colors.blue },
    ["@text.html"] = { fg = colors.fg },
    ["@text.jsx"] = { fg = colors.fg },
    ["@text.tsx"] = { fg = colors.fg },

    -- Markup
    ["@text.emphasis"] = { italic = true },
    ["@text.strong"] = { bold = true },
    ["@text.uri"] = { fg = colors.func, underline = true },
    ["@text.title"] = { fg = colors.gold, bold = true },
    ["@text.literal"] = { fg = colors.string, bg = colors.bg_highlight },
    ["@text.reference"] = { fg = colors.purple, underline = true },

    -- Diffs
    ["@diff.plus"] = { fg = colors.string, bold = true },
    ["@diff.minus"] = { fg = colors.red, bold = true },
    ["@diff.delta"] = { fg = colors.git_change },
  }
end

return M

