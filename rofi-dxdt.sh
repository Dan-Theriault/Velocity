#!/usr/bin/env bash

{ 
    notebook=$( dxdt-get | rofi -dmenu -p 'Notebooks:' -no-custom ) 
} && { 
    page=$( dxdt-get --book $notebook | rofi -dmenu -p 'Page:' ) 
} && {
    dxdt $notebook "$page"
}
