local M = {}

-- Get all highlights without applying them
function M.get_highlights(colors, config)
  local highlights = {}

  -- Helper function to add highlight
  local function add_hl(group, opts)
    highlights[group] = opts
  end

  -- Editor highlights (Enhanced Core UI)
  add_hl("Normal", { fg = colors.fg, bg = config.transparent_background and colors.none or colors.bg })
  add_hl("NormalFloat", { fg = colors.fg, bg = colors.bg_dark })
  add_hl("Cursor", { fg = colors.bg, bg = colors.purple }) -- Grape lollipop cursor
  add_hl("CursorLine", { bg = colors.bg_highlight })
  add_hl("CursorColumn", { bg = colors.bg_highlight })
  add_hl("ColorColumn", { bg = colors.bg_highlight })
  add_hl("LineNr", { fg = colors.fg_gutter })
  add_hl("CursorLineNr", { fg = colors.purple, bold = true }) -- Grape accent
  add_hl("VertSplit", { fg = colors.border })
  add_hl("Folded", { fg = colors.purple, bg = colors.bg_highlight, italic = true })
  add_hl("FoldColumn", { fg = colors.fg_gutter })
  add_hl("SignColumn", { bg = config.transparent_background and colors.none or colors.bg })
  add_hl("MatchParen", { fg = colors.gold, bg = colors.bg_highlight, bold = true, underline = true }) -- Candy corn highlight
  add_hl("StatusLine", { fg = colors.fg, bg = colors.bg_dark, bold = true })
  add_hl("StatusLineNC", { fg = colors.fg_dark, bg = colors.bg_dark })
  add_hl("Search", { fg = colors.bg, bg = colors.gold, bold = true }) -- Candy corn search
  add_hl("IncSearch", { fg = colors.bg, bg = colors.purple, bold = true }) -- Grape highlight
  add_hl("Visual", { bg = colors.selection })
  add_hl("Directory", { fg = colors.blue, bold = true }) -- Blue raspberry

  -- Enhanced Diff highlights with candy colors
  add_hl("DiffAdd", { fg = colors.string, bg = colors.bg_highlight, bold = true }) -- Lime candy
  add_hl("DiffChange", { fg = colors.blue, bg = colors.bg_highlight }) -- Blue raspberry
  add_hl("DiffDelete", { fg = colors.red, bg = colors.bg_highlight, bold = true }) -- Cherry
  add_hl("DiffText", { fg = colors.purple, bg = colors.bg_highlight, bold = true }) -- Grape

  -- Refined Popup menu with candy theme
  add_hl("Pmenu", { fg = colors.fg, bg = colors.bg_dark })
  add_hl("PmenuSel", { fg = colors.fg, bg = colors.selection, bold = true })
  add_hl("PmenuSbar", { bg = colors.bg_highlight })
  add_hl("PmenuThumb", { bg = colors.purple }) -- Grape scrollbar

  -- Enhanced Tab line with candy accents
  add_hl("TabLine", { fg = colors.fg_dark, bg = colors.bg_dark })
  add_hl("TabLineSel", { fg = colors.purple, bg = colors.bg, bold = true }) -- Grape accent
  add_hl("TabLineFill", { bg = colors.bg_dark })

  -- Improved UI Elements with candy theme
  add_hl("WildMenu", { fg = colors.fg, bg = colors.selection, bold = true })
  add_hl("QuickFixLine", { bg = colors.bg_highlight, bold = true })
  add_hl("SpellBad", { undercurl = true, sp = colors.red }) -- Cherry error
  add_hl("SpellCap", { undercurl = true, sp = colors.gold }) -- Candy corn warning
  add_hl("SpellRare", { undercurl = true, sp = colors.purple }) -- Grape rare
  add_hl("SpellLocal", { undercurl = true, sp = colors.blue }) -- Blue raspberry info
  add_hl("NonText", { fg = colors.fg_gutter })
  add_hl("SpecialKey", { fg = colors.purple }) -- Grape special

  -- Enhanced Syntax highlights with candy colors
  add_hl("Comment", { fg = colors.comment, italic = config.styles.comments.italic, bold = config.styles.comments.bold })
  add_hl("Constant", { fg = colors.constant, bold = config.styles.constants.bold }) -- Orange cream
  add_hl("String", { fg = colors.string, italic = config.styles.strings.italic }) -- Lime candy
  add_hl("Character", { fg = colors.string })
  add_hl("Number", { fg = colors.gold, bold = config.styles.constants.bold }) -- Candy corn
  add_hl("Boolean", { fg = colors.purple, bold = config.styles.constants.bold }) -- Grape
  add_hl("Float", { fg = colors.gold, bold = config.styles.constants.bold }) -- Candy corn
  add_hl("Identifier", { fg = colors.blue, italic = config.styles.variables.italic }) -- Blue raspberry
  add_hl("Function", { fg = colors.func, bold = config.styles.functions.bold, italic = config.styles.functions.italic })
  add_hl("Statement", { fg = colors.keyword, bold = config.styles.keywords.bold }) -- Cherry
  add_hl(
    "Conditional",
    { fg = colors.purple, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold }
  )
  add_hl("Repeat", { fg = colors.purple, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold })
  add_hl("Label", { fg = colors.gold, bold = config.styles.keywords.bold }) -- Candy corn
  add_hl("Operator", { fg = colors.purple }) -- Grape
  add_hl("Keyword", { fg = colors.keyword, italic = config.styles.keywords.italic, bold = config.styles.keywords.bold })
  add_hl("Exception", { fg = colors.red, bold = true }) -- Cherry error
  add_hl("PreProc", { fg = colors.blue, bold = true }) -- Blue raspberry
  add_hl("Include", { fg = colors.purple, bold = true }) -- Grape include
  add_hl("Define", { fg = colors.purple, bold = true }) -- Grape define
  add_hl("Title", { fg = colors.gold, bold = true }) -- Candy corn
  add_hl("Type", { fg = colors.type, bold = config.styles.types.bold, italic = config.styles.types.italic }) -- Mint chocolate
  add_hl("StorageClass", { fg = colors.gold, bold = config.styles.types.bold }) -- Candy corn
  add_hl("Structure", { fg = colors.gold, bold = config.styles.types.bold }) -- Candy corn
  add_hl("Special", { fg = colors.purple, bold = true }) -- Grape special
  add_hl("SpecialComment", { fg = colors.comment, italic = true, bold = config.styles.comments.bold })
  add_hl("Error", { fg = colors.error, bold = true }) -- Cherry error
  add_hl("Todo", { fg = colors.gold, bold = true }) -- Candy corn warning
  add_hl("Underlined", { underline = true })

  -- Enhanced LSP highlights with candy theme
  add_hl("DiagnosticError", { fg = colors.error, bold = true }) -- Cherry error
  add_hl("DiagnosticWarn", { fg = colors.gold, bold = true }) -- Candy corn warning
  add_hl("DiagnosticInfo", { fg = colors.info }) -- Blue raspberry info
  add_hl("DiagnosticHint", { fg = colors.hint }) -- Mint hint
  add_hl("DiagnosticUnderlineError", { undercurl = true, sp = colors.error })
  add_hl("DiagnosticUnderlineWarn", { undercurl = true, sp = colors.gold }) -- Candy corn warning
  add_hl("DiagnosticUnderlineInfo", { undercurl = true, sp = colors.info })
  add_hl("DiagnosticUnderlineHint", { undercurl = true, sp = colors.hint })
  add_hl("DiagnosticVirtualTextError", { fg = colors.error, bg = colors.bg_highlight, bold = true })
  add_hl("DiagnosticVirtualTextWarn", { fg = colors.gold, bg = colors.bg_highlight, bold = true }) -- Candy corn warning
  add_hl("DiagnosticVirtualTextInfo", { fg = colors.info, bg = colors.bg_highlight })
  add_hl("DiagnosticVirtualTextHint", { fg = colors.hint, bg = colors.bg_highlight })
  add_hl("LspReferenceText", { bg = colors.bg_highlight })
  add_hl("LspReferenceRead", { bg = colors.bg_highlight })
  add_hl("LspReferenceWrite", { bg = colors.bg_highlight, bold = true })

  -- Enhanced TreeSitter highlights with candy theme
  add_hl("@variable", { fg = colors.variable, italic = config.styles.variables.italic }) -- Cotton candy
  add_hl("@field", { fg = colors.blue }) -- Blue raspberry
  add_hl("@property", { fg = colors.func }) -- Blue raspberry
  add_hl("@parameter", { fg = colors.gold, italic = true }) -- Candy corn
  add_hl("@function.builtin", { fg = colors.purple, bold = true }) -- Grape
  add_hl("@constructor", { fg = colors.gold, bold = true }) -- Candy corn
  add_hl("@tag", { fg = colors.blue, bold = true }) -- Blue raspberry
  add_hl("@tag.attribute", { fg = colors.purple }) -- Grape
  add_hl("@tag.delimiter", { fg = colors.fg_dark })
  add_hl("@punctuation", { fg = colors.purple }) -- Grape
  add_hl("@string.escape", { fg = colors.red, bold = true }) -- Cherry escape
  add_hl("@text.emphasis", { italic = true })
  add_hl("@text.strong", { bold = true })
  add_hl("@text.uri", { fg = colors.func, underline = true }) -- Blue raspberry
  add_hl("@text.title", { fg = colors.gold, bold = true }) -- Candy corn
  add_hl("@text.literal", { fg = colors.string, bg = colors.bg_highlight }) -- Lime candy
  add_hl("@text.reference", { fg = colors.purple, underline = true }) -- Grape

  -- Git highlights with candy theme
  add_hl("GitSignsAdd", { fg = colors.string, bold = true }) -- Lime candy
  add_hl("GitSignsChange", { fg = colors.git_change }) -- Candy corn
  add_hl("GitSignsDelete", { fg = colors.red, bold = true }) -- Cherry
  add_hl("GitSignsCurrentLineBlame", { fg = colors.comment, italic = true })

  -- Load plugin integrations
  local plugin_highlights = require("morta.groups").load(colors, config)
  for group, opts in pairs(plugin_highlights) do
    add_hl(group, opts)
  end

  return highlights
end

-- Apply highlights
function M.setup(colors, config)
  local highlights = M.get_highlights(colors, config)
  for group, opts in pairs(highlights) do
    vim.api.nvim_set_hl(0, group, opts)
  end
end

return M

