
import textwrap
import os

from click.testing import CliRunner
from bash import bash

import szczypiorek as env
from szczypiorek.crypto import encrypt
from szczypiorek.cli import cli
from tests import BaseTestCase


class MyEnvParser(env.EnvParser):

    a = env.CharField()


class SensitiveEnvParser(env.EnvParser):

    password = env.CharField()
    my_super_password = env.CharField()
    secret = env.CharField()
    some_secret = env.CharField()
    my_key = env.CharField()
    key = env.CharField()
    not_some_important = env.CharField()
    a = env.CharField()
    c = env.CharField()


my_env = None

sensitive_env = None


class CliTestCase(BaseTestCase):

    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()

        try:
            self.root_dir.join('.szczypiorek_encryption_key').remove()

        except Exception:
            pass

        try:
            del os.environ['SZCZYPIOREK_ENCRYPTION_KEY']

        except KeyError:
            pass

        try:
            del os.environ['SZCZYPIOREK_ENCRYPTION_KEY_FILE']

        except KeyError:
            pass

        MyEnvParser._envs_gpg_cache = {}
        SensitiveEnvParser._envs_gpg_cache = {}
        env.EnvParser._envs_gpg_cache = {}

    #
    # PRINT_ENV
    #
    def test_print_env(self):

        content = encrypt(textwrap.dedent('''
            a: b
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        global my_env
        my_env = MyEnvParser().parse()  # noqa

        result = self.runner.invoke(
            cli, ['print-env', 'tests.test_cli.my_env'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            a: b
        ''').strip()

    def test_print_env__hide_sensitive(self):

        content = encrypt(textwrap.dedent('''
            password: my.secret
            my_super_password: 123whatever
            secret: not tell anyone
            some_secret: not just any secret
            my_key: to open any doors
            key: yup
            not_some_important: just show it
            a: b
            c: '{"my_password": "yes hidden"}'
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        global my_env
        my_env = SensitiveEnvParser().parse()  # noqa

        result = self.runner.invoke(
            cli, ['print-env', 'tests.test_cli.my_env'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            a: b
            c: {
                "my_password": "**********"
            }
            key: **********
            my_key: **********
            my_super_password: **********
            not_some_important: just show it
            password: **********
            secret: **********
            some_secret: **********
        ''').strip()

    #
    # ENCRYPT
    #
    def test_encrypt__no_yaml_files(self):

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_encrypt__specific_file(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.szczypiorek_encryption_key\n'
            'a.yml\n'
        )

        result = self.runner.invoke(
            cli, ['encrypt', str(self.root_dir.join('a.yml'))])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
        ]

    def test_encrypt__some_yaml_files(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        self.root_dir.join('b.yml').write(textwrap.dedent('''
            a: whatever
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.szczypiorek_encryption_key\n'
            'a.yml\n'
            'b.yml\n'
        )

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
            str(self.root_dir.join('b.szczyp')),
            str(self.root_dir.join('b.yml')),
        ]

    def test_encrypt__specific_file_and_custom_key_file(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.development_encryption_key\n'
            'a.yml\n'
        )

        result = self.runner.invoke(
            cli,
            [
                'encrypt',
                '-k', '.development_encryption_key',
                str(self.root_dir.join('a.yml'))
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.development_encryption_key')),
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
        ]

    def test_encrypt__some_error(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert 'Error: Well it seems that the' in result.output.strip()

    def test_encrypt__some_error__do_not_overwrite_existing(self):

        self.root_dir.join('a.szczyp').write('hello gpg')

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert 'Error: Well it seems that the' in result.output.strip()
        assert self.root_dir.join('a.szczyp').read() == 'hello gpg'

    #
    # DECRYPT
    #
    def test_decrypt__no_gpg_files(self):

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_decrypt__specific_gpg_file(self):

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('e2e.szczyp').write(content, mode='w')

        result = self.runner.invoke(
            cli,
            ['decrypt', str(self.root_dir.join('e2e.szczyp'))])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('e2e.szczyp')),
            str(self.root_dir.join('e2e.yml')),
        ]

    def test_decrypt__some_gpg_files(self):

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])
        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env.szczyp')),
            str(self.root_dir.join('env.yml')),
        ]

    def test_decrypt__specific_file_and_custom_key_file(self):

        content = encrypt(
            textwrap.dedent('''
                secret:
                  key: secret.whatever
                is_important: true
                aws:
                  url: {{ a.b.c }}

                number:
                  of:
                    workers: '113'
                a:
                  b:
                    c: http://hello.word.org
            '''),
            '.e2e_encryption_key')
        self.root_dir.join('e2e.szczyp').write(content, mode='w')

        result = self.runner.invoke(
            cli,
            [
                'decrypt',
                '-k', '.e2e_encryption_key',
                str(self.root_dir.join('e2e.szczyp'))
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.e2e_encryption_key')),
            str(self.root_dir.join('e2e.szczyp')),
            str(self.root_dir.join('e2e.yml')),
        ]

    def test_decrypt__some_error(self):

        self.root_dir.join('a.szczyp').write('whatever')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert (
            "Something went wrong while attempting to decrypt" in
            result.output.strip())

    def test_decrypt__some_error__do_not_overwrite_existing(self):

        self.root_dir.join('a.szczyp').write('whatever')
        self.root_dir.join('a.yml').write('hello yml')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert (
            "Something went wrong while attempting to decrypt" in
            result.output.strip())
        assert self.root_dir.join('a.yml').read() == 'hello yml'
