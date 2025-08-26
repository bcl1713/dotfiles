# dotfiles

My personal configuration files managed with [GNU Stow](https://www.gnu.org/software/stow/).

## What's Included

- **zsh** - Shell configuration (`.zshrc`)
- **git** - Git configuration (`.gitconfig`) and global gitignore
- **neovim** - Neovim configuration with Lazy.nvim and plugins
- **fish** - Fish shell configuration
- **git** - Additional git configuration in `.config/git/`

## Prerequisites

- [GNU Stow](https://www.gnu.org/software/stow/)
- Git
- Your preferred shell (zsh/fish)
- Neovim (if using nvim config)

### Installing Stow

**macOS:**

```bash
brew install stow
```

**Ubuntu/Debian:**

```bash
sudo apt install stow
```

**Arch Linux:**

```bash
sudo pacman -S stow
```

## Installation

1. Clone this repository to your home directory:

```bash
git clone https://github.com/bcl171/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

2. Use stow to symlink the configurations you want:

```bash
# Install all configurations
stow .

# Or install specific configurations
stow --target=$HOME --dir=. .config
```

3. For shell configurations, you may need to source them or restart your terminal:

```bash
# For zsh
source ~/.zshrc

# For fish
source ~/.config/fish/config.fish
```

## Structure

This repository uses the standard stow layout where each directory represents a
package that can be stowed independently:

```
dotfiles/
├── .config/
│   ├── fish/
│   ├── git/
│   └── nvim/
├── .gitconfig
└── .zshrc
```

## Usage

### Installing configurations

```bash
cd ~/.dotfiles
stow .  # Install everything
```

### Removing configurations

```bash
cd ~/.dotfiles
stow -D .  # Remove all symlinks
```

### Adding new configurations

1. Add your config files to the appropriate directory structure
2. Run `stow .` to create new symlinks
3. Commit and push your changes

## Notes

- This setup assumes your dotfiles repo is in `~/.dotfiles`
- Stow will create symlinks from your home directory to the files in this repo
- Make sure to backup any existing configurations before stowing
- Some configurations may require additional setup (fonts, plugins, etc.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
