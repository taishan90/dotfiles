# Path to your oh-my-zsh installation.
export SHELL=/usr/bin/zsh
source ~/.envrc
export ZSH=~/.oh-my-zsh
export LC_ALL="en_US.UTF-8"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
plurgins=(vim)
plugins+=(python)
plugins+=(tmux)
plugins+=(git)

# User configuration
set_pascal (){
    echo "Custom setting for Pascal"
    export THEME="gentoo"
    export PATH="/home/thoth/melbayad/.local/bin:~/.local/sbin:/home/thoth/melbayad/bin:/home/thoth/melbayad/.gem/ruby/2.3.0/bin"
    export PATH=$PATH":/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
    export PRINTER=impression_toshiba
}
set_edgar (){
    echo "Custom setting for Edgar"
    export THEME="gentoo"
    export PATH="/home/thoth/melbayad/.local/bin:~/.local/sbin:/home/thoth/melbayad/bin:/home/thoth/melbayad/.gem/ruby/2.3.0/bin"
    export PATH=$PATH":/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
}
set_redgns (){
    echo "Custom setting for REDGNS"
    export THEME='agnoster'
    export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/texlive/2016/bin/x86_64-linux"
    export PYTHONPATH=$PYTHONPATH:/usr/local/cellar/caffe/python
}
set_gpuhost1 () {
    echo "Custom setting for gpuhosts"
    export THEME='avit'
    setg
}
set_gpuhost2 () {
    echo "Custom setting for gpuhosts"
    export THEME='avit'
    setg
}
set_gpuhost3 () {
    echo "Custom setting for gpuhosts"
    export THEME='avit'
    setg
}
set_gpuhost4 () {
    echo "Custom setting for gpuhosts"
    export THEME='avit'
    setg
}
# Mysteriously not working!!
# alias set_edgar='set_pascal'
# alias set_gpuhost2="set_gpuhost1"
# alias set_gpuhost3="set_gpuhost1"
# alias set_gpuhost4="set_gpuhost1"

set_${HOST:r:r}

ZSH_THEME=$THEME
source $ZSH/oh-my-zsh.sh

# Aliases and functions:

# extract:  Extract most know archives with one command

extract () {
    if [ -f $1 ] ; then
      case $1 in
        *.tar.bz2)   tar xjf $1     ;;
        *.tar.gz)    tar xzf $1     ;;
        *.bz2)       bunzip2 $1     ;;
        *.rar)       unrar e $1     ;;
        *.gz)        gunzip $1      ;;
        *.tar)       tar xf $1      ;;
        *.tbz2)      tar xjf $1     ;;
        *.tgz)       tar xzf $1     ;;
        *.zip)       unzip $1       ;;
        *.Z)         uncompress $1  ;;
        *.7z)        7z x $1        ;;
        *)     echo "'$1' cannot be extracted via extract()" ;;
         esac
     else
         echo "'$1' is not a valid file"
     fi
}

# Zip folder
zipf () { zip -r "$1".zip "$1" ; }
# Ssh with zsh shell
zssh () { ssh -Y "$1" -t zsh }
cd() { builtin cd "$@"; ls; }  # Always list directory contents upon 'cd'
alias c='clear'
alias ggc='gaa && git commit -m 'auto up' && git push origin master'
alias ggp='git pull origin master'
alias m='cd ~/scratch/work/imcap'
export GHI_TOKEN="17fb84722f8708c6c4c4942719c24ded82c182e3"
alias chr='google-chrome'
alias svim='vim +PluginInstall +qall'
alias src='source ~/.zshrc'

