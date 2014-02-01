from latex_making_V1 import *
from input_addresses_V2 import *
from indicia_lookup_V1 import *
from database_V1 import *

import datetime
import csv
from multiprocessing import Process

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
tex_files_dir = os.path.join(data_dir,'raw_tex')
indicia_dir = os.path.join(data_dir,'indicias')
log_dir = os.path.join(main_dir,'outputs','logs')
address_dir = os.path.join(data_dir,'address_files')
database = os.path.join(data_dir,'database')

logo_file = 'logo.png'

def produce_pdf(file):
    """Runs LaTeX twice on the .tex file, in a separate process"""
    create_document(file)
    create_document(file)
    print('All done, pal')

def make_sets_of_pages(f,addresses,mult_list,mode):
    """Calls the various LaTeX generation functions

    f is the tex file that will be created

    addresses is a csv reader for the properly formatted address file

    mult_list is a list of line numbers. Line numbers in this list correspond to lines in the
    address file that have multiple copies going to the same address (ie are bulk ships)

    option determines whether or not the bulk or the single portion is being created
    """

    #If option is 1, bulk copies
    #If option is 2, single copies

    default_indicia = 'pic.png'

    if option == 1:
        counter = 1
        for (ii,line) in enumerate(addresses):
            if ii in mult_list:
                ind_file = find_indicia_file(line[-2])
                if ind_file is None:
                    ind_file = default_indicia
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
                counter += 1
    elif option == 2:
        counter = len(mult_list) + 1
        for (ii,line) in enumerate(addresses):
            if ii not in mult_list:
                ind_file = find_indicia_file(line[-2])
                if ind_file is None:
                    ind_file = default_indicia
                add_pics(f,ind_file,logo_file)
                make_an_address_page(f,counter,line,job_id)
                counter += 1

def make_logfile(total_num_addresses,
                 total_num_mags,
                 weight,
                 out_file,
                 countries):
    """Creates a txt logfile containing some easily readable summary
    information.  The name of the file is the same as the PDF generated,
    with '_log.txt' at the end instead of .pdf

    """

    with open(os.path.join(log_dir,out_file+'_log.txt'),'w') as f:
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
        for x in countries.keys():
            f.write(x + ' : ' + str(countries[x]))
            f.write('\n')
        f.write('\n')

if __name__ == '__main__':


    magazine_name = input('Publication: ').replace(' ','')
    volume_number = input('Volume: ')
    weight = input('Weight: ')
    add_file = input('Address File Name: ')

    job_id = get_next_job_id()

    out_file = magazine_name + '_V' + volume_number
    add_from_inputs(magazine_name,volume_number,weight,job_id,add_file,out_file)

    addresses,file_handle = get_reader(add_file)
    file_name,mult_copies_list,num_addresses,total_num_mags,countries = process_address_file(addresses,
                                                                                             file_handle)
    addresses,file_handle = get_reader(add_file)

    with open(os.path.join(tex_files_dir,'tempfile.tex'),'w') as f:

        write_preamble(f,out_file)
        start_page(f)

        bulk_page(f,len(mult_copies_list))
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,mult_copies_list,1)
        file_handle.close()

        addresses,file_handle = get_reader(add_file)
        non_bulk_page(f,(total_num_addresses - len(mult_copies_list)))
        title_row = next(addresses)
        make_sets_of_pages(f,addresses,mult_copies_list,2)
        file_handle.close()

        end_page(f)
        end_doc(f)

    maker = Process(target = create_document_fully,
                    args = ['tempfile.tex']
                    )
    maker.start()
    make_logfile(total_num_addresses,
                 total_num_mags,
                 weight,
                 out_file,
                 countries)
    

    

        

        

        
        

    
    

    
    
        
        
    
