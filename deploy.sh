#! /usr/bin/env bash
# debug False 로 변경!
git add -f env/etc
eb deploy --staged --profile danol
git reset HEAD env/etc