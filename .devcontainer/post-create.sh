git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/Pilaton/OhMyZsh-full-autoupdate ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate
mkdir -p ~/.oh-my-zsh/completions
poe _zsh_completion > ~/.oh-my-zsh/completions/_poe
# Set up uv shell completion
uv generate-shell-completion zsh > ~/.oh-my-zsh/completions/_uv
# Install project dependencies
uv sync