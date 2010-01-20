#!/usr/bin/env python

from distutils.core import setup
import os
import glob

import sipclient


setup(name         = "sipclients",
      version      = sipclient.__version__,
      author       = "AG Projects",
      author_email = "support@ag-projects.com",
      url          = "http://sipsimpleclient.com",
      description  = "SIP SIMPLE client",
      long_description = "Python command line clients using the SIP SIMPLE framework",
      platforms    = ["Platform Independent"],
      classifiers  = [
          "Development Status :: 4 - Beta",
          #"Development Status :: 5 - Production/Stable",
          #"Development Status :: 6 - Mature",
          "Intended Audience :: Service Providers",
          "License :: GNU Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python"
      ],
      packages     = ["sipclient", "sipclient.configuration"],
      data_files = [('share/sipclients/sounds', glob.glob(os.path.join('resources', 'sounds', '*.wav')))],
      scripts = ["sip-audio-session",
                 "sip-auto-publish-presence",
                 "sip-message",
                 "sip-publish-presence",
                 "sip-register",
                 "sip-session",
                 "sip-settings",
                 "sip-subscribe-mwi",
                 "sip-subscribe-presence",
                 "sip-subscribe-rls",
                 "sip-subscribe-winfo",
                 "sip-subscribe-xcap-diff",
                 "xcap-dialog-rules",
                 "xcap-directory",
                 "xcap-icon",
                 "xcap-pres-rules",
                 "xcap-rls-services"]
)


