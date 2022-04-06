from dataclasses import dataclass, field
from email.message import EmailMessage
from typing import ClassVar, Iterable, Optional
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
    html_version: Optional[str] = None,
    attachments: Optional[Iterable[Attachment]] = None,
):
    msg = EmailMessage()
    # header
    msg.add_header("From", from_)
    msg.add_header("To", to if isinstance(to, str) else ", ".join(to))
    msg.add_header("Subject", subject)
    # payload
    msg.set_content(text_version)
    if html_version:
        msg.add_alternative(html_version, subtype="html")
    if attachments:
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

    """
    # Example

    ```python
    class NaverEmailNotification(BaseEmailNotification):
        HOST = "smtp.naver.com"
        PORT = 587
        USERNAME = "naver account id"
        PASSWORD = "naver account password"

    msg = build_email_message(
        from_="from@example.com",
        to=["to@example.com"],
        subject="제목",
        text_version="Text Version",
        html_version="<html>HTML Version</html>",
        attachments=[
            Attachment(filename="filename.txt", bytes=b"file.read()"),
        ],
    )

    sender = NaverEmailNotification()
    asyncio.run(sender.send(msg))
    ```
    """

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
