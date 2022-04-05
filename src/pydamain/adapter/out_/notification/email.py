from dataclasses import dataclass, field
from email.message import EmailMessage
from typing import ClassVar, Iterable
import mimetypes

from aiosmtplib import send


@dataclass(slots=True, kw_only=True)
class Attachment:
    content_type: str = field(init=False)
    filename: str
    bytes: bytes

    def __post_init__(self):
        content_type, encoding = mimetypes.guess_type(self.filename)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        self.content_type = content_type


def build_email_message(
    *,
    from_: str,
    to: str | Iterable[str],
    subject: str,
    text_version: str,
    html_version: str,
    attachments: Iterable[Attachment] = [],
):
    msg = EmailMessage()
    # header
    msg.add_header("From", from_)
    msg.add_header("To", to if isinstance(to, str) else ", ".join(to))
    msg.add_header("Subject", subject)
    # payload
    msg.add_alternative(text_version)
    msg.add_alternative(html_version, subtype="html")
    for attachment in attachments:
        main, sub = attachment.content_type.split("/", 1)
        msg.add_attachment(
            attachment.bytes,
            maintype=main,
            subtype=sub,
            filename=attachment.filename,
        )
    return msg


class BaseEmailNotification:

    HOST: ClassVar[str]
    PORT: ClassVar[int]
    USERNAME: ClassVar[str]
    PASSWORD: ClassVar[str]

    async def send(self, msg: EmailMessage):
        await send(
            msg,
            hostname=self.HOST,
            port=self.PORT,
            username=self.USERNAME,
            password=self.PASSWORD,
            start_tls=True,
        )
