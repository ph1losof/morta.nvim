local Util = require("morta.util")

local M = {}

M.name = "render_markdown"
M.url = "https://github.com/MeanderingProgrammer/render-markdown.nvim"

---@type fun(colors: table, opts: table): table
function M.get(c, _opts)
  -- stylua: ignore
  local ret = {
    RenderMarkdownBullet     = { fg = c.gold },
    RenderMarkdownCode       = { bg = c.bg_dark },
    RenderMarkdownDash       = { fg = c.gold },
    RenderMarkdownTableHead  = { fg = c.red },
    RenderMarkdownTableRow   = { fg = c.gold },
    RenderMarkdownCodeInline = "@markup.raw.markdown_inline",
  }

  local heading_colors = {
    c.blue, -- H1
    c.purple, -- H2
    c.gold, -- H3
    c.string, -- H4
    c.type, -- H5
    c.red, -- H6
  }

  for i, color in ipairs(heading_colors) do
    ret["RenderMarkdownH" .. i .. "Fg"] = { fg = color, bold = true }
  end
  return ret
end

return M
