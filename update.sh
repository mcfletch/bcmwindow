#! /bin/bash
git push pi master
ssh pi.dev "cd bcmwindow && git pull origin master"
