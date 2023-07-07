# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import logging
from slack_sdk import WebClient
from odoo.tools.config import config, configmanager
import pytz
import os


class MyHandler(logging.Handler):
    config_file = os.path.join('/etc/odoo/', 'odoo.conf')
    cm = configmanager(fname=config_file)
    slack_bot_token = str(cm.get('slack_bot_token'))
    slack_error_channel = str(cm.get('slack_error_channel'))
    slack_warning_channel = str(cm.get('slack_warning_channel'))
    sc = WebClient(slack_bot_token)

    def emit(self, record):
        if record:
            text = ''
            if record.exc_text:
                text = record.exc_text
            elif record.message:
                text = record.message
            now = fields.Datetime.now().replace(tzinfo=pytz.UTC)
            now = now.astimezone(pytz.timezone("Europe/Berlin")).strftime('%Y-%m-%d %H:%M:%S')
            channel = False
            if record.levelname in ['ERROR']:
                channel = self.slack_error_channel,
            elif record.levelname in ['WARNING']:
                channel = self.slack_warning_channel,
            if channel:
                try:
                    response = self.sc.chat_postMessage(
                        channel=self.slack_warning_channel,
                        text=now + "    " + text
                    )
                except Exception as e:
                    print(e)


mh = MyHandler()
logging.getLogger().addHandler(mh)


class SlackCalls(models.TransientModel):
    _name = 'slack.calls'
    _description = "slack"

    @api.model
    def notify_slack(self, source, message, channel_id=None, attachment=None):
        pass
        # slack_bot_token = self.env['ir.config_parameter'].get_param('slack_bot_token')
        # slack_cron_info_channel_id = self.env['ir.config_parameter'].get_param('slack_cron_info_channel_id')
        # if not channel_id:
        #     channel_id = self.env['ir.config_parameter'].get_param('slack_odoo_cron_info_channel_id')
        # sc = WebClient(slack_bot_token)
        # slack_channel_id = ' '
        # response = self.sc.chat_postMessage(
        #     channel=self.slack_channel_id,
        #     text=message
        # )
