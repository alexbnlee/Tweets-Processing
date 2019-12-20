### 01_txt2csv.py

- Function of calculating area of bounding box.

- Columns: `['id', 'created_at', 'coordinates', 'co_lon', 'co_lat', 'geo', 'geo_lat',
       'geo_lon', 'user_location', 'place_type', 'place_name',
       'place_full_name', 'place_country', 'place_bounding_box', 'pb_avg_lon',
       'pb_avg_lat', 'min_lon', 'min_lat', 'max_lon', 'max_lat', 'bb_area',
       'lang', 'source', 'text']`.
       
- `user->location`: replace `"\n"` into `" "`; replace `"\""` and `"\'"` into `""`. Since sometimes there exist commas, when saving text into csv, text should be wraped by double quotation marks.

- `text`: the same to `user->location`.

### 02_data_cleaning.py

- `df = df.drop_duplicates(["id"])`: delete duplicate tweets based on `"id"`.

- `df.dtypes`: get data types of all columns.

- `df = df.astype({"created_at":"datetime64[ns]"})`: change data type to datetime.

- `df['co_lon'] = df['co_lon'].astype(float)`: if all values of `'co_lon'` are numeric.

- `df.source.value_counts()`: get total number of every source.

- `df.coordinates.value_counts()`: get total number of tweets with goe-tags.

- `df = df[df['place_country'] == 'Australia']`: get tweets from Aus.

- `df = df[df['lang'] == 'en']`: get English tweets.

- `re.sub("[^a-zA-Z]", " ", name)`: change all the non-alphabet characters to single space.

- `re.sub(r"\s+", " ", name)`: eliminate duplicate whitespaces.

- Convert all the characters into lower case.

- Delete links like `https://github.com/alexbnlee/Tweets-Processing/edit/master/README.md`.

- Extract flu related tweets.

### 03_read_Gazetteer.py

- Get all results with name of Kingsford.

- Get the suburb with name of Kingford.

### 04_tfidf.py

- Get keywords from articles.

### 05_NER.py

- Standford NER

- spaCy

- NTLK

- get continuous words starting with a capital letter (2 methods)

- delete stopwords

### 06_tweets_stats.py

- weekly tweets

- flu related tweets

- user number

- processing with progress bar

### 07_bounding_box_percentage.py

- Calculate numbers of tweets based on different area.

### 08_modelling.py

- Function of distance between two points.

- Data processing. 

- Mean error distance.

- Median error distance.
