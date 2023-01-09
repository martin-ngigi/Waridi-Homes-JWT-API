from django.db import models

'''
{
	"agent_id": 1
	"agent_name": "",
	"phone": "",
	"houses"[
		{
			"id": 1,
			"title": "",
			"category": "",
			"description": "",
			"loaction": "",
            "status": "",
            "add_date": "",
			"monthly_price": 200,
			"images": [
				{
					"id": 1,
					"title": "",
					"description": "",
					"url": ""
				},
				{
					"id": 1,
					"title": "",
					"description": "",
					"url": ""
				}
				]
		},
	]
}
'''

# Create your models here.

STATUS = (('Vacant', 'Vacant'), ('Occupied', 'Occupied'))
#STATUSALIVE = (('A','Alive'),('D','Dead'),)
class Users(models.Model):
	agent_id = models.IntegerField() #This id is the users id after registration
	agent_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=30)
	
	class Meat:
		ordering = ('agent_id')
	
	def __str__(self):
		return self.agent_name+' '+self.agent_id
    
class Houses(models.Model):
	user = models.ForeignKey(Users, related_name='houses', on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	category = models.CharField(max_length=50)
	description= models.TextField(max_length=100000)
	location = models.CharField(max_length=100)
	status = models.TextField(max_length=20, choices=STATUS, default='Vacant')
	add_date = models.DateTimeField(auto_now_add=True)
	monthly_price=models.IntegerField()
	
	class Meat:
		ordering = ('category')
	
	def __str__(self):
		return self.category+' '+self.monthly_price
    

class Images(models.Model):
	house = models.ForeignKey(Houses, related_name='images', on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	description= models.TextField(max_length=100000)
	#url = models.URLField(max_length=300)
	url= models.TextField(max_length=100000)
	
	class Meat:
		ordering = ('title')
	
	def __str__(self):
		return self.title
    
