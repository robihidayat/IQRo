#!/usr/bin/env python

from lxml.html import parse
import argparse
import signal
import sys


# TODO : change to http://docs.python-guide.org/en/latest/scenarios/scrape/
# don't use selenium (to slow for static page)
class ParseTable:
    """Class for parsing html table"""
    def __init__(self, file_path):
        self.doc = parse(file_path).getroot()

    def parsercolumn(self, tab, col, top_offset=0, bottom_offset=0, debug=False):
        '''
        For parsing table column
        '''
        # table
        doc = self.doc
        xpath = ''
        contents = []
        count_div = doc.xpath("count(//div/table)")
        count_table = doc.xpath("count(//table)")

        if count_div < count_table:
            xpath += '//table['+str(tab)+']'
        else:
            xpath += '//div['+str(tab)+']/table'
        table = doc.xpath(xpath)

        # row APL - 0002.htm /x:div[4]/x:table/x:tbody/x:tr[1]/x:td[1]
        xpath += "//tr/td["+str(col)+"]/p"
        rows = table[0].xpath(xpath)
        for row in rows:
            count_br = row.xpath("count(./br)")
            if count_br > 0:
                contents += row.xpath("./br/preceding::text()[1]")[:1] # 1 data sebelum <br>
                contents += row.xpath("./br/following::text()[1]") # setelah <br>

            else:
                contents += row.xpath("text()")

        if debug: print xpath

        bottom_offset = len(contents)-bottom_offset
        return contents[top_offset:bottom_offset]

    def parsecell(self, tab_id, col_id, row_id, top_offset=0, bottom_offset=0, debug=False):
        '''
        For parsing table cell
        '''
        # table
        doc = self.doc
        xpath = ''
        contents = []
        count_div = doc.xpath("count(//div/table)")
        count_table = doc.xpath("count(//table)")

        if count_div < count_table:
            xpath += '//table['+str(tab_id)+']'
        else:
            xpath += '//div['+str(tab_id)+']/table'
        table = doc.xpath(xpath)

        # row APL - 0002.htm /x:div[4]/x:table/x:tbody/x:tr[1]/x:td[1]
        xpath += "//tr["+str(row_id)+"]/td["+str(col_id)+"]/p"
        rows = table[0].xpath(xpath)
        for row in rows:
            count_br = row.xpath("count(./br)")
            if count_br > 0:
                contents += row.xpath("./br/preceding::text()[1]")[:1] # 1 data sebelum <br>
                contents += row.xpath("./br/following::text()[1]") # setelah <br>
            else:
                contents += row.xpath("text()")

        if debug: print xpath

        bottom_offset = len(contents)-bottom_offset
        return ''.join(contents[top_offset:bottom_offset])


if __name__ == '__main__':
    def exit_gracefully(signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, original_sigint)

        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)

        except KeyboardInterrupt:
            print("Ok ok, quitting")
            # browser.quit()
            sys.exit(1)

            # restore the exit gracefully handler here
            signal.signal(signal.SIGINT, exit_gracefully)

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    # Parse Argument
    parser = argparse.ArgumentParser(description='Parse html table from abyy finereader result')
    parser.add_argument('url', type=str,
                            help='url of the file (.html)')
    parser.add_argument('table', metavar='i', type=int,
                        help='table i that wanted to get')
    parser.add_argument('column', metavar='c', type=int,
                        help='column c of the table i that wanted to get')
    parser.add_argument('-t', '--top_offset', type=int, default=0,
                            help='top offset')
    parser.add_argument('-b', '--bottom_offset', type=int, default=0,
                            help='bottom offset')
    parser.add_argument('-r', '--row', type=int, default=0,
                            help='specify row')
    args = parser.parse_args()

    pt = ParseTable(args.url)
    if args.row == 0:
        data = pt.parsercolumn(args.table, args.column, args.top_offset, args.bottom_offset)
        for d in data:
            print d
    else:
        print pt.parsecell(args.table, args.column, args.row)
