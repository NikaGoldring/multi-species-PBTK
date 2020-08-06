from configparser import ConfigParser
import mysql.connector
import pandas as pd
import numpy as np


#### Initialisation with config file
def read_db_config():
    
    filename='config_PBTK.ini'
    section='mysql'

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db



#### Query to get the species_list table
def sp_table(): 
    
    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    sp_list  = []
    sp_id_   = []  #*
    sciname_ = []
    fam      = []
    fb_name  = []
    occurr   = []
    order    = []
    
    # Get * from data table
    query = ("SELECT * FROM species_list")     
    cursor.execute(query)
    
    # Writing query result in the created lists        
    for (sp_id, sciname, family, fishbase_name, occurrence, sp_order) in cursor:
        sp_id_.append("{}".format(sp_id))
        sciname_.append("{}".format(sciname))
        fam.append("{}".format(family))
        fb_name.append("{}".format(fishbase_name))
        occurr.append("{}".format(occurrence))     
        order.append("{}".format(sp_order))
    
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe 
    sp_list= [np.array(sp_id_), sciname_, fam, fb_name, occurr, order]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(sp_id = sp_list[0].astype(int), sciname = sp_list[1], family = sp_list[2], fb_name = sp_list[3], occurrence = sp_list[4], sp_order = sp_list[5])
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df



#### Query to get the oxygen consumption table
def oxygen_con_table():

    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    oxc_list = []
    oxc_id_  = []  #*
    sp_id_   = []  #*
    species_ = []
    fam      = []
    value    = []  ##*
    temp     = []  ##*
    value20  = []  ##*
    weight   = []  ##*
    salt     = []  ##*
    active   = []  
    stress   = []
    
    # Get * from data table
    ox_query = ("SELECT * FROM oxygen_consumption") 
    cursor.execute(ox_query)

    # Writing query result in the created lists 
    for (oxc_id, sp_id, species, family, oxc_value, temp_c, oxc_value20, weight_g, salinity, activity, applied_stress) in cursor:
        oxc_id_.append("{}".format(oxc_id))
        sp_id_.append("{}".format(sp_id))
        species_.append("{}".format(species))     
        fam.append("{}".format(family))
        value.append("{}".format(oxc_value))
        temp.append("{}".format(temp_c))
        value20.append("{}".format(oxc_value20))     
        weight.append("{}".format(weight_g))
        salt.append("{}".format(salinity))
        active.append("{}".format(activity))
        stress.append("{}".format(applied_stress))     
        
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe         
    oxc_list = [np.array(oxc_id_), np.array(sp_id_), species_, fam, np.array(value), np.array(temp), np.array(value20), 
                np.array(weight), np.array(salt), active, stress]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(oxc_id = oxc_list[0].astype(int), sp_id = oxc_list[1].astype(int), species = oxc_list[2], family = oxc_list[3], 
              value = oxc_list[4].astype(float), temp = oxc_list[5].astype(float), value20 = oxc_list[6].astype(float),
              weight = oxc_list[7].astype(float), salt = oxc_list[8].astype(float), active = oxc_list[9], stress = oxc_list[10])
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df



#### Query to get the cardiac_output table
def cardiac_output_table():
    
    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    q_list    = []
    q_id_     = []  #*
    sp_id_    = []  #*
    species_  = []
    fam       = []
    value     = []  ##*
    value_sd  = []  ##*
    weight    = []  ##*
    weight_sd = []  ##*
    temp      = []  ##*
    temp_sd   = []  ##*
    
    # Get * from data table
    q_query = ("SELECT * FROM cardiac_output") 
    cursor.execute(q_query)

    # Writing query result in the created lists 
    for (q_id, sp_id, species, family, q_value, q_value_sd, weight_g, weight_sd_g, temperature, temperature_sd) in cursor:
        q_id_.append("{}".format(q_id))
        sp_id_.append("{}".format(sp_id))
        species_.append("{}".format(species))     
        fam.append("{}".format(family))
        value.append("{}".format(q_value))
        value_sd.append("{}".format(q_value_sd))
        weight.append("{}".format(weight_g))     
        weight_sd.append("{}".format(weight_sd_g))
        temp.append("{}".format(temperature))
        temp_sd.append("{}".format(temperature_sd)) 
        
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe         
    q_list = [np.array(q_id_), np.array(sp_id_), species_, fam, np.array(value), np.array(value_sd), np.array(weight), 
              np.array(weight_sd), np.array(temp), np.array(temp_sd)]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(q_id = q_list[0].astype(int), sp_id = q_list[1].astype(int), species = q_list[2], family = q_list[3], 
              value = q_list[4].astype(float), value_sd = q_list[5].astype(float), weight = q_list[6].astype(float),
              weight_sd = q_list[7].astype(float), temp = q_list[8].astype(float), temp_sd = q_list[9].astype(float))
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df



