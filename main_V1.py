##import time
#this is used for basic profiling
from latex_making_V1 import *
#I shouldn't wildcard import, but I am
from input_addresses_V1 import *
#I shouldn't wildcard import, but I am
from indicia_lookup_V1 import *
#I shouldn't wildcard import, but I am
from database_V1 import *
#I shouldn't wildcard import, but I am
import datetime
#This is used to fill out log files with the date
import csv
#For CSV reading and writing
from multiprocessing import Process
#For multicore work
##import cProfile
#for profiling
##import pstats
#For reading profiling data because fuck you


#The main directory of this project
main_dir = os.path.split(os.path.abspath(__file__))[0]
#I used this method once and I guess I liked it?
data_dir = os.path.join(main_dir,'data')
tex_files_dir = os.path.join(data_dir,'raw_tex')
indicia_dir = os.path.join(data_dir,'indicias')
log_dir = os.path.join(main_dir,'outputs','logs')
address_dir = os.path.join(data_dir,'address_files')
database = os.path.join(data_dir,'database')

#TODO: Add support for choosing custom logo files
logo_file = 'logo.png' #The default globgistics logo



def create_document_fully(file):
    """Runs LaTex twice on the .tex file (called from a separate process"""
    create_document(file)
    create_document(file)
    print('All finished, man')
    
def choose_indicia(c_reader):
    """Selects the appropriate indicia based on the dict in indicia_lookup"""
    #country is actually a 1 element list consisting of the string name of
    #the country, because csv reading and writing is a tad picky
    country = next(c_reader)
    file = find_indicia_file(country[0])
    if file is not None:
        return file
    else:
        return None
    
def make_sets_of_pages(f,addresses,c_reader,mult_list,option):
    """Calls the various LaTeX generation functions.

    f is the tex file that will be created

    addresses is a csv reader for the properly formatted address file

    c_reader is a csv reader generated from the country text file (for choosing indicias)
    This needs to be separate from the address file because the countries are re-ordered
    according to bulk data, but the address file is not.
        
    mult_list is a list of line numbers. Line numbers in this list correspond to lines in the
    address file that have multiple copies going to the same address (ie are bulk ships)

    option determines whether or not the bulk or the single portion is being created
    """

    #If option is 1, we are doing the bulk copies
    #If option is 2, we are doing the single copies

    default_indicia = 'pic.png'
    #Latex knows about the picture file and gets cranky about \ vs /, so just
    #the filename is required, not the dir path

    if option==1:
        #counter is for page numbering
        counter = 1
        for (ii,line) in enumerate(addresses):
            if ii in mult_list:
                ind_file = choose_indicia(c_reader) 
                if ind_file is None:
                    ind_file = default_indicia
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
                counter+=1
    elif option==2:
        #bulk copies go first, so counter has to start at [last bulk copy page num]+1
        counter = len(mult_list) + 1
        for(ii,line) in enumerate(addresses):
            if ii not in mult_list:
                ind_file = choose_indicia(c_reader)
                if ind_file is None:
                    ind_file = default_indicia
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
                counter+=1


    
def make_logfile(total_num_addresses,total_num_mags,weight,out_file,countries):
    """Creates a txt logfile containing some easily readable summary information.
    The name of the file is the same as the CarrierSheet generated, with _logs appended
    """

    with open(os.path.join(log_dir,out_file+'_logs.txt'),'w') as f:
        
        f.write('Total Number of Addresses: '+str(total_num_addresses))
        f.write('\n')
        f.write('Total Number of Magazines: '+str(total_num_mags))
        f.write('\n')
        f.write('Total Weight: '+str(float(total_num_mags)*float(weight)))
        f.write('\n')
        f.write('Date Printed: '+str(date.date.today()))
        f.write('\n')
        f.write('Country Breakdown:')
        f.write('\n')
        for x in countries:
            f.write(x+': '+str(countries[x]))
            f.write('\n')
        f.write('\n')



