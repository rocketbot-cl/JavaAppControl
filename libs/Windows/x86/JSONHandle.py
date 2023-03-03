import json 

# initializing string  
test_string = '{"title":"Texty - Text Editor","indices":[1,2,1,0],"component":{"name":"Edit","role":"menu","index":1}}' 
  
# printing original string  
print("The original string : " + str(test_string)) 
  
# using json.loads() 
# convert dictionary string to dictionary 
res = json.loads(test_string) 
  
# print result 
print("The converted dictionary : " + str(res)) 

print(res['indices'])
print(type(res['indices']))