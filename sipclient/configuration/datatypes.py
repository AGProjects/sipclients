
"""Definitions of datatypes for use in settings extensions"""

__all__ = ['ResourcePath', 'UserDataPath', 'SoundFile', 'AccountSoundFile']

import os
import sys
import urlparse

from application.python.descriptor import classproperty, WriteOnceAttribute
from sipsimple.configuration.datatypes import Hostname

## Path datatypes

class ResourcePath(object):
    def __init__(self, path):
        if not isinstance(path, unicode):
            path = path.decode(sys.getfilesystemencoding())
        self.path = os.path.normpath(path)

    def __getstate__(self):
        return unicode(self.path)

    def __setstate__(self, state):
        self.__init__(state)

    @property
    def normalized(self):
        path = os.path.expanduser(self.path)
        if os.path.isabs(path):
            return os.path.realpath(path)
        return os.path.realpath(os.path.join(self.resources_directory, path))

    @classproperty
    def resources_directory(cls):
        binary_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        if os.path.basename(binary_directory) == 'bin':
            application_directory = os.path.dirname(binary_directory)
        else:
            application_directory = binary_directory
        from sipsimple.configuration.settings import SIPSimpleSettings
        settings = SIPSimpleSettings()
        if os.path.basename(binary_directory) == 'bin':
            resources_component = settings.resources_directory or 'share/sipclients'
        else:
            resources_component = settings.resources_directory or 'resources'
        return os.path.realpath(os.path.join(application_directory, resources_component))

    def __eq__(self, other):
        try:
            return self.path == other.path
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)

    def __unicode__(self):
        return unicode(self.path)


class UserDataPath(object):
    def __init__(self, path):
        if not isinstance(path, unicode):
            path = path.decode(sys.getfilesystemencoding())
        self.path = os.path.normpath(path)

    def __getstate__(self):
        return unicode(self.path)

    def __setstate__(self, state):
        self.__init__(state)

    @property
    def normalized(self):
        path = os.path.expanduser(self.path)
        if os.path.isabs(path):
            return path
        from sipsimple.configuration.settings import SIPSimpleSettings
        settings = SIPSimpleSettings()
        return os.path.realpath(os.path.join(settings.user_data_directory, path))

    def __eq__(self, other):
        try:
            return self.path == other.path
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)

    def __unicode__(self):
        return unicode(self.path)


class SoundFile(object):
    def __init__(self, path, volume=100):
        self.path = ResourcePath(path)
        self.volume = int(volume)
        if self.volume < 0 or self.volume > 100:
            raise ValueError("illegal volume level: %d" % self.volume)

    def __getstate__(self):
        return u'%s,%s' % (self.path.__getstate__(), self.volume)

    def __setstate__(self, state):
        try:
            path, volume = state.rsplit(u',', 1)
        except ValueError:
            self.__init__(state)
        else:
            self.__init__(path, volume)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.path, self.volume)

    def __unicode__(self):
        return u'%s,%d' % (self.path, self.volume)


class AccountSoundFile(object):
    class DefaultSoundFile(object):
        def __init__(self, setting):
            self.setting = setting
        def __repr__(self):
            return 'AccountSoundFile.DefaultSoundFile(%s)' % self.setting
        __str__ = __repr__
    
    def __init__(self, sound_file, *args, **kwargs):
        if isinstance(sound_file, self.DefaultSoundFile):
            self._sound_file = sound_file
            if args or kwargs:
                raise ValueError("other parameters cannot be specified if sound file is instance of DefaultSoundFile")
        else:
            self._sound_file = SoundFile(sound_file, *args, **kwargs)

    def __getstate__(self):
        if isinstance(self._sound_file, self.DefaultSoundFile):
            return u'default:%s' % self._sound_file.setting
        else:
            return u'file:%s' % self._sound_file.__getstate__()

    def __setstate__(self, state):
        type, value = state.split(u':', 1)
        if type == u'default':
            self._sound_file = self.DefaultSoundFile(value)
        elif type == u'file':
            self._sound_file = SoundFile.__new__(SoundFile)
            self._sound_file.__setstate__(value)

    @property
    def sound_file(self):
        if isinstance(self._sound_file, self.DefaultSoundFile):
            from sipsimple.configuration.settings import SIPSimpleSettings
            setting = SIPSimpleSettings()
            for comp in self._sound_file.setting.split('.'):
                setting = getattr(setting, comp)
            return setting
        else:
            return self._sound_file

    def __repr__(self):
        if isinstance(self._sound_file, self.DefaultSoundFile):
            return '%s(%r)' % (self.__class__.__name__, self._sound_file)
        else:
            return '%s(%r, volume=%d)' % (self.__class__.__name__, self._sound_file.path, self._sound_file.volume)

    def __unicode__(self):
        if isinstance(self._sound_file, self.DefaultSoundFile):
            return u'DEFAULT'
        else:
            return u'%s,%d' % (self._sound_file.path, self._sound_file.volume)


class HTTPURL(object):
    url = WriteOnceAttribute()

    def __init__(self, value):
        url = urlparse.urlparse(value)
        if url.scheme not in (u'http', u'https'):
            raise ValueError(NSLocalizedString("Illegal HTTP URL scheme (http and https only): %s", "Preference option error") % url.scheme)
        # check port and hostname
        Hostname(url.hostname)
        if url.port is not None:
            if not (0 < url.port < 65536):
                raise ValueError(NSLocalizedString("Illegal port value: %d", "Preference option error") % url.port)
        self.url = url

    def __getstate__(self):
        return unicode(self.url.geturl())

    def __setstate__(self, state):
        self.__init__(state)

    def __getitem__(self, index):
        return self.url.__getitem__(index)

    def __getattr__(self, attr):
        if attr in ('scheme', 'netloc', 'path', 'params', 'query', 'fragment', 'username', 'password', 'hostname', 'port'):
            return getattr(self.url, attr)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr))

    def __unicode__(self):
        return unicode(self.url.geturl())

