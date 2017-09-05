
"""
SIP SIMPLE Client account settings extensions.
"""

__all__ = ['AccountExtension']

from sipsimple.configuration import Setting, SettingsGroup, SettingsObjectExtension
from sipsimple.account import RTPSettings

from sipclient.configuration.datatypes import AccountSoundFile


class RTPSettingsExtension(RTPSettings):
    inband_dtmf = Setting(type=bool, default=False)


class SoundsSettings(SettingsGroup):
    audio_inbound = Setting(type=AccountSoundFile, default=AccountSoundFile(AccountSoundFile.DefaultSoundFile('sounds.audio_inbound')), nillable=True)


class AccountExtension(SettingsObjectExtension):
    rtp = RTPSettingsExtension
    sounds = SoundsSettings


