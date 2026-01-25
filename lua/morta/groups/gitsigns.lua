local M = {}

M.url = "https://github.com/lewis6991/gitsigns.nvim"

function M.get(colors, config)
  return {
    GitSignsAdd = { fg = colors.git_add, bold = true }, -- diff mode: Added line
    GitSignsChange = { fg = colors.git_change }, -- diff mode: Changed line
    GitSignsDelete = { fg = colors.git_delete, bold = true }, -- diff mode: Deleted line (uses error color)
  }
end

return M
