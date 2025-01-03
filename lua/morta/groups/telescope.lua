local M = {}

M.url = "https://github.com/nvim-telescope/telescope.nvim"

-- Get telescope.nvim highlights
---@param colors table
---@param config table
function M.get(colors, config)
  return {

    TelescopeBorder = { fg = colors.purple, bg = colors.bg_dark },
    TelescopeNormal = { fg = colors.fg, bg = colors.bg_dark },
    TelescopePromptBorder = { fg = colors.gold, bg = colors.bg_dark },
    TelescopePromptTitle = { fg = colors.gold, bg = colors.bg_dark, italic = true },
    TelescopeResultsTitle = { fg = colors.blue, bg = colors.bg_dark, italic = true },
    TelescopePreviewTitle = { fg = colors.purple, bg = colors.bg_dark, italic = true },
    TelescopeResultsComment = { fg = colors.comment, italic = true },

    TelescopePromptNormal = { fg = colors.fg, bg = colors.bg_dark },
    TelescopePromptPrefix = { fg = colors.gold, italic = true },
    TelescopePromptCounter = { fg = colors.type, italic = true },

    TelescopeResultsNormal = { fg = colors.fg, bg = colors.bg_dark },
    TelescopeSelectionCaret = { fg = colors.red, bg = colors.selection },
    TelescopeSelection = { bg = colors.selection },
    TelescopeMatching = { fg = colors.gold, italic = true },

    TelescopePreviewNormal = { fg = colors.fg, bg = colors.bg_dark },
    TelescopePreviewBorder = { fg = colors.purple, bg = colors.bg_dark },
    TelescopePreviewLine = { bg = colors.bg_highlight },
    TelescopePreviewMatch = { fg = colors.gold, bg = colors.selection },

    TelescopeMultiSelection = { bg = colors.bg_highlight },
    TelescopeMultiIcon = { fg = colors.red, italic = true },
  }
end

return M

