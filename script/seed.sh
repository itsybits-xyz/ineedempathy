#!/bin/bash

starting_size=$(curl -so /dev/null localhost:8000/cards -w '%{size_download}')
echo "_____________________________"
echo "♠️  Starting Card Size: ${starting_size}"
echo "*****************************"
if [ "$starting_size" -ge "8000" ]; then
    echo "😳 Error: Too many cards have already been added."
    exit 1
fi

echo "_____________________"
echo "💎 Starting Feelings!"
echo "*********************"
for p in $(cat script/data/feelings.txt)
do
    curl -X POST "http://localhost:8000/cards" -H  "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"$p\",\"type\":\"feeling\"}"
done

echo "__________________"
echo "🏔 Starting Needs!"
echo "******************"
for p in $(cat script/data/needs.txt)
do
    curl -X POST "http://localhost:8000/cards" -H  "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"$p\",\"type\":\"need\"}"
done

echo "____________________________"
echo "😍 Cards successfully added!"
echo "****************************"
