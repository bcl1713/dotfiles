# dotfiles

My personal configuration files managed with [GNU Stow](https://www.gnu.org/software/stow/).

## What's Included

- **[zsh](https://www.zsh.org/)** - Shell configuration with [Powerlevel10k](https://github.com/romkatv/powerlevel10k) (`.zshrc`, `.p10k.zsh`)
- **[fish](https://fishshell.com/)** - Fish shell configuration
- **[git](https://git-scm.com/)** - Git configuration (`.gitconfig`) and global gitignore
- **[neovim](https://neovim.io/)** - Neovim configuration with [LazyVim](https://github.com/LazyVim/LazyVim) and plugins
- **[hypr](https://hyprland.org/)** - Hyprland window manager configuration
- **[waybar](https://github.com/Alexays/Waybar)** - Status bar for Wayland compositors
- **[wofi](https://hg.sr.ht/~scoopta/wofi)** - Application launcher for Wayland
- **[swaync](https://github.com/ErikReider/SwayNotificationCenter)** - Notification daemon for sway/Hyprland
- **[ghostty](https://ghostty.org/)** - Terminal emulator configuration
- **[wal](https://github.com/dylanaraps/pywal)** - Pywal color scheme templates
- **[syncthing](https://syncthing.net/)** - File synchronization configuration

## Prerequisites

- [GNU Stow](https://www.gnu.org/software/stow/)
- [Git](https://git-scm.com/)
- Your preferred shell ([zsh](https://www.zsh.org/)/[fish](https://fishshell.com/))
- [Neovim](https://neovim.io/) (if using nvim config)
- [Hyprland](https://hyprland.org/) (for window manager config)
- [Waybar](https://github.com/Alexays/Waybar) (for status bar)
- [Wofi](https://hg.sr.ht/~scoopta/wofi) (for application launcher)
- [SwayNotificationCenter](https://github.com/ErikReider/SwayNotificationCenter) (for notifications)
- [Ghostty](https://ghostty.org/) (for terminal config)
- [Pywal](https://github.com/dylanaraps/pywal) (for color scheme generation)

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
│   ├── fish/           # Fish shell configuration
│   ├── git/            # Git ignore patterns
│   ├── nvim/           # Neovim with LazyVim
│   ├── hypr/           # Hyprland window manager
│   ├── waybar/         # Status bar configuration
│   ├── wofi/           # Application launcher
│   ├── swaync/         # Notification daemon
│   ├── ghostty/        # Terminal emulator
│   ├── wal/            # Pywal templates
│   └── syncthing/      # File synchronization
├── .gitconfig          # Git user configuration
├── .zshrc              # Zsh configuration
├── .p10k.zsh           # Powerlevel10k theme
└── .stignore           # Syncthing ignore patterns
```

## Usage

### Installing configurations

```bash
cd ~/dotfiles
stow .  # Install everything
```

### Removing configurations

```bash
cd ~/dotfiles
stow -D .  # Remove all symlinks
```

### Adding new configurations

1. Add your config files to the appropriate directory structure
2. Run `stow .` to create new symlinks
3. Commit and push your changes

## Notes

- This setup assumes your dotfiles repo is in `~/dotfiles`
- Stow will create symlinks from your home directory to the files in this repo
- Make sure to backup any existing configurations before stowing
- Some configurations may require additional setup (fonts, plugins, etc.)
- Hyprland configs include window rules, keybindings, and startup applications
- Waybar configuration includes custom scripts for system information
- Neovim uses LazyVim as the base configuration with additional plugins
- Zsh includes Powerlevel10k theme configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
