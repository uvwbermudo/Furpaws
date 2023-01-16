import datetime
from flaskr import mysql
from flask_login import UserMixin, current_user
import datetime


# ZIPS CURSOR.FETCHALL() SO WE CAN INDEX IT LIKE A DICTIONARY
def result_zip(cursor):
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    result = []
    for row in rows:
        row = dict(zip(columns, row))
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

    def __repr__(self):
        return f'User: {self.tag}, {self.email}'

    def __hash__(self):
        return hash(self.tag)

    def __eq__(self, other):
        if isinstance(other, Users):
            return self.tag == other.tag
        return False

    @classmethod
    def convert_to_object(cls, rows):
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

    def add(self):  # must first create a user object then use add
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO users(email, tag, user_password, account_type, first_name,\
                last_name, city, state, zipcode, country) VALUES('{self.email}', '{self.tag}',\
                '{self.password}', '{self.account_type}','{ self.first_name}', '{self.last_name}', '{self.city}',\
                '{self.state}', '{self.zipcode}', '{self.country}')"
        cursor.execute(sql)

    @classmethod
    def query_get(cls, tag):  # takes a tag, returns a user object
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
    @classmethod
    def query_filter(cls, email=None, name=None, exact_match=False, username=None, tag=None, account_type=None):
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
        if account_type:
            sql = sql + f" AND account_type = '{account_type}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Users.convert_to_object(result)
        if username:
            print(result, 'HI?')
        if result:
            return result[0]
        else:
            return []

    @classmethod
    def query_all(cls, account_type=None):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM users"
        if account_type:
            sql = sql + f" WHERE account_type = '{account_type}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Users.convert_to_object(result)
        return result

    # to update user, just call Users.update_user(<params here>)
    @classmethod
    def update_user(cls, target_tag, new_tag=None, new_email=None, new_password=None, new_account_type=None,
                    new_first_name=None, new_last_name=None, new_city=None, new_state=None, new_zipcode=None,
                    new_country=None):
        cursor = mysql.connection.cursor()
        if new_tag:
            sql = f"UPDATE users SET tag = '{new_tag}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_email:
            sql = f"UPDATE users SET email = '{new_email}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_password:
            sql = f"UPDATE users SET user_password = '{new_password}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_account_type:
            sql = f"UPDATE users SET account_type = '{new_account_type}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_first_name:
            sql = f"UPDATE users SET first_name = '{new_first_name}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_last_name:
            sql = f"UPDATE users SET last_name = '{new_last_name}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_city:
            sql = f"UPDATE users SET city = '{new_city}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_state:
            sql = f"UPDATE users SET state = '{new_state}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_zipcode:
            sql = f"UPDATE users SET zipcode = '{new_zipcode}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)
        if new_country:
            sql = f"UPDATE users SET country = '{new_country}' WHERE tag ='{target_tag}'"
            cursor.execute(sql)

    # pass only the target_tag
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

    @property
    def comments(self):
        comments = Comments.query_filter(author_tag=self.tag)
        return comments

    @property
    def likes(self):
        likes = Likes.query_filter(author_tag=self.tag)
        return likes


