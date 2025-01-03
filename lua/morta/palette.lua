local M = {}

M.colors = {
  -- Base colors - Soft pastel candy shop ambiance
  bg = "#1F1A23", -- Soft purple-tinted darkness
  bg_dark = "#191520", -- Gentle dark depth
  bg_highlight = "#2D2435", -- Soft mystical highlight

  -- Primary accent colors - Soft pastel candy inspired
  purple = "#C4A0F3", -- Soft grape taffy
  red = "#FF9CAF", -- Cotton candy pink
  blue = "#89C7FF", -- Pastel blue raspberry
  gold = "#FFB570", -- Creamy caramel

  -- Text colors - Gentle pastel contrast
  fg = "#EBE3FF", -- Soft marshmallow white
  fg_dark = "#C2B5E3", -- Gentle lavender cream
  fg_gutter = "#463A54", -- Soft chocolate shadow

  -- UI elements - Soft candy wrapper accents
  border = "#463A54", -- Gentle wrapper edge
  cursor = "#C4A0F3", -- Soft grape cursor
  selection = "#3D3147", -- Gentle grape shadow

  -- Syntax highlighting - Pastel candy shop palette
  string = "#A8E6B3", -- Soft mint candy
  keyword = "#FF9CAF", -- Cotton candy
  func = "#89C7FF", -- Pastel blue raspberry
  constant = "#FFB570", -- Creamy caramel
  type = "#7DE3D0", -- Soft mint ice cream
  variable = "#EBE3FF", -- Soft marshmallow
  comment = "#8B7BA1", -- Gentle grape shadow

  -- Special highlights - Soft candy signals
  warning = "#FFB570", -- Creamy caramel
  error = "#FF9CAF", -- Cotton candy pink
  info = "#89C7FF", -- Pastel blue raspberry
  hint = "#7DE3D0", -- Soft mint

  -- Git colors - Pastel candy markers
  git_add = "#A8E6B3", -- Soft mint candy
  git_change = "#FFB570", -- Creamy caramel
  git_delete = "#FF9CAF", -- Cotton candy pink

  -- Terminal colors - Soft candy shop terminal
  terminal_black = "#1F1A23",
  terminal_blue = "#89C7FF",
  terminal_cyan = "#7DE3D0",
  terminal_green = "#A8E6B3",
  terminal_magenta = "#C4A0F3",
  terminal_red = "#FF9CAF",
  terminal_white = "#EBE3FF",
  terminal_yellow = "#FFB570",
}

return M
