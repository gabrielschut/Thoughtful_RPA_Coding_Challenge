from datetime import date

class Article:
    title : str
    publich_date : date
    description : str
    picture_file_name : str
    times_search_term_appears : int
    money_on_text : bool

    def __init__(self, title, publich_date, description, picture_file_name, money_on_text, times_search_term_appears):
        self.title = title
        self.publich_date = publich_date
        self.description = description
        self.picture_file_name = picture_file_name
        self.times_search_term_appears = times_search_term_appears
        self.money_on_text = money_on_text


    def to_dict(self):
        return {
            'title': self.title,
            'date': self.publich_date.strftime(),
            'description': self.description,
            'picture file name': self.picture_file_name,
            'times_search_term_appears': self.times_search_term_appears,
            'Money on text': 'TRUE' if self.money_on_text else 'False'
            }