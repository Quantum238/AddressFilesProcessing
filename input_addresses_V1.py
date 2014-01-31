import csv
import os
import random
import math

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
address_dir = os.path.join(data_dir,'address_files')



def get_reader(filename):
    """Returns a csv reader and a file_handle to input file, assuming
    it exists in the address_dir.  Catastrophic failure otherwise

    'Private' function
    """
    
    f = open(os.path.join(address_dir,filename),'r+')
    add_reader = csv.reader(f)
    return add_reader,f


def generate_job_id(cache = []):
    """Creates a new job id number from a random number.

    You'll notice the cache in the input.  This doesn't work, because it's
    not preserved across code invocations.  If you do several files in one
    instantiation of the interactive editor, you will be guaranteed unique
    ID's.  If you don't, you'll probably be safe because it seeds from the
    system time, but this is not acceptable for production code.  Probably?
    I have to seriously consider this.  Maybe pickle the cache?
    """
    
    new_id = math.ceil(random.random() * 10**5)
    if new_id in cache:
        new_id = generate_job_id()
    cache.append(new_id)
    return new_id

def define_mapping(x,header):
    """Changes the name of a column header to a user input one.
    Will only accept a canonical header.
    """
    
    print(x,' is not a standard header name.\n')
    new = 'elephant man'
    while new not in header:
        new = input('What should it map to? ')
    return new
    

def reformat_address_file(reader,file):
    """Reformat is a bit of a misnomer at this point.
    Standardizes and correctly orders the header row,
    then reorders columns to match.  Along the way,
    counts various things and creates two additional
    csv files to store country ordering and bulk/single data
    """

    #canonical titles and order or keyrow
    header = ['Other 1',
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
              'Number of Copies']
                      

    #Initialize some things
    title_row = next(reader)
    sort_helper = []
    mult_copies_list = []
    countries = []
    incredulity_counter = 0
    total_num_mags = 0


    #ensure title row is in correct order and contains correct headings
    for x in title_row:
        if x!='' and x in header:
            sort_helper.append(header.index(x))
        elif x!='' and x not in header:
            new_header = define_mapping(x,header)
            sort_helper.append(header.index(new_header))
            

    #temp will be the new main csv
    temp = os.path.join(address_dir,'temp.csv')
    
    #these two hold the orders of bulk and single
    bulk_country = os.path.splitext(file.name)[0]+'_btemp.csv'
    single_country = os.path.splitext(file.name)[0]+'_stemp.csv'

    #open all these lovely files
    with open(temp,'w',newline = '') as new_file, open(bulk_country,'w',newline = '') as bulk_country,open(single_country,'w',newline='') as single_country:

        #get writers for all necessary files
        writer = csv.writer(new_file)
        bc_writer = csv.writer(bulk_country)
        sc_writer = csv.writer(single_country)

        
        writer.writerow(header)

        #shuffle every row according to sort_helper and write it into temp
        #also count how many magazines there are
        for line in reader:
            new_line = [x for (y,x) in sorted(zip(sort_helper,line))]
            writer.writerow(new_line)
            num_copies = int(new_line[-1])
            total_num_mags+=num_copies


            #countries go into separate files depending on bulk or singleton
            #This ends up being not necessary I think, after I refactor it
            #But for now, it is easiest.
            country = new_line[-2]
            if num_copies>1:
                bc_writer.writerow([country])
            elif num_copies==1:
                sc_writer.writerow([country])
                

            
            #if there is more than 1 copy, we need to know about that,
            #and where it happens
            if num_copies>1:
                mult_copies_list.append(incredulity_counter)

            incredulity_counter+=1
            
            
        
            
    #close the initial address file
    file.close()
    #delete it
    os.remove(file.name)
    #rename the newly formatted temp file to what the old address file was
    os.rename('C:\\Users\\DannyBrosef\\Desktop\\MyCodes\\CrystalReportsClone\\data\\address_files\\temp.csv',
              file.name)

    return file.name,mult_copies_list,incredulity_counter,total_num_mags
    
            
        
        
            
    
