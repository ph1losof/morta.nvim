local M = {}

M.url = "https://github.com/glepnir/lspsaga.nvim"

-- Get lspsaga.nvim highlights with soft candy theme
---@param colors table
---@param config table
function M.get(colors, config)
  return {
    DefinitionCount = { fg = colors.purple, italic = true },
    DefinitionIcon = { fg = colors.blue },
    ReferencesCount = { fg = colors.purple, italic = true },
    ReferencesIcon = { fg = colors.blue },

    DiagnosticInformation = "DiagnosticInfo",
    DiagnosticWarning = "DiagnosticWarn",

    LspFloatWinBorder = { fg = colors.purple },
    LspFloatWinNormal = { bg = colors.bg_dark },

    LspSagaBorderTitle = { fg = colors.type, italic = true },
    LspSagaCodeActionBorder = { fg = colors.blue },
    LspSagaCodeActionContent = { fg = colors.purple },
    LspSagaCodeActionTitle = { fg = colors.blue, italic = true },
    LspSagaDefPreviewBorder = { fg = colors.string },
    LspSagaFinderSelection = { bg = colors.selection },
    LspSagaHoverBorder = { fg = colors.blue },
    LspSagaRenameBorder = { fg = colors.string },
    LspSagaSignatureHelpBorder = { fg = colors.red },

    TargetWord = { fg = colors.type, italic = true },

    LspSagaDiagnosticBorder = { fg = colors.purple },
    LspSagaDiagnosticHeader = { fg = colors.gold, italic = true },
    LspSagaDiagnosticTruncateLine = { fg = colors.purple },
    LspSagaDocTruncateLine = { fg = colors.purple },
    LspSagaFinderPreview = { fg = colors.string },
    LspSagaLspFinderBorder = { fg = colors.blue },
    LspSagaShTruncateLine = { fg = colors.purple },
    LspSagaSignatureHelpTruncateLine = { fg = colors.purple },
  }
end

return M

