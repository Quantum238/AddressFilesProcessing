import csv
import os
import random
import math

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
##tex_files_dir = os.path.join(data_dir,'raw_tex')
##indicia_dir = os.path.join(data_dir,'indicias')
##pdf_dir = os.path.join(main_dir,'outputs')
##junk_dir = os.path.join(main_dir,'junk')
address_dir = os.path.join(data_dir,'address_files')

def get_reader(filename):
    f = open(os.path.join(address_dir,filename),'r+')
    add_reader = csv.reader(f)
    return add_reader,f

def generate_job_id(cache = []):
    new_id = math.ceil(random.random() * 10**5)
    if new_id in cache:
        new_id = generate_job_id()
    cache.append(new_id)
    return new_id

def define_mapping(x,header):
    print(x,' is not a standard header name.\n')
    new = 'elephant man'
    while new not in header:
        new = input('What should it map to? ')
    return new
    

def reformat_address_file(reader,file):

    #Actual Address files might have things out of order
    #and might also be missing some columns
    #This puts them in printing order
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
                      

    title_row = next(reader)
    sort_helper = []
    mult_copies_list = []
    countries = []
    incredulity_counter = 0
    total_num_mags = 0

    for x in title_row:
        if x!='' and x in header:
            sort_helper.append(header.index(x))
        elif x!='' and x not in header:
            new_header = define_mapping(x,header)
            sort_helper.append(header.index(new_header))
            

    temp = os.path.join(address_dir,'temp.csv')
    bulk_country = os.path.splitext(file.name)[0]+'_btemp.csv'
    single_country = os.path.splitext(file.name)[0]+'_stemp.csv'
    with open(temp,'w',newline = '') as new_file, open(bulk_country,'w',newline = '') as bulk_country,open(single_country,'w',newline='') as single_country:

        writer = csv.writer(new_file)
        bc_writer = csv.writer(bulk_country)
        sc_writer = csv.writer(single_country)

        writer.writerow(header)
        for line in reader:
            new_line = [x for (y,x) in sorted(zip(sort_helper,line))]
            writer.writerow(new_line)
            num_copies = int(new_line[-1])
            total_num_mags+=num_copies

            #I think it will be easier if we have a sep file of the countries
            #Then I can assign indicias quickly
            #note: Blank country field simply means no inidicia
            #One file for bulk ship and one for single ship
            #because I have to do that anyway later and this is easier
            #Sort of
            country = new_line[-2]
            if num_copies>1:
                bc_writer.writerow([country])
            elif num_copies==1:
                sc_writer.writerow([country])
                

            
            #if there is more than 1 copy, we need to know about that
            if num_copies>1:
                mult_copies_list.append(incredulity_counter)

            incredulity_counter+=1
            
            
        
            

    file.close()    
    os.remove(file.name)
    os.rename('C:\\Users\\DannyBrosef\\Desktop\\MyCodes\\CrystalReportsClone\\data\\address_files\\temp.csv',
              file.name)
    return file.name,mult_copies_list,incredulity_counter,total_num_mags
    
            
        
        
            
    
