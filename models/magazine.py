from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def articles(self):
        from models.article import Article  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        
        if not articles:
            return []
        
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def contributors(self):
        from models.author import Author 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        
        if not authors:
            return []
        
        return [Author(author['id'], author['name']) for author in authors]

    # CRUD operations for Magazine

    @classmethod
    def create_magazine(cls, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        ''', (name, category))
        conn.commit()
        conn.close()
        
        return cls(cursor.lastrowid, name, category)

    def update_magazine(self, name=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if name:
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (name, self.id))
            self.name = name
        
        if category:
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (category, self.id))
            self.category = category
        
        conn.commit()
        conn.close()

    def delete_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM magazines WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()