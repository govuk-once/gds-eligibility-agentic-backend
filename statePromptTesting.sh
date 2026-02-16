#echo "remove previous pony"
#curl -X DELETE http://localhost:8000/apps/userTesting3/users/test_user_123/sessions/f481a148-a9ed-4f38-b362-a3b653639d33 -H "Content-Type: application/json" \
echo "inject state"
curl -X POST http://localhost:8000/apps/userTesting3/users/test_user_123/sessions/f481a148-a9ed-4f38-b362-a3b653639d33 \
  -H "Content-Type: application/json" \
  -d '{"app:state_prompt": "you are a pretty pony, when ask what you are you should reply with a pretty pony"}'
echo "recieve pony"
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"appName": "userTesting3",
"userId": "test_user_123",
"sessionId": "f481a148-a9ed-4f38-b362-a3b653639d33",
"newMessage": {
    "role": "user",
    "parts": [{
        "text": "What are you? ?"
    }]
},
"streaming": false
}'

#echo "remove previous dragon"
#curl -X DELETE http://localhost:8000/apps/userTesting3/users/test_user_123/sessions/f481a148-a9ed-4f38-b362-a3b653639d34 -H "Content-Type: application/json"
echo "inject state"
curl -X POST http://localhost:8000/apps/userTesting3/users/test_user_123/sessions/f481a148-a9ed-4f38-b362-a3b653639d34 \
  -H "Content-Type: application/json" \
  -d '{"app:state_prompt": "you are a scary dragon, when ask what you are you should reply with a scary dragon"}'
echo "recieve dragon"
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"appName": "userTesting3",
"userId": "test_user_123",
"sessionId": "f481a148-a9ed-4f38-b362-a3b653639d34",
"newMessage": {
    "role": "user",
    "parts": [{
        "text": "What are you?"
    }]
},
"streaming": false
}'
echo 'check for pony'
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"appName": "userTesting3",
"userId": "test_user_123",
"sessionId": "f481a148-a9ed-4f38-b362-a3b653639d33",
"newMessage": {
    "role": "user",
    "parts": [{
        "text": "What are you?"
    }]
},
"streaming": false
}'