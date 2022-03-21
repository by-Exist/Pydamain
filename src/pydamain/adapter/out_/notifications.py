from typing import ClassVar, Literal
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from aiosmtplib import SMTP

from pydamain.port.out_.notifications import AbstractNotification


class BaseEmailNotification(AbstractNotification):

    host: ClassVar[str]
    port: ClassVar[int]
    username: ClassVar[str | None] = None
    password: ClassVar[str | None] = None

    def __init__(self) -> None:
        config = {
            "hostname": self.host,
            "port": self.port,
        }
        if self.username and self.password:
            config["username"] = self.username
            config["password"] = self.password
            config["start_tls"] = True
        self.smtp_client = SMTP(**config)

    def pre_send(self):
        ...

    def post_send(self):
        ...

    async def send(
        self,
        from_: str,
        to: str | list[str],
        subject: str,
        text: str,
        subtype: Literal["html", "plain"] = "plain",
        files: list[tuple[str, bytes]] = [],
    ) -> None:
        self.pre_send()
        message: MIMEMultipart = MIMEMultipart("alternative")
        message["From"] = from_
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(text, subtype, "utf-8"))
        for file_name, file_bytes in files:
            ma = MIMEApplication(file_bytes)
            ma.add_header(
                "content-disposition", "attachment", filename=file_name
            )
            message.attach(ma)
        async with self.smtp_client:
            await self.smtp_client.send_message(message)
        self.post_send()