class Posts:

    def __init__(self, author_tag=None, post_content=None, date_posted=None, post_id=None):
        self.author_tag = author_tag
        self.post_content = post_content
        self.post_id = post_id
        if date_posted is None:
            self.date_posted = datetime.datetime.now()
        else:
            self.date_posted = date_posted

    def __repr__(self):
        return f'Post {self.post_id}, {self.author_tag}'

    def __hash__(self):
        return int(self.post_id)

    def __eq__(self, other):
        if isinstance(other, Posts):
            return self.post_id == other.post_id
        else:
            return False

    @classmethod
    def update_post(cls, target_post, post_content):
        cursor = mysql.connection.cursor()
        sql = f'UPDATE posts SET post_content ="{post_content}" WHERE post_id="{target_post}"'
        cursor.execute(sql)

    def add(self):
        cursor = mysql.connection.cursor()
        if not self.post_content:
            self.post_content = ''
        sql = None
        if self.post_content:
            sql = f'INSERT INTO posts(author_tag, post_content, date_posted)\
                    VALUES("{self.author_tag}", "{self.post_content}", "{self.date_posted}")'
        else:
            sql = f'INSERT INTO posts(author_tag, date_posted)\
                    VALUES("{self.author_tag}", "{self.date_posted}")'
        cursor.execute(sql)

    @classmethod
    def convert_to_object(cls, rows):
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

    # ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, all=False, post_id=None, post_content=None, author_tag=None, order_by='date_posted', order='DESC'):
        cursor = mysql.connection.cursor()
        sql = ''
        if post_content:
            sql = f"SELECT * FROM posts WHERE MATCH(post_content) AGAINST ('{post_content}')"
        if author_tag:
            sql = f"SELECT * FROM posts where author_tag LIKE '%{author_tag}%'"
        if post_id:
            sql = f"SELECT * FROM posts where post_id LIKE '%{post_id}%'"
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

    @property
    def comments(self):
        comments = Comments.query_filter(post_commented=self.post_id)
        return comments

    @property
    def likes(self):
        likes = Likes.query_filter(post_liked=self.post_id)
        return likes

    @property
    def shares(self):
        shares = SharePost.query_filter(shared_post_id=self.post_id)
        return shares


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

    # ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, author_tag=None, post_id=None, order_by='date_created', order='DESC'):
        cursor = mysql.connection.cursor()
        sql = ''
        if author_tag:
            sql = f"SELECT * FROM create_post where author_tag='{author_tag}'"
        if post_id:
            sql = f"SELECT * FROM create_post where post_id='{post_id}'"
        order = f" ORDER BY {order_by} {order};"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = CreatePost.convert_to_object(result)
        return result

    @classmethod
    def convert_to_object(cls, rows):
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


