
CREATE TABLE articles
(
  id       INT          NOT NULL AUTO_INCREMENT,
  title    VARCHAR(50)  NULL    ,
  content  VARCHAR(500) NULL    ,
  catagory VARCHAR(25)  NULL    ,
  user_id  INT          NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE catagories
(
  id            INT         NOT NULL AUTO_INCREMENT,
  catagory_name VARCHAR(50) NULL    ,
  article_id    INT         NOT NULL,
  PRIMARY KEY (id)
) COMMENT 'OPTIONAL';

CREATE TABLE favorites
(
  id         INT NOT NULL AUTO_INCREMENT,
  user_id    INT NOT NULL,
  article_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE users
(
  id         INT          NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(500) NULL    ,
  last_name  VARCHAR(500) NULL    ,
  email      VARCHAR(500) NULL    ,
  password   VARCHAR(500) NULL    ,
  PRIMARY KEY (id)
);

ALTER TABLE articles
  ADD CONSTRAINT FK_users_TO_articles
    FOREIGN KEY (user_id)
    REFERENCES users (id);

ALTER TABLE favorites
  ADD CONSTRAINT FK_users_TO_favorites
    FOREIGN KEY (user_id)
    REFERENCES users (id);

ALTER TABLE favorites
  ADD CONSTRAINT FK_articles_TO_favorites
    FOREIGN KEY (article_id)
    REFERENCES articles (id)
    ON DELETE CASCADE;