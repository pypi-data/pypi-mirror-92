# -*- coding: utf-8 -*-
import os

import yaml
import json
import requests


class APIModern:

    syntax = (':{', '{', '},', '}', ':[', '[', ']', '],', ':', ',')

    exception_messages = {
        'api_missing': 'An API Key must be defined in the configuration file.',
        'not_found': 'The provided JSON file path is not correct.'
    }

    def __init__(self):
        self.files = {}
        self.config = self._load_config()

        if self.config.get('api_key') is None:
            raise Exception(self.exception_messages['api_missing'])

        if self.config.get('lang') is None:
            self.config['lang'] = ['fr', 'en', 'de']

    @staticmethod
    def _load_config():
        """
        Load configuration from config.yaml
        :return: The config dictionary from the file
        """
        try:
            with open('config.yaml', 'r') as config_file:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
                return config if config is not None else {}
        except FileNotFoundError:
            return {}

    def translate(self, target, files, source=None, path=None):
        """
        Call all functions to proceed with the translation
        :param target: The target language
        :param files: The list of files to translate
        :param source: The source language (optional)
        :param path: The destination path of translated files (optional)
        :return: The list of translated file
        """
        if not isinstance(files, (str, list, tuple)):
            raise TypeError("Files must be a string or a list.")

        # Cast files params to list of files path
        files = [files] if isinstance(files, str) else files

        # Read all files to save their content
        self._read_files(files)
        self._prepare_for_api()
        self._call_api(target, source)
        self._prepare_for_files()
        translated_files = self._write_files_content(target, path)
        # Reset files dictionary
        self.files = {}

        return translated_files

    def _read_files(self, files):
        """
        Read each files to extract their content into dictionaries
        :param files: The list of files to read
        :return:
        """
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as json_content:
                    self.files[file] = {
                        'content': json.load(json_content)
                    }
            except FileNotFoundError:
                raise FileNotFoundError(self.exception_messages['not_found'])

    def _write_files_content(self, target, path=None):
        """
        Write the new files previously translated
        :param target: The target language to rename the file
        :return: The list of translated path files
        """
        translated_files = []
        for filename, data in self.files.items():
            for lang in self.config['lang']:
                filename = filename.replace(lang, target)

            if path is not None:
                filename = os.path.join(path, filename)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(
                    json.dumps(data['content'], ensure_ascii=False, indent=2)
                )
                translated_files.append(os.path.abspath(filename))

        return translated_files

    def _prepare_for_api(self):
        """
        For each files get the list of string from the json
        :return:
        """
        for key, data in self.files.items():
            self.files[key] = self.json_to_str(data)
            self.files[key] = self.remove_syntax(data)
            self.files[key] = self.divide_list(data)

    def _prepare_for_files(self):
        """
        For each files get the json from the string list
        :return:
        """
        for key, data in self.files.items():
            self.files[key] = self.concat_list(data)
            self.files[key] = self.add_syntax(data)
            self.files[key] = self.str_to_json(data)

    @staticmethod
    def json_to_str(data):
        """
        Parse json to string list
        :param data: The data of file
        :return: The new parsed data
        """
        result = []

        def insert_value(value, add_double_points):
            # If value is object
            if type(value) is dict:
                if add_double_points:
                    result.append(':{')
                else:
                    result.append('{')
                flat(value)
                result.append('},')
            # If value is an array
            elif type(value) is list:
                if add_double_points:
                    result.append(':[')
                else:
                    result.append('[')
                flat(value)
                result.append('],')
            # Else the value is a string
            else:
                result.append(':')
                result.append(str(value))
                result.append(',')

        def flat(_content):
            # If content is an array
            if type(_content) is list:
                for value in _content:
                    insert_value(value, False)
            # Else content is an object
            else:
                for key, value in _content.items():
                    # Append key associated to the value
                    result.append(key)
                    insert_value(value, True)

        result.append('{' if type(data['content']) is dict else '[')
        flat(data['content'])
        result.append('}' if type(data['content']) is dict else ']')

        data['content'] = result

        return data

    def str_to_json(self, data):
        """
        Build the json from the string list
        :param data: The data
        :return:
        """
        result = ""
        for content in data['content']:
            if content in self.syntax:
                result += content
            else:
                result += '"' + content + '"'

        replace_dict = (
            (',}', '}'), (',]', ']'), ('\r', ''),
            ('\n', ''), (',:', ','), ('[:', '[')
        )
        for char_from, char_to in replace_dict:
            result = result.replace(char_from, char_to)

        data['content'] = json.loads(result)

        return data

    def remove_syntax(self, data):
        """
        Remove the syntax to get a lighter list for the API call
        :return: The data with sanitize content and memories for syntax
        """
        data['syntax_memories'] = {}
        new_content = []

        for index, content in enumerate(data['content']):
            if content in self.syntax:
                data['syntax_memories'][index] = content
            else:
                new_content.append(content)

        data['content'] = new_content

        return data

    @staticmethod
    def add_syntax(data):
        """
        Add syntax previously removed into the list
        :return: The data
        """
        for index, content in data['syntax_memories'].items():
            data['content'].insert(index, content)

        del data['syntax_memories']  # Remove unnecessary dictionary key
        return data

    @staticmethod
    def divide_list(data):
        """
        Divide a long list to multiple list to call API
        :return: The data
        """
        max_list_size = 128

        new_content = []
        length = len(data['content'])
        slice_count = (length // max_list_size) + 1

        for i in range(0, slice_count):
            begin = max_list_size * i
            if begin + max_list_size < length:
                end = begin + max_list_size
            else:
                end = length

            new_content.append(data['content'][begin:end])

        data['content'] = new_content

        return data

    @staticmethod
    def concat_list(data):
        """
        Concat all list to one list
        :return: The data
        """
        data['content'] = [content
                           for contents in data['content']
                           for content in contents]

        return data

    def _call_api(self, target, source=None):
        """
        Process the API call to translate
        :param target: The target language
        :param source: The source language (optional)
        :return:
        """
        url = 'https://api.modernmt.com/translate'
        headers = {
            'MMT-ApiKey': self.config['api_key'],
            'X-HTTP-Method-Override': 'GET',
            'Content-Type': 'application/json'
        }

        payload = {
            'target': target,
            'priority': 'background',
        }

        if source is not None:
            payload['source'] = source

        for key, data in self.files.items():
            new_content = []
            for q in data['content']:
                payload['q'] = q
                r = requests.post(url, json=payload, headers=headers)

                r_json = r.json()

                if r.status_code != 200:
                    raise Exception(r.status_code, r_json['error'])

                # Extract the translation of response data
                # and build the list of the translated text
                translation = []
                for translated_data in r_json['data']:
                    translation.append(translated_data['translation'])

                new_content.append(translation)

            self.files[key]['content'] = new_content