#### Query to get the tissue volumes table
def tissue_volumes_table():
    
    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    tv_list   = []
    tv_id_    = []  #*
    sp_id_    = []  #*
    species_  = []
    fam       = []
    tissue_   = []
    sex_      = []
    value     = []  ##*
    value_sd  = []  ##*
    weight    = []  ##*
    weight_sd = []  ##*
    
    # Get * from data table
    tv_query = ("SELECT * FROM tissue_volumes") 
    cursor.execute(tv_query)

    # Writing query result in the created lists 
    for (tv_id, sp_id, species, family, tissue, sex, tv_value, tv_value_sd, weight_g, weight_sd_g) in cursor:
        tv_id_.append("{}".format(tv_id))
        sp_id_.append("{}".format(sp_id))
        species_.append("{}".format(species))     
        fam.append("{}".format(family))
        tissue_.append("{}".format(tissue))
        sex_.append("{}".format(sex))
        value.append("{}".format(tv_value))
        value_sd.append("{}".format(tv_value_sd))
        weight.append("{}".format(weight_g))     
        weight_sd.append("{}".format(weight_sd_g))
             
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe         
    tv_list = [np.array(tv_id_), np.array(sp_id_), species_, fam, tissue_, sex_, np.array(value), np.array(value_sd), 
              np.array(weight), np.array(weight_sd)]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(tv_id = tv_list[0].astype(int), sp_id = tv_list[1].astype(int), species = tv_list[2], family = tv_list[3], 
              tissue = tv_list[4], sex = tv_list[5], value = tv_list[6].astype(float), value_sd = tv_list[7].astype(float), 
              weight = tv_list[8].astype(float), weight_sd = tv_list[9].astype(float))
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df



#### Query to get the lipid contents table
def lipid_content_table():
    
    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    lipid_list = []
    lipid_id_  = []  #*
    sp_id_     = []  #*
    species_   = []
    fam        = []
    tissue_    = []
    sex_       = []
    value      = []  ##*
    value_sd   = []  ##*
    weight     = []  ##*
    weight_sd  = []  ##*
    
    # Get * from data table
    lipid_query = ("SELECT * FROM lipid_content") 
    cursor.execute(lipid_query)

    # Writing query result in the created lists 
    for (lipid_id, sp_id, species, family, tissue, sex, lipid_value, lipid_value_sd, weight_g, weight_sd_g) in cursor:
        lipid_id_.append("{}".format(lipid_id))
        sp_id_.append("{}".format(sp_id))
        species_.append("{}".format(species))     
        fam.append("{}".format(family))
        tissue_.append("{}".format(tissue))
        sex_.append("{}".format(sex))
        value.append("{}".format(lipid_value))
        value_sd.append("{}".format(lipid_value_sd))
        weight.append("{}".format(weight_g))     
        weight_sd.append("{}".format(weight_sd_g))
             
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe         
    lipid_list = [np.array(lipid_id_), np.array(sp_id_), species_, fam, tissue_, sex_, np.array(value), np.array(value_sd), 
              np.array(weight), np.array(weight_sd)]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(lipid_id = lipid_list[0].astype(int), sp_id = lipid_list[1].astype(int), species = lipid_list[2], family = lipid_list[3], 
              tissue = lipid_list[4], sex = lipid_list[5], value = lipid_list[6].astype(float), value_sd = lipid_list[7].astype(float), 
              weight = lipid_list[8].astype(float), weight_sd = lipid_list[9].astype(float))
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df



#### Query to get the blood flow table
def blood_flow_table():
    
    dbconfig = read_db_config()
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    
    # Create empty lists to store database colums in. They CAN'T have the same name due to overwriting the variabe.
    bf_list  = []
    bf_id_   = []  #*
    sp_id_   = []  #*
    species_ = []
    fam      = []
    tissue_  = []
    value    = []  ##*
    weight   = []  ##*
    length   = []  ##*
    temp     = []  ##*
    
    # Get * from data table
    bf_query = ("SELECT * FROM blood_flow") 
    cursor.execute(bf_query)

    # Writing query result in the created lists 
    for (bf_id, sp_id, species, family, tissue, bf_value, weight_g, length_cm, temperature) in cursor:
        bf_id_.append("{}".format(bf_id))
        sp_id_.append("{}".format(sp_id))
        species_.append("{}".format(species))     
        fam.append("{}".format(family))
        tissue_.append("{}".format(tissue))
        value.append("{}".format(bf_value))
        weight.append("{}".format(weight_g))
        length.append("{}".format(length_cm))
        temp.append("{}".format(temperature))
             
    # Storing all lists in a list. 
    # *IMPORTANT: all int and float lists must be arrays in order to define their types in the dataframe         
    bf_list = [np.array(bf_id_), np.array(sp_id_), species_, fam, tissue_, np.array(value), np.array(weight), 
                np.array(length), np.array(temp)]    
    
    # Convert list of lists into a dataframe to basically rebuilt the table
    df = dict(bf_id = bf_list[0].astype(int), sp_id = bf_list[1].astype(int), species = bf_list[2], family = bf_list[3], 
              tissue = bf_list[4], value = bf_list[5].astype(float), weight = bf_list[6].astype(float), 
              length = bf_list[7].astype(float), temp = bf_list[8].astype(float), )
    df = pd.DataFrame.from_dict(df, orient='columns', dtype=None)
    
    cursor.close()
    conn.close()
    
    return df