class SharePost:

    def __init__(self, reference_id=None, sharer_tag=None, shared_post_id=None, date_created=None):
        self.reference_id = reference_id
        self.sharer_tag = sharer_tag
        self.shared_post_id = shared_post_id
        if date_created is None:
            self.date_created = datetime.datetime.now()
        else:
            self.date_created = date_created

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO share_post(reference_id, sharer_tag, shared_post_id, date_created)\
                VALUES('{self.reference_id}','{self.sharer_tag}', '{self.shared_post_id}','{self.date_created}')"
        cursor.execute(sql)

    # ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, all=False, reference_id=None, sharer_tag=None, shared_post_id=None, order_by='date_created', order='DESC'):
        cursor = mysql.connection.cursor()
        sql = ''
        if sharer_tag:
            sql = f"SELECT * FROM share_post where sharer_tag='{sharer_tag}'"
        if shared_post_id:
            sql = f"SELECT * FROM share_post where shared_post_id='{shared_post_id}'"
        if reference_id:
            sql = f"SELECT * FROM share_post where reference_id='{reference_id}'"
        order = f" ORDER BY {order_by} {order};"
        if all:
            sql = f"SELECT * FROM share_post"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = SharePost.convert_to_object(result)
        return result

    @classmethod
    def query_get(cls, shared_post_id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM share_post WHERE shared_post_id = '{shared_post_id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = SharePost.convert_to_object(result)
        if result:
            return result[0]
        return result

    @classmethod
    def convert_to_object(cls, rows):
        object_results = []
        for row in rows:
            new_obj = SharePost(
                reference_id=row['reference_id'],
                shared_post_id=row['shared_post_id'],
                sharer_tag=row['sharer_tag'],
                date_created=row['date_created']
            )
            object_results.append(new_obj)
        return object_results

    @property
    def sharer(self):
        author = Users.query_get(self.sharer_tag)
        return author

    @property
    def post(self):
        post = Posts.query_get(self.shared_post_id)
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
    def convert_to_object(cls, rows):
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
    def delete(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM photos WHERE photo_id = '{id}'"
        cursor.execute(sql)

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
        sql = ''
        if photo_id:
            sql = f"SELECT * FROM photos WHERE photo_id='{photo_id}'"
        if parent_post:
            sql = f"SELECT * FROM photos WHERE parent_post='{parent_post}'"
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
    def convert_to_object(cls, rows):
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
        sql = ''
        if video_id:
            sql = f"SELECT * FROM videos WHERE video_id='{video_id}'"
        if parent_post:
            sql = f"SELECT * FROM videos WHERE parent_post='{parent_post}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Videos.convert_to_object(result)
        return result

    @property
    def post(self):
        post = Posts.query_get(self.parent_post)
        return post

    @classmethod
    def delete(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM videos WHERE video_id = '{id}'"
        cursor.execute(sql)
class Comments:

    def __init__(self, comment_id=None, comment_content=None, post_commented=None, author_tag=None, date_commented=None):
        self.comment_id = comment_id
        self.post_commented = post_commented
        self.comment_content = comment_content
        self.author_tag = author_tag
        if date_commented is None:
            self.date_commented = datetime.datetime.now()
        else:
            self.date_commented = date_commented

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f'INSERT INTO comments(post_commented, author_tag, date_commented, comment_content)\
                VALUES("{self.post_commented}","{self.author_tag}", "{self.date_commented}", "{self.comment_content}")'
        cursor.execute(sql)

    @classmethod
    def convert_to_object(cls, rows):
        object_results = []
        for row in rows:
            new_obj = Comments(
                comment_id=row['comment_id'],
                post_commented=row['post_commented'],
                comment_content=row['comment_content'],
                author_tag=row['author_tag'],
                date_commented=row['date_commented']
            )
            object_results.append(new_obj)
        return object_results

    @classmethod
    def update_comment(cls, target_comment, comment_content):
        cursor = mysql.connection.cursor()
        sql = f'UPDATE comments SET comment_content ="{comment_content}" WHERE comment_id="{target_comment}"'
        cursor.execute(sql)

    @classmethod
    def query_get(cls, comment_id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM comments WHERE comment_id = '{comment_id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Comments.convert_to_object(result)
        if result:
            return result[0]
        return result

    @classmethod
    def delete(cls, comment_id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM comments WHERE comment_id='{comment_id}';"
        cursor.execute(sql)

    @classmethod
    def query_filter(cls, comment_id=None, post_commented=None, author_tag=None, comment_content=None):
        cursor = mysql.connection.cursor()
        sql = ''
        if comment_id:
            sql = f'SELECT * FROM comments WHERE comment_id="{comment_id}"'
        if post_commented:
            sql = f'SELECT * FROM comments WHERE post_commented="{post_commented}"'
        if author_tag:
            sql = f'SELECT * FROM comments WHERE author_tag="{author_tag}"'
        if comment_content:
            sql = f'SELECT * FROM comments WHERE comment_content="{comment_content}"'
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Comments.convert_to_object(result)
        return result

    @property
    def post(self):
        post = Posts.query_get(self.post_commented)
        return post


class Likes:
    def __init__(self, id=None, post_liked=None, author_tag=None, date_liked=None):
        self.id = id
        self.post_liked = post_liked
        self.author_tag = author_tag
        if date_liked is None:
            self.date_liked = datetime.datetime.now()
        else:
            self.date_liked = date_liked

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f'INSERT INTO likes(post_liked, author_tag, date_liked)\
                VALUES("{self.post_liked}","{self.author_tag}", "{self.date_liked}")'
        cursor.execute(sql)

    @classmethod
    def convert_to_object(cls, rows):
        object_results = []
        for row in rows:
            new_obj = Likes(
                id=row['id'],
                post_liked=row['post_liked'],
                author_tag=row['author_tag'],
                date_liked=row['date_liked']
            )
            object_results.append(new_obj)
        return object_results

    @classmethod
    def query_get(cls, id=None, post_liked=None):
        cursor = mysql.connection.cursor()
        sql = ''
        if id:
            sql = f"SELECT * FROM likes WHERE id = '{id}'"
        if post_liked:
            sql = F"SELECT * FROM likes where post_liked = '{post_liked}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Likes.convert_to_object(result)
        if result:
            return result[0]
        return result

    @classmethod
    def delete(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM likes WHERE id ='{id}';"
        cursor.execute(sql)

    @classmethod
    def query_filter(cls, all=False, post_liked=None, author_tag=None, order_by='date_liked', order='DESC'):
        cursor = mysql.connection.cursor()
        sql = ''
        if post_liked:
            sql = f"SELECT * FROM likes where post_liked LIKE '%{post_liked}%'"
        if author_tag:
            sql = f"SELECT * FROM likes where author_tag LIKE '%{author_tag}%'"
        order = f" ORDER BY {order_by} {order};"
        if all:
            sql = f"SELECT * FROM likes"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Likes.convert_to_object(result)
        return result

    @property
    def post(self):
        post = Likes.query_get(self.post_liked)
        return post


class Jobs:

    def __init__(self, job_id=None, date_accepted=None, date_posted=None, date_finished=None,
                 job_status=None, job_type=None, job_description=None, job_rate=None, job_schedule=None):
        self.job_id = job_id
        self.date_accepted = date_accepted
        self.date_posted = date_posted
        self.date_finished = date_finished
        self.job_status = job_status
        self.job_type = job_type
        self.job_description = job_description
        self.job_rate = job_rate
        self.job_schedule = job_schedule
    
    def __repr__(self):
        return f'Job: {self.job_id}'

    def add(self):
        cursor = mysql.connection.cursor()
        cursor.execute("START TRANSACTION")
        sql = f"""
                INSERT INTO jobs(job_id, date_accepted ,date_posted,date_finished, job_status, job_type, 
                job_description, job_schedule, job_rate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        values = (self.job_id, self.date_accepted, self.date_posted, self.date_finished, 
                self.job_status, self.job_type, self.job_description, self.job_schedule, self.job_rate)
        cursor.execute(sql,values)
        cursor.execute("SELECT LAST_INSERT_ID()")
        self.job_id = cursor.fetchone()[0]
        self.add_creates_jobs()
    
    def add_creates_jobs(self):
        new_create= CreateJobs(pet_owner_tag=current_user.tag,job_id=self.job_id, 
                            date_posted=self.date_posted, job_status=self.job_status)
        new_create.add()
    
    @classmethod
    def query_get(cls, job_id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM jobs where job_id = '{job_id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = Jobs.convert_to_object(result)
            return result[0]
        return []

    @classmethod
    def query_filter(cls, all=False,  job_status=None, order_by='date_posted', order='DESC'):
        cursor = mysql.connection.cursor()
        sql=''
        if job_status:
            sql = f"SELECT * FROM jobs WHERE job_status='{job_status}'"
        if all:
            sql = f"SELECT * FROM jobs"
        order = f" ORDER BY {order_by} {order};"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = Jobs.convert_to_object(result)
        return result

    @classmethod 
    def convert_to_object(cls,rows):
        if not rows:
            return []
        object_results = []
        
        for row in rows:
            new_obj = Jobs(
                job_id=row['job_id'],
                date_posted=row['date_posted'],
                date_accepted=row['date_accepted'],
                date_finished=row['date_finished'],
                job_status=row['job_status'],
                job_type=row['job_type'],
                job_description=row['job_description'],
                job_rate=row['job_rate'],
                job_schedule=row['job_schedule'],
                )
            object_results.append(new_obj)
        return object_results

    @property
    def poster_details(self):
        job = CreateJobs.query_filter(job_id=self.job_id)
        poster = Users.query_get(job.pet_owner_tag)
        return poster

    @property
    def applicants(self):
        job = ApplyJobs.query_filter(job_id=self.job_id, application_status='Sent')
        applicant_list = []
        for applications in job:
            applicant_list.append(applications.applicant_details)
        return applicant_list

    @property
    def worker_details(self):
        job = WorksOn.query_filter(job_id=self.job_id)
        if job:
            worker = Users.query_get(job.freelancer_tag)
            return worker
        return False

    @classmethod
    def update_status(cls, new_status=None, job_id=None):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE jobs SET job_status ='{new_status}' where job_id = '{job_id}';"
        cursor.execute(sql)
        sql = f"UPDATE posts_jobs SET job_status ='{new_status}' where job_id = '{job_id}';"
        cursor.execute(sql)
        sql = f"UPDATE applies_jobs SET job_status ='{new_status}' where job_id = '{job_id}';"
        cursor.execute(sql)

    @classmethod
    def update_accept(cls, accepted_datetime=None, job_id=None):
        cursor = mysql.connection.cursor()
        sql = f"""
            UPDATE jobs SET date_accepted ='{accepted_datetime}' where job_id = '{job_id}';
            """
        cursor.execute(sql)

    @classmethod
    def update_post(cls, target_post, post_content):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE posts SET post_content ='{post_content}' WHERE post_id='{target_post}'"
        cursor.execute(sql)


    @classmethod
    def delete(cls, post_id):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM posts WHERE post_id='{post_id}';" 
        cursor.execute(sql)


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


class CreateJobs:

    def __init__(self, id=None, pet_owner_tag=None, job_id=None, date_posted=None, job_status=None):
        self.id = id
        self.pet_owner_tag = pet_owner_tag
        self.job_id = job_id
        self.date_posted = date_posted
        self.job_status = job_status

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"""
                INSERT INTO posts_jobs(id, job_id, pet_owner_tag, date_posted, job_status) 
                VALUES(%s,%s,%s,%s,%s)
               """
        values = (self.id, self.job_id, self.pet_owner_tag, self.date_posted, self.job_status)
        cursor.execute(sql, values)
    
    #ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, ongoing=False, pet_owner=None, all=False, job_id=None,order_by='date_posted', order='ASC'):
        cursor = mysql.connection.cursor()
        sql=''
        if pet_owner:
            sql= f"SELECT * FROM posts_jobs where pet_owner_tag='{pet_owner}'"
        if job_id:
            sql= f"SELECT * FROM posts_jobs where job_id='{job_id}'"
        if all:
            sql= f"SELECT * FROM posts_jobs"

            
        order = f" ORDER BY {order_by} {order};"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = CreateJobs.convert_to_object(result)
        if job_id:
            return result[0]
        return result

    @classmethod
    def query_get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM posts_jobs where id = '{id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = CreateJobs.convert_to_object(result)
            return result[0]
        return []

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = CreateJobs(
                id=row['id'], 
                pet_owner_tag=row['pet_owner_tag'],
                job_id=row['job_id'],
                date_posted=row['date_posted'],
                job_status=row['job_status'],
                )
            object_results.append(new_obj)
        return object_results

    @property
    def job_details(self):
        job = Jobs.query_get(self.job_id)
        return job

    @property
    def poster_details(self):
        poster = Users.query_get(self.pet_owner_tag)
        return poster

class WorksOn:
    
    def __init__(self, id=None, freelancer_tag=None, job_id=None):
        self.id = id
        self.freelancer_tag = freelancer_tag
        self.job_id = job_id 
    
    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"""
                INSERT INTO works_on(id, job_id, freelancer_tag) VALUES(%s,%s,%s)
               """
        values = (self.id, self.job_id, self.freelancer_tag)
        cursor.execute(sql, values)

    @classmethod
    def query_get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM works_on where id = '{id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = WorksOn.convert_to_object(result)
            return result[0]
        return []

    @classmethod
    def query_filter(cls, freelancer=None, all=False, job_id=None):
        cursor = mysql.connection.cursor()
        sql=''
        if freelancer:
            sql= f"SELECT * FROM works_on where freelancer_tag='{freelancer}'"
        if all:
            sql= f"SELECT * FROM works_on"
        if job_id:
            sql= f"SELECT * FROM works_on where job_id ='{job_id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        result = WorksOn.convert_to_object(result)
        if job_id and result:
            return result[0]
        return result

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = WorksOn(
                id=row['id'], 
                freelancer_tag=row['freelancer_tag'],
                job_id=row['job_id'],
                )
            object_results.append(new_obj)
        return object_results

    @property
    def job_details(self):
        job = Jobs.query_get(self.job_id)
        return job


class ApplyJobs:

    def __init__(self, id=None, freelancer_tag=None, job_id=None, date_applied=None, job_status=None, application_status=None):
        self.id = id
        self.freelancer_tag = freelancer_tag
        self.job_id = job_id
        self.date_applied = date_applied
        self.job_status = job_status
        self.application_status = application_status

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"""
                INSERT INTO applies_jobs(id, job_id, freelancer_tag, date_applied, job_status, application_status) 
                VALUES(%s,%s,%s,%s,%s,%s)
               """
        values = (self.id, self.job_id, self.freelancer_tag, self.date_applied, self.job_status, self.application_status)
        cursor.execute(sql, values)

    #ORDER_BY IS THE COLUMN IN THE DATABASE, ORDER SHOULD BE EITHER 'DESC' or 'ASC'
    @classmethod
    def query_filter(cls, freelancer=None, all=False, job_id=None, application_status=None, order_by='date_applied', order='ASC'):
        cursor = mysql.connection.cursor()
        sql=''
        if freelancer:
            sql= f"SELECT * FROM applies_jobs where freelancer_tag='{freelancer}'"
        if all:
            sql= f"SELECT * FROM applies_jobs"
        if job_id:
            sql= f"SELECT * FROM applies_jobs where job_id ='{job_id}'"

        if application_status and freelancer:
                sql= f"SELECT * FROM applies_jobs where freelancer_tag ='{freelancer}' and application_status ='{application_status}'"

        order = f" ORDER BY {order_by} {order};"
        sql = sql+order
        cursor.execute(sql)
        result = result_zip(cursor)
        result = ApplyJobs.convert_to_object(result)
        return result

    @classmethod
    def set_hired(cls, job_id=None, freelancer_tag=None):
        cursor= mysql.connection.cursor()
        sql = f"""
            UPDATE applies_jobs SET application_status='Hired' where job_id = '{job_id}' AND 
            freelancer_tag = '{freelancer_tag}'
            """
        cursor.execute(sql)
        sql = f"""
            UPDATE applies_jobs SET application_status='Unavailable' where job_id = '{job_id}' AND 
            freelancer_tag != '{freelancer_tag}'
            """
        cursor.execute(sql)

    @classmethod
    def update_application_status(cls, job_id=None, freelancer_tag=None, status=None):
        cursor= mysql.connection.cursor()
        sql = f"""
            UPDATE applies_jobs SET application_status='{status}' where job_id = '{job_id}' AND 
            freelancer_tag = '{freelancer_tag}'
            """
        cursor.execute(sql)
    @classmethod
    def query_get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM applies_jobs where id = '{id}'"
        cursor.execute(sql)
        result = result_zip(cursor)
        if result:
            result = ApplyJobs.convert_to_object(result)
            return result[0]
        return []

    @classmethod 
    def convert_to_object(cls,rows):
        object_results = []
        for row in rows:
            new_obj = ApplyJobs(
                id=row['id'], 
                freelancer_tag=row['freelancer_tag'],
                job_id=row['job_id'],
                date_applied=row['date_applied'],
                job_status=row['job_status'],
                application_status=row['application_status']
                )
            object_results.append(new_obj)
        return object_results

    @property
    def job_details(self):
        job = Jobs.query_get(self.job_id)
        return job

    @property
    def applicant_details(self):
        poster = Users.query_get(self.freelancer_tag)
        return poster


