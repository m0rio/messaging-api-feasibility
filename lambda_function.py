from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    PostbackEvent,
    LocationMessage, LocationSendMessage, StickerSendMessage, ImagemapSendMessage,
    BaseSize, Video, ImagemapArea, ExternalLink, URIImagemapAction, MessageImagemapAction,
    PostbackAction, MessageAction, URIAction, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage, BubbleContainer, ImageComponent,
    QuickReply, QuickReplyButton, DatetimePickerAction, RichMenu, RichMenuArea,
    RichMenuBounds, RichMenuSize
)
from linebot import (
    LineBotApi, WebhookHandler
)
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)


def lambda_handler(event, context):
    logger.info(event)
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    # テキストメッセージを受け取った時に呼ばれるイベント======================================
    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        # ユーザー情報を取得する
        profile = LINE_BOT_API.get_profile(line_event.source.user_id)
        logger.info(profile)

        message = line_event.message.text.lower()
        # 受取ったメッセージに応じて、対応するメッセージオブジェクトを返却する。
        if message == '位置情報':
            LINE_BOT_API.reply_message(
                line_event.reply_token, location_message)
        elif message == 'スタンプ':
            LINE_BOT_API.reply_message(
                line_event.reply_token, sticker_message)
        elif message == 'イメージマップ':
            LINE_BOT_API.reply_message(
                line_event.reply_token, imagemap_message)
        elif message == 'ボタンテンプレート':
            LINE_BOT_API.reply_message(
                line_event.reply_token, buttons_template_message)
        elif message == '確認テンプレート':
            LINE_BOT_API.reply_message(
                line_event.reply_token, confirm_template_message)
        elif message == 'カルーセルテンプレート':
            LINE_BOT_API.reply_message(
                line_event.reply_token, carousel_template_message)
        elif message == '画像テンプレート':
            LINE_BOT_API.reply_message(
                line_event.reply_token, image_carousel_template_message)
        elif message == 'フレックスメッセージ':
            LINE_BOT_API.reply_message(
                line_event.reply_token, flex_message)
        elif message == 'クイックリプライ':
            LINE_BOT_API.reply_message(
                line_event.reply_token, text_message)
        elif message == '日時選択':
            LINE_BOT_API.reply_message(
                line_event.reply_token, buttons_template_message_datetime)
        else:
            LINE_BOT_API.reply_message(
                line_event.reply_token, TextSendMessage("こんにちは！"))

    LINE_HANDLER.handle(body, signature)
    return 0
    # ==================================================================================


# 以下はMessage objects定義===============================================================
location_message = LocationSendMessage(
    title='my location',
    address='Tokyo',
    latitude=35.65910807942215,
    longitude=139.70372892916203
)
sticker_message = StickerSendMessage(
    package_id='1',
    sticker_id='1'
)

imagemap_message = ImagemapSendMessage(
    base_url='https://linebot-img.s3.ap-northeast-1.amazonaws.com/img/',
    alt_text='this is an imagemap',
    base_size=BaseSize(height=130, width=600),
    actions=[
        URIImagemapAction(
            link_uri='https://www.google.com/',
            area=ImagemapArea(
                x=0, y=0, width=520, height=1040
            )
        ),
        MessageImagemapAction(
            text='hello',
            area=ImagemapArea(
                x=520, y=0, width=520, height=1040
            )
        )
    ]
)

buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://prtimes.jp/i/33692/1/resize/d33692-1-628976-0.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            ),
            URIAction(
                label='uri',
                uri='http://example.com/'
            )
        ]
    )
)

confirm_template_message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='Are you sure?',
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            )
        ]
    )
)

carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://pbs.twimg.com/profile_images/1194506255898820608/Ykq-vveX_400x400.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    ),
                    URIAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://www.f-l-p.co.jp/wordpress/wp-content/uploads/2018/09/saison.png',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)
image_carousel_template_message = TemplateSendMessage(
    alt_text='ImageCarousel template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://pbs.twimg.com/profile_images/1194506255898820608/Ykq-vveX_400x400.jpg',
                action=PostbackAction(
                    label='postback1',
                    display_text='postback text1',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url='https://www.f-l-p.co.jp/wordpress/wp-content/uploads/2018/09/saison.png',
                action=PostbackAction(
                    label='postback2',
                    display_text='postback text2',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)

flex_message = FlexSendMessage(
    alt_text='hello',
    contents=BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url='https://example.com/cafe.jpg',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(uri='http://example.com', label='label')
        )
    )
)
# Flex Message===========================================================================
# Flex Message Simulatorで作成したJson
# true ->Trueに書き換える必要あり
payload = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
            "type": "uri",
            "uri": "http://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Brown Cafe",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "baseline",
                "margin": "md",
                "contents": [
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                    },
                    {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                    }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Place",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Time",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "10:00 - 23:00",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "CALL",
                    "uri": "https://linecorp.com"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": "https://linecorp.com"
                }
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "margin": "sm"
            }
        ],
        "flex": 0
    }
}
# new_from_json_dictメソッドはJSONデータをFlexMessage等各種オブジェクトに変換してくれるメソッドです
# FlexSendMessage.new_from_json_dict(対象のJSONデータ）とすることで、
# FlexSendMessage型に変換されます
flex_message = FlexSendMessage(
    alt_text='hello',
    contents=payload
)
# ==================================================================================================

text_message = TextSendMessage(
    text='please select',
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(
            label="label", text="text")),
        QuickReplyButton(action=MessageAction(
            label="label2", text="text")),
        QuickReplyButton(action=MessageAction(
            label="label3", text="text"))
    ]))

buttons_template_message_datetime = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://prtimes.jp/i/33692/1/resize/d33692-1-628976-0.jpg',
        title='日時選択',
        text='Please select',
        actions=[
            DatetimePickerAction(
                type="datetimepicker",
                label="Select date",
                data="storeId=12345",
                mode="datetime",
                initial="2017-12-25t00:00",
                max="2018-01-24t23:59",
                min="2017-12-25t00:00"
            )
        ]
    )
)

# リッチメニュー===================================================
rich_menu_to_create = RichMenu(
    # 全体のサイズを設定できます。widthは幅、heightは高さを表します。
    # sizeが2500×1686, 2500×843, 1200×810, 1200×405, 800×540, 800×270のみ
    size=RichMenuSize(width=1200, height=405),
    # デフォルトでリッチメニューを表示するならTrueにしましょう。
    selected=True,
    # ユーザには表示されないリッチメニューの名前です。リッチメニューの管理に役立ちます。
    name='richmenu',
    # チャットバーに表示されるテキストです。
    chat_bar_text='メニュー',
    # タップ領域の座標とサイズを定義します。
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=600, height=202),
            action=MessageAction(
                label='1',
                text='1'
            )
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=600, y=0, width=1200, height=405),
            action=MessageAction(
                label='2',
                text='2'
            )
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=864, width=1268, height=818),
            action=PostbackAction(data="not_submitted")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1273, y=877, width=1227, height=805),
            action=PostbackAction(data="forget")
        )
    ]
)
richMenuId = LINE_BOT_API.create_rich_menu(rich_menu=rich_menu_to_create)
# 画像のアップロード
with open("img/menu.png", 'rb') as f:
    LINE_BOT_API.set_rich_menu_image(richMenuId, "image/png", f)
# リッチメニューを設置
LINE_BOT_API.set_default_rich_menu(richMenuId)
# ===================================================================================
