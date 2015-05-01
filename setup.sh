#! /usr/bin/env sh
# -*- coding: utf-8 -*-
eval "$(rbenv init -)"
bundle install --path vendor/bundle
sh bin/copy_config_files.sh
bundle exec rake secret
bundle exec rake db:create
bundle exec rake db:migrate
bundle exec rake db:seed
bundle exec rake test_data:create
bundle exec rake test_article_data:create
brew install mongo
mongod -f /usr/local/etc/mongod.conf # confを指定しないと /data/db は存在しないっていうエラーになるかも
brew install redis
redis-server
bundle exec rake admin:assign
bundle exec rails s
bundle exec rails c
bundle exec rails r db/insert_hot_topics_to_redis.rb
