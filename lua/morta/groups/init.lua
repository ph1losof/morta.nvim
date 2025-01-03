local M = {}

function M.load(colors, config)
  local highlights = {}

  local plugins = {
    "cmp",
    "blink_cmp",
    "gitsigns",
    "lazy",
    "lspsaga",
    "lualine",
    "telescope",
    "treesitter",
    "treesitter_context",
    "trouble",
  }

  for _, plugin in ipairs(plugins) do
    if config.plugins[plugin] then
      local ok, plugin_hl = pcall(require, "morta.groups." .. plugin)
      if ok and type(plugin_hl.get) == "function" then
        local hl = plugin_hl.get(colors, config)

        for group, opts in pairs(hl) do
          if type(opts) == "string" then
            highlights[group] = { link = opts }
          else
            highlights[group] = opts
          end
        end
      end
    end
  end

  return highlights
end

return M
