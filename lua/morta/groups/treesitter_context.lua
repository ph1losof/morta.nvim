local M = {}

M.url = "https://github.com/nvim-treesitter/nvim-treesitter-context"

function M.get(colors, config)
  return {
    TreesitterContext = { bg = colors.bg_highlight },
  }
end

return M

