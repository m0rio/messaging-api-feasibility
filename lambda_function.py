import os
import sys
import logging

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数からLINEBotのチャンネルアクセストークンとシークレットを読み込む
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# apiとhandlerの生成（チャンネルアクセストークンとシークレットを渡す）
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Lambdaのメインの動作


def lambda_handler(event, context):

    logger.info(event)

# 認証用のx-line-signatureヘッダー
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

# テキストメッセージを受け取った時に呼ばれるイベント ================================
    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):

        # ユーザー情報を取得
        profile = line_bot_api.get_profile(line_event.source.user_id)
        logger.info(profile)
        logger.info(line_event)
        text = line_event.message.text
        line_bot_api.reply_message(
            line_event.reply_token, TextSendMessage(text=text))

    return {
        "statusCode": 200,
        "body": ""
    }
# ================================================================================
