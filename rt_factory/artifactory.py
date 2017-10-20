# -*- coding: utf-8 -*-
import os
import requests
from support import AbstractApi, ApiError

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

# get the artifactory url from the environment
ARTIFACTORY_URL = os.environ.get('ARTIFACTORY_URL',
                                 'http://localhost:8080/artifactory/api/')
ARTIFACTORY_API_KEY = os.environ.get('ARTIFACTORY_API_KEY', '')


class ArtifactoryApi(AbstractApi):

    def __init__(self, url=ARTIFACTORY_URL):
        super(ArtifactoryApi, self).__init__(url=url)
        self.api_key_header = {}

    def get_repository(self, name):
        return self._get(name).json()

    def create_repository(self, name, configuration):
        for repo in self._get('repositories'):
            if repo['key'] == name:
                print('Warning: repository {} already exists. '
                      'Ignoring creating it to avoid dataloss.'.format(name))
                return

        path = 'repositories/{}'.format(name)
        return self._put(path, configuration)

    def update_repository(self, name, data):
        # make sure the repo exists
        self.create_repository(name, data)

        path = 'repositories/{}'.format(name)
        return self._post(path, data)

    def create_or_replace_user(self, name, password,
                               groups=None):
        if not groups:
            groups = ['developers', 'readers']
        path = 'security/users/{}'.format(name)
        self._put(path, {'email': '{}@melexis.com'.format(name),
                         'password': password,
                         'groups': groups,
                         })

    def create_group(self, name, description=''):
        path = 'security/groups/{}'.format(name)
        try:
            group = self._get(path)
        except ApiError:
            group = {}

        group['name'] = name
        group['description'] = description
        self._put(path, group)

    def create_user(self, name):
        path = 'security/users/{}'.format(name)
        try:
            user = self._get(path)
            print("User {} already exists".format(name))
            return user
        except ApiError:
            user = {}

        user['name'] = name
        user['email'] = name + "@melexis.com"
        user['password'] = 'password'
        user['groups'] = ['users', 'readers']
        self._put(path, user)

    def add_user_to_group(self, user, group):
        path = 'security/users/{}'.format(user)
        user = self._get(path)
        if group not in user['groups'] or []:
            user['groups'].append(group)
        self._post(path, user)

    def get_permission(self, target_name):
        path = 'security/permissions/{}'.format(target_name)
        current = self._get(path)
        return current

    def add_group_to_permission(self, target_name, group_name,
                                access=None):
        if not access:
            access = ["r", "n"]
        path = 'security/permissions/{}'.format(target_name)
        current = self.get_permission(target_name)

        print(current)
        groups = current['principals'].get('groups', {})
        groups[group_name] = access
        current['principals']['groups'] = groups
        self._put(path, current)

    def add_repository_to_permission(self, target_name, repo):
        path = 'security/permissions/{}'.format(target_name)
        current = self.get_permission(target_name)

        repos = current['repositories']
        if repo not in repos:
            repos.append(repo)
        current['repositories'] = repos
        self._put(path, current)

    def create_permission(self, target_name, includes="**", excludes=""):
        path = 'security/permissions/{}'.format(target_name)
        try:
            current = self.get_permission(target_name=target_name)
        except ApiError:
            current = {}

        current['name'] = target_name
        current['includesPattern'] = includes
        current['excludesPattern'] = excludes
        current['repositories'] = current.get('repositories', [])
        current['principals'] = current.get('principals',
                                            {'users': {}, 'groups': {}})
        self._put(path, current)

    def add_public_key(self, filename):
        path = 'gpg/key/public'
        self._put_file(path, filename)

    def add_private_key(self, filename, phrase):
        path = 'gpg/key/private'
        self._put_file(path, filename, headers={'X-GPG-PASSPHRASE': phrase})

    def get_link_to_last_modified(self, repository, path):
        """ Searches for artifacts with the latest modification date.

        Args:
            repository (str): The repository name.
            path (str): The full path to the file to be searched for.

        Returns:
            str: Download url to the artifact.
        """
        path = 'storage/{repo}/{path}/?lastModified'.format(repo=repository,
                                                            path=path)
        temp_link = self._get(path)['uri']
        return self._get_from_url(temp_link)['downloadUri']

    def get_link_to_last_version(self, repository, path):
        """ Search for last version of artifact

        Searches for artifacts with the latest value in the "version" property.
        Only artifacts with a "version" property expressly defined in lower case
        will be taken into account.

        Args:
            repository (str): The repository name.
            path (str): The full path to the file to be searched for.

        Returns:
            str: Download url to the artifact.

        Notes:
            Requires an authenticated user (not anonymous).
        """
        path = 'versions/{repo}/{path}?listFiles=1'.format(repo=repository,
                                                           path=path)
        temp_link = self._get(path)
        return temp_link['artifacts'][0]['downloadUri']

    def download_file(self, url, path_to_file):
        """ Download a file from the Artifactory server.

        Args:
            url (str): Url to the file to be downloaded.
            path_to_file (str): Path + filename for downloading the file.
        """
        dl_content = requests.get(url, stream=True, headers=self.api_key_header)
        with open(path_to_file, 'wb') as output_file:
            for chunk in dl_content.iter_content(chunk_size=1024):
                if chunk:
                    output_file.write(chunk)

    def set_authentication_api_key(self, api_key=ARTIFACTORY_API_KEY):
        """ Set the API Key for running commands needing authentication.

        Args:
            api_key (str): The users Artifactory API key.
        """
        self.api_key_header = {'X-JFrog-Art-Api': api_key}

    def add_properties(self, repository, path, properties):
        """ Set properties of an artifact

        Args:
            repository (str): The repository name.
            path (str): The full path to the file to be searched for.
            properties (list): Json list of properties to set on the artifact.
        """
        prop = urlencode(properties).replace('&', '|')
        path = 'storage/{repo}/{path}?properties={prop}&recursive=1'\
            .format(repo=repository, path=path, prop=prop)
        self._put(path, properties)
