git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/Pilaton/OhMyZsh-full-autoupdate ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate
mkdir ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/poetry
poetry completions zsh > ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/poetry/_poetry
mkdir -p ~/.oh-my-zsh/completions
poe _zsh_completion > ~/.oh-my-zsh/completions/_poe