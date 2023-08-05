# Copyright 2019 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
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
"""EiffelTestExecutionRecipeCollectionCreatedEvent.

https://github.com/eiffel-community/eiffel/blob/master/eiffel-vocabulary/EiffelTestExecutionRecipeCollectionCreatedEvent.md
"""
from eiffellib.events.eiffel_base_event import (EiffelBaseEvent, EiffelBaseLink,
                                                EiffelBaseData, EiffelBaseMeta)


class EiffelTestExecutionRecipeCollectionCreatedLink(EiffelBaseLink):
    """Link object for eiffel test execution recipe collection created event."""


class EiffelTestExecutionRecipeCollectionCreatedData(EiffelBaseData):
    """Data object for eiffel test execution recipe collection created event."""


class EiffelTestExecutionRecipeCollectionCreatedEvent(EiffelBaseEvent):
    """Eiffel test execution recipe collection created event."""

    version = "4.0.0"

    def __init__(self, version=None):
        """Initialize data, meta and links."""
        super(EiffelTestExecutionRecipeCollectionCreatedEvent, self).__init__(version)
        self.meta = EiffelBaseMeta("EiffelTestExecutionRecipeCollectionCreatedEvent", self.version)
        self.links = EiffelTestExecutionRecipeCollectionCreatedLink()
        self.data = EiffelTestExecutionRecipeCollectionCreatedData()
