import qrcode
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from src.clup.entities.observer_abc import Observer


class NotifyEnabledReservationOwner(Observer):
    def __init__(self, reservation_provider, user_provider, email_service_provider):
        self.reservation_provider = reservation_provider
        self.user_provider = user_provider
        self.email_service_provider = email_service_provider
        self.subject = 'Your reservation has been enabled'

    def execute(self, reservation_id):
        user_id = self.reservation_provider.get_user_id(reservation_id)
        user = self.user_provider.get_user(user_id)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['To'] = user.username
        
        text = MIMEText('<h3>Go shopping!</h3><br><img src="cid:qrimage">', 'html')
        msg.attach(text)

        img = qrcode.make(reservation_id)
        output = io.BytesIO()
        img.save(output, format='JPEG')
        image = MIMEImage(output.getvalue())
        image.add_header('Content-ID', '<qrimage>')
        msg.attach(image)
        self.email_service_provider.send(user.username, msg)

    def update(self, store_pool):
        reservation_id = store_pool.last_added
        self.execute(reservation_id)
