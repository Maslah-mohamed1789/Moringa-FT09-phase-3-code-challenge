from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        from models.article import Article  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        
        if not articles:
            return []
        
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def magazines(self):
        from models.magazine import Magazine  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        
        if not magazines:
            return []
        
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]

    @classmethod
    def create_author(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO authors (name)
            VALUES (?)
        ''', (name,))
        conn.commit()
        conn.close()
        
        return cls(cursor.lastrowid, name)

    def update_author(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (name, self.id))
        self.name = name
        conn.commit()
        conn.close()

    def delete_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authors WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()