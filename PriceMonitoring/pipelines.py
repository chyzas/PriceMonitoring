# -*- coding: utf-8 -*-

from PriceMonitoring.models import *
from time import strftime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class PricemonitoringPipeline(object):
    def process_item(self, item, spider):
        price_original = item['price']
        price = self.to_int(price_original)
        item_id = item['item_id']

        last = Prices.select().where(Prices.item == item_id).order_by(Prices.id.desc())

        if last.count() == 0:
            Prices.create(
                item=item['item_id'],
                price_original=price_original,
                price=price,
                created_at=strftime("%Y-%m-%d %H:%M:%S")
            )
        else:
            if self.to_int(last.get().price_original) != price:
                try:
                    result = Prices.create(
                        item=item['item_id'],
                        price_original=price_original,
                        price=price,
                        created_at=strftime("%Y-%m-%d %H:%M:%S")
                    )
                    history = Prices.select().where(Prices.item == item_id)
                    self.send_mail(item, self.get_message(result, history), spider)
                except Exception as e:
                    print e
        return item

    def to_int(self, str):
        return int(''.join([i for i in str if i.isdigit()]))

    def get_message(self, result, history):
        message = '<h3>Kaina pasikeite</h3>'
        message += '<br>'
        message += '<br>'
        message += 'Adresas: ' + result.item.url
        message += '<br>'
        message += '<br>'
        if len(history) > 1:
            message += '<br>'.join([str(x.created_at) + ' - ' + str(x.price_original) for x in history])

        return message

    def send_mail(self, item, message, spider):
        try:
            mail_settings = spider.settings.get('MAIL')
            msg = MIMEMultipart()
            msg['From'] = mail_settings['from']
            msg['To'] = mail_settings['to']
            msg['Subject'] = 'Kainos pasikeitimas ' +item['name']

            msg.attach(MIMEText(message, 'html', _charset='utf-8'))
            mailServer = smtplib.SMTP(mail_settings['server'], mail_settings['port'])
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(mail_settings['user'], mail_settings['pass'])
            mailServer.sendmail(mail_settings['from'], mail_settings['to'], msg.as_string())
            mailServer.close()
        except Exception as e:
            print e