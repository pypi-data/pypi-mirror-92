from dataclasses import dataclass
from typing import Dict, Literal, Type
import pyrogram.methods.messages
import pyrogram.scaffold
import telethon.tl.functions.messages

_MethodName = Literal["SendMessage", "SendPhoto", "..."]

PyrogramMethodBase = pyrogram.scaffold.Scaffold
TelethonMethodBase = telethon.tl.TLRequest


@dataclass
class Method:
    pyrogram: Type[PyrogramMethodBase]
    telethon: Type[TelethonMethodBase]


# noinspection PyTypeChecker,PydanticTypeChecker
METHOD_MAP: Dict[_MethodName, Method] = {
    "SendMessage": Method(
        pyrogram=pyrogram.methods.messages.SendMessage,
        telethon=telethon.tl.functions.messages.SendMessageRequest,
    )
}
