import asyncio
import logging

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, Message, ChatMember, ReplyKeyboardMarkup, \
    InputMediaPhoto, InputMediaVideo
from telegram.constants import ParseMode, MessageLimit
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, PicklePersistence, \
    ConversationHandler
import pytz
import datetime
from server import server

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

PRIVATE_CHAT_ID = from_chat_id = -1001833792693

sub_chat = -1001833792693

BOT_TOKEN = "6684113299:AAHz5tnsKA8ZSEETEkkEkLPbs0IeicXwhZ0"

reply_keyboard = [["نشر"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
reply_keyboard1 = [
    ["Replace photo", "Replace text"],
    ["Replace link", "Replace button"],
    ["Review post"],
    ["Create post"]
]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard2 = [["تاكيد", "الغاء"]]

markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True, resize_keyboard=True)
CHOOSING, ConAns, link, photo, text, post, button, review, review0, link1, photo1, text1, button1 = range(13)
Anser, Anser1, Anser2, Anser3 = range(4)
PEA, EM, EditLink, EditText, EditMsgId, EditPhoto, EditButton = range(7)

wait_for_msg = False
wait_for_msg2 = False
wait_for_msg3 = False


async def ForwardMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user_id = update.effective_user.id
    bot_data = context.bot_data
    user_name = update.effective_user.full_name
    chat_id = sub_chat
    if "Url" not in bot_data:
        bot_data.setdefault("Url", "https://short-jambo.com/Zm8GgeL")
    if "KeyUrl" not in bot_data:
        bot_data.setdefault("KeyUrl", "SAO")
    chat_member = await Bot(BOT_TOKEN).getChatMember(chat_id, user_id)
    chat_member_list = [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]
    if "subs" not in bot_data:
        bot_data.setdefault("subs", {})
    if "user_ids" not in bot_data:
        bot_data.setdefault("user_ids", {})
    if chat_member.status in chat_member_list and user_id not in bot_data.get("subs"):
        if user_id not in bot_data.get("subs"):
            mydict2 = {user_id: user_name}
            bot_data.get("subs").update(mydict2)
    elif chat_member.status not in chat_member_list:
        if user_id in bot_data.get("subs", {}):
            del bot_data["subs"][user_id]

        url = f"https://t.me/{context.bot.username}"
        text = "انت لست مشتركا بالقناة قم بالشتراك ثم اعد المحاولة"
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="اشتراك", url=url)
        )
        await update.message.reply_text(text, reply_markup=keyboard)
        await asyncio.sleep(5)
    try:
        if str(context.args[0]) == bot_data["KeyUrl"] and chat.id not in bot_data.get("user_ids",
                                                                                      {}) and chat.id in bot_data.get(
            "subs",
            {}):
            mydict2 = {user_id: user_name}
            bot_data.get("user_ids").update(mydict2)
            await update.effective_message.reply_text(f"شكرا {user_name}. على دعمك.")
            await update.effective_message.reply_text("يمكنك الان تحميل التطبيقات")
            return
    except (IndexError, ValueError):
        pass
    try:

        if chat.id not in bot_data.get("user_ids", {}) and chat.id in bot_data.get("subs", {}):
            await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=PRIVATE_CHAT_ID,
                                              message_id="17")

            url = bot_data["Url"]
            text = ("قم بتخطي الرابط التالي لتتمكن من استخدام البوت:")
            keyboard = InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="تخطي الرابط", url=url)
            )
            await update.message.reply_text(text, reply_markup=keyboard)
            await asyncio.sleep(3)
    except (IndexError, ValueError):
        pass
    try:
        if chat.id in bot_data.get("user_ids", {}) and chat.id in bot_data.get("subs", {}):

            if (context.args[0]).isdigit() and int(context.args[0]) in bot_data["msgs_data"]:
                if int(context.args[0]) > 1 and chat.id in bot_data.get("user_ids", {}) and chat.id in bot_data.get(
                        "subs",
                        {}):
                    await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=PRIVATE_CHAT_ID,
                                                      message_id=int(context.args[0]), protect_content=True)
                    await asyncio.sleep(2)
    except (IndexError, ValueError):
        await update.effective_message.reply_text("لتحميل تطبيق استخدم رابطه الموجود في القناة")


