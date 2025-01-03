local M = {}

M.url = "https://github.com/supermaven-inc/supermaven-nvim"

-- Get supermaven-nvim highlights
---@param colors table
---@param config table
function M.get(colors, config)
  return {
    SupermavenSuggestion = { fg = colors.comment },

    SupermavenInline = { fg = colors.comment, italic = true },
    SupermavenBorder = { fg = colors.border, bg = colors.bg_dark },
    SupermavenFloating = { bg = colors.bg_dark },
    SupermavenSelected = { bg = colors.selection },
  }
end

return M

