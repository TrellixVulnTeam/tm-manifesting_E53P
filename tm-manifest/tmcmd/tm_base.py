#/usr/bin/python3 -tt

import requests as HTTP_REQUESTS
import json
from pdb import set_trace

class TmCmd():

    # url ='http://rocky42.americas.hpqcorp.net:31178/manifesting/api/'
    #url='http://localhost:31178/manifesting/api/'
    url = 'http://zachv.americas.hpqcorp.net:31178/manifesting/api/'
    args = {}

    def __init__(self, sort=True, headers=None, indent=4, **options):
        if headers is None:
            self.header = {'Accept' : 'application/json; version=1.0'}
        else:
            self.header = headers
        self.json_indent = indent
        self.json_sort = sort
        self.show_name = None
        self.verbose = options.get('verbose', False)


    def listall(self, arg_list=None, **options):
        """
            Intended to be overridden by inherited class.
        """
        if arg_list is None:
            arg_list = []
        assert len(arg_list) == 0, 'This function does not take non-optional arguments!'
        if 'verbose' in options and options['verbose']:
            print(' - Sending request to "%s"...' % self.url)


    def show(self, target, **options):
        """
            Intended to be overridden by inherited class.
        """
        assert len(target) >= 1, 'Missing argument: thisfunction <name>!'
        # Let user pass both types to avoid confusion passing args as "list" for a single argument.
        #Passing list is helpfull for a generic function call, (as in tm_manifest.py)
        self.show_name = target[0] if type(target) is list else target
        if 'verbose' in options and options['verbose']:
            print(' - Sending request to "%s"...' % self.url)


    def http_request(self, url, **options):
        """
            Do a http request on the provided url and return a response
        in jsong format (if abailable).
        :param 'url': [str] url request.
        :param 'options[payload]': [dict]
        :return: [json]
        """
        headers = options.get('headers', self.header)
        if options.get('payload', False):
            http_resp = HTTP_REQUESTS.put(url, options['payload'], headers=headers)
        else:
            http_resp = HTTP_REQUESTS.get(url, headers=headers)
        jsondata = self.to_json(http_resp)
        return jsondata


    def http_download(self, url, destination, **options):
        """
            Do a download http request on the provided url that is pointing to a file.
        Save the file to the requested destination.
        :param 'url': [str] url lint to a file to download.
        :param 'destination': [str] destination on the local disk to save downloaded file to.
        :return: None
        """
        headers = options.get('headers', self.header)
        downloaded = HTTP_REQUESTS.get(url, stream=True, headers=headers)
        with open(destination, "wb") as dest_file:
            # need to feedback a download bar to the screen here.
            dest_file.write(downloaded.content)


    def to_json(self, content):
        """
            Convert concent to json string with class parameters.
        """
        try:
            if isinstance(content, HTTP_REQUESTS.models.Response):
                return content.json()
            else:
                return json.dumps(content, indent=self.json_indent, sort_keys=self.json_sort)
        except (ValueError, TypeError) as err:
            if self.verbose:
                return '{ "error" : %s }' % (err)
            else:
                return '{ "error" : "couldn \'t parse server\'s response"}'


    def update_cmd(self, arg_dict):
        """
            Add "doc string" of each function defined in the derived from TmCmd class.
        Since it is passed by reference - there is no return value for this function.
        """
        new_keys = arg_dict.keys()
        existed_keys = self.args.keys()
        overlap = list(set(new_keys) & set(existed_keys))
        if (overlap):
            raise KeyError('Can not merge cmd args! Keys collision.')
        arg_dict.update(self.args)
