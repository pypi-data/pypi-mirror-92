"""A basic application which applications will inherit."""
import os
import sys
import username
import shutil

from .config import ConfigParser

CONTROL_NAME = 'control'
CONTROL_FILE = '.'.join([CONTROL_NAME, 'ini'])


class ApplicationClass():
    """
    A class that gets the users and configuration for an application.

    In variables the word <directory> implies the path to a directory,
        the word <file> implies the path to a file.

    Parameters
    ----------
    id : str
        An identifier for the application
    use_user_ini : boolean
        if True then separate config_dir and user_id files are used
    use_var_dir : boolean
        If True then the file var_dir is used
    use_config_ini : boolean
        if True then config_dir and control_file are used

    Attributes
    ----------
    config_dir : str
        The path to the application in the config path
    control_file : str
        The path to an ini file that contains general ini data
    user_id : str
        the current user id
    var_dir : str
        The path to directory for variable data associated with the current id
    """
    def __init__(self,
                 id,
                 use_user_ini,
                 use_config_ini,
                 use_var_dir,
                 user_class,
                 attributes=None,
                 **kwargs):
        super().__init__()
        # parameter variables
        self._id = id
        self._use_user_ini = use_user_ini
        self._use_config_ini = use_config_ini
        self._use_var_dir = use_var_dir
        self._user_class = user_class

        # path variables
        self._paths = self._get_config_paths()
        self._config_dir = self._paths['config_dir']
        self._control_file = self._paths['control_file']
        self._var_dir = self._paths['var_dir']
        self.downloads_dir = self._paths['downloads_dir']

        # attributes
        self.attributes = attributes
        if not attributes:
            self.attributes = {}
        if use_user_ini:
            self.attributes['last_user_id'] = ('general', 'string', '',)
        if attributes or use_user_ini or use_config_ini:
            self.config = ConfigParser(self)
            self.config.get_attributes(self._control_file)
        else:
            self.config = None
        self.control_file_name = CONTROL_FILE

        # users
        self._user = None
        self.users = self._get_users()
        if use_user_ini:
            if not self.last_user_id and username() in self.users:
                self.last_user_id = username()
            if not username() in self.users:
                self.add_user(username())

        # General class variables
        self.title = 'Application default Title'
        self.version = '0.0.0'

        # help
        self.help_url = ''

    def __str__(self):
        """A string summary of the application."""
        return f'Application - {self.title}, Version: {self.version}'

    def __repr__(self):
        """A string representation of the application."""
        repr_list = [
            f'id: {self.id}',
            f'title: {self.title}',
            f'uses user.ini: {self.use_user_ini}',
            f'uses control.ini: {self.use_config_ini}',
            f'uses var dir: {self.use_var_dir}',
        ]
        repr = ',\n'.join(repr_list)
        return f'ApplicationClass:\n{repr}'

    @property
    def id(self):
        """Return the value of id."""
        return self._id

    @property
    def config_dir(self):
        """Return the value of config_dir."""
        return self._config_dir

    @property
    def use_user_ini(self):
        """Return the value of user_user_ini."""
        return self._use_user_ini

    @property
    def use_config_ini(self):
        """Return the value of user_user_ini."""
        return self._use_config_ini

    @property
    def use_var_dir(self):
        """Return the value of user_user_ini."""
        return self._use_var_dir

    @property
    def user_class(self):
        """Return the value of user_user_class."""
        return self._user_class

    @property
    def var_dir(self):
        """Return the value of var_dir."""
        return self._var_dir

    @property
    def last_user(self):
        """Return the value of the last user."""
        if self.last_user_id in self.users:
            return self.users[self.last_user_id]
        else:
            return None

    def save(self):
        """Save the config to file."""
        if self._control_file:
            self.config.save(self._control_file)

    def add_user(self, user_id):
        """Add a user to the app and create a default config."""
        if not self._use_user_ini:
            raise ValueError('Users cannot be added to this application!')
        user = self._user_class(app=self, user_id=user_id)
        user.save()
        self.users[user_id] = user
        self.save()
        if not self.last_user_id:
            self.last_user_id = user_id
        return user

    def switch_user(self, user_id):
        """Switch users."""
        if user_id in self.users:
            self.last_user_id = user_id
            self.save()

    def _get_users(self):
        """Return a dict of users."""
        users = {}
        if self._user_class:
            root_directory = self._config_dir
            for directory_name, subdir_list, file_list in os.walk(root_directory):
                for file_name in file_list:
                    user_file = os.sep.join([directory_name, file_name])
                    user_id = os.path.splitext(file_name)[0]
                    if user_id != CONTROL_NAME:
                        user = self._user_class(self, user_id)
                        user.get_attributes(user_file)
                        users[user_id] = user
        return users

    def _get_config_paths(self):
        """Return config_dir and config_file strings."""

        # config_path is the path to the main config directory
        # e.g. /home /<username>/.config/
        config_path, downloads_dir = self._get_os_dependant_paths()

        # config_dir is the path to the application in the config path
        # e.g. /home /<username>/.config/launch
        config_dir = os.sep.join([config_path, self.id])

        if self._use_user_ini or self._use_config_ini:
            config_dir = self._make_dir(config_path, self.id)

        # control_file is the path to an ini file that contains general ini data
        # e.g. /home/<username>/.config/launch/control.ini
        if self._use_config_ini or self._use_user_ini:
            control_file = os.sep.join([config_dir, f'{CONTROL_FILE}'])
        else:
            control_file = None

        # var_dir is a directory for variable data associated with the current
        # instance of the application
        # e.g. /home/<username>/.var/launch
        var_path_general = config_path.replace('.config', '.var')
        var_path = os.sep.join([var_path_general, 'app'])
        if self._use_var_dir:
            var_dir = self._make_dir(var_path, self.id)
        else:
            var_dir = os.sep.join([var_path, self.id])

        paths = {
            'config_dir': config_dir,
            'control_file': control_file,
            'var_dir': var_dir,
            'downloads_dir': downloads_dir
        }
        return paths

    def _remove_config_dir(self):
        """Remove the control directory - use in testing."""
        self.users = {}
        if os.path.isdir(self._config_dir):
            shutil.rmtree(self._config_dir)

    def _remove_var_dir(self):
        """Remove the var directory - use in testing."""
        if os.path.isdir(self._var_dir):
            os.removedirs(self._var_dir)

    @staticmethod
    def _make_dir(parent, dir_name):
        """Create a directory if necessary and return its path."""
        new_dir = os.sep.join([parent, dir_name])
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)
        return new_dir

    @staticmethod
    def _get_os_dependant_paths():
        # Unix file structure
        if 'linux' in sys.platform:
            home_path = os.path.expanduser('~')
            config_dir = os.sep.join([home_path, '.config'])
            downloads_dir = os.sep.join([os.path.expanduser('~'), 'Downloads'])
        
        # Windows file structure
        elif sys.platform[:3] == 'win':
            config_path = os.getenv('APPDATA')
            downloads_dir = os.path.join(os.getenv('USERPROFILE'), 'Downloads')

        else:
            raise OSError('Unspecified Platform')
        return config_dir, downloads_dir
