return {
  "saghen/blink.cmp",
  dependencies = {
    "saghen/blink.compat",
  },
  opts = {
    keymap = {
      preset = "default",
      ["<CR>"] = {},  -- disable CR for completion
      ["<C-y>"] = { "accept" },  -- use C-y to accept completion
    },
    sources = {
      default = {
        "obsidian",
        "obsidian_new", 
        "obsidian_tags",
        "lsp",
        "path",
        "snippets",
        "buffer"
      },
      providers = {
        obsidian = {
          name = "obsidian",
          module = "blink.compat.source",
        },
        obsidian_new = {
          name = "obsidian_new", 
          module = "blink.compat.source",
        },
        obsidian_tags = {
          name = "obsidian_tags",
          module = "blink.compat.source", 
        },
      },
    },
  },
  opts_extend = { "sources.default" }
}