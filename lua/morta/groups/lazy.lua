local M = {}

M.url = "https://github.com/folke/lazy.nvim"

function M.get(colors, config)
  return {
    LazyProgressDone = { bold = true, fg = colors.magenta },
    LazyProgressTodo = { bold = true, fg = colors.gray },
  }
end

return M

