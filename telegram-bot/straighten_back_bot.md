# Assignment: Telegram "Posture Reminder" Bot

## Goal

Build a Telegram bot that sends a subscriber a posture reminder **every hour**: `Straighten your back!`

The bot must support subscribe/unsubscribe commands and work with multiple users simultaneously.

---

## What You Need to Know First

### 1. `async def` — asynchronous function

A regular function blocks the program until it finishes. If it's sending a message over the network, everything else has to wait.

`async def` declares a **coroutine** — a function that can be "paused" while it waits for a network response, letting other tasks run in the meantime.

```python
def sync_function():
    return "I'm a regular function"

async def async_function():
    return "I'm a coroutine"
```

In `python-telegram-bot` (v20+), **all command handlers must be `async`** because the library is built on `asyncio`.

### 2. `await` — wait for a coroutine's result

`await` goes before a coroutine call and means: "pause this function until that one returns, and let other tasks run while we wait."

```python
async def send_hello(bot, chat_id):
    # bot.send_message is a coroutine, so we use await
    await bot.send_message(chat_id=chat_id, text="Hello!")
```

Important: `await` can **only** be used inside an `async def`. Using it in a regular function is a SyntaxError.

### 3. `JobQueue` and `Job` — scheduled tasks

`JobQueue` is the built-in scheduler in `python-telegram-bot`. It can run a function:

- **once after a delay** — `run_once`
- **repeatedly with an interval** — `run_repeating` (this is what we need)
- **at a specific time of day** — `run_daily`

Each scheduled task is a `Job` object with:
- `name` — task name (handy to use the chat ID so you can find and cancel it later)
- `chat_id` — which chat it's bound to
- `schedule_removal()` method — cancels the task

Example:

```python
context.job_queue.run_repeating(
    callback=my_function,   # function to call
    interval=3600,          # how often (in seconds)
    first=10,               # delay before the first run
    chat_id=chat_id,        # accessible inside the callback
    name="reminder_123"     # name for later lookup
)
```

### 4. `Update` and `Context` — handler parameters

When a user sends a command, the library calls your handler with two arguments:

- **`update`** — what happened. `update.effective_chat.id` is the chat ID; `update.message.reply_text(...)` replies to the message.
- **`context`** — your working environment. `context.bot` is the bot object, `context.job_queue` is the scheduler, `context.job` is the current task (only available inside a JobQueue callback).

---

## Required Commands

| Command  | What it does                                                       |
|----------|--------------------------------------------------------------------|
| `/start` | Subscribe the user, schedule an hourly reminder                    |
| `/stop`  | Unsubscribe the user, cancel their JobQueue task                   |
| `/now`   | Send a reminder immediately (for testing)                          |

**Reminder text:** `Straighten your back! Posture check.`

---

## Setup

1. Create a bot via [@BotFather](https://t.me/BotFather) — `/newbot` — get the token.
2. Install dependencies:
   ```bash
   pip install "python-telegram-bot[job-queue]==21.6"
   ```
3. Save the token as an environment variable:
   ```bash
   export BOT_TOKEN="123456:ABC..."   # macOS/Linux
   set BOT_TOKEN=123456:ABC...        # Windows cmd
   ```

---

## Code Skeleton

Copy this file and fill in the `# TODO` blocks. Hints are right next to each task.

```python
"""
Telegram bot: posture reminder.
"""

import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- Configuration ----------
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
INTERVAL_SECONDS = 60 * 60          # 1 hour
FIRST_DELAY_SECONDS = 10            # first reminder after 10 seconds
REMINDER_TEXT = "Straighten your back! Posture check."

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- Helpers ----------
def job_name(chat_id: int) -> str:
    """
    Return a unique job name for a given chat.
    Hint: use an f-string, e.g. f"posture_{chat_id}".
    """
    # TODO: return a unique string for this chat
    pass


def remove_existing_job(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> bool:
    """
    Remove any previously scheduled job for this chat.
    Returns True if something was removed, False otherwise.

    Hints:
    - context.job_queue.get_jobs_by_name(name) returns a list of jobs
    - each job has a schedule_removal() method
    - bool(empty_list) is False
    """
    # TODO:
    # 1) get the list of jobs by name
    # 2) iterate and remove each one
    # 3) return True/False — was there anything to remove?
    pass


# ---------- Job callback ----------
async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    JobQueue calls this function on schedule.
    context.job is the current job; it has chat_id.

    Hints:
    - context.job.chat_id — who to send to
    - context.bot.send_message(chat_id=..., text=...) is a coroutine,
      so it needs await
    """
    # TODO: get chat_id from context.job and send REMINDER_TEXT
    pass


# ---------- Command handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start — subscribe the user.

    Steps:
    1) get chat_id (update.effective_chat.id)
    2) just in case, remove any existing job for this chat
       (in case the user is already subscribed — otherwise we get a duplicate)
    3) schedule a new one via context.job_queue.run_repeating(...)
       see the parameters in the "JobQueue" section above
    4) reply to the user with update.message.reply_text(...)
       (don't forget await!)
    """
    # TODO: implement subscription
    pass


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /stop — unsubscribe the user.

    Steps:
    1) get chat_id
    2) call remove_existing_job(...) and save the result
    3) reply with a different message depending on whether
       the user was subscribed
    """
    # TODO: implement unsubscription
    pass


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /now — send a reminder immediately (for testing).
    Hint: this is a single line — await update.message.reply_text(...)
    """
    # TODO
    pass


# ---------- Entry point ----------
def main() -> None:
    if BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise SystemExit("Set the BOT_TOKEN environment variable.")

    app = Application.builder().token(BOT_TOKEN).build()

    # TODO: register three handlers:
    #   app.add_handler(CommandHandler("start", start))
    #   app.add_handler(CommandHandler("stop",  stop))
    #   app.add_handler(CommandHandler("now",   now))

    logger.info("Bot is running. Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

---

## Acceptance Criteria

1. `python bot.py` runs without errors.
2. After `/start`, the first message arrives in ~10 seconds, then every hour.
3. `/stop` cancels reminders only for the user who sent it (other subscribers keep getting messages).
4. `/now` sends a message immediately.
5. Calling `/start` twice **does not create duplicates** (verify: after two `/start` calls, the message arrives once per cycle, not twice).
6. The code has no global `while True` or `time.sleep` — scheduling is handled by `JobQueue`.

---

## How to Test Without Waiting an Hour

For debugging, temporarily change:

```python
INTERVAL_SECONDS = 60      # once a minute
FIRST_DELAY_SECONDS = 5    # first one after 5 seconds
```

Don't forget to set it back to `60 * 60` before submitting.

---

## Bonus Tasks (optional)

1. **`/help`** — list all commands with descriptions.
2. **Custom interval** — `/start 30` subscribes to a reminder every 30 minutes. Hint: `context.args` is the list of arguments after the command.
3. **Quiet hours** — don't send messages between 23:00 and 7:00. Hint: inside `send_reminder`, compare `datetime.now().hour` to the boundaries.
4. **Persistent subscribers** — save chat IDs to SQLite/JSON so jobs are restored after a bot restart.
5. **Buttons** — instead of commands, show a `ReplyKeyboardMarkup` with "Subscribe / Unsubscribe / Now" buttons.

---

## Useful Links

- [python-telegram-bot — official docs](https://docs.python-telegram-bot.org/)
- [JobQueue tutorial](https://docs.python-telegram-bot.org/en/stable/telegram.ext.jobqueue.html)
- [asyncio — async/await basics](https://docs.python.org/3/library/asyncio.html)
