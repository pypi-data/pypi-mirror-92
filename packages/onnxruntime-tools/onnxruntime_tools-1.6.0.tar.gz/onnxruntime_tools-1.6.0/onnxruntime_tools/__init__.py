###############################################################################
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
###############################################################################
"""
onnxruntime_tools
this package includes transformers model optimization tools
"""
__version__ = "1.6.0"
__git_version__ = "afd7b8b3f751e7aedbea708282003c380084606a"
__author__ = "Microsoft Corporation"
__producer__ = "onnxruntime_tools"

import os
import sys
import types

from . import transformers

_transformers_path = os.path.join(os.path.dirname(__file__), 'transformers')
sys.path.append(_transformers_path)

from .transformers import optimizer  # noqa

sys.modules[__name__ + '.optimizer'] = types.ModuleType('optimizer')
