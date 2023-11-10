import pyperclip
import json

j = json.loads(open("pages.json",'r').read())
p = "["
for page in j:
    p+=('\''+json.dumps(page)+'\',')
pyperclip.copy("/give @p written_book{title:\"\",author:\"\",pages:"+p+"]}")