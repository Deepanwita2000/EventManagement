from rest_framework import serializers
from eventapp.models import Event
from datetime import date,datetime
class EventSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(max_length=None , use_url=True , required=False)
    class Meta:
        model = Event
        fields = ['id','title','description','location','venue','date','time','organizer','banner','status']
    def validate_title(self,value):
        if str(value).isdigit():
            raise serializers.ValidationError("Name must not be a number")
        return value
    
    def validate_description(self , value):
        if len(str(value)) > 100:
             raise serializers.ValidationError("description must be within 100 characters long.")
        return value
    
    def validate_location(self,value):
        return value
    
    def validate_venue(self,value):
        return value
    
    def validate_date(self,value):
        date_string=str(value)
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        if date_object < date.today():
            raise serializers.ValidationError("Invalid date")
        
        # later on for formated date

        return value
    
    #current_date = date.today()
    def validate_time(self,value):
        return value

    def validate_organizer(self,value):
        return value
    

    
    def validate_status(self,value):
        if str(value) not in ("active" , "inactive"):
            raise serializers.ValidationError("Invalid status")
        return value
    
    # def create():
    #     pass

    # def update():
    #     pass

            # id: ObjectId, autocreated
    # title= models.CharField(max_length=100)
    # description = models.TextField()
    # location = models.CharField(max_length=100)
    # date = models.DateField()
    # time = models.TimeField()
    # organizer = models.CharField(max_length=100)
    # # banner = models.ImageField()
    # status = models.CharField()   #   modify required ...... will hold the choices ( "active" | "inactive")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # # createdBy = #left to add for foreign key

