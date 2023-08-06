import sys
from logging import Logger
import requests
import json


class JobPermissionUpdater:

    def __init__(
        self,
        logger: Logger,
        databricksHost: str,
        databricksToken: str,
    ):
        self.__logger = logger
        self.__host = databricksHost
        self.__token = databricksToken

    def run(self, configPermission, jobId):
        resOfChange = self.__changePermissions(configPermission, jobId)

        if resOfChange.status_code != 200:
            self.__logger.error(f'Permissions for job ID {jobId} were not changed')
            self.__logger.error(resOfChange.text)
            sys.exit(1)

        self.__logger.info(f'Permissions for job ID {jobId} updated')
        resOfCheck = self.__checkPermissions(jobId)
        self.__logger.info(f'Current permissions: {resOfCheck.text}')

    def __changePermissions(self, configPermission, jobId):
        self.__logger.info(f'Changing permissions for job ID {jobId}')
        url = self.__createUrl(jobId)
        auth = self.__createAuth()

        data = {
            "object_id": f"/jobs/{jobId}",
            "object_type": "job",
            "access_control_list": self.__createAccessControlList(configPermission)
        }

        return requests.patch(url, data=json.dumps(data), headers=auth)

    def __createAccessControlList(self, configPermission):
        if 'usersNames' in configPermission:
            return [{'user_name': userName, 'permission_level': configPermission['permissionLevel']} for userName in configPermission['usersNames']]

        if 'groups' in configPermission:
            return [{'group_name': groupName, 'permission_level': configPermission['permissionLevel']} for groupName in configPermission['groups']]

        raise Exception(f'Invalid permissions: {configPermission}')

    def __checkPermissions(self, jobId):
        self.__logger.info(f'Checking the results after update')
        url = self.__createUrl(jobId)
        auth = self.__createAuth()
        return requests.get(url, headers=auth)

    def __createUrl(self, jobId):
        return f'{self.__host}/api/2.0/preview/permissions/jobs/{jobId}'

    def __createAuth(self):
        return {'Authorization': f'Bearer {self.__token}'}
