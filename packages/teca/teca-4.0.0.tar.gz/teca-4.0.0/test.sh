svn co svn://missmarple.lbl.gov/work3/teca/TECA_data &
svn_pid=$!
ps -p $svn_pid -o pid=
while [ -n "$(ps -p $svn_pid -o pid=)" ]
do
  #echo -n "."
  ps -p $svn_pid -o pid=
  sleep 2s
done
ps -p $svn_pid -o pid=