async def show_bot_start_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data_subs = context.bot_data.get("subs", {})
    subs_list = ["قائمة تشغيل البوت:"]
    if bot_data_subs:
        for i, (user_id, user_name) in enumerate(bot_data_subs.items(), start=1):
            subs_list.append(f"{i}. {user_id} | {user_name}")

        text = "\n".join(subs_list)

        if len(text) <= MessageLimit.MAX_TEXT_LENGTH:
            return await update.message.reply_text(text="\n".join(subs_list), parse_mode=ParseMode.HTML,
                                                   disable_web_page_preview=True)
        else:
            parts = []
            while len(text) > 0:
                if len(text) > MessageLimit.MAX_TEXT_LENGTH:
                    part = text[:MessageLimit.MAX_TEXT_LENGTH]
                    first_lnbr = part.rfind('\n')
                    if first_lnbr != -1:
                        parts.append(part[:first_lnbr])
                        text = text[(first_lnbr + 1):]
                    else:
                        parts.append(part)
                        text = text[MessageLimit.MAX_TEXT_LENGTH:]
                else:
                    parts.append(text)
                    break

            msg = None
            for part in parts:
                msg = await update.message.reply_text(text=part, parse_mode=ParseMode.HTML,
                                                      disable_web_page_preview=True)
                await asyncio.sleep(2)
            return msg

    else:
        await update.message.reply_text('قائمة تشغيل البوت فارغة')


async def show_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data_ids = context.bot_data.get("user_ids", {})
    users_list = [":قائمة المستخدمين"]
    if bot_data_ids:
        for i, (user_id, user_name) in enumerate(bot_data_ids.items(), start=1):
            user_list = f"{i}. {user_id} | {user_name}"
            users_list.append(user_list)

        text = "\n".join(users_list)

        if len(text) <= MessageLimit.MAX_TEXT_LENGTH:
            return await update.message.reply_text(text="\n".join(users_list), parse_mode=ParseMode.HTML,
                                                   disable_web_page_preview=True)
        else:
            parts = []
            while len(text) > 0:
                if len(text) > MessageLimit.MAX_TEXT_LENGTH:
                    part = text[:MessageLimit.MAX_TEXT_LENGTH]
                    first_lnbr = part.rfind('\n')
                    if first_lnbr != -1:
                        parts.append(part[:first_lnbr])
                        text = text[(first_lnbr + 1):]
                    else:
                        parts.append(part)
                        text = text[MessageLimit.MAX_TEXT_LENGTH:]
                else:
                    parts.append(text)
                    break

            msg = None
            for part in parts:
                msg = await update.message.reply_text(text=part, parse_mode=ParseMode.HTML,
                                                      disable_web_page_preview=True)
                await asyncio.sleep(2)
            return msg


    else:
        await update.message.reply_text('قائمة المستخدمين فارغة')


