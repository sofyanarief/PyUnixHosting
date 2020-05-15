<?php
// $command=`Client.py -u sopyan`;
// $command='whoami';
$command='/usr/bin/python Client.py -u sopyan';
$return=shell_exec($command);
echo $return;
?>