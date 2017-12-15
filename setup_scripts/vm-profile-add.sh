cat >>~/.profile <<EOL
gnome-terminal --geometry 120x31+150+300 --working-directory=/home/student/labtainer/labtainer-student -e "bash -c \"/bin/cat README; exec bash\"" &
if [[ -f /home/student/labtainer/.doupdate ]]; then
    gnome-terminal --geometry 73x31+100+300 --working-directory=/home/student/labtainer -x ./update-labtainer.sh
fi
EOL
touch /home/student/labtainer/.doupdate 
