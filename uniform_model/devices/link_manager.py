class LinkManager:
    _registed_links = []

    @classmethod
    def regist_link(cls, link):
        cls._registed_links.append(link)

    @classmethod
    def get_registed_links(cls):
        return cls._registed_links