async def Clearids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text1 = "تم الغاء صلاحيات وصلول جميع المستخدمين"
    if context.bot_data.get("subs"):
        context.bot_data.get("subs").clear()
    elif not context.bot_data.get("subs"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة تشغيل البوت فارغة")
    if context.bot_data.get("user_ids"):
        context.bot_data.get("user_ids").clear()
    elif not context.bot_data.get("user_ids"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة المشتركين فارغة")
    await context.bot.sendMessage(chat_id=789221262, text=text1)
    await context.bot.sendMessage(chat_id=5475147476, text=text1)


async def AutoClearids(context: ContextTypes.DEFAULT_TYPE):
    text1 = "تم الغاء صلاحيات وصلول جميع المستخدمين"
    if context.bot_data.get("subs"):
        context.bot_data.get("subs").clear()
    elif not context.bot_data.get("subs"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة تشغيل البوت فارغة")
    if context.bot_data.get("user_ids"):
        context.bot_data.get("user_ids").clear()
    elif not context.bot_data.get("user_ids"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة المشتركين فارغة")
    await context.bot.sendMessage(chat_id=789221262, text=text1)
    await context.bot.sendMessage(chat_id=5475147476, text=text1)


async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global wait_for_msg
    wait_for_msg = True
    await update.message.reply_text("قم بتحويل الرسالة المراد حفظها من قناة السحابه")


async def add_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_id = update.message.forward_from_message_id
    global wait_for_msg
    if wait_for_msg:
        bot_data = context.bot_data
        if "msgs_data" not in bot_data:
            context.bot_data.setdefault("msgs_data", {})
        if Message.forward_from_chat:
            if msg_id in context.bot_data.setdefault("msgs_data", {}):
                await update.message.reply_text("الوثيقة موجودة مسبقا.")
                wait_for_msg = False

            elif update.effective_message.document is not None and update.effective_message.document.file_name is not None and update.effective_message.document.file_size is not None:
                app_name = update.effective_message.document.file_name
                app_size = update.effective_message.document.file_size
                mydict2 = {msg_id: {1: app_name, 2: app_size}}
                bot_data.get("msgs_data").update(mydict2)
                await update.message.reply_text("تم اضافة الوثيقة بنجاح.")
                wait_for_msg = False
            else:
                msg_id = update.message.forward_from_message_id
                app_name = "None"
                app_size = "None"
                bot_data = context.bot_data
                if "msgs_data" not in bot_data:
                    context.bot_data.setdefault("msgs_data", {})
                mydict2 = {msg_id: {1: app_name, 2: app_size}}
                bot_data.get("msgs_data").update(mydict2)
                await update.message.reply_text("تم اضافة الرسالة بنجاح.")
                wait_for_msg = False
        else:
            await update.message.reply_text("ليست رسالة محولة من قناة.")
            wait_for_msg = False


async def del_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.get("msgs_data")
    if bot_data:
        try:
            due = int(context.args[0])
            delete_index = due
            if 1 <= delete_index <= len(bot_data):
                bot_data.pop(list(bot_data.keys())[delete_index - 1])
                await update.message.reply_text("تم حذف الرسالة بنجاح.")
            else:
                await update.message.reply_text("رقم الرسالة غير صالح.")
        except (IndexError, ValueError):
            await update.message.reply_text("انت لم تقم بتحديد الرسالة لحذفها.")
    else:
        await update.message.reply_text("لا يوجد رسائل لحذفها.")


async def start_show_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global wait_for_msg2
    wait_for_msg2 = True
    await update.message.reply_text("قم بتحويل الرسالة المراد اظهارها من قناة السحابه")


async def show_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = update.message.forward_from_message_id
        channel_id = str(PRIVATE_CHAT_ID)
        bot = (await Bot(BOT_TOKEN).get_me())
        bot_name = bot.username
        channel_id = channel_id[3:]
        if "msgs_data" not in context.bot_data:
            context.bot_data.setdefault("msgs_data", {})
        bot_data = context.bot_data.get("msgs_data", {})
        global wait_for_msg2
        if wait_for_msg2:
            if Message.forward_from_chat:
                if args in bot_data:
                    if int(args) in bot_data:
                        value = bot_data[int(args)]
                        app_size = value[2]
                        app_name = value[1]
                        app_size_mb = app_size / 1_024_000
                        deepurl0 = f"https://t.me/{bot_name}?start={args}"
                        deepurl = f'<a href="{deepurl0}">Link</a>'
                        url = f"https://t.me/c/{channel_id}/{args}"
                        msg_id1 = f'<a href="{url}">{args}</a>'
                        msg_list = (f"ID: {msg_id1} - {deepurl}\n"
                                    f"App Name: <code>{(app_name)}</code> \n"
                                    f"App Size: {app_size_mb:.2f} MB \n")
                        await update.message.reply_text(msg_list, parse_mode=ParseMode.HTML,
                                                        disable_web_page_preview=True)
                        wait_for_msg2 = False
                else:
                    await update.message.reply_text("الرسالة غير مضافة.")
                    wait_for_msg2 = False
    except (IndexError, ValueError):
        await update.message.reply_text("انت لم تقم بتحديد الرسالة.")
        wait_for_msg2 = False


async def show_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_id = str(PRIVATE_CHAT_ID)
    bot = (await Bot(BOT_TOKEN).get_me())
    bot_name = bot.username
    channel_id = channel_id[3:]
    bot_data = context.bot_data.get("msgs_data", {})
    if bot_data:
        msgs_list = ["قائمة الرسائل المحفوظة:"]
        for i, (msg_id, msg_info) in enumerate(bot_data.items(), start=1):
            app_size = msg_info.get(2, "None")
            app_name = msg_info.get(1, "None")
            app_size_mb = app_size / 1_024_000 if app_size != "None" else "None"
            deepurl0 = f"https://t.me/{bot_name}?start={msg_id}"
            deepurl = f'<a href="{deepurl0}">Link</a>'
            url = f"https://t.me/c/{channel_id}/{msg_id}"
            msg_id1 = f'<a href="{url}">{msg_id}</a>'
            app_size_mb_f = f"{app_size_mb:.2f}" if app_size_mb != "None" else "None"
            msg_list = (f"{i}. ID: {msg_id1} - {deepurl}\n"
                        f"App Name: <code>{(app_name)}</code> \n"
                        f"App Size: {app_size_mb_f} MB \n")
            msgs_list.append(msg_list)
        text = "\n".join(msgs_list)

        if len(text) <= MessageLimit.MAX_TEXT_LENGTH:
            return await update.message.reply_text(text="\n".join(msgs_list), parse_mode=ParseMode.HTML,
                                                   disable_web_page_preview=True)
        else:
            parts = []
            while len(text) > 0:
                if len(text) > MessageLimit.MAX_TEXT_LENGTH:
                    part = text[:MessageLimit.MAX_TEXT_LENGTH]
                    first_lnbr = part.rfind('\n')
                    if first_lnbr != -1:
                        parts.append(part[:first_lnbr])
                        text = text[(first_lnbr + 1):]
                    else:
                        parts.append(part)
                        text = text[MessageLimit.MAX_TEXT_LENGTH:]
                else:
                    parts.append(text)
                    break

            msg = None
            for part in parts:
                msg = await update.message.reply_text(text=part, parse_mode=ParseMode.HTML,
                                                      disable_web_page_preview=True)
                await asyncio.sleep(1)
            return msg
    else:
        await update.message.reply_text('قائمة الرسائل المحفوظة فارغة')


async def check_for_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = (await Bot(BOT_TOKEN).get_me())
    bot_name = bot.username
    if update.effective_chat.id == PRIVATE_CHAT_ID:
        bot_data = context.bot_data
        if "msgs_data" not in bot_data:
            context.bot_data.setdefault("msgs_data", {})

        msg_id = update.effective_message.message_id
        app_name = update.effective_message.document.file_name
        app_size = update.effective_message.document.file_size
        mydict2 = {msg_id: {1: app_name, 2: app_size}}
        AppLink0 = f"https://t.me/{bot_name}?start={update.effective_message.id}"
        AppLink = f'<a href="{AppLink0}">AppLink</a>'
        bot_data.get("msgs_data").update(mydict2)
        text = (f"<code>###App Name###</code>\n"
                f"<code>{app_name}</code>\n\n"
                f"###{AppLink}###")
        await context.bot.send_message(text=text, chat_id=PRIVATE_CHAT_ID, parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True)
        await asyncio.sleep(1)


async def Post_EditMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="هل انت متاكد من تعديل منشور؟", reply_markup=markup2)
    return PEA


async def EditMsgConf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "تاكيد":
        await update.message.reply_text(text="قم بتحويل الرسالة المراد تعديلها")
        return EditMsgId
    elif update.effective_message.text == "الغاء":
        return ConversationHandler.END


async def EditMsgId_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.video, update.message.photo)
    context.user_data['MsgId'] = update.message.forward_from_message_id
    await update.message.reply_text("تم تحديد الرسالة المراد تعديلها -> قم بارسال الرابط الجديد")
    return EditLink


async def EditLink_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text.startswith('http') or update.effective_message.text.startswith('https'):
        context.user_data['link0'] = update.effective_message.text
        await update.message.reply_text("تم تعديل الرابط -> قم بارسال الصورة الجديدة")
        return EditPhoto
    else:
        await update.message.reply_text("هذا ليس رابطا -> اعد ارسال الرابط")
        return EditLink


async def EditPhoto_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo0'] = update.effective_message.photo[-1].file_id
    await update.message.reply_text("تم تعديل الصورة -> قم بارسال نص الرسالة الجديد")
    return EditText


async def EditText_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['text0'] = update.effective_message.text
    await update.message.reply_text("تم اضافة نص الرسالة -> قم بارسال نص الزر")
    return EditButton


async def EditButton_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['button0'] = update.effective_message.text
    await update.message.reply_text(text="تم اضافة نص الزر -> قم بمراجعة المنشور")
    button = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text=context.user_data['button0'], url=context.user_data['link0'])
    )
    await Bot(BOT_TOKEN).edit_message_media(media=InputMediaPhoto(media=context.user_data['photo0'],
                                                                  caption=context.user_data['text0']),
                                            message_id=context.user_data['MsgId'],
                                            chat_id=sub_chat,
                                            reply_markup=button)
    await update.message.reply_text(text="تم تعديل المنشور")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text="تم الخروج من وضع انشاء منشور")
    return ConversationHandler.END


