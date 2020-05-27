<?php
// $command=`Client.py -u sopyan`;
// $command='whoami';
$command='python3 Client.py -u sopyan -s 172.17.0.3 -m unreg';
$return=shell_exec($command);
echo $return;
?>