import pandas as pd
# from django.contrib.auth.models import User
# from your_app.models import Category, Products

csv_file_path = 'D:\\WORK\\SCHOOL\\web\\files\\donnees-import - Feuille 1.csv'
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    # print(row['Date'])

    sql = "INSERT INTO temp_table VALUES (row['NumSeance'], row['Film'], row['Categorie'], row['Salle'], row['Date'], row['Heure'])"

    row = Temp_table(
        num_seance=row['NumSeance'],
        film=row['Film'],
        categorie=row['Categorie'],
        salle=row['Salle'],
        date=row['Date'],
        heure=row['Heure']
    )
    row.save()

