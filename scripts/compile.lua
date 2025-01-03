#!/usr/bin/env lua

-- Add the current directory to package.path
package.path = package.path .. ";./lua/?.lua"

-- Load the colorscheme module
local morta = require("morta")

-- Compile the colorscheme
local compiled = morta.compile()

-- Write to colors/morta.vim
local file = io.open("colors/morta.vim", "w")
if file then
    file:write(compiled)
    file:close()
    print("Successfully compiled morta.vim")
else
    print("Error: Could not write to colors/morta.vim")
    os.exit(1)
end 