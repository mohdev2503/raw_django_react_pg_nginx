#!/bin/ash

# Install required packages
apk update
apk add --no-cache zsh tmux git curl

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Install zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Configure .zshrc
cat > ~/.zshrc << 'ENDOFZSHRC'
# Path to oh-my-zsh installation
export ZSH="$HOME/.oh-my-zsh"

# Theme setting
ZSH_THEME="robbyrussell"

# Plugins
plugins=(
    git
    docker
    python
    pip
    zsh-syntax-highlighting
    zsh-autosuggestions
)

# Source oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Basic configurations
export TERM="xterm-256color"
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

# Basic aliases
alias ll='ls -la'
alias l='ls -l'
alias ..='cd ..'
ENDOFZSHRC

# Basic tmux configuration
cat > ~/.tmux.conf << 'ENDOFTMUX'
# Set prefix to Ctrl-a
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Enable mouse
set -g mouse on

# Start window numbering at 1
set -g base-index 1

# Basic status bar
set -g status-style bg=black,fg=whited
set -g status-left ' #S '
set -g status-right ' %H:%M %d-%b-%y '
ENDOFTMUX

# Change shell for current user
chsh -s /bin/zsh $(whoami)

echo "Installation complete! Please run 'exec zsh' to start using zsh now"