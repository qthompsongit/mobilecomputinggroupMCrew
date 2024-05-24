import requests
#this is a test file that checks requests sent to the flask server
dictToSend = {'input':'what is the answer?'}
res = requests.post('http://192.168.1.83:5000/', json=dictToSend)
print('response from server:',res.text)
