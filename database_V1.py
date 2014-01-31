import sqlite3
import os


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
##tex_files_dir = os.path.join(data_dir,'raw_tex')
##indicia_dir = os.path.join(data_dir,'indicias')
##pdf_dir = os.path.join(main_dir,'outputs')
##junk_dir = os.path.join(main_dir,'junk')
log_dir = os.path.join(main_dir,'outputs','logs')
address_dir = os.path.join(data_dir,'address_files')
database = os.path.join(data_dir,'database')


con = sqlite3.connect(os.path.join(database,'database.db'))



def add_value(cur,table,*args):
    #For now, this is unsafe (vulnerable to injection attacks and blahblah)

    insert = "insert into "+table+" values("
    for x in args:
        insert += "'" + str(x) + "', "

    insert = insert[0:(len(insert) - 2)]
    insert+=");"

    
    cur.execute(insert)


def get_value(cur,select):
    cur.execute(select+';')
    answer = cur.fetchall()
    return answer


if __name__=='__main__':


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
        
                                                        
                                                        
                                        
                 
    

        

