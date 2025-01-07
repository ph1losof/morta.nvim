local M = {}

M.name = "kinds"

-- lsp symbol kind and completion kind highlights
local kinds = {
  Array = "@punctuation",
  Boolean = "@boolean",
  Class = "@type",
  Color = "Special",
  Constant = "@constant",
  Constructor = "@constructor",
  Enum = "@type",
  EnumMember = "@constant",
  Event = "Special",
  Field = "@field",
  File = "Normal",
  Folder = "Directory",
  Function = "@function",
  Interface = "@type",
  Key = "@field",
  Keyword = "Keyword",
  Method = "@function",
  Module = "Identifier",
  Namespace = "Identifier",
  Null = "@constant.builtin",
  Number = "@number",
  Object = "@constant",
  Operator = "@operator",
  Package = "Identifier",
  Property = "@property",
  Reference = "@text.reference",
  Snippet = "Conceal",
  String = "@string",
  Struct = "@type",
  Unit = "@type",
  Text = "Normal",
  TypeParameter = "@parameter",
  Variable = "@variable",
  Value = "@string",
}

---@param hl? table
---@param pattern? string
function M.kinds(hl, pattern)
  hl = hl or {}
  for kind, link in pairs(kinds) do
    local base = "LspKind" .. kind
    if pattern then
      hl[pattern:format(kind)] = base
    else
      hl[base] = link
    end
  end
  return hl
end

---@type fun(colors: table, config: table): table
function M.get(_colors, _config)
  return M.kinds()
end

return M
