#!/usr/bin/env bash

for folder in $(ls ../Test/);do
    for subfolder in $(ls ../Test/$folder/);do
        echo $subfolder
        mkdir -p ../output/$folder/$subfolder
        mkdir -p ../log/$folder/$subfolder
        echo main.py -c "config/$subfolder.ini" -o "../output/$folder/$subfolder/$subfolder.tsv" "../Test/$folder/$subfolder"
        python main.py -c "config/$subfolder.ini" -o "../output/$folder/$subfolder/$subfolder.tsv" "../Test/$folder/$subfolder"
        mv ../output/$folder/$subfolder/$subfolder.log ../log/$folder/$subfolder
    done
done