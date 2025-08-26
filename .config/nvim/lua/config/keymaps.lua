-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local map = vim.keymap.set

-- HA Development workflow
map(
  "n",
  "<leader>hc",
  ":!cd ~/Projects/homeassistant-dev/ && ./scripts/get-ai-context.sh<CR>",
  { desc = "Get AI Context" }
)
map(
  "n",
  "<leader>ht",
  ":!cd ~/Projects/homeassistant-dev/ && ./scripts/deploy-branch.sh<CR>",
  { desc = "Deploy Current Branch" }
)
map("n", "<leader>hr", ":!cd ~/Projects/homeassistant-dev/ && ./scripts/rollback.sh<CR>", { desc = "Rollback to Main" })

-- Obsidian Keymaps
map("n", "<leader>on", "<cmd>ObsidianNew<cr>", { desc = "New Zettelkasten Note" })
map("n", "<leader>od", "<cmd>ObsidianToday<cr>", { desc = "Open Daily Note" })
map("n", "<leader>os", "<cmd>ObsidianSearch<cr>", { desc = "Search Notes" })
map("n", "<leader>ob", "<cmd>ObsidianSearch type=backlinks<cr>", { desc = "Show Backlinks" })
