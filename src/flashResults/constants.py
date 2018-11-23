#===============================================================================
# Races
#===============================================================================
sprints = ('55', '60', '100', '200', '300', '400')
distance = ('800', '1000', '1500', '1600', '1 Mile', '3000', '2 Mile', '5000', '10000')
special = ('55 M Hurdles', '60 M Hurdles', '100 M Hurdles', '110 M Hurdles', '2000 M Steeplechase',
           '3000 M Steeplechase')
relay = ('4x100', '4x200', '4x400', '4x400', '4x800', '4x1 Mile', 'Distance Medley', 
         '1600 Sprint Medley', 'Swedish Relay', '800 Sprint Medley')
crossCountry = ()

allRaces = sprints + distance + special + relay + crossCountry

#===============================================================================
# Keywords
#===============================================================================
genders = ('male', 'female', 'men', 'women', 'boys', 'girls')
units = ('meter', 'meters', 'mile', 'miles', 'feet', 'yard', 'yards', 'kilometer', 'kilometers')
specialRaces = ('hurdle', 'hurdles', 'steeplechase', 'relay')
roundType = ('finals', 'final', 'prelims', 'prelim', 'preliminary', 'preliminaries', 'semi', 'semis',
             'semifinals', 'semifinal')

columns = ('Place', 'Bib', 'Lane', 'Athlete', 'Affiliation', 'Time')
