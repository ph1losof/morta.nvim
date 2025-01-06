local M = {}

function M.get_highlights(colors, config)
  local highlights = {}

  local function add_hl(group, opts)
    highlights[group] = opts
  end

  add_hl("Normal", { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg })
  add_hl("NormalFloat", { fg = colors.fg, bg = colors.bg_dark })
  add_hl("Cursor", { fg = colors.bg, bg = colors.purple })
  add_hl("CursorLine", { bg = colors.bg_highlight })
  add_hl("CursorColumn", { bg = colors.bg_highlight })
  add_hl("ColorColumn", { bg = colors.bg_highlight })
  add_hl("LineNr", { fg = colors.fg_gutter })
  add_hl("CursorLineNr", { fg = colors.gold, bold = true })
  add_hl("VertSplit", { fg = colors.border })
  add_hl("Folded", { fg = colors.purple, bg = colors.bg_highlight, italic = true })
  add_hl("FoldColumn", { fg = colors.fg_gutter })
  add_hl("SignColumn", { bg = config.transparent_background and colors.none or colors.bg })
  add_hl("MatchParen", { fg = colors.gold, bg = colors.bg_highlight, bold = true, underline = true })
  add_hl("StatusLine", { fg = colors.fg, bg = colors.bg_dark, bold = true })
  add_hl("StatusLineNC", { fg = colors.fg_dark, bg = colors.bg_dark })
  add_hl("Search", { fg = colors.bg, bg = colors.gold, bold = true })
  add_hl("IncSearch", { fg = colors.bg, bg = colors.purple, bold = true })
  add_hl("Visual", { bg = colors.selection })
  add_hl("Directory", { fg = colors.blue, bold = true })

  add_hl("DiffAdd", { fg = colors.string, bg = colors.bg_highlight, bold = true })
  add_hl("DiffChange", { fg = colors.blue, bg = colors.bg_highlight })
  add_hl("DiffDelete", { fg = colors.red, bg = colors.bg_highlight, bold = true })
  add_hl("DiffText", { fg = colors.purple, bg = colors.bg_highlight, bold = true })

  add_hl("Pmenu", { fg = colors.fg, bg = colors.bg_dark })
  add_hl("PmenuSel", { fg = colors.fg, bg = colors.selection, bold = true })
  add_hl("PmenuSbar", { bg = colors.bg_highlight })
  add_hl("PmenuThumb", { bg = colors.purple })

  add_hl("TabLine", { fg = colors.fg_dark, bg = colors.bg_dark })
  add_hl("TabLineSel", { fg = colors.purple, bg = colors.bg, bold = true })
  add_hl("TabLineFill", { bg = colors.bg_dark })

  add_hl("WildMenu", { fg = colors.fg, bg = colors.selection, bold = true })
  add_hl("QuickFixLine", { bg = colors.bg_highlight, bold = true })
  add_hl("SpellBad", { undercurl = true, sp = colors.red })
  add_hl("SpellCap", { undercurl = true, sp = colors.gold })
  add_hl("SpellRare", { undercurl = true, sp = colors.purple })
  add_hl("SpellLocal", { undercurl = true, sp = colors.blue })
  add_hl("NonText", { fg = colors.fg_gutter })
  add_hl("SpecialKey", { fg = colors.purple })

  add_hl("Comment", { fg = colors.comment, italic = config.styles.comments.italic, bold = config.styles.comments.bold })
  add_hl("Constant", { fg = colors.constant, bold = config.styles.constants.bold })
  add_hl("String", { fg = colors.string, italic = config.styles.strings.italic })
  add_hl("Character", { fg = colors.string })
  add_hl("Number", { fg = colors.gold, bold = config.styles.constants.bold })
  add_hl("Boolean", { fg = colors.purple, bold = config.styles.constants.bold })
  add_hl("Float", { fg = colors.gold, bold = config.styles.constants.bold })
  add_hl("Identifier", { fg = colors.blue, italic = config.styles.variables.italic })
  add_hl("Function", { fg = colors.func, bold = config.styles.functions.bold, italic = config.styles.functions.italic })
  add_hl("Statement", { fg = colors.keyword, bold = config.styles.keywords.bold })
  add_hl(
    "Conditional",
    { fg = colors.purple, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold }
  )
  add_hl("Repeat", { fg = colors.purple, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold })
  add_hl("Label", { fg = colors.gold, bold = config.styles.keywords.bold })
  add_hl("Operator", { fg = colors.purple })
  add_hl("Keyword", { fg = colors.keyword, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold })
  add_hl("Exception", { fg = colors.red, bold = true })
  add_hl("PreProc", { fg = colors.blue, bold = true })
  add_hl("Include", { fg = colors.purple, bold = true })
  add_hl("Define", { fg = colors.purple, bold = true })
  add_hl("Title", { fg = colors.gold, bold = true })
  add_hl("Type", { fg = colors.type, bold = config.styles.types.bold, italic = config.styles.types.italic })
  add_hl("StorageClass", { fg = colors.gold, bold = config.styles.types.bold })
  add_hl("Structure", { fg = colors.gold, bold = config.styles.types.bold })
  add_hl("Special", { fg = colors.purple, bold = true })
  add_hl("SpecialComment", { fg = colors.comment, italic = true, bold = config.styles.comments.bold })
  add_hl("Error", { fg = colors.error, bold = true })
  add_hl("Todo", { fg = colors.gold, bold = true })
  add_hl("Underlined", { underline = true })

  add_hl("DiagnosticError", { fg = colors.error, bold = true })
  add_hl("DiagnosticWarn", { fg = colors.gold, bold = true })
  add_hl("DiagnosticInfo", { fg = colors.info })
  add_hl("DiagnosticHint", { fg = colors.hint })
  add_hl("DiagnosticUnderlineError", { undercurl = true, sp = colors.error })
  add_hl("DiagnosticUnderlineWarn", { undercurl = true, sp = colors.gold })
  add_hl("DiagnosticUnderlineInfo", { undercurl = true, sp = colors.info })
  add_hl("DiagnosticUnderlineHint", { undercurl = true, sp = colors.hint })
  add_hl("DiagnosticVirtualTextError", { fg = colors.error, bg = colors.bg_highlight, bold = true })
  add_hl("DiagnosticVirtualTextWarn", { fg = colors.gold, bg = colors.bg_highlight, bold = true })
  add_hl("DiagnosticVirtualTextInfo", { fg = colors.info, bg = colors.bg_highlight })
  add_hl("DiagnosticVirtualTextHint", { fg = colors.hint, bg = colors.bg_highlight })
  add_hl("LspReferenceText", { bg = colors.bg_highlight })
  add_hl("LspReferenceRead", { bg = colors.bg_highlight })
  add_hl("LspReferenceWrite", { bg = colors.bg_highlight, bold = true })

  add_hl("@variable", { fg = colors.variable, italic = config.styles.variables.italic })
  add_hl("@field", { fg = colors.blue })
  add_hl("@property", { fg = colors.func })
  add_hl("@parameter", { fg = colors.gold, italic = true })
  add_hl("@function.builtin", { fg = colors.purple, bold = true })
  add_hl("@constructor", { fg = colors.gold, bold = true })
  add_hl("@tag", { fg = colors.blue, bold = true })
  add_hl("@tag.attribute", { fg = colors.purple })
  add_hl("@tag.delimiter", { fg = colors.fg_dark })
  add_hl("@punctuation", { fg = colors.purple })
  add_hl("@string.escape", { fg = colors.red, bold = true })
  add_hl("@text.emphasis", { italic = true })
  add_hl("@text.strong", { bold = true })
  add_hl("@text.uri", { fg = colors.func, underline = true })
  add_hl("@text.title", { fg = colors.gold, bold = true })
  add_hl("@text.literal", { fg = colors.string, bg = colors.bg_highlight })
  add_hl("@text.reference", { fg = colors.purple, underline = true })

  add_hl("GitSignsAdd", { fg = colors.string, bold = true })
  add_hl("GitSignsChange", { fg = colors.git_change })
  add_hl("GitSignsDelete", { fg = colors.red, bold = true })
  add_hl("GitSignsCurrentLineBlame", { fg = colors.comment, italic = true })

  local plugin_highlights = require("morta.groups").load(colors, config)
  for group, opts in pairs(plugin_highlights) do
    add_hl(group, opts)
  end

  return highlights
end

function M.setup(colors, config)
  local highlights = M.get_highlights(colors, config)
  for group, opts in pairs(highlights) do
    vim.api.nvim_set_hl(0, group, opts)
  end
end

return M
