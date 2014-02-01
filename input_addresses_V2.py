import csv
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
address_dir = os.path.join(data_dir,'address_files')

def get_reader(filename):
    """'Public Function'
    Return a csv reader and a file handle for address files.

    Assumes file exists in the address_dir directory.
    Otherwise it will throw an unhandled exception.
    """

    f = open(os.path.join(address_dir,filename),'r+')
    add_reader = csv.reader(f)
    return add_reader,f

def generate_job_id(last_num=0):
    """'Private Function'
    Create a new job id number.

    May need to make this thread safe later, but for now this simply reads
    in a value from main code and increments it.
    """
    
    return last_num+1

def load_job_id():
    """'Private Function'
    Read job id in from [implementation not yet decided]

    """
    pass

def save_job_id():
    """'Private Function'
    Updates persistent copy of last job id number.  Counterpart to load_job_id
    [implementation not yet decided upon]

    """
    pass

def get_next_job_id():
    """'Public Function'
    Returns the next job id number.  Guaranteed to be unique.

    """
    load_job_id()
    job_number = generate_job_id()
    save_job_id()

    return job_number

def define_mapping(x,header,cache = {}):
    """'Private Function'
    Changes the name of a column header to either a value from the cache or,
    if none defined, asks the user for one and updates the cache.

    May need to be less free with the auto cacheing.  It is possible, I suppose
    for various customers to incorrectly name columns in contradictory ways.

    """

    if x in cache.keys():
        return cache[x]
    else:
        print(x,' is not a standard header name.\n')
        new = 'elephant man'
        while new not in header:
            new = input('What should it map to? ')
        cache[x] = new
        return new

def validate_header(keyline):
    """'Private Function'
    Checks header row to see if it conforms to specs.  Reorders
    as necessary.  Returns shuffle order

    """
    header_row = ['Other 1',
              'Other 2',
              'Name',
              'Title',
              'Company',
              'Address 1',
              'Address 2',
              'Address 3',
              'City',
              'State',
              'Zip',
              'Country',
              'Number of Copies'
              ]
    sort_helper = []

    for x in keyline:
        if x in header_row:
            sort_helper.append(header_row.index(x))
        elif x!='' and x not in header_row:
            new_header = define_mapping(x,header_row)
            sort_helper.append(header.index(new_header))

    return sort_helper

def validate_country(country,cache = {}):
    """'Private Function'
    Ensures country is a proper country (none of that South Volta nonesense)

    """

    #maybe read this in from a file or something?
    acceptable_countries = []
    return country #for now

##    if country in accepable_countries:
##        return country
##    elif country in cache.keys():
##        return cache[country]
##    else:
##        print(country,' is not a known country.  If you would like to map it \
##to something else, type in the name of a known country.  If you would like to \
##add it as is, enter 0\n')
##        new_name = 'elephant man'
##        while new_name not in acceptable_countries and new_name != 0:
##            new_name = input('New Name: ')
##        if new_name == '0':
##            #this function doesn't exist yet
##            update_countries_list(new_name)
##        else:
##            cache[country] = new_name
##
##        return new_name

def update_countries_list(country):
    """'Private Function
    Updates the list of acceptable countries.
    Implementation not yet decided upon.

    """

    pass
    

def process_address_file(reader,file):
    """'Public Function'
    Takes a raw address file from customer, produces a new file that conforms
    to assumptions, and collects/outputs some data about the file

    """

    mult_copies_list = []
    countries = []
    row_counter = 0
    total_num_mags = 0
    countries = {}
    new_file = os.path.join(address_dir,'temp.csv')

    keyline = next(reader)
    sort_helper = validate_header(keyline)

    with open(temp,'w',newline = '') as f:
        writer = csv.writer(f)

        for line in reader:
            new_line = [x for (y,x) in sorted(zip(sort_helper,line))]

            num_copies = int(new_line[-1])
            total_num_mags += num_copies
            
            country = new_line[-2]
            country = validate_country(country)
            try:
                countries[country] += 1
            except KeyError:
                countries[country] = 1
            

            if num_copies>1:
                mult_copies_list.append(row_counter)
            
            writer.writerow(new_line)
            row_counter += 1


    file.close()
    os.remove(file.name)
    os.rename(new_file,file.name)

    return file.name,mult_copies_list,row_counter,total_num_mags,countries

        
            

    

    

    
