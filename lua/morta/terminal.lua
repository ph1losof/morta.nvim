local M = {}

-- Set terminal colors
---@param colors table The color palette
function M.setup(colors)
  -- Terminal colors
  vim.g.terminal_color_0 = colors.bg_dark
  vim.g.terminal_color_8 = colors.bg_highlight

  vim.g.terminal_color_1 = colors.red
  vim.g.terminal_color_9 = colors.red

  vim.g.terminal_color_2 = colors.git_add
  vim.g.terminal_color_10 = colors.git_add

  vim.g.terminal_color_3 = colors.gold
  vim.g.terminal_color_11 = colors.gold

  vim.g.terminal_color_4 = colors.blue
  vim.g.terminal_color_12 = colors.blue

  vim.g.terminal_color_5 = colors.purple
  vim.g.terminal_color_13 = colors.purple

  vim.g.terminal_color_6 = colors.type
  vim.g.terminal_color_14 = colors.type

  vim.g.terminal_color_7 = colors.fg
  vim.g.terminal_color_15 = colors.fg_dark
end

return M

