#!/usr/bin/env bash

{ 
    notebook=$( dxdt get | rofi -dmenu -p 'Books:' -no-custom -i ) 
} && { 
    page=$( dxdt get $notebook | rofi -dmenu -p 'Page:' -i ) 
} && {
    dxdt open $notebook "$page"
}
