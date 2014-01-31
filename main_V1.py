import time
from latex_making_V1 import *
from input_addresses_V1 import *
from indicia_lookup_V1 import *
from database_V1 import *
import datetime
import csv
from multiprocessing import Process
##import cProfile
##import pstats


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
tex_files_dir = os.path.join(data_dir,'raw_tex')
indicia_dir = os.path.join(data_dir,'indicias')
##pdf_dir = os.path.join(main_dir,'outputs')
##junk_dir = os.path.join(main_dir,'junk')
log_dir = os.path.join(main_dir,'outputs','logs')
address_dir = os.path.join(data_dir,'address_files')
database = os.path.join(data_dir,'database')

logo_file = 'logo.png'
def create_document_fully(file):
    create_document(file)
    create_document(file)
    print('All finished, man')
    
def choose_indicia(c_reader):
    #so later, there'll be some kind of table lookup going on,
    #matching country to indicia file (so probably more arguments there)
    #For now I'm just going to print out the country

    country = next(c_reader)
    file = find_indicia_file(country[0])
    if file is not None:
        return file
    else:
        return None
    
def make_sets_of_pages(f,addresses,c_reader,mult_list,option):
    #If option is 1, we are doing the bulk copies
    #If option is 2, we are doing the single copies

    if option==1:
        counter = 1
        for (ii,line) in enumerate(addresses):
            if ii in mult_list:
                ind_file = choose_indicia(c_reader) #later this will be the picname
                if ind_file is None:
                    ind_file = 'pic.png'
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
##                make_an_address_page(f,counter,line,'Job ID')
                counter+=1
    elif option==2:
        counter = len(mult_list) + 1
        for(ii,line) in enumerate(addresses):
            if ii not in mult_list:
                ind_file = choose_indicia(c_reader)
                if ind_file is None:
                    ind_file = 'pic.png'
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
##                make_an_address_page(f,counter,line,'Job ID')
                counter+=1


    
def make_logfile(total_num_addresses,total_num_mags,weight,out_file,countries):


    with open(os.path.join(log_dir,out_file+'_logs.txt'),'w') as f:
        
        f.write('Total Number of Addresses: '+str(total_num_addresses))
        f.write('\n')
        f.write('Total Number of Magazines: '+str(total_num_mags))
        f.write('\n')
        f.write('Total Weight: '+str(float(total_num_mags)*float(weight)))
        f.write('\n')
        f.write('Date Printed: '+str(datetime.date.today()))
        f.write('\n')
        f.write('Country Breakdown:')
        f.write('\n')
        for x in countries:
            f.write(x+': '+str(countries[x]))
            f.write('\n')
        f.write('\n')



if __name__ =='__main__':

##    #main()
##    cProfile.run('main()','stats')
##    p=pstats.Stats('stats')
##    p.strip_dirs().sort_stats('time').print_stats(10)
    
    

    magazine_name = input('Publication: ').replace(' ','')
    volume_number = input('Volume: ') #or date or issue or w/e
    weight = input('Weight: ')
    add_file = input('Address File Name: ')
##    magazine_name = 'ProfileTest'
##    volume_number = '1'
##    weight = '1'
##    add_file = 'test_addresses.csv'

    job_id = generate_job_id()
    out_file = magazine_name+'_V'+volume_number



    con = sqlite3.connect(os.path.join(database,'database.db'))
    cur = con.cursor()

    add_value(cur,
              'Customers',
              'Danny',
              magazine_name)

    add_value(cur,
              'Publications',
              magazine_name,
              int(volume_number),
              1,
              '',
              '')

    add_value(cur,
              'ShippingInfo',
              magazine_name,
              int(volume_number),
              1,
              float(weight),
              '',
              '',
              '',
              '',
              job_id,
              '')
    
    add_value(cur,
              'AddressFiles',
              magazine_name,
              int(volume_number),
              1,
              add_file,
              '')
    
    add_value(cur,
              'CarrierFiles',
              add_file,
              out_file)


    names = get_value(cur,'select * from Publications')
    for x in names:
        print(x)

    con.commit()
    con.close()
    
    #Prepare to read possible incorrectly formatted file
    addresses,file_handle = get_reader(add_file)
    #Reformat file
    file_name,mult_copies_list,total_num_addresses,total_num_mags = reformat_address_file(addresses,
                                                                      file_handle)
    #Prepare to actually read from file
    addresses,file_handle = get_reader(file_name)

    #As a result of reformat_address_file
    #A new file called [addressfile]_temp.csv
    #is created.  This has the countries in it, in order
    #from which the correct indicia can be selected
    #I guess?  That's the way I'm gonna do it
    #to try and save memory space.  Anywho, you should have a reference to
    #that file.

    bulk_country_file = open(os.path.splitext(file_name)[0]+'_btemp.csv',
                             'r',
                             newline='')
    single_country_file = open(os.path.splitext(file_name)[0]+'_stemp.csv',
                             'r',
                             newline='')
    bc_reader = csv.reader(bulk_country_file)
    sc_reader = csv.reader(single_country_file)
    
    
    with open(os.path.join(tex_files_dir,'tempfile.tex'),'w') as f:
        write_preamble(f,out_file)
        
        #will eventually also loop over carriers
        start_page(f)
        bulk_page(f,len(mult_copies_list))
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,bc_reader,mult_copies_list,1)
        non_bulk_page(f,(total_num_addresses - len(mult_copies_list)))
        file_handle.close()
        addresses,file_handle = get_reader(file_name)
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,sc_reader,mult_copies_list,2)
        end_page(f)
        end_doc(f)
        file_handle.close()
        bulk_country_file.close()
        single_country_file.close()
    
    maker = Process(target = create_document_fully,
                             args = ['tempfile.tex'])
    maker.start()

    #there are several temp files created
    #in the address file along with this.  Don't need em
    files = next(os.walk(address_dir))[2]
    countries = {}

    for file in files:
        temp = os.path.splitext(file)[0]
        temp = temp[len(temp)-4:len(temp)]
        if temp=='temp':
            #later I'll want a country breakdown.  Here is where
            #I shall grab it from
            with open(os.path.join(address_dir,file),'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    country = line[0]
                    try:
                        countries[country] = countries[country] + 1
                    except KeyError:
                        countries[country] = 1
            
                    
            os.remove(os.path.join(address_dir,file))
    
    make_logfile(total_num_addresses,total_num_mags,weight,out_file,countries)





    
    
    
        
