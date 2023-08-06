#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import bz2
import sys
import json
import os.path
import argparse
from collections import namedtuple

import retrying
import timeout_wrapper
from tqdm import tqdm
from sqlitedict import SqliteDict
from marcxml_parser import MARCXMLRecord
from edeposit.amqp.aleph import aleph
from edeposit.amqp.aleph.aleph import DocumentNotFoundException
from edeposit.amqp.aleph.aleph import InvalidAlephBaseException


# Functions & classes =========================================================
class KeywordInfo(namedtuple("KeywordInfo", ["uid",
                                             "sysno",
                                             "zahlavi",
                                             "odkazovana_forma",
                                             "angl_ekvivalent",
                                             "mdt",
                                             "mrf",
                                             "zdroj_angl_ekvivalentu",
                                             "poznamka"])):
    @classmethod
    def from_marc(cls, sysno, marc):
        def first_or_none(item):
            if not item:
                return None

            if type(item) in [tuple, list]:
                return item[0]

            return item

        def parse_mrf(mrf):
            if not mrf:
                return mrf

            return mrf.split("_")[0]

        def de_entity(s):
            if not s:
                return s

            if isinstance(s, list) or isinstance(s, tuple):
                return [de_entity(x) for x in s]

            if isinstance(s, dict):
                return {key: de_entity(val) for key, val in s.iteritems()}

            return s.replace("&nbsp;", " ") \
                    .replace("&quot;", '"') \
                    .replace("&apos;", "'") \
                    .replace("&amp;", "&")

        return cls(
            uid=first_or_none(marc["001"]),
            sysno=sysno,
            zahlavi=de_entity(first_or_none(marc["150a"])),
            odkazovana_forma=marc.get("450a", []),
            mdt=de_entity(first_or_none(marc["080a"])),
            mrf=de_entity(parse_mrf(first_or_none(marc["0802"]))),
            angl_ekvivalent=de_entity(first_or_none(marc["750a07"])),
            zdroj_angl_ekvivalentu=de_entity(first_or_none(marc["750a02"])),
            poznamka=de_entity(first_or_none(marc["680i"])),
        )


@retrying.retry(stop_max_attempt_number=3)
@timeout_wrapper.timeout(5)
def _download(doc_id):
    """
    Function used to download data authority data from aleph. Function retries
    failed attempts to download data and also has timeout.

    Args:
        doc_id (int): Sysno of the document you wish to receive.

    Returns:
        str: MARC for given record.

    Raises:
        DocumentNotFoundException: In case that document was not found.
        InvalidAlephBaseException: In case that document was not found.
    """
    return aleph.downloadMARCOAI(str(doc_id), "aut10")


def _download_items(db, last_id):
    """
    Download items from the aleph and store them in `db`. Start from `last_id`
    if specified.

    Args:
        db (obj): Dictionary-like object used as DB.
        last_id (int): Start from this id.
    """
    MAX_RETRY = 20  # how many times to try till decision that this is an end
    MAX_DOC_ID = 10000000  # this is used for download iterator

    not_found_cnt = 0  # circuit breaker
    for doc_id in xrange(last_id, MAX_DOC_ID):
        doc_id += 1
        print "Downloading %d.." % (doc_id)

        if not_found_cnt >= MAX_RETRY:
            print "It looks like this is an end:", doc_id - MAX_RETRY
            break

        try:
            record = _download(doc_id)
        except (DocumentNotFoundException, InvalidAlephBaseException):
            print "\tnot found, skipping"
            not_found_cnt += 1
            continue

        not_found_cnt = 0
        db["item_%d" % doc_id] = record
        db["last_id"] = doc_id - MAX_RETRY if doc_id > MAX_RETRY else 1

        if doc_id % 100 == 0:
            db.commit()


def download_items(cache_fn, start=None):
    """
    Open the `cache_fn` as database and download all not-yet downloaded items.

    Args:
        cache_fn (str): Path to the sqlite database. If not exists, it will be
            created.
        start (int, default None): If set, start from this sysno.
    """
    with SqliteDict(cache_fn) as db:
        last_id = db.get("last_id", 0) if not start else start
        _download_items(db, last_id)
        db.commit()


def _pick_keywords(db):
    """
    Go thru downloaded data stored in `db` and filter keywords, which are
    parsed and then yielded.

    Shows nice progress bar.

    Args:
        db (obj): Opened database connection.

    Yields:
        obj: :class:`KeywordInfo` instances for yeach keyword.
    """
    for key, val in tqdm(db.iteritems(), total=len(db)):
        # skip counter of the last downloaded document
        if key == "last_id":
            continue

        # this is optimization to speed up skipping of the unwanted elements
        # by the factor of ~20
        piece = val[:500] if len(val) > 500 else val
        if '<fixfield id="001">ph' not in piece.lower():
            continue

        parsed = MARCXMLRecord(val)

        code = parsed.get("001")
        if not code:
            continue

        # record was disabled
        if parsed["682i"]:
            continue

        if code.lower().startswith("ph"):
            yield KeywordInfo.from_marc(
                sysno=int(key.split("_")[-1]),  # item_xxx -> int(xxx)
                marc=parsed,
            )


def generate(cache_fn):
    """
    Go thru `cache_fn` and filter keywords. Store them in `keyword_list.json`.

    Args:
        cache_fn (str): Path to the file with cache.

    Returns:
        list: List of :class:`KeywordInfo` objects.
    """
    if not os.path.exists(cache_fn):
        print >> sys.stderr, "Can't access `%s`!" % cache_fn
        sys.exit(1)

    with SqliteDict(cache_fn) as db:
        for item in _pick_keywords(db):
            yield item


# Main program ================================================================
if __name__ == '__main__':
    default_cache_fn = "./aleph_kw_index.sqlite"
    default_output_fn = "./keyword_list.json"

    parser = argparse.ArgumentParser(
        description="""Aleph keyword index builder. This program may be used to
    build fast index for the keywords from AUT base."""
    )
    parser.add_argument(
        "-c",
        "--cache",
        default=default_cache_fn,
        help="Name of the cache file. Default `%s`." % default_cache_fn
    )
    parser.add_argument(
        "-o",
        "--output",
        default=default_output_fn,
        help="Name of the output file. Default `%s`." % default_output_fn
    )
    parser.add_argument(
        "-s",
        "--start-at",
        metavar="N",
        dest="start_at",
        type=int,
        help="Start from N instead of last used value."
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="Don't download, only generate data from dataset."
    )

    args = parser.parse_args()

    if not args.generate:
        download_items(args.cache, start=args.start_at)

    with bz2.BZ2File(args.output + ".bz2", "w") as f:
        f.write(
            json.dumps(
                [keyword._asdict() for keyword in generate(args.cache)],
                indent=4
            )
        )
