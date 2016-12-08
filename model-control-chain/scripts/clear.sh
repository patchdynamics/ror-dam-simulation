#!/bin/bash
set +e
read -p "Are you sure you want to remove weights and stats ? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
   # do dangerous stuff
   directory=models/$(date +%Y%m%d_%H%M%S)
   mkdir $directory
   mv stats/* $directory
   mv weights.npy $directory
   mv qvalues.npy $directory
fi
