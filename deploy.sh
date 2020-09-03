#! /usr/bin/env bash
git add -f env/etc
eb deploy --staged --profile danol
git reset HEAD env/etc