from config import DB_HOST, DB_PASSWORD, DB_USERNAME, DB_NAME
import mysql.connector

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD
)

cursor = db.cursor()


def create_db():
    cursor.execute(f"""
    CREATE DATABASE IF NOT EXISTS {DB_NAME};
    USE {DB_NAME};

    CREATE TABLE IF NOT EXISTS users (
	tag VARCHAR(25) NOT NULL,
	email VARCHAR(150) NULL DEFAULT NULL,
	user_password VARCHAR(150) NOT NULL,
	account_type VARCHAR(20) NOT NULL,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	city VARCHAR(50) NOT NULL,
	state VARCHAR(50) NOT NULL,
	zipcode VARCHAR(50) NOT NULL,
	country VARCHAR(50) NOT NULL,
	PRIMARY KEY (tag),
	UNIQUE(email),
	FULLTEXT(first_name,last_name,tag,email)
    );

    CREATE TABLE IF NOT EXISTS posts (
        author_tag VARCHAR(25) NOT NULL,
        post_id INT NOT NULL AUTO_INCREMENT,
        post_content TEXT,
        date_posted DATETIME NOT NULL,
        PRIMARY KEY (post_id) ,
        CONSTRAINT `posts_ibfk_1` FOREIGN KEY (author_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
        FULLTEXT(post_content)
    );

    CREATE TABLE IF NOT EXISTS create_post (
        id INT NOT NULL AUTO_INCREMENT,
        author_tag VARCHAR(25) NOT NULL,
        post_id INT NOT NULL,
        date_created DATETIME NOT NULL,
        PRIMARY KEY (id) ,
        CONSTRAINT `create_post_ibfk_1` FOREIGN KEY(author_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT `create_post_ibfk_2` FOREIGN KEY(post_id) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS share_post (
        reference_id INT AUTO_INCREMENT,
        sharer_tag VARCHAR(25) NOT NULL,
        shared_post_id INT NOT NULL,
        date_created DATETIME NOT NULL,
        PRIMARY KEY (reference_id) ,
        CONSTRAINT `share_post_ibfk_1` FOREIGN KEY(sharer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT `share_post_ibfk_2` FOREIGN KEY(shared_post_id) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS photos (
        photo_id INT NOT NULL AUTO_INCREMENT,
        parent_post INT NULL DEFAULT NULL,
        photo_url VARCHAR(150) NULL DEFAULT NULL,
        PRIMARY KEY (photo_id),
        CONSTRAINT `photos_ibfk_1` FOREIGN KEY (parent_post) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS videos (
        video_id INT NOT NULL AUTO_INCREMENT,
        parent_post INT NULL DEFAULT NULL,
        video_url VARCHAR(150) NULL DEFAULT NULL,
        PRIMARY KEY (video_id),
        CONSTRAINT `videos_ibfk_1` FOREIGN KEY (parent_post) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
        CREATE TABLE IF NOT EXISTS comments (
        comment_id INT NOT NULL AUTO_INCREMENT,
        author_tag VARCHAR(25) NOT NULL,
        post_commented INT NOT NULL,
        comment_content TEXT,
        date_commented DATETIME NOT NULL,
        PRIMARY KEY (comment_id) ,
        CONSTRAINT `comments_ibfk_1` FOREIGN KEY(author_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT `comments_ibfk_2` FOREIGN KEY(post_commented) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );
        CREATE TABLE IF NOT EXISTS likes (
        id INT NOT NULL AUTO_INCREMENT,
        author_tag VARCHAR(25) NOT NULL,
        post_liked INT NOT NULL,
        date_liked DATETIME NOT NULL,
        PRIMARY KEY (id) ,
        CONSTRAINT `likes_ibfk_1` FOREIGN KEY(author_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT `likes_ibfk_2` FOREIGN KEY(post_liked) REFERENCES posts(post_id) ON UPDATE CASCADE ON DELETE CASCADE
    );""")
