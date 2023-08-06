import io
import json
from webshotapi.ApiException import ApiException

class RESTResponse(io.IOBase):
    def __init__(self, resp):
        '''
        Create RestResponse object

        :param resp:
            response object from urllib3
        '''

        self.response = resp
        self.status = resp.status_code
        self.reason = resp.reason
        self.headers = {}
        for k in resp.headers:
            self.headers[str(k).lower()] = str(resp.headers[k])

        try:
            self.data = json.loads(resp.content.decode('utf-8'))
        except ValueError:
            self.data = resp.content


    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.headers

    def is_json(self):
        '''
        Check that response data is json document

        :rtype:
            bool
        '''
        ct = self.getheader('content-type')
        if ct is None:
            return False

        return 'application/json' in ct

    def getheader(self, name, default=None):
        '''
        Returns a given response header.
        
        :param name:
            Header name
        :param default:
            Set default value if header not exists
        :rtype:
            string
        '''
        if name not in self.headers:
            return default

        return self.headers[name]

    def get_data(self):
        '''
        Return data downloaded from api
        
        :return:
            return data from api
        '''

        return self.data

    def save(self,path):
        '''
        Save response data to file.
        If you set file path without extension method will auto detect output file extension from mime type.
        Example you take screenshot and want to save to jpg.
        Set path to:
        1. /tmp/example_1_file_name -> will detect extension from mime type and save file to /tmp/example_1_file_name.jpg
        2. /tmp/example_2_file_name.jpg -> extension is in file path so dont detect extension from mime and save to /tmp/example_2_file_name.jpg

        :param path:
            string file path
        :return:
            return saved file path
        :rtype:
            string
        '''

        #find extension
        ext = None
        dirs = path.split('/')
        if len(dirs) > 0:
            ext_s = dirs[-1].split('.')
            if len(ext_s) > 0:
                ext = ext_s[-1]

        add_ext_to_path = False
        if not (ext and ext in ['json','png','jpg','pdf']):
            content_type = self.getheader('content-type')
            if 'jpeg' in content_type:
                ext = 'jpg'
            elif 'png' in content_type:
                ext = 'png'
            elif 'pdf' in content_type:
                ext = 'pdf'
            elif 'json' in content_type:
                ext = 'json'

            add_ext_to_path = True

        if not ext:
            raise ApiException("Unknown file extension to save")

        save_path = path
        if(add_ext_to_path):
            save_path = path + '.' +ext

        if ext in ['png','jpg','pdf']:
            f = open(save_path, 'wb')
            f.write(self.data)
            f.close()
        elif ext == 'json':
            json.dump(self.data, open(save_path,'w'))
        else:
            raise ApiException('Unknown save type')

        return save_path
