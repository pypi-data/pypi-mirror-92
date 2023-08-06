#  Copyright (c) 2020. WebShotApi All right reserved
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from webshotapi.RequestClient import RequestClient
from webshotapi.RESTResponse import RESTResponse

class ApiClient(RequestClient):

    def screenshot_png(self, link:str, params:dict):

        '''
        Take screenshot and return png image

        :param link:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/api/
        :example:
           import webshotapi\n
           TOKEN = 'PUT_YOUR_TOKEN_HERE'

           client = webshotapi(TOKEN)

        :return:
            RESTResponse object
        '''
        
        params['link'] = link
        if self.is_multi:
            self.add_multi(('screenshot/png','POST', params))
            return self

        return self.request('screenshot/png','POST', params)

    def screenshot_jpg(self, link:str, params:dict):
        '''
        Take screenshot and return jpg image

        :param link:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/api/
        :return:
            RESTResponse object
        '''
        params['link'] = link
        if self.is_multi:
            self.add_multi(('screenshot/jpg','POST', params))
            return self

        return self.request('screenshot/jpg','POST', params)

    def screenshot_json(self, link:str, params:dict):
        '''
        Take screenshot and return json data. You can also extract html and text

        :param link:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/api/
        :return:
            RESTResponse object
        '''
        params['link'] = link
        if self.is_multi:
            self.add_multi(('screenshot/json','POST', params))
            return self

        return self.request('screenshot/json','POST', params)

    def pdf(self, link:str, params:dict):
        '''
        Take screenshot and return pdf file

        :param link:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/api/
        :return:
            RESTResponse object
        '''
        params['link'] = link
        if self.is_multi:
            self.add_multi(('screenshot/pdf','POST', params))
            return self

        return self.request('screenshot/pdf','POST', params)

    def extract(self,link:str, params:dict):
        '''
        Extract html selectors with css styles, words with coordinates(x,y,width,height).
        You can also extract html of rendered page and clean text
        
        :param link:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/api/
        :return:
            RESTResponse object
        '''

        params['link'] = link
        if self.is_multi:
            self.add_multi(('extract','POST', params))
            return self

        return self.request('extract','POST', params)

