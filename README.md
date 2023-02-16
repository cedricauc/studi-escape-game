# Escape Game

Il est constitué de 3 parties à savoir : 
- une application web : reservations des séances
- une application mobile : lancement des parties
- une application desktop : surveillances des parties

Ce projet est un outil de reservation d'escape game. 

[lien de la version en ligne](https://cedricauc.alwaysdata.net/) 


Le projet web Escape Game consiste au développement d'une application python, 
une api REST et une base de donnée relationnelle pour permettre la réservation en ligne de séances d'Escape Game.
Les séances ainsi que les scénarios et la FAQ sont gérés depuis l'interface d’administration automatique de Django.

## Pré-requis

Pour l'application web : 
- [Python](https://www.python.org/downloads/) : back-end
- [bootstrap](https://getbootstrap.com/docs/5.2/getting-started/download/) : front
- [PostGreSQL 15](https://www.postgresql.org/download/) : SGBD


## Installation

- A la racine du projet, lancez les commandes 
```python
pip install virtualenv
python -m venv env
./env/Scripts/activate
pip install -r requirements.txt
```

## Utilisation

Commandes pour lancer le serveur Django
```python
python manage.py makemigrations 
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures.json
python manage.py runserver
```

Lancement de l'application en local.\
Ouvrir [http://localhost:8000](http://localhost:8000) pour afficher dans le navigateur.

Lancement de la console d'administration de l'application en local.\
Ouvrir [http://localhost:8000/admin](http://localhost:8000/admin) pour afficher dans le navigateur.

## Test du projet Python

Commandes pour lancer les tests
```python
pytest
```

Commandes pour lancer la couverture de test
```python
pytest --cov=.
```

## Transaction SQL

Ci-dessous une transaction SQL pour vérifier le traitement relatif aux objectifs précédemment fixés de manipulations des données:
- Liste toutes les parties qui n’ont pas été encore commencées pour une journée 
- Démarre une des parties 
- Attend 5 seconds 
- Arrête la partie 
- Récupère toutes les parties terminées pour une journée afin de vérifier la bonne présence de notre partie

```sql
do
$$
    <<outer_block>>
        declare
        booking_id       integer;
        start_datetime   varchar(50);
        end_datetime     varchar(50);
        selected_booking booking%rowtype;
    begin
        start_datetime := to_char(current_date, 'yyyy-mm-dd') || ' 00:00:00';
        end_datetime := to_char(current_date, 'yyyy-mm-dd') || ' 23:59:00';

        -- Créer une table temporaire pour la liste des parties
        DROP TABLE IF EXISTS temp_booking;
        CREATE TEMP TABLE temp_booking
        (
            id int
        )
            ON COMMIT DELETE ROWS;

        raise notice 'Liste toutes les parties qui n’ont pas été encore commencées pour une journée';

        -- Remplir la table temporaire
        INSERT INTO temp_booking
        SELECT b.id
        FROM booking as b
                 INNER JOIN game as g ON b.game_id = g.id
                 INNER JOIN scenario as s ON g.scenario_id = s.id
        WHERE g.start_time > TO_TIMESTAMP(start_datetime, 'YYYY-MM-DD HH24:MI:SS')
          AND g.end_time < TO_TIMESTAMP(end_datetime, 'YYYY-MM-DD HH24:MI:SS')
          AND in_progress = False
          AND is_complete = False;

        -- Récupérer le premier élément de la table temporaire
        booking_id := (SELECT id FROM temp_booking LIMIT 1);

        raise notice 'Démarre une des parties avec l''identifiant %', booking_id;

        -- Maj de la réservation
        UPDATE booking
        SET in_progress   = True,
            start_hour    = extract(hour from current_time),
            start_minutes = extract(minutes from current_time)
        WHERE id = booking_id;

        raise notice 'Commence le retard de l''execution : %', (SELECT clock_timestamp());

        PERFORM pg_sleep_for('5 seconds');

        raise notice 'Termine le retard de l''execution : %', (SELECT clock_timestamp());
        raise notice 'Arrête la partie avec l''identifiant %', booking_id;

        -- Maj de la réservation
        UPDATE booking
        SET in_progress = False,
            is_complete = True,
            end_hour    = extract(hours from current_time),
            end_minutes = extract(minutes from current_time)
        WHERE id = booking_id;

        -- Copie des parties terminées vers la table selected_booking
        SELECT b.id
        FROM booking as b
                 INNER JOIN game as g ON b.game_id = g.id
                 INNER JOIN scenario as s ON g.scenario_id = s.id
        WHERE g.start_time > TO_TIMESTAMP(start_datetime, 'YYYY-MM-DD HH24:MI:SS')
          AND g.end_time < TO_TIMESTAMP(end_datetime, 'YYYY-MM-DD HH24:MI:SS')
          AND in_progress = False
          AND is_complete = True
          AND b.id = booking_id
        INTO selected_booking;

        -- Vérifier que la partie précédemment modifiée est dans la liste
        if not found then
            raise notice 'La partie avec l''identifiant % n''a pas pu être trouvé', booking_id;
        else
            raise notice 'La partie avec l''identifiant % a correctement été récupéré depuis la liste des parties terminées pour la journée', booking_id;
        end if;

        DROP TABLE IF EXISTS temp_booking;

    end outer_block
$$;
```

## Visuel de l'application

**Page d'accueil**
![Page d'accueil](./img/home.png)

**Page d'un scénario**
![Page d'un scénario](./img/scenario.png)

**Page de réservation**
![Page de réservation](./img/booking.png)
