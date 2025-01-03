local M = {}

M.url = "https://github.com/folke/lazy.nvim"

-- Get lazy.nvim highlights
---@param colors table
---@param config table
function M.get(colors, config)
  return {
    LazyProgressDone = { bold = true, fg = colors.purple },
    LazyProgressTodo = { bold = true, fg = colors.fg_gutter },

    LazyH1 = { fg = colors.gold, bold = true },
    LazyButton = { fg = colors.fg_dark, bg = colors.bg_highlight },
    LazyButtonActive = { fg = colors.fg, bg = colors.bg_highlight, bold = true },
    LazySpecial = { fg = colors.blue },
    LazyComment = { fg = colors.comment },
    LazyValue = { fg = colors.purple },
    LazyNoCond = { fg = colors.red },
    LazyLocal = { fg = colors.gold },
    LazyDimmed = { fg = colors.fg_dark },
    LazyUrl = { fg = colors.blue, underline = true },
    LazyReasonPlugin = { fg = colors.purple },
    LazyReasonRuntime = { fg = colors.gold },
    LazyReasonEvent = { fg = colors.gold },
    LazyReasonStart = { fg = colors.blue },
    LazyReasonCmd = { fg = colors.purple },
    LazyReasonSource = { fg = colors.blue },
    LazyReasonFt = { fg = colors.blue },
    LazyReasonImport = { fg = colors.blue },
    LazyReasonRequire = { fg = colors.blue },
    LazyReasonKeys = { fg = colors.purple },
  }
end

return M
