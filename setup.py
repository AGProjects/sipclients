#!/usr/bin/python2

from distutils.core import setup
import os
import glob

import sipclient

setup(
    name='sipclients',
    version=sipclient.__version__,

    description='SIP SIMPLE client',
    long_description='Python command line clients using the SIP SIMPLE framework',
    url='http://sipsimpleclient.org',

    author='AG Projects',
    author_email='support@ag-projects.com',

    platforms=['Platform Independent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Service Providers',
        'License :: GNU Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],

    packages=['sipclient', 'sipclient.configuration'],
    data_files=[('share/sipclients/sounds', glob.glob(os.path.join('resources', 'sounds', '*.wav')))],
    scripts=[
        'sip-audio-session',
        'sip-message',
        'sip-publish-presence',
        'sip-register',
        'sip-session',
        'sip-settings',
        'sip-subscribe-mwi',
        'sip-subscribe-presence',
        'sip-subscribe-rls',
        'sip-subscribe-winfo',
        'sip-subscribe-xcap-diff'
    ]
)
