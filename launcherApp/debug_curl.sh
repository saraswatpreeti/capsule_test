#!/bin/bash
while IFS=$'\t' read -r col1 col2 col3 || [[ -n "$col1" ]];
do
  #echo $col1
  #echo $col2
  T=$(printf '\t') 
  output=$(curl -s -d '{"canTypeId":"bixby-mobile-en-US","capsuleContext":"bixby.launcher" ,"language":"en-US", "svcId": "testServiceid", "accountId": "zilgjlusna", "timeZone": "America/Los_Angeles", "oauthProvider": "Samsung", "nl": "'"$col1"'", "requestId": "123", "conversationId": "asd"}' -H "Content-Type: application/json" -X POST http://qa-usw2-user-proxy.dev-aibixby.com/debug/user/crc/v1 | python -mjson.tool | grep 'alignedNl'|cut -c 26-) 
   
   # echo "$output"
   #echo "$col1$T$col2$T$output"
  echo "$col1$T$col2$T$col3$T$output" | sed -e 's/\r//' | sed 's/"//g'|sed 's/"//g'| sed 's/\(.*\),/\1/'| sed 's/\t$//g'  >> debugoutput_final.tsv

done < debug_test.tsv
