-- chrometric_export.lua
-- Universal colorscheme extractor for the Chrometric framework
-- Resolves semantic tokens via nvim_get_hl() with Treesitter-first, legacy fallback

-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    lazypath,
  })
end
vim.opt.runtimepath:prepend(lazypath)

require("lazy").setup({
  { "ph1losof/morta.nvim", branch = "2.0" },
  { "rebelot/kanagawa.nvim" },
  { "folke/tokyonight.nvim" },
  { "catppuccin/nvim", name = "catppuccin" },
  { "Mofiqul/dracula.nvim", name = "dracula" },
  { "morhetz/gruvbox", name = "gruvbox" },
  { "rose-pine/neovim", name = "rose-pine" },
  { "nvim-treesitter/nvim-treesitter" },
}, {
  ui = { custom_handler = function() end },
})

-------------------------------------------------------
-- Chrometric Universal Extractor
-------------------------------------------------------

-- Semantic token definitions with fallback chain
-- Priority order: Treesitter -> LSP -> Legacy vim highlights
local SEMANTIC_TOKENS = {
  -- Core syntax tokens
  ["bg"]        = { { "Normal", "bg" } },
  ["fg"]        = { { "Normal", "fg" } },
  ["keyword"]   = { { "@keyword", "fg" }, { "@keyword.return", "fg" }, { "Statement", "fg" }, { "Keyword", "fg" } },
  ["string"]    = { { "@string", "fg" }, { "String", "fg" } },
  ["function"]  = { { "@function", "fg" }, { "@function.call", "fg" }, { "Function", "fg" } },
  ["variable"]  = { { "@variable", "fg" }, { "@lsp.type.variable", "fg" }, { "Identifier", "fg" } },
  ["type"]      = { { "@type", "fg" }, { "@lsp.type.type", "fg" }, { "Type", "fg" } },
  ["constant"]  = { { "@constant", "fg" }, { "Constant", "fg" } },
  ["comment"]   = { { "@comment", "fg" }, { "Comment", "fg" } },
  ["operator"]  = { { "@operator", "fg" }, { "Operator", "fg" } },
  ["number"]    = { { "@number", "fg" }, { "Number", "fg" } },
  ["boolean"]   = { { "@boolean", "fg" }, { "Boolean", "fg" } },
  ["property"]  = { { "@property", "fg" }, { "@field", "fg" }, { "Identifier", "fg" } },
  ["parameter"] = { { "@parameter", "fg" }, { "@lsp.type.parameter", "fg" }, { "Identifier", "fg" } },
  ["namespace"] = { { "@namespace", "fg" }, { "@module", "fg" }, { "Include", "fg" } },
  ["punctuation"] = { { "@punctuation.bracket", "fg" }, { "@punctuation.delimiter", "fg" }, { "Delimiter", "fg" } },

  -- Diagnostic colors
  ["error"]     = { { "DiagnosticError", "fg" }, { "Error", "fg" } },
  ["warning"]   = { { "DiagnosticWarn", "fg" }, { "WarningMsg", "fg" } },
  ["info"]      = { { "DiagnosticInfo", "fg" }, { "MoreMsg", "fg" } },
  ["hint"]      = { { "DiagnosticHint", "fg" }, { "Comment", "fg" } },

  -- UI elements
  ["cursor_line"]   = { { "CursorLine", "bg" } },
  ["cursor_column"] = { { "CursorColumn", "bg" } },
  ["line_nr"]       = { { "LineNr", "fg" } },
  ["line_nr_cur"]   = { { "CursorLineNr", "fg" } },
  ["popup_bg"]      = { { "NormalFloat", "bg" }, { "Pmenu", "bg" } },
  ["popup_fg"]      = { { "NormalFloat", "fg" }, { "Pmenu", "fg" } },
  ["popup_sel"]     = { { "PmenuSel", "bg" } },
  ["visual"]        = { { "Visual", "bg" } },
  ["search"]        = { { "Search", "bg" } },
  ["inc_search"]    = { { "IncSearch", "bg" } },
  ["status_line"]   = { { "StatusLine", "bg" } },
  ["status_line_nc"]= { { "StatusLineNC", "bg" } },
  ["vert_split"]    = { { "VertSplit", "fg" }, { "WinSeparator", "fg" } },
  ["fold"]          = { { "Folded", "bg" } },
  ["sign_column"]   = { { "SignColumn", "bg" } },

  -- Diff colors
  ["diff_add"]      = { { "DiffAdd", "bg" }, { "Added", "fg" } },
  ["diff_delete"]   = { { "DiffDelete", "bg" }, { "Removed", "fg" } },
  ["diff_change"]   = { { "DiffChange", "bg" }, { "Changed", "fg" } },

  -- Git signs (if available)
  ["git_add"]       = { { "GitSignsAdd", "fg" }, { "diffAdded", "fg" }, { "DiffAdd", "fg" } },
  ["git_delete"]    = { { "GitSignsDelete", "fg" }, { "diffRemoved", "fg" }, { "DiffDelete", "fg" } },
  ["git_change"]    = { { "GitSignsChange", "fg" }, { "diffChanged", "fg" }, { "DiffChange", "fg" } },
}

