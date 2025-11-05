import time
from psycopg2 import OperationalError
from database import get_db_connection


def init_database():
    """Initialize the database with required tables"""
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            print("Attempting to connect to database...")
            conn = get_db_connection()
            cursor = conn.cursor()

            # Create districts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS districts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    population INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create municipalities table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS municipalities (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    district_id INTEGER NOT NULL,
                    population INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE CASCADE,
                    UNIQUE(name, district_id)
                )
            """
            )

            # Create parishes table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS parishes (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    municipality_id INTEGER NOT NULL,
                    population INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (municipality_id) REFERENCES municipalities(id) ON DELETE CASCADE,
                    UNIQUE(name, municipality_id)
                )
            """
            )

            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INTEGER NOT NULL CHECK (age >= 0),
                    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female', 'other')),
                    street VARCHAR(255) NOT NULL,
                    street_number VARCHAR(20) NOT NULL,
                    apartment VARCHAR(50),
                    postal_code VARCHAR(20) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    is_volunteer BOOLEAN DEFAULT FALSE,
                    is_assisted BOOLEAN DEFAULT FALSE,
                    has_organisation BOOLEAN DEFAULT FALSE,
                    organisation_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create organisation_allowed_municipalities junction table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS organisation_allowed_municipalities (
                    id SERIAL PRIMARY KEY,
                    organisation_id INTEGER NOT NULL,
                    municipality_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(organisation_id, municipality_id)
                )
            """
            )

            # Create organisation_allowed_parishes junction table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS organisation_allowed_parishes (
                    id SERIAL PRIMARY KEY,
                    organisation_id INTEGER NOT NULL,
                    parish_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(organisation_id, parish_id)
                )
            """
            )

            # Create organisations table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS organisations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    head_user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT NOT NULL,
                    date DATE NOT NULL,
                    organisation_id INTEGER,
                    interested_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE SET NULL
                )
            """
            )

            # Create event_interest table to track which users are interested in which events
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS event_interest (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    event_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                    UNIQUE(user_id, event_id)
                )
            """
            )

            # Add foreign key constraints
            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'users_organisation_id_fkey'
                    ) THEN
                        ALTER TABLE users 
                        ADD CONSTRAINT users_organisation_id_fkey 
                        FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE SET NULL;
                    END IF;
                END $$;
            """
            )

            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'organisations_head_user_id_fkey'
                    ) THEN
                        ALTER TABLE organisations 
                        ADD CONSTRAINT organisations_head_user_id_fkey 
                        FOREIGN KEY (head_user_id) REFERENCES users(id) ON DELETE RESTRICT;
                    END IF;
                END $$;
            """
            )

            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'org_allowed_municipalities_org_fkey'
                    ) THEN
                        ALTER TABLE organisation_allowed_municipalities 
                        ADD CONSTRAINT org_allowed_municipalities_org_fkey 
                        FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE CASCADE;
                    END IF;
                END $$;
            """
            )

            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'org_allowed_municipalities_mun_fkey'
                    ) THEN
                        ALTER TABLE organisation_allowed_municipalities 
                        ADD CONSTRAINT org_allowed_municipalities_mun_fkey 
                        FOREIGN KEY (municipality_id) REFERENCES municipalities(id) ON DELETE CASCADE;
                    END IF;
                END $$;
            """
            )

            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'org_allowed_parishes_org_fkey'
                    ) THEN
                        ALTER TABLE organisation_allowed_parishes 
                        ADD CONSTRAINT org_allowed_parishes_org_fkey 
                        FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE CASCADE;
                    END IF;
                END $$;
            """
            )

            cursor.execute(
                """
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'org_allowed_parishes_parish_fkey'
                    ) THEN
                        ALTER TABLE organisation_allowed_parishes 
                        ADD CONSTRAINT org_allowed_parishes_parish_fkey 
                        FOREIGN KEY (parish_id) REFERENCES parishes(id) ON DELETE CASCADE;
                    END IF;
                END $$;
            """
            )

            # Create indexes for better performance
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_events_date ON events(date)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_events_name ON events(name)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_events_organisation ON events(organisation_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_users_organisation ON users(organisation_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_event_interest_user ON event_interest(user_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_event_interest_event ON event_interest(event_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_municipalities_district ON municipalities(district_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_parishes_municipality ON parishes(municipality_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_org_allowed_mun_org ON organisation_allowed_municipalities(organisation_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_org_allowed_par_org ON organisation_allowed_parishes(organisation_id)
            """
            )

            # Insert initial data: District of Braga
            cursor.execute(
                """
                INSERT INTO districts (name, population, description)
                VALUES ('Braga', NULL, NULL)
                ON CONFLICT (name) DO NOTHING
            """
            )

            # Get district_id for Braga
            cursor.execute("SELECT id FROM districts WHERE name = 'Braga'")
            district_result = cursor.fetchone()
            if district_result:
                district_id = district_result[0]

                # Insert all municipalities of Braga district
                municipalities = [
                    'Celorico de Basto',
                    'Cabeceiras de Basto',
                    'Fafe',
                    'Guimarães',
                    'Póvoa de Lanhoso',
                    'Vieira do Minho',
                    'Vila Nova de Famalicão',
                    'Vizela',
                    'Amares',
                    'Barcelos',
                    'Braga',
                    'Esposende',
                    'Terras de Bouro',
                    'Vila Verde'
                ]

                for municipality in municipalities:
                    cursor.execute(
                        """
                        INSERT INTO municipalities (name, district_id, population, description)
                        VALUES (%s, %s, NULL, NULL)
                        ON CONFLICT (name, district_id) DO NOTHING
                        """,
                        (municipality, district_id)
                    )

                # Get municipality_id for Braga
                cursor.execute(
                    "SELECT id FROM municipalities WHERE name = 'Braga' AND district_id = %s",
                    (district_id,)
                )
                municipality_result = cursor.fetchone()
                if municipality_result:
                    municipality_id = municipality_result[0]

                    # Insert all parishes of Braga municipality
                    parishes = [
                        'Adaúfe',
                        'Arentim e Cunha',
                        'Braga (Maximinos, Sé e Cividade)',
                        'Braga (São José de São Lázaro e São João do Souto)',
                        'Braga (São Vicente)',
                        'Braga (São Vítor)',
                        'Cabreiros e Passos (São Julião)',
                        'Celeirós, Aveleda e Vimieiro',
                        'Crespos e Pousada',
                        'Escudeiros e Penso (Santo Estêvão e São Vicente)',
                        'Espinho',
                        'Esporões',
                        'Este (São Pedro e São Mamede)',
                        'Ferreiros e Gondizalves',
                        'Figueiredo',
                        'Gualtar',
                        'Guisande e Oliveira (São Pedro)',
                        'Lamas',
                        'Lomar e Arcos',
                        'Merelim (São Paio), Panóias e Parada de Tibães',
                        'Merelim (São Pedro) e Frossos',
                        'Mire de Tibães',
                        'Morreira e Trandeiras',
                        'Nogueira, Fraião e Lamaçães',
                        'Nogueiró e Tenões',
                        'Padim da Graça',
                        'Palmeira',
                        'Pedralva',
                        'Priscos',
                        'Real, Dume e Semelhe',
                        'Ruilhe',
                        'Santa Lucrécia de Algeriz e Navarra',
                        'Sequeira',
                        'Sobreposta',
                        'Tadim',
                        'Tebosa',
                        'Vilaça e Fradelos'
                    ]

                    for parish in parishes:
                        cursor.execute(
                            """
                            INSERT INTO parishes (name, municipality_id, population, description)
                            VALUES (%s, %s, NULL, NULL)
                            ON CONFLICT (name, municipality_id) DO NOTHING
                            """,
                            (parish, municipality_id)
                        )

            conn.commit()
            cursor.close()
            conn.close()

            print("Database initialized successfully!")
            return True

        except OperationalError as e:
            retry_count += 1
            print(
                f"Database connection failed (attempt {retry_count}/{max_retries}): {e}"
            )
            if retry_count < max_retries:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Failed to connect to database after multiple attempts")
                raise
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise


if __name__ == "__main__":
    init_database()