async def AskForCon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="هل انت متاكد من انشاء منشور؟", reply_markup=markup2)
    return ConAns


async def start_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "تاكيد":
        await update.message.reply_text(text="قم بارسال الرابط")
        return link
    elif update.effective_message.text == "الغاء":
        return ConversationHandler.END


async def link_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text.startswith('http') or update.effective_message.text.startswith('https'):
        context.user_data['link'] = update.effective_message.text
        await update.message.reply_text("تم اضافة الرابط -> قم بارسال الصورة")
        return photo
    else:
        await update.message.reply_text("هذا ليس رابطا -> اعد ارسال الرابط")
        return link


async def photo_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo'] = update.effective_message.photo[-1].file_id
    await update.message.reply_text("تم اضافة الصورة -> قم بارسال نص الرسالة")
    return text


async def text_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['text'] = update.effective_message.text
    await update.message.reply_text("تم اضافة نص الرسالة -> قم بارسال نص الزر")
    return button


async def button_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['button'] = update.effective_message.text
    await update.message.reply_text(text="تم اضافة نص الزر -> قم بمراجعة المنشور", reply_markup=markup1)
    button = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text=context.user_data['button'], url=context.user_data['link'])
    )
    await update.message.reply_photo(photo=context.user_data['photo'], caption=context.user_data['text'],
                                     reply_markup=button)
    return review


