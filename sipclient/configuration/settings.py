# Copyright (C) 2010 AG Projects. See LICENSE for details.
#

"""
SIP SIMPLE Client settings extensions.
"""

__all__ = ['SIPSimpleSettingsExtension']

import os

from sipsimple.configuration import Setting, SettingsGroup, SettingsObjectExtension
from sipsimple.configuration.datatypes import Path
from sipsimple.configuration.settings import AudioSettings, FileTransferSettings, LogsSettings

from sipclient.configuration.datatypes import SoundFile, UserDataPath


class AudioSettingsExtension(AudioSettings):
    directory = Setting(type=UserDataPath, default=UserDataPath('history'))


class FileTransferSettingsExtension(FileTransferSettings):
    directory = Setting(type=UserDataPath, default=None, nillable=True)


class LogsSettingsExtension(LogsSettings):
    directory = Setting(type=UserDataPath, default=UserDataPath('logs'))
    trace_notifications = Setting(type=bool, default=False)


class SoundsSettings(SettingsGroup):
    audio_inbound = Setting(type=SoundFile, default=SoundFile('sounds/ring_inbound.wav'), nillable=True)
    audio_outbound = Setting(type=SoundFile, default=SoundFile('sounds/ring_outbound.wav'), nillable=True)
    message_received = Setting(type=SoundFile, default=SoundFile('sounds/message_received.wav'), nillable=True)
    message_sent = Setting(type=SoundFile, default=SoundFile('sounds/message_sent.wav'), nillable=True)
    file_received = Setting(type=SoundFile, default=SoundFile('sounds/file_received.wav'), nillable=True)
    file_sent = Setting(type=SoundFile, default=SoundFile('sounds/file_sent.wav'), nillable=True)


class SIPSimpleSettingsExtension(SettingsObjectExtension):
    user_data_directory = Setting(type=Path, default=Path(os.path.expanduser('~/.sipclient')))
    resources_directory = Setting(type=Path, default=None, nillable=True)

    audio = AudioSettingsExtension
    file_transfer = FileTransferSettingsExtension
    logs = LogsSettingsExtension
    sounds = SoundsSettings


