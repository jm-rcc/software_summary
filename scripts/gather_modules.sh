#!/bin/bash

if [ ! -d $MODS_WORKING_PATH ]
then
    mkdir -p $MODS_WORKING_PATH
fi

find $MODS_MODULE_PATH/*/modules/all/ > $MODS_WORKING_PATH/allmodules.txt
find $MODS_NOARCH_PATH/*/modules > $MODS_WORKING_PATH/noarchmodules.txt