async def edit_link_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text.startswith('http') or update.effective_message.text.startswith('https'):
        context.user_data['link'] = update.effective_message.text
    await update.message.reply_text(text="تم استبدال الرابط", reply_markup=markup1)
    return review


async def edit_photo_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo'] = update.effective_message.photo[-1].file_id
    await update.message.reply_text(text="تم استبدال الصورة", reply_markup=markup1)
    return review


async def edit_text_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['text'] = update.effective_message.text
    await update.message.reply_text(text="تم استبدال النص", reply_markup=markup1)
    return review


async def edit_button_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['button'] = update.effective_message.text
    await update.message.reply_text(text="تم استبدال نص الزر", reply_markup=markup1)
    return review


async def review_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "Replace link":
        await update.message.reply_text("قم بارسال الرابط الجديد")
        return link1

    elif update.effective_message.text == "Replace photo":
        await update.message.reply_text("قم بارسال الصورة الجديدة")
        return photo1

    elif update.effective_message.text == "Replace text":
        await update.message.reply_text("قم بارسال النص الجديد")
        return text1

    elif update.effective_message.text == "Replace button":
        await update.message.reply_text("قم بارسال نص الزر الجديد")
        return button1

    elif update.effective_message.text == "Review post":
        await update.message.reply_text("المنشور الحالي:")
        button = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text=context.user_data['button'], url=context.user_data['link'])
        )
        await update.message.reply_photo(photo=context.user_data['photo'], caption=context.user_data['text'],
                                         reply_markup=button)
        return review
    elif update.effective_message.text == "Create post":
        await update.message.reply_text(text="هل تريد نشر المنشور؟\n"
                                             "يمكنك الغاء الامر عن طريق ارسال /cancel", reply_markup=markup)
        return post


async def create_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text=context.user_data['button'], url=context.user_data['link'])
    )
    await context.bot.send_photo(photo=context.user_data['photo'], caption=context.user_data['text'], chat_id=sub_chat,
                                 reply_markup=button)
    return ConversationHandler.END


async def StartChangekeyUrl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="هل انت متاكد من تغيير المفتاح و الرابط؟", reply_markup=markup2)
    return Anser


async def StartChangeKeyUrl_step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "تاكيد":
        await update.message.reply_text(text="قم بارسال الرابط")
        return Anser2
    elif update.effective_message.text == "الغاء":
        return ConversationHandler.END


async def ChangeKeyUrl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    if update.effective_message.text.startswith('http') or update.effective_message.text.startswith('https'):
        bot_data["Url"] = update.effective_message.text
        await update.message.reply_text(text="قم بارسال المفتاح")
        return Anser3
    else:
        await update.message.reply_text(text="هذا ليس رابط -> اعد ارسال الرابط")
        return Anser2


async def StartChangeKeyUrl_step3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    bot_data["KeyUrl"] = update.effective_message.text
    await update.message.reply_text(text=f"{bot_data['KeyUrl']}تم تغيير المفتاح و الرابط -> المفتاح الحالي: ")
    return ConversationHandler.END


