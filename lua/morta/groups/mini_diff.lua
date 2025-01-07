local M = {}

M.url = "https://github.com/echasnovski/mini.diff"
M.name = "mini_diff"

---@type fun(colors: table, opts: table): table
function M.get(c)
  -- stylua: ignore
  return {
    MiniDiffOverAdd     = "DiffAdd",
    MiniDiffOverChange  = "DiffText",
    MiniDiffOverContext = "DiffChange",
    MiniDiffOverDelete  = "DiffDelete",
    MiniDiffSignAdd     = { fg = c.git_add },
    MiniDiffSignChange  = { fg = c.git_change },
    MiniDiffSignDelete  = { fg = c.git_delete },
  }
end

return M
