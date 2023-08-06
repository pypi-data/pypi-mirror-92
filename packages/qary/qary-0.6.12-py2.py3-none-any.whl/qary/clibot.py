#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         bot = qary.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!

```bash
$ bot -b 'pattern,parul' -vv -p --num_top_replies=1
YOU: Hi
bot: Hello!
YOU: Looking good!
```
"""
from collections import abc
import importlib
import json
import logging
import os
import sys

import numpy as np
import pandas as pd

from qary import constants
from qary.skills.base import normalize_replies

__author__ = "see AUTHORS.md and README.md: Travis, Nima, Erturgrul, Aliya, Xavier, Maria, Hobson, ..."
__copyright__ = "Hobson Lane"
__license__ = "The Hippocratic License (MIT + *Do No Harm*, see LICENSE.txt)"


log = logging.getLogger(__name__)

log.info(f'sys.path: {sys.path}')
log.info(f'constants: {dir(constants)}')
log.info(f'BASE_DIR: {constants.BASE_DIR}')
log.info(f'SRC_DIR: {constants.SRC_DIR}')
log.info(f'sys.path (after append): {sys.path}')
from qary.scores.quality_score import QualityScore  # noqa

BOT = None


class CLIBot:
    """ Conversation manager intended to interact with the user on the command line, but can be used by other plugins/

    >>> CLIBot(bots='parul,pattern'.split(','), num_top_replies=1).reply('Hi')
    'Hello!'
    """
    bot_names = []
    bot_modules = []
    bots = []

    def __init__(
            self,
            bots=constants.DEFAULT_BOTS,
            num_top_replies=None,
            **quality_kwargs):
        if isinstance(bots, str):
            bots = bots.split(',')
        if not isinstance(bots, abc.Mapping):
            bots = dict(zip(bots, [{}] * len(bots)))
        log.info(f'CLIBot(bots={bots}')
        for bot_name, bot_kwargs in bots.items():
            bot_kwargs = {} if bot_kwargs is None else dict(bot_kwargs)
            self.add_skill(bot_name, **bot_kwargs)
        self.num_top_replies = constants.DEFAULT_CONFIG['num_top_replies'] if num_top_replies is None else min(
            max(int(num_top_replies), 1), 10000)
        self.repliers = [bot.reply if hasattr(bot, 'reply') else bot for bot in self.bots if bot is not None]
        log.debug(f'Loaded skills: {self.bots}')
        self.quality_score = QualityScore(**quality_kwargs)

    def add_skill(self, bot_name, **bot_kwargs):
        log.info(f'Adding bot named {bot_name}')
        self.bot_names.append(bot_name)
        bot_module = importlib.import_module(f'qary.skills.{bot_name}')
        new_modules, new_skills = [], []
        if bot_module.__class__.__name__ == 'module':
            module_vars = tuple(vars(bot_module).items())
            for bot_class in (c for n, c in module_vars if n.endswith('Skill') and callable(getattr(c, 'reply', None))):
                log.info(f'Adding a Skill class {bot_class} from module {bot_module}...')
                new_skills.append(bot_class(**bot_kwargs))
                new_modules.append(bot_module)
        else:
            log.warning(f'FIXME: add feature to allow import of specific bot classes like "qary.skills.{bot_name}"')
        self.bots.extend(new_skills)
        self.bot_modules.extend(new_modules)
        return new_skills

    def log_reply(self, statement, reply):
        history_path = os.path.join(constants.DATA_DIR, 'history.json')
        try:
            history = list()
            with open(history_path, 'r') as f:
                history = json.load(f)
        except IOError as e:
            log.error(str(e))
            with open(history_path, 'w') as f:
                f.write('[]')
        except json.JSONDecodeError as e:
            log.error(str(e))
            log.info('Saving history.json contents to history.json.swp before overwriting')
            with open(history_path, 'r') as f:
                data = f.read()
            with open(history_path + '.swp', 'w') as f:
                f.write(data)
        history.append(['user', statement])
        history.append(['bot', reply])
        with open(history_path, 'w') as f:
            json.dump(history, f)

    def reply(self, statement='', context=None):
        ''' Collect replies from from loaded bots and return best reply (str). '''
        log.info(f'statement={statement}')
        replies = []
        # Collect replies from each bot.
        for bot in self.bots:
            bot_replies = []
            log.info(f'Running bot {bot}')
            # FIXME: create set_context() method on those bots that need it and do away with context try/except
            try:
                bot_replies = bot.reply(statement, context=context)
                log.info("{bot.__name__} replies: {bot_replies}")
            except TypeError as e:
                log.debug(f"TypeError: bot.reply probably got an unexpected keyword argument 'context': {e}")
                bot_replies = bot.reply(statement)
            except Exception as e:
                log.error(f'Error trying to run {bot.__self__.__class__}.reply("{statement}", context={context})')
                log.error(str(e))
                if constants.args.debug:
                    raise e
            log.debug(repr(bot))
            bot_replies = normalize_replies(bot_replies)
            replies.extend(bot_replies)

        # Weighted random selection of reply from those with top n confidence scores
        log.info(f"{len(replies)} replies from {len(self.bots)} bots:")
        log.info(repr(replies))
        if len(replies):
            log.info(f'Found {len(replies)} suitable replies, limiting to {self.num_top_replies}...')
            replies = self.quality_score.update_replies(replies, statement)
            replies = sorted(replies, reverse=True)[:self.num_top_replies]

            conf_sums = np.cumsum(list(r[0] for r in replies))
            roll = np.random.rand() * conf_sums[-1]

            for i, threshold in enumerate(conf_sums):
                if roll < threshold:
                    reply = replies[i][1]
                    self.log_reply(statement, replies[i][0])
                    return reply
            log.error(f"Error rolling dice to select reply."
                      f"\n    roll:{roll}"
                      f"\n    threshold: {threshold}"
                      f"\n    conf_sums: {conf_sums}\n"
                      f"\n    replies: {pd.DataFrame(replies)}")
            return replies[0][1]
        else:
            log.error(f"No replies ({replies}) were returned by {self.bots}!!")

        reply = "Sorry, something went wrong. Not sure what to say..."
        self.log_reply(statement, reply)
        return reply


def run_skill():
    global BOT
    if BOT is None:
        BOT = CLIBot(
            bots=constants.args.bots,
            num_top_replies=constants.args.num_top_replies,
            semantic=constants.args.semantic,
            sentiment=constants.args.sentiment,
            spell=constants.args.spell)
    if constants.args.persist:
        print('Type "quit" or "exit" to end the conversation...')

    log.debug(f'FINAL PROCESSED ARGS AFTER INSTANTIATING CLIBot:\n{vars(constants.args)}\n')
    return BOT


def cli(args,
        exit_commands='exit quit bye goodbye cya hasta seeya'.split(),
        max_turns=constants.MAX_TURNS):
    global BOT
    BOT = run_skill() if BOT is None else BOT
    state = {}
    user_statement = ' '.join(args.words).strip() or None
    if user_statement is not None:
        max_turns = 0
    history = [dict(user=user_statement, bot=None, **state)]
    log.warning(f'user_cli_statement: `{user_statement}`')
    while True:
        if user_statement and user_statement.lower().strip() in exit_commands:
            break
        log.info(f"Computing a reply to {user_statement}...")
        if user_statement is None:
            bot_statement = None
        else:
            bot_statement = BOT.reply(user_statement)
        history[-1]['bot'] = bot_statement
        if bot_statement is None:
            pass
            # print()
            # print(f"{args.nickname}: Hi! I'm **{args.nickname}**. Ask me anything!")
        else:
            print(f'{args.nickname}: ')
            print(bot_statement)
        if max_turns > 0 or not user_statement:
            user_statement = input("YOU: ")
            history.append(dict(user=user_statement, skill=None, **state))
    return pd.DataFrame(history)


def main():
    global BOT
    BOT = run_skill() if BOT is None else BOT
    # args = constants.parse_argv(argv=sys.argv)
    statements = cli(constants.args)
    if constants.args.loglevel >= 50:
        return
    return statements


if __name__ == "__main__":
    statements = main()