-- Convert integer color to hex string
local function int_to_hex(int)
  if type(int) == "number" then
    return string.format("#%06x", int)
  end
  return nil
end

-- Resolve a single highlight group attribute
local function resolve_hl_attr(group, attr)
  local ok, hl = pcall(vim.api.nvim_get_hl, 0, { name = group, link = false })
  if not ok or not hl then
    return nil
  end

  local value = hl[attr]
  if value then
    return int_to_hex(value)
  end

  -- Handle linked groups by following the chain
  if hl.link then
    return resolve_hl_attr(hl.link, attr)
  end

  return nil
end

-- Resolve a semantic token using its fallback chain
local function resolve_semantic_token(token_name)
  local fallback_chain = SEMANTIC_TOKENS[token_name]
  if not fallback_chain then
    return nil
  end

  for _, spec in ipairs(fallback_chain) do
    local group, attr = spec[1], spec[2]
    local color = resolve_hl_attr(group, attr)
    if color then
      return color
    end
  end

  return nil
end

-- Extract all semantic colors for the current colorscheme
local function extract_colors()
  local colors = {}

  for token_name, _ in pairs(SEMANTIC_TOKENS) do
    local color = resolve_semantic_token(token_name)
    if color then
      colors[token_name] = color
    end
  end

  return colors
end

-- Get metadata about the colorscheme
local function get_metadata()
  local bg = vim.o.background or "dark"
  local termguicolors = vim.o.termguicolors

  return {
    background = bg,
    termguicolors = termguicolors,
    nvim_version = vim.version().major .. "." .. vim.version().minor .. "." .. vim.version().patch,
  }
end

-- Export a single colorscheme
local function export_scheme(scheme_name)
  local ok = pcall(vim.cmd.colorscheme, scheme_name)
  if not ok then
    return nil
  end

  -- Small delay to ensure highlight groups are fully loaded
  vim.cmd("redraw")

  local colors = extract_colors()
  local metadata = get_metadata()

  -- Only return if we got meaningful colors
  if not colors.bg or not colors.fg then
    return nil
  end

  return {
    name = scheme_name,
    colors = colors,
    metadata = metadata,
  }
end

-- List of colorschemes to export
local COLORSCHEMES = {
  -- Morta
  "morta",

  -- Kanagawa variants
  "kanagawa",
  "kanagawa-wave",
  "kanagawa-dragon",
  "kanagawa-lotus",

  -- Tokyo Night variants
  "tokyonight",
  "tokyonight-night",
  "tokyonight-storm",
  "tokyonight-moon",
  "tokyonight-day",

  -- Catppuccin variants
  "catppuccin",
  "catppuccin-latte",
  "catppuccin-frappe",
  "catppuccin-macchiato",
  "catppuccin-mocha",

  -- Others
  "dracula",
  "gruvbox",
  "rose-pine",
  "rose-pine-main",
  "rose-pine-moon",
  "rose-pine-dawn",
}

-- Export all colorschemes to JSON file
local function export_all()
  local results = {}

  for _, scheme in ipairs(COLORSCHEMES) do
    local ok, data = pcall(export_scheme, scheme)
    if ok and data then
      table.insert(results, data)
    end
  end

  -- Write to file
  local json_str = vim.json.encode(results)
  local file = io.open("chrometric_data.json", "w")
  if file then
    file:write(json_str)
    file:close()
    io.write("Chrometric: Exported " .. #results .. " colorschemes to chrometric_data.json\n")
    io.flush()
  else
    io.stderr:write("Error: Could not write to chrometric_data.json\n")
  end

  return results
end

-- Command for manual execution
vim.api.nvim_create_user_command("ChrometricExport", export_all, {})

-- Auto-run if launched in headless mode
if #vim.api.nvim_list_uis() == 0 then
  vim.defer_fn(function()
    export_all()
    vim.cmd("quitall!")
  end, 500)  -- Increased delay to ensure plugins are loaded
end
