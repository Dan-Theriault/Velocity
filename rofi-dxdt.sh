#!/usr/bin/env bash

{ 
    notebook=$( dxdt get | rofi -dmenu -p 'Notebooks:' -no-custom ) 
} && { 
    page=$( dxdt get $notebook | rofi -dmenu -p 'Page:' ) 
} && {
    dxdt open $notebook "$page"
}
