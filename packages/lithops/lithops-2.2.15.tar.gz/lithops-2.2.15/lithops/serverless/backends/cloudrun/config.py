#
# (C) Copyright Cloudlab URV 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
from lithops.version import __version__
from lithops.utils import version_str

RUNTIME_NAME_DEFAULT = 'lithops-cloudrun'

RUNTIME_TIMEOUT_DEFAULT = 600  # 10 minutes
RUNTIME_MEMORY_DEFAULT = 256  # 256Mi
CONCURRENT_WORKERS_DEFAULT = 100

FH_ZIP_LOCATION = os.path.join(os.getcwd(), 'lithops_cloudrun.zip')


def load_config(config_data):
    if 'cloudrun' not in config_data:
        raise Exception("cloudrun section is mandatory in configuration")

    required_keys = ('project_id', 'region')
    if not set(required_keys) <= set(config_data['cloudrun']):
        raise Exception('You must provide {} to access to Cloud Run'.format(required_keys))

    if 'runtime_memory' not in config_data['serverless']:
        config_data['serverless']['runtime_memory'] = RUNTIME_MEMORY_DEFAULT
    if 'runtime_timeout' not in config_data['serverless']:
        config_data['serverless']['runtime_timeout'] = RUNTIME_TIMEOUT_DEFAULT

    if 'runtime' not in config_data['serverless']:
        project_id = config_data['cloudrun']['project_id']
        python_version = version_str(sys.version_info).replace('.', '')
        revision = 'latest' if 'dev' in __version__ else __version__.replace('.', '')
        runtime_name = '{}/{}-v{}:{}'.format(project_id, RUNTIME_NAME_DEFAULT, python_version, revision)
        config_data['serverless']['runtime'] = runtime_name

    if 'workers' not in config_data['lithops']:
        config_data['cloudrun']['workers'] = CONCURRENT_WORKERS_DEFAULT
        config_data['lithops']['workers'] = CONCURRENT_WORKERS_DEFAULT
