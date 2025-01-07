local M = {}

local function safe_require(module)
  local ok, result = pcall(require, module)
  if ok then
    return result
  end
  return nil
end

function M.load(colors, config)
  local highlights = {}

  -- Load plugin highlight groups
  local plugins = {
    "morta.groups.blink_cmp",
    "morta.groups.gitsigns",
    "morta.groups.hipatterns",
    "morta.groups.lazy",
    "morta.groups.lspsaga",
    "morta.groups.semantic",
    "morta.groups.snacks",
    "morta.groups.treesitter",
    "morta.groups.treesitter_context",
    "morta.groups.mini_diff",
    "morta.groups.trouble",
    "morta.groups.kinds",
    "morta.groups.render_markdown",
    "morta.groups.cmp",
  }

  for _, plugin in ipairs(plugins) do
    local group = safe_require(plugin)
    if group and config.plugins[group.name or plugin:match("%.([^.]+)$")] then
      local plugin_highlights = group.get(colors, config)
      for hl_group, hl_opts in pairs(plugin_highlights) do
        highlights[hl_group] = hl_opts
      end
    end
  end

  return highlights
end

return M
