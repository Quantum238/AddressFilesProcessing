import sqlite3
import os


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
log_dir = os.path.join(main_dir,'outputs','logs')
address_dir = os.path.join(data_dir,'address_files')
database = os.path.join(data_dir,'database')


##con = sqlite3.connect(os.path.join(database,'database.db'))



def add_value(cur,table,*args):
    #For now, this is unsafe (vulnerable to injection attacks and blahblah)

    insert = "insert into "+table+" values("
    for x in args:
        insert += "'" + str(x) + "', "

    insert = insert[0:(len(insert) - 2)]
    insert+=");"

    
    cur.execute(insert)


def get_value(cur,select):
    #Don't actually use this.  I don't know what kind of searches we'll have to
    #do.  This is just a placeholder of the lowest order
    cur.execute(select+';')
    answer = cur.fetchall()
    return answer

def add_from_inputs(magazine_name,volume_number,weight,job_id,add_file,out_file):
    """Creates and executes appropriate SQL queries to add entries to
    the database when new magazines are processed.
    """
    
    con = sqlite3.connect(os.path.join(database,'database.db'))
    with con:
        
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


   
if __name__=='__main__':

    #Basically, run this file to erase and recreate the database.
    #Import it to use the database

    #Some things need to be added


    con = sqlite3.connect(os.path.join(database,'database.db'))

    #if run, create database
    with con:
        cur = con.cursor()

        cur.execute('drop table if exists Customers')
        cur.execute('drop table if exists Publications')
        cur.execute('drop table if exists ShippingInfo')
        cur.execute('drop table if exists AddressFiles')
        cur.execute('drop table if exists CarrierFiles')
        
        
        makeCustomers = '''create table Customers(Customer varchar(20),
                                                  Name varchar(20),                                         
                                                  primary key(Customer
                                                              ));'''
        makePublications = '''create table Publications(Name varchar(20),
                                                        Volume int,
                                                        Issue int,
                                                        FrontScan varchar(20),
                                                        BackScan varchar(20),
                                                        primary key(Name,
                                                                    Volume,
                                                                    Issue),
                                                        foreign key(Name) references Customers);
                                                        '''
        makeShippingInfo = '''create table ShippingInfo(Name varchar(20),
                                                        Volume int,
                                                        Issue int,
                                                        Weight float(2),
                                                        DateReceived date,
                                                        DateApproved date,
                                                        DatePrinted date,
                                                        DateShipped date,
                                                        JobNumber varchar(20),
                                                        Cost float(2),
                                                        primary key(Name,
                                                                    Volume,
                                                                    Issue)
                                                        foreign key(Name,Volume,Issue) references Publications);
                                                        '''
        makeAddressFiles = '''create table AddressFiles(Name varchar(20),
                                                        Volume int,
                                                        Issue int,
                                                        AddressFile varchar(20),
                                                        CountryBreakDown varchar(20),
                                                        primary key(Name,
                                                                    Volume,
                                                                    Issue),
                                                        foreign key(Name,Volume,Issue) references Publications);
                                                        '''
        makeCarrierFiles = ''' create table CarrierFiles(AddressFile varchar(20),
                                                         CarrierFile varchar(20),
                                                         primary key(AddressFile,
                                                                     CarrierFile),
                                                         foreign key(AddressFile) references AddressFiles);
                                                         '''


        cur.executescript(makeCustomers)
        cur.executescript(makePublications)
        cur.executescript(makeShippingInfo)
        cur.executescript(makeAddressFiles)
        cur.executescript(makeCarrierFiles)
        
                                                        
                                                        
                                        
                 
    

        

