export PATH=$PATH:/Users/kkchuchu/workspace/kkchuchu.mushroom

export MUSHROOMBASE=~/workspace/kkchuchu.mushroom
export GITAWAREPROMPT=${MUSHROOMBASE}/bin/git-aware-prompt
source "${GITAWAREPROMPT}/main.sh"
export PS1="\u@\h \W \[$txtcyn\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]\$ "

