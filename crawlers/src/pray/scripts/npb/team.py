#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import sys
import argparse


import lxml.etree
from pymongo import MongoClient
from pray import crequests as requests
from pray.contexts import XPathContext


class NPBTeamCollectionContext(XPathContext):
    @property
    def _teams_elm(self):
        return self.xpath('//td[@class="categoryColor"]')[0]

    def get_teams(self):
        for elm in self._teams_elm.xpath('table/tr/td[@class="smenuMenu"]/a'):
            yield elm


class NPBTeamContext(XPathContext):
    @property
    def name(self):
        return self.xpath('text()')[0].strip(u'・')


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)
    res = requests.get('http://www.npb.or.jp/teams/')

    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client.npb
    team = db.team
    element = lxml.etree.HTML(res.content)
    team_team_collection = NPBTeamCollectionContext(element)
    for elm in team_team_collection.get_teams():
        context = NPBTeamContext(elm)
        obj = team.find({'name': context.name})
        if obj.count() == 0:
            team.insert({
                'name': context.name,
                })


if __name__ == '__main__':
    main()
