#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""JSON Datasource definition"""

from typing import Text

from zenml.core.datasources.base_datasource import BaseDatasource


class JSONDatasource(BaseDatasource):
    """ZenML JSON datasource definition."""
    DATA_STEP = None

    def __init__(self, name: Text, json_obj, schema=None, **unused_kwargs):
        """
        Initialize numpy datasource.
        Args:
            name: name of datasource
            json_obj: json obj
        """
        super().__init__(name, schema, **unused_kwargs)
        raise NotImplementedError('Its coming soon!')
