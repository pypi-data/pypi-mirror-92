from webshotapi.RequestClient import RequestClient
from webshotapi.RESTResponse import RESTResponse

class Project(RequestClient):

    def projects(self):
        """
        Get all projects

        :rtype: RESTResponse
        """
        return self.request('projects','GET',{})
    
    def get(self, id:int):
        '''
        Return project data by id

        :param id:
        :return: RESTResponse
        '''
        return self.request('project/'+str(id),'GET',{})

    def create(self, params:dict):
        '''
        Create new project

        :param params: dict with data for new project
        :return: RESTResponse
        '''
        return self.request('project','POST',params)

    def remove(self,id:int):
        '''
        Remove project by id

        :param id: project id
        :return: RESTResponse
        '''
        return self.request('project/'+str(id),'DELETE',{})

    def update(self,id:int,data:dict):
        '''
        Update existing project

        :param id: project id
        :param data: project data
        :return: RESTResponse
        '''
        return self.request('project/'+str(id),'PUT', data)

    def url_add(self,id:int,urls:list,params:dict):
        '''
        Add url to download for selected project

        :param id: project_id
        :param urls: list with urls
        :param params: dict with parameters
        :return: RESTResponse
        '''
        return self.request('project/'+str(id)+'/urls','POST',{'urls':urls,'params':params})

    def url_delete(self,id:int,url_id:int):
        '''
        Delete specific url for project

        :param id: project id
        :param url_id: link id
        :return: RESTResponse
        '''
        return self.request('project/'+str(id)+'/urls/'+str(url_id),'DELETE')

    def urls_get(self,id:int,page=1):
        '''
        Get urls for project
        
        :param id: project id
        :param page: page number
        :return: RESTResponse
        '''
        return self.request('project/'+str(id)+'/urls/'+str(page),'GET',{})
