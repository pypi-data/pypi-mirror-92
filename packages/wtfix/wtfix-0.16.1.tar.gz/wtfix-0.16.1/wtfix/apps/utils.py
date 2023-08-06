# This file is a part of WTFIX.
#
# Copyright (C) 2018-2021 John Cass <john.cass77@gmail.com>
#
# WTFIX is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# WTFIX is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from wtfix.apps.base import BaseApp
from wtfix.conf import settings
from wtfix.message.message import FIXMessage

logger = settings.logger


class OutboundLoggingApp(BaseApp):
    """
    Logs outbound messages.
    """

    name = "outbound_logger"

    async def on_send(self, message: FIXMessage) -> FIXMessage:
        logger.info(f" --> {message:t}")

        return message


class InboundLoggingApp(BaseApp):
    """
    Logs inbound messages.
    """

    name = "inbound_logger"

    async def on_receive(self, message: FIXMessage) -> FIXMessage:
        logger.info(f" <-- {message:t}")

        return message


class PipelineTerminationApp(BaseApp):
    """
    Terminates the pipeline and encourages garbage collection of the message.
    """

    name = "pipeline_termination"

    async def on_receive(self, message: FIXMessage) -> None:
        del message
