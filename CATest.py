import requests

def checkServiceForWord(url, keyword):
    try:
        x = requests.get(url)
        print(x.text)
        serverStatus=1
        if keyword in x.text:
            print("found keyword")
            return True
    except:
        print("error")
        return False


url = 'http://localhost:5000/getProducts'
result = checkServiceForWord(url, 'id')
print(result)

url = 'http://localhost:5000/GetTitles'
result = checkServiceForWord(url, 'title')
print(result)