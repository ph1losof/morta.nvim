local M = {}

M.url = "https://github.com/echasnovski/mini.hipatterns"

-- Get mini.hipatterns highlights
---@param colors table
---@param config table
function M.get(colors, config)
  return {
    MiniHipatternsFixme = { fg = colors.bg, bg = colors.error, bold = true },
    MiniHipatternsHack = { fg = colors.bg, bg = colors.warning, bold = true },
    MiniHipatternsNote = { fg = colors.bg, bg = colors.hint, bold = true },
    MiniHipatternsTodo = { fg = colors.bg, bg = colors.info, bold = true },
  }
end

return M

