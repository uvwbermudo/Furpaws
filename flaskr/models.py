import datetime
from flaskr import mysql
from flask_login import UserMixin
import datetime


#ZIPS CURSOR.FETCHALL() SO WE CAN INDEX IT LIKE A DICTIONARY
def result_zip(cursor):
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    result = []
    for row in rows:
        row = dict(zip(columns,row))
        result.append(row)
    if result:
        return result
    return []

# FOR ALL TRANSACTIONS, COMMIT MUST NOT BE CALLED IN HERE TO ALLOW THE USE OF ROLLBACK
# IN THE BACKEND DURING ERRORS
class Users(UserMixin):
    def __init__(self, tag=None, email=None, password=None, account_type=None, first_name=None,
                last_name=None, city=None, state=None, zipcode=None, country=None):
        self.tag = tag
        self.email = email
        self.password = password
        self.account_type = account_type
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
    
    @classmethod 
    def convert_to_object(cls,rows):
        if not rows:
            return []
        object_results = []
        for row in rows:
            new_obj = Users(
                tag=row['tag'], 
                email=row['email'],
                password=row['user_password'],
                account_type=row['account_type'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                city=row['city'],
                state=row['state'],
                zipcode=row['zipcode'],
                country=row['country'],
                )
            object_results.append(new_obj)
        return object_results

    def add(self):                                  #must first create a user object then use add
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO users(email, tag, user_password, account_type, first_name,\
                last_name, city, state, zipcode, country) VALUES('{self.email}', '{self.tag}',\
                '{self.password}', '{self.account_type}','{ self.first_name}', '{self.last_name}', '{self.city}',\
                '{self.state}', '{self.zipcode}', '{self.country}')" 
        cursor.execute(sql)

    @classmethod
    def query_get(cls, tag):                   #takes a tag, returns a user object
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM users where tag = '{tag}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = Users.convert_to_object(result)
            return result[0]
        return []

    # query with filter, use True exact match for exact match duh 
    # RETURNS A LIST OF ROWS SO IT NEEDS TO BE INDEXED
    def query_filter(email=None, name=None, exact_match=False, username=None, tag=None): 
        cursor = mysql.connection.cursor()
        sql = ''
        if exact_match:
            if email:
                sql = f"SELECT * FROM USERS WHERE email='{email}'"
            if tag:
                sql = f"SELECT * FROM USERS WHERE tag='{tag}'"
        else:
            if email:
                sql = f"SELECT * FROM USERS WHERE email LIKE '%{email}%'"
            if tag:
                sql = f"SELECT * FROM USERS WHERE tag LIKE '%{tag}%'"
        if name:
            sql = f"SELECT * FROM USERS WHERE MATCH(first_name,last_name,tag,email) AGAINST('{name}')"
        if username:
            sql = f"SELECT * FROM USERS WHERE email='{username}' or tag='{username}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Users.convert_to_object(result)
        if username:
            return result[0]
        return result

    #to update user, just call Users.update_user(<params here>)
    @classmethod
    def update_user(cls, target_tag, new_tag=None, new_email=None, new_password=None, new_account_type=None, 
                    new_first_name=None, new_last_name=None, new_city=None, new_state=None, new_zipcode=None, 
                    new_country=None):
        cursor=mysql.connection.cursor()
        if new_tag:
            sql=f"UPDATE users SET tag = '{new_tag}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_email:
            sql=f"UPDATE users SET email = '{new_email}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_password:
            sql=f"UPDATE users SET user_password = '{new_password}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_account_type:
            sql=f"UPDATE users SET account_type = '{new_account_type}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_first_name:
            sql=f"UPDATE users SET first_name = '{new_first_name}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_last_name:
            sql=f"UPDATE users SET last_name = '{new_last_name}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_city:
            sql=f"UPDATE users SET city = '{new_city}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_state:
            sql=f"UPDATE users SET state = '{new_state}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_zipcode:
            sql=f"UPDATE users SET zipcode = '{new_zipcode}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_country:
            sql=f"UPDATE users SET country = '{new_country}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
    
    #pass only the target_tag
    @classmethod
    def delete(cls, target_tag):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM users WHERE TAG = '{target_tag}';"
        cursor.execute(sql)
    
    # for user mixin, DON'T TOUCH!
    def get_id(self):
        return self.tag

    @property
    def posts(self):
        posts = Posts.query_filter(author_tag=self.tag)
        return posts
    

class Posts:

    def __init__(self, author_tag=None, post_content=None, date_posted=None, post_id=None):
        self.author_tag = author_tag
        self.post_content = post_content
        self.post_id = post_id
        if date_posted is None:
            self.date_posted = datetime.datetime.now()
        else:
            self.date_posted = date_posted
    
    @classmethod
    def update_post(cls, target_post, post_content):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE posts SET post_content ='{post_content}' WHERE post_id='{target_post}'"
        cursor.execute(sql)


    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO posts(author_tag, post_content, date_posted)\
                VALUES('{self.author_tag}', '{self.post_content}','{self.date_posted}')" 
        cursor.execute(sql)

    @classmethod 
    def convert_to_object(cls,rows):
        if not rows:
            return []
        object_results = []
        for row in rows:
            new_obj = Posts(
                author_tag=row['author_tag'],
                post_id=row['post_id'],
                post_content=row['post_content'],
                date_posted=row['date_posted']
                )
            object_results.append(new_obj)
        return object_results

    @classmethod
    def delete(cls, post_id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM posts WHERE post_id='{post_id}';" 
        cursor.execute(sql)

    @classmethod
    def query_get(cls, post_id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM posts where post_id = '{post_id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = Posts.convert_to_object(result)
            return result[0]
        return []

    #ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, all=False,post_content=None, author_tag=None, order_by='date_posted', order='DESC'):
        cursor = mysql.connection.cursor()
        sql=''
        if post_content:
            sql = f"SELECT * FROM posts where post_content LIKE '%{post_content}%'"
        if author_tag:
            sql = f"SELECT * FROM posts where author_tag LIKE '%{author_tag}%'"
        order = f" ORDER BY {order_by} {order};"
        if all:
            sql = f"SELECT * FROM posts"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Posts.convert_to_object(result)
        return result

    @classmethod
    def last_inserted(cls):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM posts WHERE post_id = LAST_INSERT_ID()"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Posts.convert_to_object(result)
        if result:
            return result[0]
        return result

    @property
    def author(self):
        author = Users.query_get(self.author_tag)
        return author
    
    @property
    def photos(self):
        photos = Photos.query_filter(parent_post=self.post_id)
        return photos
    
    @property
    def videos(self):
        videos = Videos.query_filter(parent_post=self.post_id)
        return videos


        

        
class CreatePost:

    def __init__(self, id=None, author_tag=None, post_id=None, date_created=None):
        self.id = id
        self.author_tag = author_tag
        self.post_id = post_id
        if date_created is None:
            self.date_created = datetime.datetime.now()
        else:
            self.date_created = date_created

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO create_post(author_tag, post_id, date_created)\
                VALUES('{self.author_tag}', '{self.post_id}','{self.date_created}')" 
        cursor.execute(sql)
    
    #ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, author_tag=None, post_id=None, order_by='date_created', order='DESC'):
        cursor = mysql.connection.cursor()
        sql=''
        if author_tag:
            sql=f"SELECT * FROM create_post where author_tag='{author_tag}'"
        if post_id:
            sql=f"SELECT * FROM create_post where post_id='{post_id}'"
        order = f" ORDER BY {order_by} {order};"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = CreatePost.convert_to_object(result)
        return result

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = CreatePost(
                id=row['id'], 
                post_id=row['post_id'],
                author_tag=row['author_tag'],
                date_created=row['date_created'],
                )
            object_results.append(new_obj)
        return object_results

    @property
    def author(self):
        author = Users.query_get(self.author_tag)
        return author

    @property
    def post(self):
        post = Posts.query_get(self.post_id)
        return post


class Photos:

    def __init__(self, photo_id=None, parent_post=None, photo_url=None):
        self.photo_id = photo_id
        self.parent_post = parent_post
        self.photo_url = photo_url
    
    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO photos(parent_post, photo_url)\
                VALUES('{self.parent_post}','{self.photo_url}')" 
        cursor.execute(sql)

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = Photos(
                photo_id=row['photo_id'], 
                parent_post=row['parent_post'],
                photo_url=row['photo_url'],
                )
            object_results.append(new_obj)
        return object_results


    @classmethod
    def query_get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM photos WHERE photo_id = '{id}'" 
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Photos.convert_to_object(result)
        if result:
            return result[0]
        return result

    @classmethod
    def query_filter(cls, photo_id=None, parent_post=None):
        cursor = mysql.connection.cursor()
        sql=''
        if photo_id:
            sql=f"SELECT * FROM photos WHERE photo_id='{photo_id}'"
        if parent_post:
            sql=f"SELECT * FROM photos WHERE parent_post='{parent_post}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Photos.convert_to_object(result)
        return result
    
    @property
    def post(self):
        post = Posts.query_get(self.parent_post)
        return post
    

class Videos:

    def __init__(self, video_id=None, parent_post=None, video_url=None):
        self.video_id = video_id
        self.parent_post = parent_post
        self.video_url = video_url
    
    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO videos(parent_post, video_url)\
                VALUES('{self.parent_post}','{self.video_url}')" 
        cursor.execute(sql)

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = Videos(
                video_id=row['video_id'], 
                parent_post=row['parent_post'],
                video_url=row['video_url'],
                )
            object_results.append(new_obj)
        return object_results


    @classmethod
    def query_get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM videos WHERE video_id = '{id}'" 
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Videos.convert_to_object(result)
        if result:
            return result[0]
        return result

    @classmethod
    def query_filter(cls, video_id=None, parent_post=None):
        cursor = mysql.connection.cursor()
        sql=''
        if video_id:
            sql=f"SELECT * FROM videos WHERE video_id='{video_id}'"
        if parent_post:
            sql=f"SELECT * FROM videos WHERE parent_post='{parent_post}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Videos.convert_to_object(result)
        return result

    @property
    def post(self):
        post = Posts.query_get(self.parent_post)
        return post
    
