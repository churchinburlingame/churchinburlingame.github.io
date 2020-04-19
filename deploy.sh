#!/bin/sh

echo Commit

d=$(date)

git add .
git commit -m "Pushed at $d"
git push
