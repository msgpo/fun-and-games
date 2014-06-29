#!/usr/bin/env python

# ============================================================================
# The MIT License (MIT)
# 
# Copyright (c) 2014 Michael Hansen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ============================================================================

import argparse, re, os
from collections import defaultdict
import xml.etree.ElementTree as etree
import xml.dom.minidom

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Converts a MageArena deck to the Cockatrice format")
    parser.add_argument("mage_deck", type=str, help="Path to MageArena deck (.dec)")
    parser.add_argument("cockatrice_deck", type=str, help="Path to Cockatrice deck (.cod)")
    args = parser.parse_args()


    # Use file name for deck name
    dir_name, file_name = os.path.split(args.mage_deck)
    deck_name = os.path.splitext(file_name)[0]
    deck_name = deck_name.replace("_", " ")

    deck_comments = ""

    # Read in deck
    card_str_regex = re.compile(r"^(\d+) (.+)$")
    comment_regex = re.compile(r"^>(.+)$")
    cards = defaultdict(int)

    print "Reading", args.mage_deck
    with open(args.mage_deck, "r") as in_file:
        for line in in_file:
            # Skip blank lines and comments
            if len(line.strip()) == 0 or line.strip().startswith("#"):
                continue

            # Match card
            match = card_str_regex.search(line)
            if match:
                card_count = int(match.group(1))
                card_name = match.group(2)
                cards[card_name] += card_count
            else:
                # Match comment
                match = comment_regex.search(line)
                if match:
                    deck_comments = match.groups(1)[0]

    num_cards = sum(cards.values())
    print "Converting {0} ({1} cards)".format(deck_name, num_cards)

    # Convert to XML
    xml_deck = etree.Element("cockatrice_deck", version="1")

    xml_deck_name = etree.SubElement(xml_deck, "deckname")
    xml_deck_name.text = deck_name

    xml_deck_comments = etree.SubElement(xml_deck, "comments")
    try:
        xml_deck_comments.text = deck_comments.encode("utf-8", "ignore")
    except UnicodeDecodeError:
        pass

    xml_zone = etree.SubElement(xml_deck, "zone", name="main")
    for card_name, card_count in cards.iteritems():
        etree.SubElement(xml_zone, "card",
            name=card_name, number=str(card_count), price="0")

    # Write XML file
    with open(args.cockatrice_deck, "w") as out_file:
        xml_str = etree.tostring(xml_deck, encoding="utf-8")
        xml = xml.dom.minidom.parseString(xml_str)
        out_file.write(xml.toprettyxml(encoding="utf-8"))

    print "Wrote to", args.cockatrice_deck
