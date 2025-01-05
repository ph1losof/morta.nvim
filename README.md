# Morta
![CleanShot 2025-01-05 at 10 57 06@2x](https://github.com/user-attachments/assets/82937c93-559e-4a32-9993-128e6bd43139)

## Features

- Dark theme with rich purples and ethereal blues
- Support for popular plugins
- Optional terminal colors
- Compiled cache for better performance

## Installation

Using [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
   {
   "philosofonusus/morta.nvim",
    name = 'morta',
    priority = 1000,
    opts = {},
    config = function()
      vim.cmd.colorscheme 'morta'
    end,
  }
```
