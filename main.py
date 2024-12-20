import ptbot
import os
import pytimeparse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def wait(author_id, message, bot):
    delay = pytimeparse.parse(message)
    if delay is not None and delay > 0:
        message_id = bot.send_message(author_id, "Запускаю таймер...")
        bot.create_countdown(delay, notify_progress, message_id=message_id, author_id=author_id, total=delay, bot=bot)
    else:
        bot.send_message(author_id, "Введите корректное время, например, '5s', '2m', '1h'.")


def notify_progress(secs_left, message_id, author_id, total, bot):
    progress_bar = render_progressbar(total, total - secs_left, length=30, fill='█', zfill='░')
    if secs_left > 0:
        bot.update_message(author_id, message_id, f"Осталось {secs_left} секунд\n{progress_bar}")
    else:
        bot.update_message(author_id, message_id, f"Осталось {secs_left} секунд\n{progress_bar}")
        bot.send_message(author_id, "Время вышло!")


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == "__main__":
    main()
