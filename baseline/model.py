'''
Modeling users, interactions and items from
the recsys challenge 2017.

by Daniel Kohlsdorf
'''

class User:

    def __init__(self, title, clevel, indus, disc, country, region, avgemployment, expyears):
        self.title   = title
        self.clevel  = clevel
        self.indus   = indus
        self.disc    = disc
        self.country = country
        self.region  = region
        self.avgemployment = avgemployment
        self.expyears = expyears

class Item:

    def __init__(self, title, clevel, indus, disc, country, region, avgexpyears, employment):
        self.title   = title
        self.clevel  = clevel
        self.indus   = indus
        self.disc    = disc
        self.country = country
        self.region  = region
        self.avgexpyears = avgexpyears
        self.employment = employment

    def title_match(self, item):
        return float(len(set(self.title).intersection(set(item.title))))

    def clevel_match(self, item):
        if self.clevel == item.clevel:
            return 1.0
        else:
            return 0.0

    def indus_match(self, item):
        if self.indus == item.indus:
            return 1.0
        else:
            return 0.0

    def discipline_match(self, item):
        if self.disc == item.disc:
            return 1.0
        else:
            return 0.0

    def country_match(self, item):
        if self.country == item.country:
            return 1.0
        else:
            return 0.0

    def region_match(self, item):
        if self.region == item.region:
            return 1.0
        else:
            return 0.0

    def expyears_match(self, item):
        if abs(self.avgexpyears - item.avgexpyears) < 2:
            return 1.0
        else:
            return 0.0

    def employment_match(self, item):
        if abs(self.employment == item.employment) < 2:
            return 1.0
        else:
            return 0.0

    def compare(self, item):
        return(sum([self.title_match(item), self.clevel_match(item), self.indus_match(item),
                    self.country_match(item), self.region_match(item)]))


class Interaction:
    
    def __init__(self, user, item, interaction_type):
        self.user = user
        self.item = item
        self.interaction_type = interaction_type

    def title_match(self):
        return float(len(set(self.user.title).intersection(set(self.item.title))))

    def clevel_match(self):
        if self.user.clevel == self.item.clevel:
            return 1.0
        else:
            return 0.0

    def indus_match(self):
        if self.user.indus == self.item.indus:
            return 1.0
        else:
            return 0.0

    def discipline_match(self):
        if self.user.disc == self.item.disc:
            return 2.0
        else:
            return 0.0

    def country_match(self):
        if self.user.country == self.item.country:
            return 1.0
        else:
            return 0.0

    def region_match(self):
        if self.user.region == self.item.region:
            return 1.0
        else:
            return 0.0
    
    def expyears_match(self):
        if abs(self.user.expyears - self.item.avgexpyears) < 2:
            return 1.0
        else:
            return 0.0

    def employment_match(self):
        if abs(self.user.avgemployment == self.item.employment) < 2:
            return 1.0
        else:
            return 0.0

    def features(self):
        return [
            self.title_match(), self.clevel_match(), self.indus_match(),
            self.discipline_match(), self.country_match(), self.region_match(), 
	    self.expyears_match(), self.employment_match()
        ]

    def label(self): 
        if self.interaction_type == 4: 
            return 0.0
        else:
            return 1.0


