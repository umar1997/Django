from rest_framework import serializers
from .models import Article
 
 
################################################## serializers.Serializer
class ArticleSerializer(serializers.Serializer):
    # required, max_length and default.
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()
 
 
 
    def create(self, validated_data):
 
        # Create and return a new `Article` instance, given the validated data.
        return Article.objects.create(validated_data)
 
 
    def update(self, instance, validated_data):
 
        #Update and return an existing `Article` instance, given the validated data.
 
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.email = validated_data.get('email', instance.email)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

################################################## serializers.ModelSerializer
# It will automatically generate a set of fields for you, based on the model.
# It will automatically generate validators for the serializer, such as unique_together validators.
# It includes simple default implementations of .create() and .update().


from rest_framework import serializers
from .models import Article
 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']