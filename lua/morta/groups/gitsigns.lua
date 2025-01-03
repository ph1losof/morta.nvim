local M = {}
local Util = require("morta.util")

M.url = "https://github.com/lewis6991/gitsigns.nvim"

-- Get gitsigns.nvim highlights with soft candy theme
---@param colors table
---@param config table
function M.get(colors, config)
  return {

    GitSignsAdd = { fg = colors.string },
    GitSignsChange = { fg = colors.git_change },
    GitSignsDelete = { fg = colors.red },

    GitSignsAddLn = { bg = Util.blend_bg(colors.string, 0.1) },
    GitSignsChangeLn = { bg = Util.blend_bg(colors.git_change, 0.1) },
    GitSignsDeleteLn = { bg = Util.blend_bg(colors.red, 0.1) },

    GitSignsAddNr = { fg = colors.string },
    GitSignsChangeNr = { fg = colors.git_change },
    GitSignsDeleteNr = { fg = colors.red },

    GitSignsAddPreview = { bg = Util.blend_bg(colors.string, 0.1) },
    GitSignsDeletePreview = { bg = Util.blend_bg(colors.red, 0.1) },

    GitSignsCurrentLineBlame = { fg = colors.comment, italic = true },

    GitSignsAddInline = { bg = Util.blend_bg(colors.string, 0.2) },
    GitSignsChangeInline = { bg = Util.blend_bg(colors.git_change, 0.2) },
    GitSignsDeleteInline = { bg = Util.blend_bg(colors.red, 0.2) },
  }
end

return M
