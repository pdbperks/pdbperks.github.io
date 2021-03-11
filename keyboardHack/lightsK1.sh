#!/bin/bash 

trap 'cleanExit' EXIT  #redirect CtrlC

if [ "$1" = "" ] 
then 
loops=2
else 
loops=$1
fi

#for i in  1 2 3 ; do gpio mode $i out; done

function flashAll {
for i in  1 2 3 ; do xset led $i; sleep 0.2; done
sleep 0.5;
for i in 0 1 2 3 4; do xset -led $i; sleep 0.2; done
sleep 0.5
}
function cleanExit {
xset -led
echo -e '\nClean exit. Thank you.';
}


function randomFlash {
rFlash=$((RANDOM%2))
xset led $rFlash+1
sleep 0.2;
xset -led $rFlash+1
sleep 0.2
}

flashAll
randomFlash

while [ $loops -gt 0 ]
do
for i in 1 2 3 ; do xset led $i;
sleep 1;
xset -led;
done

let "loops=$loops-1"
done

flashAll

randomFlash
