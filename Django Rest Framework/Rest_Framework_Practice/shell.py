python manage.py shell

from api_basic.models import Article
from api_basic.serializers import ArticleSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

a = Article(title = 'New Article', author ='Parwiz', email = 'par@gmail.com', )
a.save()
serializer = ArticleSerializer(a)
serializer.data
# Output
# {'title': 'Article Title', 'author': 'John', 'email': 'john@gmail.com', 'date':
# '2020-05-24T09:14:02.081688Z'}
content = JSONRenderer().render(serializer.data)
# content
# b'{"title":"Article Title","author":"John","email":"john@gmail.com","date":"202
# 0-05-24T09:14:02.081688Z"}'

# OR

serializer = ArticleSerializer(Article.objects.all(), many=True)
serializer.data