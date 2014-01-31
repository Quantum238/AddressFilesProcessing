import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
##tex_files_dir = os.path.join(data_dir,'raw_tex')
indicia_dir = os.path.join(data_dir,'indicias')
##pdf_dir = os.path.join(main_dir,'outputs')
##junk_dir = os.path.join(main_dir,'junk')


#later this will need another dic per country
#for non publications
#and some of the entries should be off standard weights
#and they should probably be integers and not strings
#and I guess capitalized?  Or some string processing in the find function
indicia_dic = {
    'Belgium':
    {'Flats < 5 0z': 'RMNetherlandsSticker.png',
     'Flats 5-17 Oz': 'RM Netherlands Sticker.png',
     'Packets 17-70 Oz': 'RM Netherlands Sticker.png'},
    'Greece':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': 'Swiss direct entry indicia.png', #Says Swiss OE?
     'Packets 17-70 Oz': 'Swiss direct entry indicia.png'}, #Says Swiss OE?
    'Ireland':
    {'Flats < 5 0z': 'Spring Economy Indicia.png', #Just says Spring.  Also, <3 oz
     'Flats 5-17 Oz': 'La Poste Sticker Economy.png',
     'Packets 17-70 Oz': 'La Poste Sticker Economy.png'},
    'Norway':
    {'Flats < 5 0z': 'La Poste Sticker Economy.png',
     'Flats 5-17 Oz': 'Spring Economy Indicia.png', #Just says Spring. Chose Eco
     'Packets 17-70 Oz': 'Spring Economy Indicia.png'}, #Just says Spring.  
    'Portugal':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #Interpost Pub Rates
     'Packets 17-70 Oz': None},
    'Israel':
    {'Flats < 5 0z': 'La Poste Sticker Economy.png',
     'Flats 5-17 Oz': 'Swiss direct entry indicia.png', #Says Swiss OE?
     'Packets 17-70 Oz': 'Swiss direct entry indicia.png'}, #Says Swiss OE?
    'Philippines':
    {'Flats < 5 0z': 'La Poste Sticker Economy.png',
     'Flats 5-17 Oz': 'La Poste Sticker Economy.png',
     'Packets 17-70 Oz': 'La Poste Sticker Economy.png'},
    'Denmark':
    {'Flats < 5 0z': 'Swiss direct entry indicia.png',
     'Flats 5-17 Oz': 'Swiss direct entry indicia.png', #Just says Swiss OE
     'Packets 17-70 Oz': 'Swiss direct entry indicia.png'},
    'Canada':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None, #CME/USPS
     'Packets 17-70 Oz': None},
    'Australia':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None, #AMS
     'Packets 17-70 Oz': None},
    'New Zealand':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #USPS
     'Packets 17-70 Oz': None},
    'Czech Republic':
    {'Flats < 5 0z': 'RM Netherlands Sticker.png',
     'Flats 5-17 Oz': 'RM Netherlands Sticker.png', 
     'Packets 17-70 Oz': 'RM Netherlands Sticker.png'}, #Some hand note here
    'Germany':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #Says IMN in handwriting
     'Packets 17-70 Oz': None},
    'Austria':
    {'Flats < 5 0z': 'Swiss direct entry indicia.png', #Says OE in pen
     'Flats 5-17 Oz': 'Swiss direct entry indicia.png',
     'Packets 17-70 Oz': 'Swiss direct entry indicia.png'}, #Says something
    'Italy':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #interpost Pub Rates
     'Packets 17-70 Oz': None},
    'Spain':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #Interpost
     'Packets 17-70 Oz': None},
    'Switzerland':
    {'Flats < 5 0z': 'Swiss direct entry indicia.png',
     'Flats 5-17 Oz': 'Swiss direct entry indicia.png',
     'Packets 17-70 Oz': 'Swiss direct entry indicia.png'},
    'Saudi Arabia':
    {'Flats < 5 0z': None,#AJWW
     'Flats 5-17 Oz': None,#AJWW
     'Packets 17-70 Oz': None},#ITS
    'South Africa':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None, #Mail Africa
     'Packets 17-70 Oz': None},
    'Brazil':
    {'Flats < 5 0z': 'Mail Americas Brazil Indicia.png',
     'Flats 5-17 Oz': 'Mail Americas Brazil Indicia.png',
     'Packets 17-70 Oz': 'Mail Americas Brazil Indicia.png'}, #Some note
    'Great Britain':
    {'Flats < 5 0z': 'Keymail Indicia.png',
     'Flats 5-17 Oz': None,  #inspire
     'Packets 17-70 Oz': None}, #inspire
    'Japan':
    {'Flats < 5 0z': 'La Poste Sticker Economy.png',
     'Flats 5-17 Oz': None, #OCS
     'Packets 17-70 Oz': None}, #OCS
    'Russia':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None,  #Russia
     'Packets 17-70 Oz': None},
    'Finland':
    {'Flats < 5 0z': 'RM Netherlands Sticker.png',
     'Flats 5-17 Oz': 'RM Netherlands Sticker.png',
     'Packets 17-70 Oz': 'RM Netherlands Sticker.png'},
    'France':
    {'Flats < 5 0z': 'RM Netherlands Sticker.png',
     'Flats 5-17 Oz': 'RM Netherlands Sticker.png',
     'Packets 17-70 Oz': 'RM Netherlands Sticker.png'},
    'Sweden':
    {'Flats < 5 0z': 'RM Netherlands Sticker.png',
     'Flats 5-17 Oz': 'RM Netherlands Sticker.png',
     'Packets 17-70 Oz': 'RM Netherlands Sticker.png'},
    'Netherlands':
    {'Flats < 5 0z': None,
     'Flats 5-17 Oz': None, #spring Alternative
     'Packets 17-70 Oz': None}
    }
    

def find_indicia_file(country,weight='Flats < 5 0z'):
    try:
        file = indicia_dic[country][weight]
    except KeyError:
        file = None
    
    return file
    
