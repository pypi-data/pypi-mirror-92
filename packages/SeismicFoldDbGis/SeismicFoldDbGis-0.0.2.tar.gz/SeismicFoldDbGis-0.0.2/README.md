# Seismic Fold Db GIS

### module to load calculated fold from CSV file to GIS database

1. Dependencies:
    ```
    SQLAlchemy>=1.3.22
    GeoAlchemy2>=0.8.4
    ```    

2. CSV format
    * first line is header
    * comma separated
    * columns order: 'Easting', 'Northing', 'Fold', 'Bin Number', 'Row', 'Column'

3. DB engine connection
    * SQLite with spatial extension
        ```python
        def load_spatialite(dbapi_conn, connection_record):
            dbapi_conn.enable_load_extension(True)
            dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
        
        db_file = '/some_folder/fold.sqlite'
        engine = create_engine('sqlite:///' + db_file, echo=True)
        ```
    * PostgreSQL with PostGIS extension
        ```python
        engine = create_engine('postgresql://user:password@db_host/db_fold')
        ```
4. Usage:
   ```python
   engine = create_engine('postgresql://user:password@db_host/db_fold')
   
   fold = FoldDbGis(engine)
   fold.create_table()
   
   # to load fold file to empty db
   fold.load_from_csv(csv_file1)
   
   # to update db with fold file that do not overlap previously loaded data
   fold.load_from_csv(csv_file2)
   
   # to update db with fold file that overlaps with previously loaded data (i.e. two adjacent zippers)
   fold.update_from_csv(csv_file3)
   ```