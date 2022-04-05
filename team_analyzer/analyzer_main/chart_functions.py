def league_df_todb(output_df):
    from sqlalchemy import create_engine
    from django.conf import settings
    import os

    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']

    db_type = settings.DB_TYPE

    database_url = 'postgresql+psycopg2://{user}:{password}@{db_type}:5432/{database_name}'.format(
        user=user,
        password=password,
        db_type=db_type,
        database_name=database_name,
    )

    engine = create_engine(database_url, echo=False)
    output_df.to_sql('league_output', con=engine, if_exists='append', index=False)

def leaguetotals_df_todb(output_df):
    from sqlalchemy import create_engine
    from django.conf import settings
    import os

    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']

    db_type = settings.DB_TYPE

    database_url = 'postgresql+psycopg2://{user}:{password}@{db_type}:5432/{database_name}'.format(
        user=user,
        password=password,
        db_type=db_type,
        database_name=database_name,
    )

    engine = create_engine(database_url, echo=False)
    output_df.to_sql('league_totalval_table', con=engine, if_exists='append', index=False)
