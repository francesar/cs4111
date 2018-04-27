Databases CS4111 Project 

Yulissa Arroyo-Paredes ya2340
Cesar Francisco Ibarra cfi2103

SQL Account: 
    hostname: 35.227.79.146
    Database Name: proj1part2
    SQL Account: cfi2103 

URL: http://35.190.176.72:7000/

3 Expanded Features 

1. Added TEXT attribute to Representative_Comments table (body attribute). This was added because apart from having comments about specific zipcodes, 
it is also important to give citizens the option to provide their opinions on the different representatives that work within their 
zipcode. This allows us to be able to extract information on a more granular level, since before we only had overall sentiment for a 
specific zipcode, which almost always is representated by different people.

2. Defined parse_body trigger. When inserting into the Representative_Comments table, we defined this trigger to automatically tokenize and populate 
the Tokens attribute of that table. Using the tokens, we set ourselves up to easily do more advanced natural language processing work based off of 
people's tokenized comments. The trigger itself runs before an insert or after an update, in each case, there is a possibility that a new/updated comment
is being inputed into the database, so we found it important that the token attribute of that table be updated to reflect the new value for the comment.
The trigger also checks to see whether or not the body field was populated before tokenizing the body. 

3.

Example Queries 

1. Gives us all comments that contain the word 'bad' in them

SELECT body 
FROM representative_comments 
WHERE tokens @@ to_tsquery('bad')


2. Trigger Definition 

    CREATE FUNCTION parse_body() RETURNS trigger AS $parse_body$
        BEGIN
            IF NEW.body IS NULL THEN
                RAISE EXCEPTION 'comment body cannot be null';
            END IF;
            NEW.tokens := to_tsvector(NEW.body);
            RETURN NEW;
        END;
    $parse_body$ LANGUAGE plpgsql;


    CREATE TRIGGER parse_body BEFORE INSERT OR UPDATE ON representative_comments
    FOR EACH ROW EXECUTE PROCEDURE parse_body();

3. 