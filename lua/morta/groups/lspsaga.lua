local M = {}

M.url = "https://github.com/glepnir/lspsaga.nvim"

function M.get(colors, config)
  return {
    DefinitionCount = { fg = colors.purple },
    DefinitionIcon = { fg = colors.blue },
    DiagnosticInformation = "DiagnosticInfo",
    DiagnosticWarning = "DiagnosticWarn",
    LspFloatWinBorder = { fg = colors.border },
    LspFloatWinNormal = { bg = colors.bg_float },
    LspSagaBorderTitle = { fg = colors.cyan },
    LspSagaCodeActionBorder = { fg = colors.blue },
    LspSagaCodeActionContent = { fg = colors.purple },
    LspSagaCodeActionTitle = { fg = colors.blue },
    LspSagaDefPreviewBorder = { fg = colors.green },
    LspSagaFinderSelection = { fg = colors.selection },
    LspSagaHoverBorder = { fg = colors.blue },
    LspSagaRenameBorder = { fg = colors.green },
    LspSagaSignatureHelpBorder = { fg = colors.red },
    ReferencesCount = { fg = colors.purple },
    ReferencesIcon = { fg = colors.blue },
    TargetWord = { fg = colors.cyan },

    SagaFileName = { fg = colors.fg },
    SagaFolderName = { fg = colors.gold },
    SagaFolder = { fg = colors.gold },

    SagaWinbar = { bg = colors.bg_float, fg = colors.fg },
    SagaWinbarSep = { bg = colors.bg_float, fg = colors.border },
    SagaWinbarFileName = { bg = colors.bg_float, fg = colors.fg },
    SagaWinbarFolderName = { bg = colors.bg_float, fg = colors.gold },
    SagaWinbarFolder = { bg = colors.bg_float, fg = colors.gold },
    SagaWinbarFileIcon = { bg = colors.bg_float },
  }
end

return M
