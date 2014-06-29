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

import argparse, re, codecs
from collections import defaultdict
from ConfigParser import ConfigParser
import xml.etree.ElementTree as etree
import xml.dom.minidom

def get_section_name(config, name):
    """Finds a config section in a case-insensitive manner"""
    for section in config.sections():
        if section.lower() == name.lower():
            return section
    return name

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Converts a Forge deck to the Cockatrice format")
    parser.add_argument("forge_deck", type=str, help="Path to Forge deck (.dck)")
    parser.add_argument("cockatrice_deck", type=str, help="Path to Cockatrice deck (.cod)")
    args = parser.parse_args()

    print "Reading", args.forge_deck
    config = ConfigParser(allow_no_value=True)
    config.optionxform = str  # Don't lowercase key names
    with open(args.forge_deck, "r") as in_file:
        config.readfp(in_file)

    metadata_section = get_section_name(config, "metadata")
    main_section = get_section_name(config, "main")

    deck_name = config.get(metadata_section, "Name")
    deck_comments = config.get(metadata_section, "Description")
    card_list = config.items(main_section)

    # Read in deck
    card_str_regex = re.compile(r"^(\d+) ([^|]+)")
    cards = defaultdict(int)
    for card_str, _ in card_list:
        match = card_str_regex.search(card_str)
        card_count = int(match.group(1))
        card_name = match.group(2)
        cards[card_name] += card_count

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
