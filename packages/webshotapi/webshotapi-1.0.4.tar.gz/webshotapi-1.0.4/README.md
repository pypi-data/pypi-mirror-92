# WebShotApi.com API client for Python

Take screenshot and save image in JPG, PNG, PDF. You can also extract selectors for all HTML elements with coordinates and css styles after browser rendering.
In our api you can create project and send all you urls to queue. Our server will do all the work for you

Full documentation about our api you can find in this website [Website screenshot API DOCS](https://webshotapi.com/docs/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/webshotapi) to install our client in Python.

```bash
pip install webshotapi
```

OR
```bash
pip3 install webshotapi
```

## API KEY
Api key you can generate after register.
[https://webshotapi.com/dashboard/api/](https://webshotapi.com/dashboard/api/)

## Usage

### Take screenshot and save jpg to file
```python
from ApiClient import ApiClient
from ApiException import ApiException

if __name__ == "__main__":
    try:
        TOKEN = 'YOUR TOKEN HERE'
        client = ApiClient(TOKEN)
        result = client.screenshot_jpg('https://www.cnn.com',{
            'remove_modals': 1
        })

        if result.save('/tmp/testa.jpg'):
            print("File saved")
        else:
            print("Error with save file")

    except ApiException as e:
        print("Error:")
        print(e)
```

### Take screenshot and save PDF to file
You can covert your html page to invoice in PDF.
```python
from ApiClient import ApiClient
from ApiException import ApiException

if __name__ == "__main__":
    try:
        TOKEN = 'YOUR TOKEN HERE'
        client = ApiClient(TOKEN)
        result = client.screenshot_pdf('https://www.example.com',{
            'remove_modals': 1
        })

        if result.save('/tmp/test.pdf'):
            print("File saved")
        else:
            print("Error with save file")

    except ApiException as e:
        print("Error:")
        print(e)
```

### Extract words map and HTML elements with css styles after rendering
Unique software to extract all selectors for HTML elements from website with css styles after browser rendering. Additionally you can extract all words with position (x,y,width, height, offset from previous word). Thank that you can build words map of website.

#### Sample script:
```python

from webshotapi.ApiClient import ApiClient
from webshotapi.ApiException import ApiException

if __name__ == "__main__":
    try:

        #create object
        TOKEN = 'YOUR TOKEN HERE'
        client = ApiClient(TOKEN)

        #send request
        result = client.extract('https://www.example.com',{
            'no_cache': 1,
            'extract_selectors': 1,
            'extract_style': 1
            'extract_words': 1,
            'extract_html': 1,
            'extract_text': 1
        })
        
        #print json data from result
        print(result.get_data())

    except ApiException as e:
        print("Error:")
        print(e)
```
#### Results

```json
{
  "selectors": [
    {
      "xpath": "/html/body",
      "x": 1212,
      "y": 17,
      "w": 117,
      "h": 25,
      "style": {
        "visibility": "visible",
        "display": "inline",
        "fontWeight": "400",
        "backgroundImage": "none",
        "cursor": "pointer",
        "fontSize": "22px",
        "color": "rgb(255, 255, 255)",
        "position": "static",
        "textDecoration": "none solid rgb(255, 255, 255)",
        "text-decoration-line": "none",
        "backgroundColor": "rgba(0, 0, 0, 0)"
      },
      "class": ".col-12 col-sm-12",
      "id": "#price",
      "itemprop": "price"
    }
  ],
  "words": [
    {
      "xpath": "/html/body/div[1]/div[2]/div/div[2]/ul/li[5]/a",
      "word": "Welcome",
      "position": {
        "x": 434.8,
        "y": 343.4,
        "w": 434,
        "h": 43
      },
      "word_index": 2,
      "offset": 14
    }
  ],
  "html": "<!doctype html><html lang='en' dir='ltr'><head><base hr...",
  "text": "Welcome in our page\nToday is Monday...",
  "screenshot_url": "https://api.webshotapi.com/v1/screenshot/?token=....&width=1920&height=960",
  "status_code": 200
}

```

## API docs
Full documentation about our api you can find in this website [API DOCS](https://webshotapi.com/docs/python/)

## About our service
You can use our service with free plan for 100 free requests 

## License
[MIT](https://choosealicense.com/licenses/mit/)