if __name__ =='__main__':

  
    #get name of publication and other shit from user
    magazine_name = input('Publication: ').replace(' ','')
    volume_number = input('Volume: ') #or date or issue or w/e
    weight = input('Weight: ')
    add_file = input('Address File Name: ')

    #TODO there are a few more things on that google doc that need to be collected


    #as of right now, this is just a random number.  Only goes up to about 10**5
    #need to implement a systemwide cache or shift to pure incrementing with some sort of
    #system knowledge of what number to use next
    job_id = generate_job_id()

    #this is just a string, the main portion of all generated filenames
    out_file = magazine_name+'_V'+volume_number


    #update database entries based on user inputs so far
    add_from_inputs(magazine_name,volume_number,weight,job_id,add_file,out_file)


    
    #Prepare to read possible incorrectly formatted file
    #addresses is a csv reader (not used atm), file_handle is a file object pointer thing
    addresses,file_handle = get_reader(add_file)

    #Reformat file
    #this actually deletes and remakes several files, so the old file pointer is no good
    #file_name is just a string with no directory info
    file_name,mult_copies_list,total_num_addresses,total_num_mags = reformat_address_file(addresses,
                                                                      file_handle)

    #Prepare to actually read from file. A new csv reader and file pointer are needed
    addresses,file_handle = get_reader(file_name)

    #As a result of reformat_address_file, two other files are created,
    #containing the bulk and singleton country listings.
    #We will need handles to these files and reader objects for them
    

    bulk_country_file = open(os.path.splitext(file_name)[0]+'_btemp.csv',
                             'r',
                             newline='')
    single_country_file = open(os.path.splitext(file_name)[0]+'_stemp.csv',
                             'r',
                             newline='')
    bc_reader = csv.reader(bulk_country_file)
    sc_reader = csv.reader(single_country_file)
    

    #let's generate a tex file
    with open(os.path.join(tex_files_dir,'tempfile.tex'),'w') as f:
        
        write_preamble(f,out_file)

        #will eventually also loop over carriers, if Peter isn't a crazy man?
        #this is sort of the last logical spec thing that needs to be answered
        start_page(f)

        #read through the address file, paying attention only to the bulk countries
        #as determined by mult_list (all in make_sets_of_pages)
        bulk_page(f,len(mult_copies_list))
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,bc_reader,mult_copies_list,1)
        file_handle.close()

        #we have to churn through the same file again, this time for single countries
        #A new file handle and reader are required because the file had to be closed
        #after the bulk reading because I don't know how to tell python to go
        #back to the top

        addresses,file_handle = get_reader(file_name)
        non_bulk_page(f,(total_num_addresses - len(mult_copies_list)))
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,sc_reader,mult_copies_list,2)

        
        end_page(f)
        end_doc(f)

        #clean up all these files
        file_handle.close()
        bulk_country_file.close()
        single_country_file.close()

    #end with statement

    #start making the PDF from the tex file in another 'thread'
    #I don't know how to profile this type of thing properly, so I don't know
    #if I should use a thread or a process
    maker = Process(target = create_document_fully,
                             args = ['tempfile.tex'])
    maker.start()

    #there are several 'temp' files created in the address folder (lists of countries,
    #basically) during all this processing.  Don't need em

    #this is a list of string names of all files in the address dir
    files = next(os.walk(address_dir))[2]
    #empty dict to collect country summary data with
    countries = {}


    for file in files:
        #grab the last 4 letters of the file name (before the extension)
        temp = os.path.splitext(file)[0]
        temp = temp[len(temp)-4:len(temp)]

        #only temp files end with temp, so this is safe
        if temp=='temp':
            #While I'm here, I'll count the countries up.  This could be done in a number
            #of other places, and probably should be, in order to eliminate this extra
            #read of all these files.  Probably move it up to the indicia selection
            #or thereabouts
            with open(os.path.join(address_dir,file),'r') as f:
                reader = csv.reader(f)

                for line in reader:
                    #again, the file contains rows that are 1-element lists
                    country = line[0]

                    #increment the counter for that country
                    try:
                        countries[country] = countries[country] + 1
                    except KeyError:
                        countries[country] = 1
                #end for

            #end with
            #delete the temp file
            os.remove(os.path.join(address_dir,file))
        #end if
    #end for
    make_logfile(total_num_addresses,total_num_mags,weight,out_file,countries)





    
    
    
        
