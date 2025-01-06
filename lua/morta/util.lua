local M = {}

---Convert hex color to RGB
---@param hex_str string
---@return number, number, number
local function hex_to_rgb(hex_str)
  local hex = hex_str:gsub("#", "")
  return tonumber(hex:sub(1, 2), 16), tonumber(hex:sub(3, 4), 16), tonumber(hex:sub(5, 6), 16)
end

---Convert RGB to hex color
---@param r number
---@param g number
---@param b number
---@return string
local function rgb_to_hex(r, g, b)
  return string.format("#%02x%02x%02x", r, g, b)
end

---Blend foreground color with background color
---@param fg string foreground color
---@param alpha number blend amount (0-1)
---@param bg? string background color, defaults to black
---@return string
function M.blend(fg, alpha, bg)
  bg = bg or "#000000"
  local fg_r, fg_g, fg_b = hex_to_rgb(fg)
  local bg_r, bg_g, bg_b = hex_to_rgb(bg)

  local function blend_channel(fg, bg)
    return math.floor(fg * alpha + bg * (1 - alpha))
  end

  return rgb_to_hex(blend_channel(fg_r, bg_r), blend_channel(fg_g, bg_g), blend_channel(fg_b, bg_b))
end

---Blend color with background
---@param color string
---@param alpha number
---@return string
function M.blend_bg(color, alpha)
  return M.blend(color, alpha, "#000000")
end

return M

