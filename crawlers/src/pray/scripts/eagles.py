#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import six
import os
import sys
import datetime
import argparse
import lxml.etree

if six.PY3:
    import enum
    import unittest.mock as mock
else:
    import enum34 as enum
    import mock  # noqa

import pray.crequests as requests


class UserAgent(enum.Enum):
    FIREFOX = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1)'  # 9.0


icon_team = {
    'pl_2012.png': 'LIONS',
    'pf_2012.png': 'FIGHTERS',
    'ph_2012.png': 'HAWKS',
    'pb_2012.png': 'BUFFRLOWS',
    'pm_2012.png': 'MARINES',
    'ct_2012.png': 'TIGERS',
    'cg_2012.png': 'GIANTS',
    }


class TeamIcon(enum.Enum):
    LIONS = 'pl_2012.png'
    FIGHTERS = 'pf_2012.png'
    HAWKS = 'ph_2012.png'
    BUFFRLOWS = 'pb_2012.png'
    MARINES = 'pm_2012.png'
    TIGERS = 'ct_2012.png'
    GIANTS = 'cg_2012.png'


class HomeRunData(object):
    def __init__(self):
        self.player = None
        self.num = None


class XpathContext(object):
    def __init__(self, core):
        self._core = core

    def xpath(self, *args, **kwds):
        return self._core.xpath(*args, **kwds)


class GameSheduleContext(XpathContext):
    @property
    def table(self):
        return self.xpath('//div[id("mainMap")]/div[id("calendar")][@class="contentsArea01"]/table[@class="typeA01"][1]')[0]

    @property
    def rows(self):
        return self.table.xpath('tr')[1:]

    def __iter__(self):
        for row in self.rows:
            yield GameDetailContext(row)

    def next(self):
        return self.__iter__


class GameDetailContext(XpathContext):
    def __init__(self, core):
        super().__init__(core)
        self.target = None
        self.score = None
        self.studium = None
        self.winlose = None
        self.start_picker = None
        self.win_picker = None
        self.s_picker = None
        self.lose_picker = None
        self.home_runs = None
        self.links = None

    @property
    def date(self):
        day = int(self.xpath('td[1]/span/text()')[0])
        now = datetime.date.today()
        return datetime.date(year=now.year, month=now.month, day=day)

    @property
    def target_image(self):
        return self.xpath('td[2]/table/tr[1]/td[1]/img/@src')[0]

    @property
    def opponent(self):
        """対戦相手"""
        image_filename = os.path.basename(self.target_image)
        return icon_team.get(image_filename, 'UNKNOWN')


class RakutenEaglesCrawler(object):
    URL = 'http://www.rakuteneagles.jp/game/schedule/'

    def start(self):
        res = requests.get(self.URL)
        element = lxml.etree.HTML(res.content)
        game_schedule = GameSheduleContext(element)
        for game_detail in game_schedule:
            print('{} - {}'.format(game_detail.date, os.path.basename(game_detail.opponent)))


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)

    crawler = RakutenEaglesCrawler()
    crawler.start()


if __name__ == '__main__':
    main()
