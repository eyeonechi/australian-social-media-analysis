#!/usr/bin/env python

import loggin
import re

from __future__ import absolute_import
from twac import Twarc
from twitter_stream_warc_iter import TwitterStreamWarcIter
from twitter_rest_warc_iter import TwitterRestWarcIter
from requests.exceptions import HTTPError

log = loggin.getLogger(__name__)

class TwitterHarvester(BaseHarvester):
    def __init__(
        self,
        working_path,
        strem_restart_interval_secs=30 * 60,
        mq_config=None,
        debug=False,
        connection_errors=5,
        http_errors=5,
        debug_warcprox=False,
        tries=3
    ):
        self.twarc = None
        self.connection_errors = connection_errors
        self.http_errors = http_errors
        self.extract_media = False
        self.extract_web_resources = False
        self.extract_user_profile_images = False

    def harvest_seeds(self):
        self._create_twarc()
        self.extract_media = self.message.get("options", {}).get("media", False)
        self.extract_web_resources = self.message.get("options", {}).get("resources", False)
        self.extract_user_profile_images = self.message.get("options", {}).get("user_images", False)

        harvest_type = self.message.get("type")
        log.debug("Harvest type is %s", harvest_type)
        if harvest_type == "search":
            self.search()
        elif harvest_type == "filter":
            self.filter()
        elif harvest_type == "sample":
            self.sample()
        elif harvest_type == "user_timeline":
            self.user_timeline()
        else:
            raise KeyError

    def filter(self):
        assert len(self.message.get("seeds", [])) == 1
        track = self.message["seeds"][0]["token"].get("track")
        follow = self.message["seeds"][0]["token"].get("follow")
        locations = self.message["seeds"][0]["token"].get("locations")
        self._harvest_tweets(
            self.twarc.filter(
                track=track,
                follow=follow,
                locations=locations,
                event=self.stop_harvest_seeds_event
            )
        )

    def sample(self):
        self._harvest_tweets(self.twarc.sample(self.stop_harvest_seeds_event))

    def search(self):
        assert len(self.message.get("seeds", [])) == 1
        incremental = self.message.get("options", {}).get("incremental", False)
        since_id = self.state_store.get_state(
            __name__,
            u"{}.since_id".format(self._search_id())
        ) if incremental else None
        query, geocode = self._search_parameters()
        self._harvest_tweets(self.twarc.search(query, geocode=geocode, since_id=since_id))

    def user_timeline(self):
        incremental = self.message.get("options", {}).get("incremental", False)
        for seed in self.message.get("seeds", []):
            seed_id = seed["id"]
            user_id = seed.get("uid")
            log.debug(
                "Processing seed (%s) with screen name %s and user id %s",
                seed_id,
                screen_name,
                user_id
            )
            assert screen_name or user_id

            if screen_name and not user_id:
                user_id = self._lookup_user_id(screen_name)
                if user_id:
                    self.result.uids[seed_id] = user_id
                else:
                    msg = u"User id not found for user {} because account is not found or suspended".format(screen_name)
                    log.exception(msg)
                    self.result.warnings.append(Msg(CODE_TOKEN_NOT_FOUND, msg, seed_id=seed_id))
            else:
                new_screen_name = self._lookup_screen_name(user_id)
                if not new_screen_name:
                    msg = "Screen name not found for user id {} because account is not found or suspended".format(user_id)
                    log.exception(msg)
                    self.result.warnings.append(Msg(CODE_TOKEN_NOT_FOUND, msg, seed_id=seed_id))
                    user_id = None
                if new_screen_name and new_screen_name != screen_name:
                    self.result.token_updates[seed_id] = new_screen_name
                    screen_name = new_screen_name

            if user_id:
                try:
                    since_id = self.state_store.get_state(
                        __name__,
                        "timeline.{}.since_id".format(user_id)
                    ) if incremental else None
                    self._harvest_tweets(self.twarc.timeline(user_id=user_id, since_id=since_id))
                except HTTPError as e:
                    if e.response.status_code == 401:
                        account = u"user {} (User ID: {})".format(
                            screen_name,
                            user_id
                        ) if screen_name else "user ID: {}".format(user_id)
                        msg = "Unauthorized for {} because account is suspended or protected".format(account)
                        log.exception(msg)
                        self.result.warnings.append(Msg(CODE_TOKEN_UNAUTHROIZED, msg, seed_id=seed_id))
                    else:
                        raise e

    def _create_twarc(self):
        self.twarc = Twarc(
            self.message["credentials"]["consumer_key"],
            self.message["credentials"]["consumer_secret"],
            self.message["credentials"]["access_token"],
            self.message["credentials"]["access_token_secret"],
            http_errors=self.http_errors,
            connection_errors=self.connection_errors,
            tweet_mode="extended"
        )

    def _search_id(self):
        query, geocode = self._search_parameters()
        if query and not geocode:
            return query
        if geocode and not query:
            return geocode
        return ":".join([query, geocode])

    def _search_parameters(self):
        if type(self.message["seeds"][0]["token"]) is dict:
            query = self.message["seeds"][0]["token"].get("query")
            geocode = self.message["seeds"][0]["token"].get("geocode")
        else:
            query = self.message["seeds"][0]["token"]
            geocode = None
        return query, geocode

    def _lookup_screen_name(self, user_id):
        try:
            users = list(self.)
