import urllib
import urllib2
from lxml import etree
import StringIO
import re


class ScrapesBurgh():

    # checks the url to make sure it's valid
    # and, if so, reads in the html
    @staticmethod
    def open_url(url):
        click = urllib.urlopen(url)
        if click.getcode() == 200:
            html = click.read()
            return html
        else:
            raise Exception("Nice try. Bad link.")
            # pass

    # initial parse of the html
    @staticmethod
    def parse_html(html):
        parser = etree.HTMLParser()
        master_tree = etree.parse(StringIO.StringIO(html), parser)

        return master_tree

    # gets the parsed tree to begin the scrape
    @staticmethod
    def treeify(url):
        html = ScrapesBurgh.open_url(url)
        tree = ScrapesBurgh.parse_html(html)

        return tree

    # gets all the ids we'll need to create the scraping urls dynamically
    @staticmethod
    def all_urls(url):
        tree = ScrapesBurgh.treeify(url)

        board_ids = []

        for option in tree.xpath('//*[@id="form1"]/blockquote/select/option'):
            try:
                board_id = int(option.values()[0])
                board_ids.append(board_id)
            except:
                pass

        board_ids = sorted(board_ids)

        return tree, board_ids

    # creates the urls to scrape and opens each, beginning the scrape
    @staticmethod
    def scrape_data(board_ids):
        # print board_ids
        for board_id in board_ids:
            url = "http://www.alleghenycounty.us/boards/index.asp?Board=%d&button1=View" % board_id
            tree = ScrapesBurgh.treeify(url)
            print url
            board_name, history, creation, contact, address, meeting_place, meeting_time, phone, email, link, members = ScrapesBurgh.get_board_info(url, tree)
            ScrapesBurgh.clean_board_info(url, board_name, history, creation, contact, address, meeting_place, meeting_time, phone, email, link, members)

    # points the scraper in the direction of the data it needs
    @staticmethod
    def get_board_info(url, tree):

        # print html
        board_name_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[1]/td/font/b/text()'
        history_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[7]/td/font/p/text()'
        contact_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[2]/td[2]/font/text()'
        address_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[4]/td[2]/font/text()'
        creation_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[2]/td[4]/font/text()'
        meeting_place_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[4]/td[4]/font/text()'
        meeting_time_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[5]/td[3]/font/text()'
        phone_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[3]/td[4]/font/text()'
        email_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[3]/td[2]/font/a/@href'
        link_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[1]/td/font/b/a/@href'
        members_xpath = '//*[@id="form1"]/blockquote/table[2]/tr/td/font/text()'

        if len(tree.xpath(board_name_xpath)) != 1:
            board_name_xpath = '//*[@id="form1"]/blockquote/table[1]/tr[1]/td/font/b/a/text()'

        board_name = tree.xpath(board_name_xpath)
        history = tree.xpath(history_xpath)
        creation = tree.xpath(creation_xpath)
        contact = tree.xpath(contact_xpath)
        address = tree.xpath(address_xpath)
        meeting_place = tree.xpath(meeting_place_xpath)
        meeting_time = tree.xpath(meeting_time_xpath)
        phone = tree.xpath(phone_xpath)
        email = tree.xpath(email_xpath)
        link = tree.xpath(link_xpath)
        members = tree.xpath(members_xpath)

        return board_name, history, creation, contact, address, meeting_place, meeting_time, phone, email, link, members

    # cleans up the filthy, filthy data to prepare for storage
    # PTOOEY. so dirty. your mother would be ashamed.
    @staticmethod
    def clean_board_info(url, board_name, history, creation, contact, address, meeting_place, meeting_time, phone, email, link, members):

        board_name = board_name[0].strip()

        try:
            creation = creation[0].strip()
        except:
            pass

        contact = contact[0].replace(u'\xa0', u'')
        meeting_place = meeting_place[0].replace(u'\xa0', u'')
        meeting_time = meeting_time[0].replace(u'\xa0', u'')
        phone = phone[0].replace(u'\xa0', u'')

        address_list = []
        for addr in address:
            addr = addr.strip()
            address_list.append(addr)

        members_dict = {}
        no_members_dict = {}

        for member in members:
            member = member.strip()

            name_pattern = '([A-Z][^\s,]+)'
            name_match = re.findall(name_pattern, '%s' % member)

            if "Members" not in name_match:
                name = name_match[1].replace(u'\xa0', u'') + ' ' + name_match[0]
                date_pattern = '(\d+/\d+/\d+)'
                date_match = re.search(date_pattern, '%s' % member)
                if date_match:
                    date_final = date_match.group()
                    members_dict[name] = (board_name, date_final)
                else:
                    members_dict[name] = (board_name, "No end of term given")

            # elif len(name_match) == 1 and "Members" not in name_match:
            #     first_initial_pattern = '([A-Z]\.)'
            #     first_initial_match = re.findall(first_initial_pattern, '%s' % member)
            #     name = first_initial_match[0] + ' ' + name_match[0]
            else:
                no_members_dict[board_name] = ("%s has no members" % board_name, url)

        print board_name, '\n', history, '\n', creation, '\n', members_dict, '\n', contact, '\n', link, '\n', address_list, '\n', meeting_place, '\n', meeting_time, '\n', phone, '\n', email, '\n', no_members_dict

    # starts the whole ball o' wax
    @staticmethod
    def start_scrape():
        tree, board_ids = ScrapesBurgh.all_urls('http://www.alleghenycounty.us/boards/index.asp')

        ScrapesBurgh.scrape_data(board_ids)
