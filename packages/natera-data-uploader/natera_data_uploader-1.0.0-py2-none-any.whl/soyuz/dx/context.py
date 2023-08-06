#!/usr/bin/env python

import dxpy

from soyuz.utils import UploaderException


class DxContext(object):
    def __init__(self, token):
        self.__token = token
        dxpy.set_security_context({'auth_token_type': 'Bearer', 'auth_token': token})
        projects = self.__get_projects()
        size = len(projects)
        if size == 0 or size > 1:
            raise UploaderException("Auth Token must have access to exactly 1 project with UPLOAD permission.")
        self.__project = projects[0]
        dxpy.set_project_context(self.__project)
        dxpy.set_workspace_id(self.__project)

    def get_token(self):
        return self.__token

    def get_project_id(self):
        return self.__project

    def get_project(self):
        return dxpy.DXProject(self.get_project_id())

    @staticmethod
    def __get_projects():
        result = []
        try:
            for project in dxpy.bindings.search.find_projects(level='UPLOAD'):
                result.append(str(project['id']))
        except dxpy.exceptions.InvalidAuthentication:
            pass
        return result
