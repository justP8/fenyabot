import asyncio

import aiogram.exceptions

from cfg import logger
from bot import run_webhook, run_polling
from loader import postgres


async def main():
    mode = input('Webhook (w) / polling (p)?\n')
    modes = {'webhook': run_webhook, 'w': run_webhook, 'wh': run_webhook,
             'polling': run_polling, 'p': run_polling, 'poll': run_polling}
    while mode not in modes:
        print('Unknown mode, try again')
        mode = input('Webhook (w) / polling (p)?')

    await postgres.init_orm()
    await modes[mode]()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except aiogram.exceptions.AiogramError as e:
        logger.info(f'Во время работы бота произошла ошибка: {e.args}')
    except KeyboardInterrupt:
        logger.info('Bot offline')
    # except Exception as e:
    #     logger.info(f'Во время работы кода произошла ошибка: {e.args}')
