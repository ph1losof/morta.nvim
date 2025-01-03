local M = {}
local Util = require("morta.util")

M.url = "https://github.com/nvim-treesitter/nvim-treesitter-context"

---@param colors table
---@param config table
function M.get(colors, config)
  return {

    TreesitterContext = { bg = Util.blend_bg(colors.purple, 0.1) },
    TreesitterContextLineNumber = { fg = colors.purple, italic = true },

    TreesitterContextBottom = { underline = true, sp = colors.gold },
    TreesitterContextSeparator = { fg = colors.purple },
  }
end

return M
