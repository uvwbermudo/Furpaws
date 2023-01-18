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
    );

    CREATE TABLE IF NOT EXISTS jobs (
    job_id INT NOT NULL AUTO_INCREMENT,
    date_accepted DATETIME NULL,
    date_posted DATETIME NULL,
    date_finished DATETIME NULL,
    job_schedule DATETIME NOT NULL,
    job_status CHAR(20) NOT NULL, 
    job_type CHAR(20) NOT NULL,
    job_description TEXT NULL,
    job_rate DECIMAL(8,2),
    PRIMARY KEY(job_id)
    );

    CREATE TABLE IF NOT EXISTS posts_jobs (
    id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    pet_owner_tag VARCHAR(25) NOT NULL,
    date_posted DATETIME NOT NULL,
    job_status CHAR(20) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT post_job_users  FOREIGN KEY(pet_owner_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT post_job_jobs FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS applies_jobs (
    id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    freelancer_tag VARCHAR(25) NOT NULL,
    date_applied DATETIME,
    job_status CHAR(20) NOT NULL,
    application_status CHAR(20) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT apply_job_users FOREIGN KEY(freelancer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT apply_job_jobs FOREIGN KEY(job_id) REFERENCES jobs(job_id) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS works_on (
    id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    freelancer_tag VARCHAR(25),
    PRIMARY KEY(id),
    CONSTRAINT works_on_jobs FOREIGN KEY(job_id) REFERENCES jobs(job_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT works_on_users FOREIGN KEY(freelancer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reviews (
    id INT NOT NULL AUTO_INCREMENT,
    reference_job INT NULL,
    message TEXT NULL,
    reviewer_tag VARCHAR(25),
    reviewee_tag VARCHAR(25),
    stars CHAR(5),
    PRIMARY KEY(id),
    CONSTRAINT reviews_petowner FOREIGN KEY(reviewer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT reviews_freelancer FOREIGN KEY(reviewee_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT reviews_jobs FOREIGN KEY(reference_job) REFERENCES jobs(job_id) ON UPDATE CASCADE ON DELETE SET NULL
    );


    CREATE TABLE IF NOT EXISTS freelancer_details (
    id INT NOT NULL AUTO_INCREMENT,
    bio TEXT NULL,
    average_rating DECIMAL(3,2),
    freelancer_tag VARCHAR(25) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT FLDetails_users FOREIGN KEY(freelancer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS job_requests (   
    id INT NOT NULL AUTO_INCREMENT,
    freelancer_tag VARCHAR(25),
    pet_owner_tag VARCHAR(25),
    reference_job INT,
    request_status VARCHAR(25),
    PRIMARY KEY(id),
    CONSTRAINT requests_user1 FOREIGN KEY(freelancer_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT requests_user2 FOREIGN KEY(pet_owner_tag) REFERENCES users(tag) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT requests_jobs FOREIGN KEY(reference_job) REFERENCES jobs(job_id) ON UPDATE CASCADE ON DELETE CASCADE
    );	

    

    
    """)
