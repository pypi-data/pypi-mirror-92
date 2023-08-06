import logging
import re

from pathlib import Path

from itsicli.content_packs.commands.base import BaseCommand, request_input
from itsicli.content_packs.files import ContentPackConfig
from itsicli.content_packs.scaffold import Scaffolder


def valid_id(id_value):
    return re.search('^[\w\-_]+$', id_value)


INVALID_ID = 'Content pack id can only contain alphanumeric, underscore, or dash characters.\n'


class InitCommand(BaseCommand):

    HELP = 'initialize an ITSI Content Pack'

    NAME = 'init'

    class Args(object):
        CONTENT_PACK_ID = 'content_pack_id'
        CONTENT_PACK_TITLE = 'content_pack_title'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        subparser.add_argument('--{}'.format(cls.Args.CONTENT_PACK_ID), help='the content pack id')
        subparser.add_argument('--{}'.format(cls.Args.CONTENT_PACK_TITLE), help='the content pack title')

    def run(self, args):
        config = self.init_config(args)

        scaffolder = Scaffolder(config.path.parent)
        scaffolder.create_file('README.md')
        scaffolder.create_file('manifest.json')

    def init_config(self, args):
        config = ContentPackConfig(Path.cwd())
        new_data = {}

        curr_id = config.id
        content_pack_id = getattr(args, self.Args.CONTENT_PACK_ID)

        if content_pack_id and not valid_id(content_pack_id):
            logging.error(INVALID_ID)

            new_data[ContentPackConfig.attr_id] = self.request_content_pack_id()

        elif not curr_id:
            new_data[ContentPackConfig.attr_id] = self.request_content_pack_id()

        curr_title = config.title
        content_pack_title = getattr(args, self.Args.CONTENT_PACK_ID)

        if not content_pack_title and not curr_title:
            new_data[ContentPackConfig.attr_title] = request_input('Content pack title')

        if not new_data:
            return config

        if config.exists():
            logging.info('Updating {}'.format(config.path))
        else:
            logging.info('Creating {}'.format(config.path))

        config.update(new_data)
        config.write()

        return config

    def request_content_pack_id(self):
        while True:
            content_pack_id = input('Content pack id: ')

            if not valid_id(content_pack_id):
                logging.error(INVALID_ID)
                continue

            if content_pack_id:
                break

        return content_pack_id
