from httpx import get as httpGet

url = 'https://v1.hitokoto.cn/?encode=text'
result = httpGet(url=url)
print(result.text)