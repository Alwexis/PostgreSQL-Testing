import psycopg2

class DB:
    connection = None

    def __init__(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                                            host="localhost",
                                            database="duoc",
                                            user="duoc_adm",
                                            password="123321")
                cur = self.connection.cursor()
                # Revisando si las tablas existen
                cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('profesor',))
                dbExists = cur.fetchone()
                # Si no existen, se crean
                if dbExists is False:
                    # Lista de Querys para creación de Tablas.
                    createData = ["""
                    CREATE TABLE IF NOT EXISTS public.especialidad (id integer NOT NULL,
                        nombre text COLLATE pg_catalog."default" NOT NULL,
                        descripcion text COLLATE pg_catalog."default" NOT NULL,
                        CONSTRAINT especialidad_pkey PRIMARY KEY (id))
                    TABLESPACE pg_default;""",
                    """
                    CREATE TABLE IF NOT EXISTS public.profesor(rut integer NOT NULL,
                        nombre text COLLATE pg_catalog."default" NOT NULL,
                        especialidad integer NOT NULL,
                        CONSTRAINT profesor_pkey PRIMARY KEY (rut),
                        CONSTRAINT fk_especialidad FOREIGN KEY (especialidad)
                            REFERENCES public.especialidad (id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION)
                    """]
                    # Ejecuto cada query
                    for query in createData:
                        cur.execute(query)
            except Exception as e:
                print(e)
                return

    def getConnection(self):
        return self.connection
    
    def insertTeacher(self, data):
        try:
            query = "INSERT INTO profesor(rut, nombre, especialidad) VALUES (%s, %s, %s)"
            self.connection.cursor().execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def insertSubject(self, data):
        try:
            query = "INSERT INTO especialidad(id, nombre, descripcion) VALUES (%s, %s, %s)"
            self.connection.cursor().execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    DB().insertSubject((1, 'Programación Movil', 'Programación Movil en Ionic, utilizando Angular y Firebase'))
    DB().insertTeacher((12345678, 'Alejandro Sepúlveda', 1))
    DB().insertSubject((2, 'Arquitectura', 'Arquitectura de Software'))
    DB().insertTeacher((87654321, 'Gonzalo Perez', 2))
