local M = {}

M.name = "trouble"
M.url = "https://github.com/folke/trouble.nvim"

---@type fun(colors: table, config: table): table
function M.get(c, _config)
  -- stylua: ignore
  return {
    TroubleText   = { fg = c.fg_dark },
    TroubleCount  = { fg = c.purple, bg = c.fg_gutter },
    TroubleNormal = { fg = c.fg, bg = c.bg_dark },
  }
end

return M
