local M = {}

M.url = "https://github.com/lewis6991/gitsigns.nvim"

function M.get(colors, config)
  return {
    GitSignsAdd = { fg = colors.string, bold = true }, -- diff mode: Added line
    GitSignsChange = { fg = colors.git_change }, -- diff mode: Changed line
    GitSignsDelete = { fg = colors.red, bold = true }, -- diff mode: Deleted line
  }
end

return M
