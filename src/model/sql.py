SQL = {
    # base table
    "CREATE_TAB_valid_db": "CREATE TABLE IF NOT EXISTS valid_db(\
                        empty INTEGER\
                    )",

    # common queries ==========================================================
    "SELECT_all_TABS": "SELECT name FROM sqlite_master WHERE type='table'",
    "DROP_TAB": "DROP TABLE IF EXISTS {}",
    "SELECT_all": "SELECT * FROM {}",

    # language ================================================================
    # base table
    "CREATE_TAB_language": "CREATE TABLE IF NOT EXISTS language(\
                        current TEXT\
                    )",
    "INSERT_language": "INSERT INTO language (current) VALUES (?)",
    "SELECT_language": "SELECT current FROM language",
    "UPDATE_language": "UPDATE language SET current=?",

    # houses ==================================================================
    # base table
    "CREATE_TAB_houses": "CREATE TABLE IF NOT EXISTS houses(\
                        id INTEGER PRIMARY KEY,\
                        house_name TEXT,\
                        house_description TEXT\
                    )",
    "SELECT_houses": "SELECT house_name, house_description FROM houses",
    "SELECT_is_house": "SELECT * FROM houses WHERE house_name=?",
    "INSERT_house": "INSERT INTO houses (house_name, house_description) VALUES (?, ?)",
    "DELETE_house": "DELETE FROM houses WHERE id=?",
    "SELECT_house_id": "SELECT id FROM houses WHERE house_name=?",

    # tariffs =================================================================
    # base table
    "CREATE_TAB_tariffs": "CREATE TABLE IF NOT EXISTS tariffs(\
                        tariff_type TEXT,\
                        tariff_value REAL\
                    )",
    "SELECT_tariffs": "SELECT tariff_type, tariff_value FROM tariffs",
    "SELECT_is_tariff": "SELECT * FROM tariffs WHERE tariff_type=? AND tariff_value=?",
    "INSERT_tariff": "INSERT INTO tariffs (tariff_type, tariff_value) VALUES (?, ?)",
    "DELETE_tariff": "DELETE FROM tariffs WHERE tariff_type=? AND tariff_value=?",
    "SELECT_tariffs_by_type": "SELECT tariff_value FROM tariffs WHERE tariff_type=?",

    # years ===================================================================
    # base table
    "CREATE_TAB_years": "CREATE TABLE IF NOT EXISTS years(\
                        house_id INTEGER,\
                        year INTEGER,\
                        num_elec_meters INTEGER,\
                        num_wat_meters INTEGER,\
                        num_gas_meters INTEGER,\
                        num_garb_meters INTEGER,\
                        FOREIGN KEY(house_id) REFERENCES houses(id)\
                    )",
    "SELECT_years": "SELECT year FROM years WHERE house_id=?",
    "SELECT_is_year": "SELECT * FROM years WHERE house_id=? AND year=?",
    "INSERT_year": "INSERT INTO years (house_id, year, num_elec_meters, num_wat_meters, num_gas_meters, num_garb_meters) VALUES (?, ?, ?, ?, ?, ?)",
    "DELETE_year": "DELETE FROM years WHERE house_id=? AND year=?",
    "DELETE_years": "DELETE FROM years WHERE house_id=?",

    # meters ==================================================================
    # base table
    "CREATE_TAB_meters": "CREATE TABLE IF NOT EXISTS meters(\
                        id INTEGER PRIMARY KEY,\
                        house_id INTEGER,\
                        year INTEGER,\
                        type TEXT,\
                        num INTEGER,\
                        name TEXT,\
                        FOREIGN KEY(house_id) REFERENCES houses(id)\
                    )",
    "INSERT_meter": "INSERT INTO meters (house_id, year, type, num, name) VALUES (?, ?, ?, ?, ?)",
    "DELETE_meters_by_house_year": "DELETE FROM meters WHERE house_id=? AND year=?",
    "DELETE_meters_by_house": "DELETE FROM meters WHERE house_id=?",
    "SELECT_meter_names": "SELECT name FROM meters WHERE house_id=? AND year=? AND type=?",
    "SELECT_meter_num": "SELECT num FROM meters WHERE house_id=? AND year=? AND type=? AND name=?",

    # tables elec_wat_gas =====================================================
    "CREATE_TAB_elec_wat_gas": "CREATE TABLE IF NOT EXISTS {}(\
                        num INTEGER,\
                        meter_readings INTEGER,\
                        consumption INTEGER,\
                        tariff REAL,\
                        price REAL\
                    )",
    "INSERT_in_elec_wat_gas": "INSERT INTO {} VALUES (?,?,?,?,?)",
    "SELECT_reads__tariff": "SELECT meter_readings, tariff FROM {}",
    "SELECT_0_reads": "SELECT meter_readings FROM {} WHERE num=0",
    "SELECT_main_reads": "SELECT * FROM {} WHERE num>0",
    "UPDATE_0_reads": "UPDATE {} SET meter_readings=? WHERE num=0",
    "UPDATE_main_reads": "UPDATE {} SET meter_readings=?, consumption=?, tariff=?, price=? WHERE num=?",

    # tables garb =============================================================
    "CREATE_TAB_garb": "CREATE TABLE IF NOT EXISTS {}(\
                        num INTEGER,\
                        tariff_price REAL\
                    )",
    "INSERT_in_garb": "INSERT INTO {} VALUES (?,?)",
    "SELECT_tariff_price": "SELECT tariff_price FROM {}",
    "UPDATE_tariff_price": "UPDATE {} SET tariff_price=? WHERE num=?"
}
