from django.db import models

class Owner(models.Model):
	Idno=models.CharField(max_length=50, primary_key=True)
	Firstname=models.CharField(max_length=50,)
	Secondname=models.CharField(max_length=50,)
	Contact=models.CharField(max_length=50,)
	Username=models.CharField(max_length=50,)
	Email=models.CharField(max_length=50)

	def __str__(self):
		return(self.Username)

class PickLoc(models.Model):
	Name=models.CharField(max_length=70)
	Description=models.CharField(max_length=70)
	City=models.CharField(max_length=70)

	def __str__(self):
		return(self.Name)
class Car(models.Model):
	RegNo=models.CharField(max_length=50, primary_key=True)
	Type=models.CharField(max_length=50,)
	Model=models.CharField(max_length=50, null=True)
	ModelYear=models.CharField(max_length=50,)
	Condition=models.CharField(max_length=50,)
	Pic=models.ImageField(upload_to="pictures")
	Owner=models.ForeignKey(Owner,on_delete=models.CASCADE)
	Location=models.ForeignKey(PickLoc,on_delete=models.CASCADE, default=1)
	Mileage=models.IntegerField()
	Fee=models.IntegerField()
	Description=models.TextField(null=True)
	Available=models.BooleanField(default=True)

	def __str__(self):
		return(self.RegNo)

class CarPic(models.Model):
	RegNo=models.ForeignKey(Car,on_delete=models.CASCADE)
	Picture=models.ImageField(upload_to="pictures")

class Client(models.Model):
	Idno=models.CharField(max_length=20, primary_key=True)
	Firstname=models.CharField(max_length=50)
	Secondname=models.CharField(max_length=50)
	Username=models.CharField(max_length=50)
	Contact=models.CharField(max_length=20)
	Email=models.CharField(max_length=50)

	def __str__(self):
		return (self.Username)



class Deal(models.Model):
	Client=models.ForeignKey(Client,on_delete=models.CASCADE)
	Saler=models.ForeignKey(Owner,on_delete=models.CASCADE)
	Location=models.ForeignKey(PickLoc,on_delete=models.CASCADE, default=1)	
	Date=models.DateField()
	To=models.DateField()
	Status=models.CharField(max_length=50,)
	Charge=models.IntegerField()
	Car=models.ForeignKey(Car,on_delete=models.CASCADE)

class Message(models.Model):
    User=models.CharField(max_length=50,)
    Body=models.TextField(max_length=50,)
    At=models.DateTimeField()
    Title=models.CharField(max_length=50)

class Code(models.Model):
	Contact=models.CharField(max_length=50,)
	Pin=models.CharField(max_length=50,)
# Create your models here.
