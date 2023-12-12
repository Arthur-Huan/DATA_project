from chirrup import database_setup, __database_path__

if __name__ == "__main__()":
    database_setup.initialize_database(__database_path__)
