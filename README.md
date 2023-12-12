# DATA_project

## Dependencies

To set up the required dependencies for this Python project, use `python -m pip install -r requirements.txt`. Alternatively, if you're using pypoetry, use `poetry update`.

## Usage 

To run Chirrup CLI, execute the following command in your terminal or command prompt:

- If using Ppython: `python -m chirrup menu`
- If using Poetry: `poetry run python -m chirrup menu`

## Database initialization

As end users should not need to initalize the database, there is no command for it in the CLI. However, you can manually run `database_setup.py` in the `chirrup` sub-directory. Alternatively, use the CLI as usual, and a databsae will be initalized for you.
