
from fastapi_mail import MessageSchema, FastMail

from starlette.responses import JSONResponse

from base.config import conf



async def send_activation_mail(receipient,body):
    message = MessageSchema(
        subject="Account Confirmation",
        recipients=receipient,  # List of recipients, as many as you can pass
        template_body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="activation.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