async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = (f"<code>/CreatePost</code> -> امر يقوم بعمل منشور مع زر\n"
                f"<code>/ShowMsgs</code> -> امر اظهار الرسائل المحفوظه\n"
                f"<code>/ShowMsg</code> -> امر اظهار رساله محفوظه\n"
                f"<code>/DelMsg</code> -> (امر حذف الرسائل المحفوظه عن طريق (رقم الرسالة\n"
                f"<code>/AddMsg</code> -> امر يقوم باضافة رسالة الى القائمة المحفوظة\n"
                f"<code>/ShowUL</code> -> امر يقوم باظهار قائمة تخطي الاعلان\n"
                f"<code>/ShowBSL</code> -> امر يقوم باظهار قائمة تشغيل البوت \n"
                f"<code>/ClearIDs</code> -> امر يقوم بحذف مباشر للمستخدمين\n"
                f"<code>/UpdateUrl</code> -> امر يقوم بتغيير المفتاح و الرابط\n")
    await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def main() -> None:
    today = datetime.time(hour=0, minute=20, second=0, tzinfo=pytz.timezone('Asia/Damascus'))
    persistence = PicklePersistence(filepath="bot_data", update_interval=30)
    # defaults = Defaults(tzinfo=pytz.timezone('Asia/Damascus'))
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    application.add_handler(CommandHandler("start", ForwardMsg))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("CreatePost", AskForCon, filters.User(user_id=[5475147476, 789221262]))],
        states={
            ConAns: [MessageHandler(filters.TEXT, start_create)],
            link: [MessageHandler(filters.TEXT, link_step)],
            photo: [MessageHandler(filters.PHOTO, photo_step)],
            text: [MessageHandler(filters.TEXT, text_step)],
            button: [MessageHandler(filters.TEXT, button_step)],
            link1: [MessageHandler(filters.TEXT, edit_link_step)],
            photo1: [MessageHandler(filters.PHOTO, edit_photo_step)],
            text1: [MessageHandler(filters.TEXT, edit_text_step)],
            button1: [MessageHandler(filters.TEXT, edit_button_step)],
            review: [MessageHandler(filters.TEXT, review_step)],
            post: [MessageHandler(filters.Regex("نشر"), create_post)]
        },
        fallbacks=[MessageHandler(filters.Regex("نشر"), create_post), CommandHandler("cancel", cancel)],
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("UpdateUrl", StartChangekeyUrl, filters.User(user_id=[5475147476, 789221262]))],
        states={
            Anser: [MessageHandler(filters.TEXT, StartChangeKeyUrl_step2)],
            Anser2: [MessageHandler(filters.TEXT, ChangeKeyUrl)],
            Anser3: [MessageHandler(filters.TEXT, StartChangeKeyUrl_step3)]
        },
        fallbacks=[MessageHandler(filters.TEXT, StartChangeKeyUrl_step3)],
    )

    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler("EditMsg", Post_EditMsg, filters.User(user_id=[5475147476, 789221262]))],
        states={
            PEA: [MessageHandler(filters.TEXT, EditMsgConf)],
            EditMsgId: [MessageHandler(filters.FORWARDED, EditMsgId_step)],
            EditLink: [MessageHandler(filters.TEXT, EditLink_step)],
            EditPhoto: [MessageHandler(filters.PHOTO, EditPhoto_step)],
            EditText: [MessageHandler(filters.TEXT, EditText_step)],
            EditButton: [MessageHandler(filters.TEXT, EditButton_step)],
        },
        fallbacks=[MessageHandler(filters.Regex("نشر"), create_post), CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)

    application.add_handler(
        CommandHandler("shelp", admin_help, filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(
        CommandHandler("ShowMsgs", show_msgs,
                       filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(
        CommandHandler("DelMsg", del_msg, filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(
        CommandHandler("ShowMsg", start_show_msg,
                       filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(
        CommandHandler("AddMsg", start_add, filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(CommandHandler("ShowBSl", show_bot_start_list,
                                           filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(CommandHandler("ShowUL", show_users_list,
                                           filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.job_queue.run_daily(callback=AutoClearids, time=today)

    application.add_handler(
        CommandHandler("ClearIDs", Clearids, filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.Document.APK, check_for_file))

    application.add_handler(MessageHandler(~filters.ChatType.CHANNEL & filters.FORWARDED, show_msg))

    application.add_handler(MessageHandler(~filters.ChatType.CHANNEL & filters.FORWARDED, add_msg))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    server()
    main()
