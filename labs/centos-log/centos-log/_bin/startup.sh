P='login'
if ps ax | grep -v grep | grep -v logind | grep $P >/dev/null
then
    echo "is running" >/dev/null
    #su student
else
    #echo "not running"
    while [ 1 ]; do
        trap login SIGINT
        /sbin/login
    done
fi

