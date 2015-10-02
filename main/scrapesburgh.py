import urllib
import urllib2
from lxml import etree
import StringIO
import re


class ScrapesBurgh():

    @staticmethod
    def open_url(url):
        click = urllib.urlopen(url)
        if click.getcode() == 200:
            html = click.read()
            return html
        else:
            raise Exception("Nice try. Bad link.")

    @staticmethod
    def parse_html(html):
        parser = etree.HTMLParser()
        master_tree = etree.parse(StringIO.StringIO(html), parser)

        return master_tree

    @staticmethod
    def treeify(url):
        html = ScrapesBurgh.open_url(url)
        tree = ScrapesBurgh.parse_html(html)

        return tree

    @staticmethod
    def next_url(tree):
        board_ids = []

        for option in tree.xpath('//*[@id="form1"]/blockquote/select/option'):
            try:
                board_id = int(option.values()[0])
                board_ids.append(board_id)
            except:
                pass

        board_ids = sorted(board_ids)
        print board_ids

        for board_id in board_ids:
            url = "http://www.alleghenycounty.us/boards/index.asp?Board='%d'&button1=View" % board_id
            ScrapesBurgh.get_board_info(url)


    @staticmethod
    def get_board_info(url):

        tree = ScrapesBurgh.treeify(url)

        # print html
        board_name_xpath ='//*[@id="form1"]/blockquote/table[1]/tr[1]/td/font/b/text()'
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

        board_name = board_name[0].strip()
        creation = creation[0].strip()

        contact = contact[0].replace(u'\xa0', u' ')
        meeting_place = meeting_place[0].replace(u'\xa0', u' ')
        meeting_time = meeting_time[0].replace(u'\xa0', u' ')
        phone = phone[0].replace(u'\xa0', u' ')

        address_list = []
        for addr in address:
            addr = addr.strip()
            address_list.append(addr)

        members_dict = {}

        for member in members:
            member = member.strip()
            name_pattern = '([A-Z]\w+)'
            name_match = re.findall(name_pattern, '%s' % member)
            name = name_match[1] + ' ' + name_match[0]
            # print name

            date_pattern = '(\d+/\d+/\d+)'
            date_match = re.search(date_pattern, '%s' % member)
            date_final = date_match.group()

            members_dict[name] = (board_name, date_final)

        # print board_name, '\n', history, '\n', creation, '\n', members_dict, '\n', contact, '\n', link, '\n', address_list, '\n', meeting_place, '\n', meeting_time, '\n', phone, '\n', email
