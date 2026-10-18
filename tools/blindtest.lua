-- Blind comparison of palette candidates. Run from anywhere:
--   nvim -c "luafile tools/blindtest.lua"
--
-- :MortaBlind [n]     n trials (default 12), mixing two kinds:
--                       prefer  - two unlabelled palettes, <Space> flips, 1/2 picks
--                       search  - count something on screen as fast as you can
-- :MortaBlindReport   preference win rates, counting speed and accuracy
--
-- Candidates are the live palette ("current") plus every tools/candidates/*.lua.
-- Each candidate is shown through the current highlight mapping, so this compares
-- colours, not group assignments. Results append to stdpath("data")/morta_blindtest.jsonl.

local root = vim.fn.fnamemodify(debug.getinfo(1, "S").source:sub(2), ":p:h:h")
vim.opt.runtimepath:prepend(root)
vim.opt.termguicolors = true
require("morta").setup({ use_compiled = false })

local log_path = vim.fn.stdpath("data") .. "/morta_blindtest.jsonl"
local uv = vim.uv or vim.loop

local function candidates()
  local list = { { name = "current", file = root .. "/lua/morta/palette.lua" } }
  for _, f in ipairs(vim.fn.globpath(root .. "/tools/candidates", "*.lua", false, true)) do
    table.insert(list, { name = vim.fn.fnamemodify(f, ":t:r"), file = f })
  end
  return list
end

local function apply(cand)
  vim.cmd("hi clear")
  require("morta.highlights").setup(dofile(cand.file).colors, require("morta").config)
  vim.cmd("redraw!")
end

local function pick(t)
  return t[math.random(#t)]
end

local NAMES = { "items", "count", "buf", "node", "opts", "value", "result", "path", "entry", "state" }
local FUNCS = { "parse", "render", "lookup", "normalize", "emit", "resolve", "flush", "merge", "attach" }
local WORDS = { "ready", "missing", "done", "retry", "cache", "token", "skip", "stale" }

-- Each statement returns its text and how many strings / calls it contains.
local STATEMENTS = {
  function()
    return ("local %s = %s(%s)"):format(pick(NAMES), pick(FUNCS), pick(NAMES)), 0, 1
  end,
  function()
    return ('local %s = "%s"'):format(pick(NAMES), pick(WORDS)), 1, 0
  end,
  function()
    return ('%s(%s, "%s")'):format(pick(FUNCS), pick(NAMES), pick(WORDS)), 1, 1
  end,
  function()
    return ("if %s > %d then return %s end"):format(pick(NAMES), math.random(1, 99), pick(NAMES)), 0, 0
  end,
  function()
    return ("-- %s %s before %s"):format(pick(WORDS), pick(NAMES), pick(FUNCS)), 0, 0
  end,
  function()
    return ("local %s = { %s = true, %s = %d }"):format(pick(NAMES), pick(NAMES), pick(NAMES), math.random(1, 9)), 0, 0
  end,
  function()
    return ("for i = 1, #%s do %s[i] = nil end"):format(pick(NAMES), pick(NAMES)), 0, 0
  end,
}

-- Syntactically valid Lua, so treesitter highlights it the way real code looks.
local function sample()
  local lines, strings, calls = {}, 0, 0
  for _ = 1, 4 do
    table.insert(lines, ("local function %s(%s, %s)"):format(pick(FUNCS), pick(NAMES), pick(NAMES)))
    for _ = 1, math.random(3, 5) do
      local text, s, c = pick(STATEMENTS)()
      table.insert(lines, "  " .. text)
      strings, calls = strings + s, calls + c
    end
    table.insert(lines, ("  return %s"):format(pick(NAMES)))
    table.insert(lines, "end")
    table.insert(lines, "")
  end
  return lines, { strings = strings, calls = calls }
end

local ns = vim.api.nvim_create_namespace("morta_blindtest")

local function show(lines)
  local buf = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  vim.bo[buf].filetype = "lua"
  vim.api.nvim_win_set_buf(0, buf)
  pcall(vim.treesitter.start, buf, "lua")
  vim.wo.number = true
  vim.wo.signcolumn = "yes"
  -- Same glyph and message for every severity, so only colour tells them apart.
  local dot = "●"
  vim.diagnostic.config({
    signs = { text = { dot, dot, dot, dot } },
    virtual_text = { prefix = dot },
    underline = true,
  }, ns)
  local diags, errors = {}, 0
  for _ = 1, math.random(4, 7) do
    local severity = math.random(1, 4)
    errors = errors + (severity == vim.diagnostic.severity.ERROR and 1 or 0)
    table.insert(diags, { lnum = math.random(0, #lines - 2), col = 0, severity = severity, message = "check this" })
  end
  vim.diagnostic.set(ns, buf, diags)
  return buf, errors
end

local function log(entry)
  vim.fn.mkdir(vim.fn.fnamemodify(log_path, ":h"), "p")
  entry.time = os.time()
  entry.hour = tonumber(os.date("%H"))
  local f = io.open(log_path, "a")
  if f then
    f:write(vim.json.encode(entry) .. "\n")
    f:close()
  end
end

local function prefer(list)
  local a, b = math.random(#list), math.random(#list - 1)
  b = b >= a and b + 1 or b
  local pair, shown = { list[a], list[b] }, 1
  show((sample()))
  while true do
    apply(pair[shown])
    vim.api.nvim_echo({ { ("Palette %d of 2  |  <Space> flip  1/2 choose  q quit"):format(shown) } }, false, {})
    local key = vim.fn.getcharstr()
    if key == " " then
      shown = 3 - shown
    elseif key == "1" or key == "2" then
      local w = tonumber(key)
      log({ kind = "prefer", winner = pair[w].name, loser = pair[3 - w].name })
      return true
    elseif key == "q" or key == "\27" then
      return false
    end
  end
end

local TASKS = {
  { key = "strings", prompt = "How many string literals? " },
  { key = "calls", prompt = "How many function calls (not definitions)? " },
  { key = "errors", prompt = "How many ERROR diagnostics (not warnings/info/hints)? " },
}

local function search(list)
  local cand, task = pick(list), pick(TASKS)
  local lines, counts = sample()
  local _, errors = show(lines)
  counts.errors = errors
  apply(cand)
  local start = uv.hrtime()
  local ok, answer = pcall(vim.fn.input, task.prompt)
  if not ok or answer == "" then
    return false
  end
  log({
    kind = "search",
    task = task.key,
    cand = cand.name,
    ms = math.floor((uv.hrtime() - start) / 1e6),
    correct = tonumber(answer) == counts[task.key],
  })
  return true
end

local function report()
  local f = io.open(log_path, "r")
  if not f then
    print("No results yet in " .. log_path)
    return
  end
  local wins, games, pairs_seen, times, right, tries = {}, {}, {}, {}, {}, {}
  for line in f:lines() do
    local ok, e = pcall(vim.json.decode, line)
    if ok and e.kind == "prefer" then
      wins[e.winner] = (wins[e.winner] or 0) + 1
      for _, n in ipairs({ e.winner, e.loser }) do
        games[n] = (games[n] or 0) + 1
      end
      local key = e.winner < e.loser and e.winner .. " vs " .. e.loser or e.loser .. " vs " .. e.winner
      pairs_seen[key] = pairs_seen[key] or { [e.winner] = 0, [e.loser] = 0 }
      pairs_seen[key][e.winner] = pairs_seen[key][e.winner] + 1
    elseif ok and e.kind == "search" then
      tries[e.cand] = (tries[e.cand] or 0) + 1
      if e.correct then
        right[e.cand] = (right[e.cand] or 0) + 1
        times[e.cand] = times[e.cand] or {}
        table.insert(times[e.cand], e.ms)
      end
    end
  end
  f:close()

  -- Two-sided exact binomial test against a 50/50 coin.
  local function binom_p(k, n)
    local function pmf(i)
      local c = 1
      for j = 1, i do
        c = c * (n - i + j) / j
      end
      return c / 2 ^ n
    end
    local p, pk = 0, pmf(k)
    for i = 0, n do
      local pi = pmf(i)
      if pi <= pk + 1e-12 then
        p = p + pi
      end
    end
    return math.min(1, p)
  end

  local out = { "Preference (win rate):" }
  for n, g in pairs(games) do
    table.insert(out, ("  %-10s %3.0f%%  of %d"):format(n, 100 * (wins[n] or 0) / g, g))
  end
  table.insert(out, "Head to head (p < 0.05 means unlikely to be chance):")
  for key, t in pairs(pairs_seen) do
    local names = vim.tbl_keys(t)
    local n = t[names[1]] + t[names[2]]
    table.insert(
      out,
      ("  %-20s %s %d - %d %s   p = %.3f"):format(
        key,
        names[1],
        t[names[1]],
        t[names[2]],
        names[2],
        binom_p(t[names[1]], n)
      )
    )
  end
  table.insert(out, "Counting (accuracy, median time of correct answers):")
  for n, total in pairs(tries) do
    local ms = times[n] or {}
    table.sort(ms)
    local median = #ms > 0 and ms[math.ceil(#ms / 2)] / 1000 or 0
    table.insert(out, ("  %-10s %3.0f%%  %.1fs  of %d"):format(n, 100 * (right[n] or 0) / total, median, total))
  end
  table.insert(out, "Aim for 20+ comparisons per pair, across several sessions and lighting conditions.")
  vim.api.nvim_echo({ { table.concat(out, "\n") } }, true, {})
end

vim.api.nvim_create_user_command("MortaBlind", function(opts)
  math.randomseed(uv.hrtime())
  local list = candidates()
  for _ = 1, tonumber(opts.args) or 12 do
    local trial = math.random() < 0.5 and prefer or search
    if not trial(list) then
      break
    end
  end
  apply(list[1])
  vim.api.nvim_echo({ { "Done. :MortaBlindReport for results." } }, false, {})
end, { nargs = "?" })

vim.api.nvim_create_user_command("MortaBlindReport", report, {})
