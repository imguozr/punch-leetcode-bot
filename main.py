import configparser
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

config = configparser.ConfigParser()
config.read_file(open(r'config.cfg'))
token = config.get('bot-config', 'token')

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="今天，你突开 LeetCode 了吗？")


def inline_query(update, context):
    query = update.inline_query.query
    questions = _query_question_number(query)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="今天突开 LeetCode 了吗？",
            description='一突开就溅得我满脸算法',
            input_message_content=InputTextMessageContent('今天突开 LeetCode 了吗？')
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="今天突开了哪些题？用空格隔开题号！",
            description=questions,
            input_message_content=InputTextMessageContent(questions)
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title='没有，没有，没有~',
            description='通过！',
            input_message_content=InputTextMessageContent('没有 没有 没有')
        )
    ]
    update.inline_query.answer(results)


def _query_question_number(inputs):
    questions = inputs.split()
    if len(questions) == 1:
        return '今天突开了第' + questions[0] + '题'
    else:
        return '今天突开了第' + '、'.join(questions) + '题'


def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(InlineQueryHandler(inline_query))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
