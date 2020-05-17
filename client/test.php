<?php
// $command=`Client.py -u sopyan`;
// $command='whoami';
$command='python3 Client.py -u sopyan -s 192.168.1.21';
$return=shell_exec($command);
echo $return;
?>