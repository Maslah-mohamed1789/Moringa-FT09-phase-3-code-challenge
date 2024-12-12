from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

    def author(self):
        from models.author import Author  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        
        if author:
            return Author(author['id'], author['name'])
        return None

    def magazine(self):
        from models.magazine import Magazine  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        
        if magazine:
            return Magazine(magazine['id'], magazine['name'], magazine['category'])
        return None

    @classmethod
    def create_article(cls, title, content, author_id, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, author_id, magazine_id))
        conn.commit()
        conn.close()
        
        return cls(cursor.lastrowid, title, content, author_id, magazine_id)

    def update_article(self, title=None, content=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if title:
            cursor.execute('UPDATE articles SET title = ? WHERE id = ?', (title, self.id))
            self.title = title
        
        if content:
            cursor.execute('UPDATE articles SET content = ? WHERE id = ?', (content, self.id))
            self.content = content
        
        conn.commit()
        conn.close()

    def delete_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()