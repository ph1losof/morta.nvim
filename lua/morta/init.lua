local M = {}

local defaults = {
  transparent_background = false,
  use_compiled = true,
  terminal_colors = false,
  styles = {
    comments = { italic = true, bold = false },
    keywords = { italic = true, bold = true },
    functions = { italic = false, bold = true },
    variables = { italic = false, bold = false },
    strings = { italic = false, bold = false },
    types = { italic = false, bold = true },
    constants = { italic = false, bold = true },
  },
  inverse = {
    match_paren = false,
    visual = false,
    search = false,
  },
  plugins = {
    cmp = true,
    treesitter = true,
    treesitter_context = true,
    lspsaga = true,
    trouble = true,
    lazy = true,
    blink_cmp = true,
    gitsigns = true,
    snacks = true,
    hipatterns = true,
  },
}

local function extend(table1, table2)
  local result = vim.deepcopy(table1)
  for k, v in pairs(table2) do
    if type(v) == "table" then
      result[k] = extend(result[k] or {}, v)
    else
      result[k] = v
    end
  end
  return result
end

function M.setup(opts)
  opts = opts or {}
  M.config = extend(defaults, opts)

  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then
    vim.cmd("syntax reset")
  end

  vim.g.colors_name = "morta"

  if M.config.use_compiled then
    local compiler = require("morta.compiler")
    local success = compiler.load_compiled()

    if not success then
      local palette = require("morta.palette")
      compiler.compile(palette.colors, M.config)
      success = compiler.load_compiled()
    end

    if not success then
      M.load_dynamic()
    end
  else
    M.load_dynamic()
  end
end

function M.load_dynamic()
  local palette = require("morta.palette")
  local highlights = require("morta.highlights")
  highlights.setup(palette.colors, M.config)

  if M.config and M.config.terminal_colors == true then
    local terminal = require("morta.terminal")
    terminal.setup(palette.colors)
  end
end

---@param plugin string
---@return boolean
function M.plugin_enabled(plugin)
  return M.config and M.config.plugins and M.config.plugins[plugin] == true
end

return M
