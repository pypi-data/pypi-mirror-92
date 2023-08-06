import os
import json
import requests
from halo import Halo

from wave_cli import COMMAND_NAME


class Backend:
    def __init__(self, context):
        self.ctx = context
        self.base_url = 'https://wavecountbackend.azurewebsites.net/api'
        self.access_token = self.ctx.obj['access_token'] if 'access_token' in self.ctx.obj else ''
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def login(self, data):
        endpoint = self.base_url + '/auth/login'
        spinner = Halo(spinner='dots3', text_color='cyan').start(text='Authenticating')
        try:
            res = requests.post(url=endpoint, json=data)
            if res.status_code == 200:
                spinner.succeed(text='voila! Authenticated')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def sync_cache(self):
        endpoint = self.base_url + '/auth/sync'
        spinner = Halo(spinner='dots3', text_color='cyan').start(text='Syncing')
        try:
            res = requests.get(url=endpoint, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='voila! Synchronized')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def register_device(self, data):
        endpoint = self.base_url + '/devices'
        spinner = Halo(spinner='dots3', text_color='cyan').start(text='Registering')
        try:
            res = requests.post(url=endpoint, json=data, headers=self.headers)
            if res.status_code == 200:
                device = res.json()
                spinner.succeed(text='voila! {} device registered successfully'.format(device['environment']))
                return device
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def get_error_flags(self):
        endpoint = self.base_url + '/errors'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Fetching')
            res = requests.get(url=endpoint, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Fetched')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def get_devices_list(self, where={}):
        endpoint = self.base_url + '/devices'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Getting Devices List')
            params = {'where': json.dumps(where)}
            res = requests.get(url=endpoint, params=params, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Got Devices List')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def get_device_info(self, device_id: str):
        endpoint = self.base_url + '/devices/{0}/info'.format(device_id)
        spinner = Halo(spinner='dots3', text_color='cyan').start('Getting Device Info')
        try:
            res = requests.get(url=endpoint, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Got Device Info')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def update_devices(self, desired_version, where={}, when=None, is_forced=False):
        endpoint = self.base_url + '/devices/update'
        spinner = Halo(spinner='dots3', text_color='cyan').start('Running')
        try:
            params = {'desiredVersion': desired_version, 'where': json.dumps(where), 'when': when, 'isForced': is_forced}
            res = requests.get(url=endpoint, params=params, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def reboot_devices(self,  where={}):
        endpoint = self.base_url + '/devices/reboot'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Running')
            params = {'where': json.dumps(where)}
            res = requests.get(url=endpoint, params=params, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def reset_service(self, where={}):
        endpoint = self.base_url + '/devices/reset'
        spinner = Halo(spinner='dots3', text_color='cyan').start('Running')
        try:
            params = {'where': json.dumps(where)}
            res = requests.get(url=endpoint, params=params, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def delete_device(self, device_id):
        endpoint = self.base_url + '/devices/{0}'.format(device_id)
        spinner = Halo(spinner='dots3', text_color='cyan').start('Deleting device {0}'.format(device_id))
        try:
            res = requests.delete(url=endpoint, headers=self.headers)
            if res.status_code == 204:
                spinner.succeed('voila! succeed')
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def request_device_logs(self, is_forced, device_id=None, serial_number=None, targets=None, period=None):
        endpoint = self.base_url + '/logs/request'
        spinner = Halo(spinner='dots3', text_color='cyan').start('Preparing logs')
        try:
            query_params = {
                'isForced': is_forced,
                'deviceId': device_id,
                'serialNumber': serial_number,
                'targets': targets,
                'period': json.dumps(period)
            }
            res = requests.get(url=endpoint, params=query_params, headers=self.headers)
            if res.status_code == 200:
                spinner.succeed('Prepared')
                return res.json()
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def download_device_logs(self, blob_name):
        endpoint = self.base_url + '/logs/download'
        spinner = Halo(spinner='dots3', text_color='cyan').start('Downloading logs')
        try:
            query_patams = {'blobName': blob_name}
            res = requests.get(url=endpoint, params=query_patams, headers=self.headers)
            if res.status_code == 200:
                file = res.content
                spinner.succeed('Downloaded')
                local_path = os.path.expanduser("~/Desktop")
                local_file_path = blob_name.replace('/', '_')
                download_file_path = os.path.join(local_path, local_file_path)
                with open(download_file_path, 'wb+') as download_file:
                    download_file.write(file)
                return download_file_path
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['error']['message']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['error']['message']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()
